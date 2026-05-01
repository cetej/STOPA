#!/usr/bin/env python3
"""evidence-corpus-build.py — Pre-built analysis tier (AHE Pattern 5).

Aggregates raw memory artifacts (outcomes/, failures/, farm-ledger.md) into
a queryable two-layer summary:

- Layer 1 (.claude/memory/intermediate/analysis-overview.md): cross-skill
  rollup — recent runs, success/failure rates, recurring patterns. PRIMARY
  read by /self-evolve Phase 0 (Setup) and Phase 2 (ρ Reflect) BEFORE
  drilling into raw outcome files.

- Layer 2 (.claude/memory/intermediate/analysis/detail/<target>.md): per-target
  breakdown — strategy effectiveness, what worked, what failed, distinct
  failure patterns. Read only when Layer 1 says drill-down is warranted.

Source: outputs/ahe-pilot-2026-04-30.md Pattern 5. AHE quote:
"do NOT skip them to read raw traces directly".

Run:
    python scripts/evidence-corpus-build.py            # build both layers
    python scripts/evidence-corpus-build.py --dry-run  # show what would be written
    python scripts/evidence-corpus-build.py --target <name>  # only that target's L2

Designed for invocation:
- By /self-evolve at Phase 0 (auto-refresh if older than 24h, AHE convention)
- By a daily scheduled task
- Manually before debugging recurring patterns

Output is intermediate/ (24h TTL per STOPA convention) — regenerable any time.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from atomic_utils import atomic_write  # noqa: E402

OUTCOMES_DIR = REPO_ROOT / ".claude/memory/outcomes"
FAILURES_DIR = REPO_ROOT / ".claude/memory/failures"
FARM_LEDGER = REPO_ROOT / ".claude/memory/intermediate/farm-ledger.md"

LAYER_1 = REPO_ROOT / ".claude/memory/intermediate/analysis-overview.md"
LAYER_2_DIR = REPO_ROOT / ".claude/memory/intermediate/analysis/detail"

RECENT_DAYS = 30  # outcomes/failures within this window are "recent"


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Parse YAML-ish frontmatter delimited by --- lines.

    Returns (frontmatter_dict, body_text). Falls back to ({}, text) if no
    frontmatter. Uses naive parser — no nested structures, just key: value.
    """
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm: dict[str, Any] = {}
    for line in parts[1].splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        fm[key] = value
    return fm, parts[2]


def parse_sections(body: str) -> dict[str, str]:
    """Extract `## Heading` sections into a dict (heading lowercased + trimmed)."""
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip().lower()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def load_outcomes() -> list[dict[str, Any]]:
    """Load all outcome files, parsing frontmatter and key sections."""
    if not OUTCOMES_DIR.exists():
        return []
    outcomes = []
    for path in sorted(OUTCOMES_DIR.glob("*.md")):
        if path.name.startswith("."):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"WARN: cannot read {path.name}: {exc}", file=sys.stderr)
            continue
        fm, body = parse_frontmatter(text)
        if not fm.get("skill"):
            continue
        sections = parse_sections(body)
        outcomes.append({
            "path": path,
            "filename": path.name,
            "skill": fm.get("skill", ""),
            "target": fm.get("task", "")[:60],
            "date": fm.get("date", ""),
            "outcome": fm.get("outcome", ""),
            "iterations": fm.get("iterations", "0"),
            "score_start": fm.get("score_start", ""),
            "score_end": fm.get("score_end", ""),
            "exit_reason": fm.get("exit_reason", ""),
            "what_worked": sections.get("what worked", "").strip(),
            "what_failed": sections.get("what failed", "").strip(),
            "trajectory": sections.get("trajectory summary", "").strip(),
        })
    return outcomes


def load_failures() -> list[dict[str, Any]]:
    """Load all failure trajectory files."""
    if not FAILURES_DIR.exists():
        return []
    failures = []
    for path in sorted(FAILURES_DIR.glob("*.md")):
        if path.name.startswith("."):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"WARN: cannot read {path.name}: {exc}", file=sys.stderr)
            continue
        fm, body = parse_frontmatter(text)
        if not fm.get("id"):
            continue
        sections = parse_sections(body)
        failures.append({
            "path": path,
            "filename": path.name,
            "id": fm.get("id", ""),
            "date": fm.get("date", ""),
            "task": fm.get("task", ""),
            "failure_class": fm.get("failure_class", ""),
            "failure_agent": fm.get("failure_agent", ""),
            "resolved": fm.get("resolved", "false"),
            "root_cause": sections.get("root cause", "").strip(),
            "reflexion": sections.get("reflexion", "").strip(),
        })
    return failures


def load_farm_ledger() -> dict[str, Any]:
    """Read the latest farm-ledger if present and not a template."""
    if not FARM_LEDGER.exists():
        return {}
    text = FARM_LEDGER.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if fm.get("task_id") in ("template", "", None):
        return {}
    pattern_lines = []
    in_patterns = False
    for line in body.splitlines():
        if line.startswith("## Discovered Patterns"):
            in_patterns = True
            continue
        if in_patterns and line.startswith("## "):
            break
        if in_patterns and line.strip() and not line.startswith("("):
            pattern_lines.append(line.strip())
    return {
        "task_id": fm.get("task_id", ""),
        "sweep": fm.get("sweep", ""),
        "task": fm.get("task", ""),
        "total_files": fm.get("total_files", "0"),
        "patterns": pattern_lines,
    }


def days_ago(date_str: str) -> int | None:
    """Return how many days ago a YYYY-MM-DD string is, or None on parse fail."""
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (date.today() - d).days


def is_recent(date_str: str) -> bool:
    da = days_ago(date_str)
    return da is not None and da <= RECENT_DAYS


def render_layer_1(outcomes: list[dict], failures: list[dict], farm: dict) -> str:
    """Render the Layer 1 cross-skill overview."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    recent_outcomes = [o for o in outcomes if is_recent(o["date"])]
    recent_failures = [f for f in failures if is_recent(f["date"])]

    by_skill: dict[str, list[dict]] = defaultdict(list)
    for o in recent_outcomes:
        by_skill[o["skill"]].append(o)
    by_outcome: Counter[str] = Counter(o["outcome"] for o in recent_outcomes)
    by_failure_class: Counter[str] = Counter(
        f["failure_class"] for f in recent_failures if f["failure_class"]
    )
    by_failure_agent: Counter[str] = Counter(
        f["failure_agent"] for f in recent_failures if f["failure_agent"]
    )

    lines = [
        "---",
        f"generated: {now}",
        "source: scripts/evidence-corpus-build.py",
        "ttl_hours: 24",
        f"outcomes_total: {len(outcomes)}",
        f"outcomes_recent: {len(recent_outcomes)}",
        f"failures_total: {len(failures)}",
        f"failures_recent: {len(recent_failures)}",
        f"window_days: {RECENT_DAYS}",
        "---",
        "",
        "# Evidence Corpus — Layer 1 Overview",
        "",
        "Pre-aggregated rollup of recent outcomes, failures, and farm activity. "
        "**READ THIS FIRST** before drilling into raw outcomes/ or failures/ files. "
        "Layer 2 detail per target lives in `.claude/memory/intermediate/analysis/detail/<target>.md`.",
        "",
        "Source: AHE Pattern 5 (`outputs/ahe-pilot-2026-04-30.md`). "
        "Quote: \"do NOT skip them to read raw traces directly\".",
        "",
        "## Recent Outcomes by Skill",
        "",
        f"Window: last {RECENT_DAYS} days. Only skills with ≥1 recent outcome shown.",
        "",
        "| Skill | Runs | Success | Partial | Failure | Last run |",
        "|-------|------|---------|---------|---------|----------|",
    ]
    for skill in sorted(by_skill.keys()):
        items = by_skill[skill]
        success = sum(1 for o in items if o["outcome"] == "success")
        partial = sum(1 for o in items if o["outcome"] == "partial")
        failure = sum(1 for o in items if o["outcome"] == "failure")
        last = max((o["date"] for o in items), default="—")
        lines.append(f"| {skill} | {len(items)} | {success} | {partial} | {failure} | {last} |")

    if not by_skill:
        lines.append("| _no recent outcomes_ | — | — | — | — | — |")

    lines.extend([
        "",
        "## Outcome Distribution",
        "",
        "| Outcome | Count |",
        "|---------|-------|",
    ])
    for outcome, count in by_outcome.most_common():
        if outcome:
            lines.append(f"| {outcome} | {count} |")
    if not by_outcome:
        lines.append("| _none_ | 0 |")

    lines.extend([
        "",
        "## Failure Patterns (recent)",
        "",
    ])
    if recent_failures:
        lines.extend([
            "By failure_class:",
            "",
            "| Class | Count |",
            "|-------|-------|",
        ])
        for cls, count in by_failure_class.most_common():
            lines.append(f"| {cls} | {count} |")
        lines.extend([
            "",
            "By failure_agent:",
            "",
            "| Agent | Count |",
            "|-------|-------|",
        ])
        for agent, count in by_failure_agent.most_common():
            lines.append(f"| {agent} | {count} |")
    else:
        lines.append("_No failure trajectory records in the recent window._ "
                     "Either nothing is failing, or `/scribe` failure-recording is not firing — "
                     "check `.claude/memory/failures/` directly.")

    lines.extend([
        "",
        "## Farm Ledger (current sweep)",
        "",
    ])
    if farm:
        lines.extend([
            f"- **task_id**: {farm['task_id']}",
            f"- **task**: {farm['task']}",
            f"- **sweep**: {farm['sweep']} of {farm.get('total_sweeps', '?')}",
            f"- **total files**: {farm['total_files']}",
            "",
        ])
        if farm["patterns"]:
            lines.append("Discovered patterns:")
            lines.extend(f"- {p}" for p in farm["patterns"][:10])
        else:
            lines.append("No patterns extracted yet (sweep 1 may still be running).")
    else:
        lines.append("_No active farm sweep_ (farm-ledger is template or absent).")

    targets = sorted({o["skill"] for o in recent_outcomes})
    lines.extend([
        "",
        "## Layer 2 Drill-Down Index",
        "",
        "Per-target detail files (read only when Layer 1 indicates a problem):",
        "",
    ])
    if targets:
        for t in targets:
            lines.append(f"- [{t}](analysis/detail/{t}.md)")
    else:
        lines.append("_No detail files yet — run with `--target <name>` or default to build all._")

    lines.extend([
        "",
        "---",
        "_End of Layer 1. Detail tier: `.claude/memory/intermediate/analysis/detail/`._",
    ])
    return "\n".join(lines) + "\n"


def render_layer_2(skill: str, outcomes: list[dict], failures: list[dict]) -> str:
    """Render per-target Layer 2 detail."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    relevant_o = [o for o in outcomes if o["skill"] == skill]
    relevant_o.sort(key=lambda x: x["date"], reverse=True)

    relevant_f = [f for f in failures if f["failure_agent"] == skill]
    relevant_f.sort(key=lambda x: x["date"], reverse=True)

    lines = [
        "---",
        f"generated: {now}",
        f"target: {skill}",
        "source: scripts/evidence-corpus-build.py",
        "ttl_hours: 24",
        f"outcomes: {len(relevant_o)}",
        f"failures: {len(relevant_f)}",
        "---",
        "",
        f"# Layer 2 Detail — {skill}",
        "",
        "Per-target evidence corpus. Aggregated from raw outcomes/ and failures/ records "
        "for this skill. Read this when Layer 1 overview signals a recurring pattern that "
        "needs deeper context.",
        "",
        f"## Recent Outcomes ({len(relevant_o)})",
        "",
        "| Date | Outcome | Iters | Δ Score | Exit reason | File |",
        "|------|---------|-------|---------|-------------|------|",
    ]
    for o in relevant_o[:20]:
        try:
            delta = float(o["score_end"]) - float(o["score_start"])
            delta_str = f"{delta:+.2f}"
        except ValueError:
            delta_str = "—"
        lines.append(
            f"| {o['date']} | {o['outcome']} | {o['iterations']} | "
            f"{delta_str} | {o['exit_reason']} | "
            f"`{o['filename']}` |"
        )
    if not relevant_o:
        lines.append("| _no records_ | — | — | — | — | — |")

    lines.extend(["", "## What Worked (aggregated)", ""])
    worked_items = [o["what_worked"] for o in relevant_o if o["what_worked"]]
    if worked_items:
        for item in worked_items[:10]:
            for line in item.splitlines():
                line = line.strip()
                if line.startswith("-"):
                    lines.append(line)
    else:
        lines.append("_No `## What Worked` sections in recent outcomes._")

    lines.extend(["", "## What Failed (aggregated)", ""])
    failed_items = [o["what_failed"] for o in relevant_o if o["what_failed"]]
    if failed_items:
        for item in failed_items[:10]:
            for line in item.splitlines():
                line = line.strip()
                if line.startswith("-"):
                    lines.append(line)
    else:
        lines.append("_No `## What Failed` sections in recent outcomes._")

    lines.extend(["", f"## Failure Trajectories ({len(relevant_f)})", ""])
    if relevant_f:
        for f in relevant_f[:10]:
            lines.extend([
                f"### {f['id']} — {f['date']}",
                "",
                f"- **task**: {f['task']}",
                f"- **failure_class**: {f['failure_class']}",
                f"- **resolved**: {f['resolved']}",
                "",
                "**Root cause:**",
                f["root_cause"] or "_(not recorded)_",
                "",
                "**Reflexion:**",
                f["reflexion"] or "_(not recorded)_",
                "",
            ])
    else:
        lines.append("_No failure records for this skill._")

    lines.extend([
        "",
        "---",
        f"_End of Layer 2 detail for {skill}._",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be written without writing")
    parser.add_argument("--target", type=str, default=None,
                        help="Build only Layer 2 for this target (skill name)")
    parser.add_argument("--max-age-hours", type=int, default=24,
                        help="Skip rebuild if output is fresher than this (default 24)")
    args = parser.parse_args()

    if not args.dry_run and not args.target and LAYER_1.exists():
        age_h = (datetime.now().timestamp() - LAYER_1.stat().st_mtime) / 3600
        if age_h < args.max_age_hours:
            print(f"Layer 1 is fresh ({age_h:.1f}h old, < {args.max_age_hours}h). Skipping rebuild. "
                  "Use --dry-run or delete the file to force.")
            return 0

    outcomes = load_outcomes()
    failures = load_failures()
    farm = load_farm_ledger()

    print(f"Loaded {len(outcomes)} outcomes, {len(failures)} failures, "
          f"farm={'active' if farm else 'inactive'}")

    if args.target:
        targets = [args.target]
    else:
        targets = sorted({o["skill"] for o in outcomes})

    if not args.target:
        layer_1_text = render_layer_1(outcomes, failures, farm)
        if args.dry_run:
            print(f"--- Would write Layer 1 ({len(layer_1_text)} chars) to {LAYER_1.relative_to(REPO_ROOT)} ---")
        else:
            LAYER_1.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(LAYER_1, layer_1_text)
            print(f"Wrote Layer 1 to {LAYER_1.relative_to(REPO_ROOT)}")

    LAYER_2_DIR.mkdir(parents=True, exist_ok=True)
    for target in targets:
        text = render_layer_2(target, outcomes, failures)
        out = LAYER_2_DIR / f"{re.sub(r'[^a-zA-Z0-9_-]', '_', target)}.md"
        if args.dry_run:
            print(f"--- Would write Layer 2/{target} ({len(text)} chars) to {out.relative_to(REPO_ROOT)} ---")
        else:
            atomic_write(out, text)
            print(f"Wrote Layer 2 detail for {target}")

    if args.dry_run:
        print("Dry-run complete — no files written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
