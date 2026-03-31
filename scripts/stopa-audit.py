#!/usr/bin/env python3
"""
STOPA Harness Audit — Deterministic health scoring across 7 categories.

Inspired by ECC's harness-audit.js: each category scores 0-10,
overall = weighted average. Output: JSON + markdown report.

Categories:
  1. Hooks Coverage     — are all hook events wired? profile system intact?
  2. Skill Quality      — frontmatter completeness, description format, sync
  3. Memory Health      — file sizes, archive compliance, staleness
  4. Learnings Health   — YAML validity, counters, staleness, critical-patterns
  5. Budget Accuracy    — ledger present, counters, history rows
  6. Checkpoint Recency — how fresh is checkpoint.md?
  7. Rules Coverage     — core invariants present, verify_check coverage

Usage:
  python scripts/stopa-audit.py                  # full report to stdout
  python scripts/stopa-audit.py --json           # JSON only
  python scripts/stopa-audit.py --output report  # write report.json + report.md
"""

import sys
import os
import json
import re
import glob
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = Path(__file__).resolve().parent.parent
CLAUDE_DIR = BASE / ".claude"
MEMORY_DIR = CLAUDE_DIR / "memory"
HOOKS_DIR = CLAUDE_DIR / "hooks"
COMMANDS_DIR = CLAUDE_DIR / "commands"
SKILLS_DIR = CLAUDE_DIR / "skills"
RULES_DIR = CLAUDE_DIR / "rules"
LEARNINGS_DIR = MEMORY_DIR / "learnings"

NOW = datetime.now()


def count_files(path: Path, pattern: str = "*.md") -> int:
    return len(list(path.glob(pattern))) if path.exists() else 0


def file_line_count(path: Path) -> int:
    if not path.exists():
        return 0
    try:
        return len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except Exception:
        return 0


def days_since_modified(path: Path) -> int:
    if not path.exists():
        return 999
    try:
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        return (NOW - mtime).days
    except Exception:
        return 999


def parse_date_from_content(path: Path) -> int:
    """Extract most recent YYYY-MM-DD from file content, return days ago."""
    if not path.exists():
        return 999
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
        if not dates:
            return 999
        latest = max(dates)
        dt = datetime.strptime(latest, "%Y-%m-%d")
        return (NOW - dt).days
    except Exception:
        return 999


# ─── Category 1: Hooks Coverage ───────────────────────────────────────

def audit_hooks() -> dict[str, Any]:
    findings: list[str] = []
    score = 10

    # Check settings.json exists and has hooks
    settings_path = CLAUDE_DIR / "settings.json"
    if not settings_path.exists():
        return {"score": 0, "findings": ["settings.json missing"]}

    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"score": 0, "findings": [f"settings.json parse error: {e}"]}

    hooks = settings.get("hooks", {})
    if not hooks:
        return {"score": 0, "findings": ["No hooks configured in settings.json"]}

    # Required hook events
    required_events = {
        "PreToolUse": "input validation",
        "PostToolUse": "activity tracking",
        "SessionStart": "initialization",
        "Stop": "cleanup",
    }

    for event, purpose in required_events.items():
        matched = [k for k in hooks if event in k]
        if not matched:
            findings.append(f"Missing {event} hooks ({purpose})")
            score -= 2

    # Check hook files exist on disk
    hook_files = list(HOOKS_DIR.glob("*.sh")) + list(HOOKS_DIR.glob("*.py"))
    if len(hook_files) < 10:
        findings.append(f"Only {len(hook_files)} hook files (expected 15+)")
        score -= 1

    # Profile system check
    profile_lib = HOOKS_DIR / "lib" / "profile-check.sh"
    if not profile_lib.exists():
        findings.append("Hook profile library missing (lib/profile-check.sh)")
        score -= 1

    # block-no-verify check
    block_nv = HOOKS_DIR / "block-no-verify.sh"
    if not block_nv.exists():
        findings.append("block-no-verify.sh missing")
        score -= 1

    # config-protection check
    config_prot = HOOKS_DIR / "config-protection.sh"
    if not config_prot.exists():
        findings.append("config-protection.sh missing")
        score -= 1

    return {"score": max(0, score), "findings": findings}


# ─── Category 2: Skill Quality ────────────────────────────────────────

def audit_skills() -> dict[str, Any]:
    findings: list[str] = []
    score = 10

    commands = list(COMMANDS_DIR.glob("*.md")) if COMMANDS_DIR.exists() else []
    if not commands:
        return {"score": 0, "findings": ["No skills found in commands/"]}

    total = len(commands)
    issues = 0

    for cmd in commands:
        name = cmd.stem
        text = cmd.read_text(encoding="utf-8", errors="replace")

        # Check YAML frontmatter
        if not text.startswith("---"):
            findings.append(f"{name}: missing YAML frontmatter")
            issues += 1
            continue

        # Check description starts with "Use when"
        desc_match = re.search(r"description:\s*[\"']?(.+?)(?:[\"']?\s*$|\n)", text)
        if desc_match:
            desc = desc_match.group(1).strip().strip("\"'")
            if not desc.startswith("Use when") and not desc.startswith("Use this"):
                findings.append(f"{name}: description doesn't start with 'Use when...'")
                issues += 1
        else:
            findings.append(f"{name}: no description field")
            issues += 1

        # Check commands/ ↔ skills/ sync
        skill_copy = SKILLS_DIR / name / "SKILL.md"
        if skill_copy.exists():
            skill_text = skill_copy.read_text(encoding="utf-8", errors="replace")
            if text.strip() != skill_text.strip():
                findings.append(f"{name}: commands/ ≠ skills/ DESYNC")
                issues += 1

    # Score: deduct proportionally
    if total > 0:
        issue_ratio = issues / total
        score = max(0, round(10 * (1 - issue_ratio * 2)))  # 50% issues = score 0

    return {"score": score, "findings": findings[:15]}  # cap findings


# ─── Category 3: Memory Health ─────────────────────────────────────────

def audit_memory() -> dict[str, Any]:
    findings: list[str] = []
    score = 10

    if not MEMORY_DIR.exists():
        return {"score": 0, "findings": ["memory/ directory missing"]}

    # Check core memory files exist
    required = ["state.md", "budget.md", "checkpoint.md", "decisions.md", "key-facts.md"]
    for f in required:
        if not (MEMORY_DIR / f).exists():
            findings.append(f"{f} missing")
            score -= 1

    # Check file sizes (max 500 lines rule)
    for md in MEMORY_DIR.glob("*.md"):
        lines = file_line_count(md)
        if lines > 500:
            findings.append(f"{md.name}: {lines} lines (max 500 — needs archival)")
            score -= 1
        elif lines > 400:
            findings.append(f"{md.name}: {lines} lines (approaching 500 limit)")

    # Check archive files exist for large memory files
    for md in MEMORY_DIR.glob("*.md"):
        if file_line_count(md) > 400:
            archive = MEMORY_DIR / f"{md.stem}-archive.md"
            if not archive.exists():
                findings.append(f"{md.stem}: no archive file prepared")

    # Staleness check — activity-log should be recent
    activity_log = MEMORY_DIR / "activity-log.md"
    days = days_since_modified(activity_log)
    if days > 7:
        findings.append(f"activity-log.md last modified {days} days ago")
        score -= 1

    return {"score": max(0, score), "findings": findings}


# ─── Category 4: Learnings Health ──────────────────────────────────────

def audit_learnings() -> dict[str, Any]:
    findings: list[str] = []
    score = 10

    if not LEARNINGS_DIR.exists():
        return {"score": 2, "findings": ["learnings/ directory missing"]}

    learning_files = list(LEARNINGS_DIR.glob("*.md"))
    total = len(learning_files)
    if total == 0:
        return {"score": 2, "findings": ["No learning files"]}

    yaml_issues = 0
    stale_count = 0
    no_verify_check = 0

    for lf in learning_files:
        text = lf.read_text(encoding="utf-8", errors="replace")

        # YAML frontmatter check
        if not text.startswith("---"):
            yaml_issues += 1
            continue

        # Check required fields
        for field in ["date:", "type:", "severity:", "summary:"]:
            if field not in text:
                yaml_issues += 1
                break

        # verify_check presence
        if "verify_check:" not in text:
            no_verify_check += 1

        # Staleness: date > 90 days
        date_match = re.search(r"date:\s*(\d{4}-\d{2}-\d{2})", text)
        if date_match:
            try:
                dt = datetime.strptime(date_match.group(1), "%Y-%m-%d")
                if (NOW - dt).days > 90:
                    stale_count += 1
            except ValueError:
                pass

    # Critical patterns file
    crit = LEARNINGS_DIR / "critical-patterns.md"
    if not crit.exists():
        findings.append("critical-patterns.md missing (always-read index)")
        score -= 1

    if yaml_issues > 0:
        findings.append(f"{yaml_issues}/{total} learnings have YAML issues")
        score -= min(3, yaml_issues)

    if no_verify_check > total * 0.5:
        findings.append(f"{no_verify_check}/{total} learnings lack verify_check")
        score -= 1

    if stale_count > total * 0.3:
        findings.append(f"{stale_count}/{total} learnings are stale (>90 days)")
        score -= 1

    findings.append(f"Total: {total} learnings, {stale_count} stale, {no_verify_check} without verify_check")

    return {"score": max(0, score), "findings": findings}


# ─── Category 5: Budget Accuracy ───────────────────────────────────────

def audit_budget() -> dict[str, Any]:
    findings: list[str] = []
    score = 10

    budget_path = MEMORY_DIR / "budget.md"
    if not budget_path.exists():
        return {"score": 0, "findings": ["budget.md missing"]}

    text = budget_path.read_text(encoding="utf-8", errors="replace")

    # Has counters table
    if "| Metric" not in text and "| Used" not in text:
        findings.append("No counters table found")
        score -= 3

    # Has history section
    if "## History" not in text:
        findings.append("No History section")
        score -= 2

    # Count history rows
    history_rows = len(re.findall(r"^\|[^|]+\|[^|]+\|[^|]+\|", text, re.MULTILINE))
    if history_rows < 3:
        findings.append(f"Only {history_rows} history rows (need 20 for heuristics)")
        score -= 1

    # Budget archive
    archive = MEMORY_DIR / "budget-archive.md"
    if not archive.exists():
        findings.append("budget-archive.md missing")

    findings.append(f"History rows: {history_rows}")

    return {"score": max(0, score), "findings": findings}


# ─── Category 6: Checkpoint Recency ────────────────────────────────────

def audit_checkpoint() -> dict[str, Any]:
    findings: list[str] = []
    score = 10

    ckpt_path = MEMORY_DIR / "checkpoint.md"
    if not ckpt_path.exists():
        return {"score": 0, "findings": ["checkpoint.md missing"]}

    text = ckpt_path.read_text(encoding="utf-8", errors="replace")

    if "No active checkpoint" in text or len(text.strip()) < 50:
        findings.append("Checkpoint is empty/placeholder")
        return {"score": 3, "findings": findings}

    # Check recency from content date
    days = parse_date_from_content(ckpt_path)
    if days > 7:
        findings.append(f"Checkpoint is {days} days old")
        score -= 3
    elif days > 3:
        findings.append(f"Checkpoint is {days} days old")
        score -= 1

    # Has resume prompt
    if "## Resume Prompt" not in text and "resume" not in text.lower():
        findings.append("No resume prompt section")
        score -= 2

    # Has branch info
    if "Branch" not in text:
        findings.append("No branch info")
        score -= 1

    # Has commit info
    if "commit" not in text.lower():
        findings.append("No commit reference")
        score -= 1

    findings.append(f"Last checkpoint: {days} days ago")

    return {"score": max(0, score), "findings": findings}


# ─── Category 7: Rules Coverage ─────────────────────────────────────────

def audit_rules() -> dict[str, Any]:
    findings: list[str] = []
    score = 10

    if not RULES_DIR.exists():
        return {"score": 0, "findings": ["rules/ directory missing"]}

    rule_files = list(RULES_DIR.glob("*.md"))
    if not rule_files:
        return {"score": 0, "findings": ["No rule files"]}

    # Check core-invariants.md exists
    core = RULES_DIR / "core-invariants.md"
    if not core.exists():
        findings.append("core-invariants.md missing")
        score -= 3
    else:
        text = core.read_text(encoding="utf-8", errors="replace")
        # Count rules (## N. pattern)
        rule_count = len(re.findall(r"^## \d+\.", text, re.MULTILINE))
        if rule_count < 5:
            findings.append(f"Only {rule_count} core invariants (recommend 5-7)")
            score -= 1
        elif rule_count > 7:
            findings.append(f"{rule_count} core invariants (max 7 — trim)")
            score -= 1

    # Check expected rule files
    expected_rules = ["memory-files.md", "python-files.md", "skill-files.md"]
    for r in expected_rules:
        if not (RULES_DIR / r).exists():
            findings.append(f"{r} missing")
            score -= 1

    # CLAUDE.md exists and is non-trivial
    claude_md = BASE / "CLAUDE.md"
    if not claude_md.exists():
        findings.append("CLAUDE.md missing")
        score -= 2
    elif file_line_count(claude_md) < 20:
        findings.append("CLAUDE.md is too short (<20 lines)")
        score -= 1

    findings.append(f"Rule files: {len(rule_files)}")

    return {"score": max(0, score), "findings": findings}


# ─── Main ───────────────────────────────────────────────────────────────

CATEGORIES = {
    "hooks_coverage": {"fn": audit_hooks, "weight": 1.5, "label": "Hooks Coverage"},
    "skill_quality": {"fn": audit_skills, "weight": 1.5, "label": "Skill Quality"},
    "memory_health": {"fn": audit_memory, "weight": 1.0, "label": "Memory Health"},
    "learnings_health": {"fn": audit_learnings, "weight": 1.0, "label": "Learnings Health"},
    "budget_accuracy": {"fn": audit_budget, "weight": 0.5, "label": "Budget Accuracy"},
    "checkpoint_recency": {"fn": audit_checkpoint, "weight": 1.0, "label": "Checkpoint Recency"},
    "rules_coverage": {"fn": audit_rules, "weight": 1.5, "label": "Rules Coverage"},
}


def run_audit() -> dict[str, Any]:
    results: dict[str, Any] = {}
    total_weighted = 0.0
    total_weight = 0.0

    for key, cat in CATEGORIES.items():
        result = cat["fn"]()
        result["label"] = cat["label"]
        result["weight"] = cat["weight"]
        results[key] = result
        total_weighted += result["score"] * cat["weight"]
        total_weight += cat["weight"]

    overall = round(total_weighted / total_weight, 1) if total_weight > 0 else 0

    return {
        "timestamp": NOW.strftime("%Y-%m-%dT%H:%M:%S"),
        "overall_score": overall,
        "max_score": 10,
        "categories": results,
        "summary": _grade(overall),
    }


def _grade(score: float) -> str:
    if score >= 9:
        return "EXCELLENT"
    elif score >= 7:
        return "GOOD"
    elif score >= 5:
        return "FAIR"
    elif score >= 3:
        return "NEEDS WORK"
    else:
        return "CRITICAL"


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# STOPA Harness Audit Report",
        "",
        f"**Date**: {report['timestamp']}",
        f"**Overall Score**: {report['overall_score']}/10 — {report['summary']}",
        "",
        "## Category Scores",
        "",
        "| Category | Score | Weight | Findings |",
        "|----------|-------|--------|----------|",
    ]

    for key, cat in report["categories"].items():
        top_finding = cat["findings"][0] if cat["findings"] else "OK"
        lines.append(
            f"| {cat['label']} | {cat['score']}/10 | {cat['weight']}x | {top_finding} |"
        )

    lines.extend(["", "## Detailed Findings", ""])

    for key, cat in report["categories"].items():
        lines.append(f"### {cat['label']} ({cat['score']}/10)")
        if cat["findings"]:
            for f in cat["findings"]:
                lines.append(f"- {f}")
        else:
            lines.append("- No issues found")
        lines.append("")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]

    report = run_audit()

    if "--json" in args:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    elif "--output" in args:
        idx = args.index("--output")
        base_name = args[idx + 1] if idx + 1 < len(args) else "audit-report"
        json_path = Path(base_name + ".json")
        md_path = Path(base_name + ".md")
        json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        md_path.write_text(to_markdown(report), encoding="utf-8")
        print(f"Written: {json_path}, {md_path}")
    else:
        # Default: markdown to stdout
        print(to_markdown(report))


if __name__ == "__main__":
    main()
