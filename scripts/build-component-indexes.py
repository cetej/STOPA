#!/usr/bin/env python3
"""Build L2 component index files and block manifest from learnings YAML frontmatter.

Generates:
  .claude/memory/learnings/index-<component>.md  — per-component L2 indexes
  .claude/memory/learnings/block-manifest.json   — machine-readable page table for context selection

Hierarchical retrieval layers:
  L1: critical-patterns.md           (always-read, top 10 patterns)
  L2: index-<component>.md           (keyword-routed, per-component table)
  L2: block-manifest.json            (scored metadata index, enables budget-aware selection)
  L3: individual learning files      (read on demand, fetched by ID from manifest)

Run during /scribe maintenance or after adding new learnings.
"""
import json
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEARNINGS_DIR = Path(".claude/memory/learnings")
INDEX_PREFIX = "index-"
MANIFEST_FILE = LEARNINGS_DIR / "block-manifest.json"

SEVERITY_WEIGHTS: dict[str, int] = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def parse_frontmatter(filepath: Path) -> dict | None:
    """Parse YAML frontmatter from a learning file. Returns None if no frontmatter."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None

    entry: dict = {"file": filepath.name}
    for line in lines[1:20]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if key == "tags":
            val = val.strip("[]")
            entry["tags"] = [t.strip().strip("'\"") for t in val.split(",") if t.strip()]
        elif key == "related":
            val = val.strip("[]")
            entry["related"] = [r.strip().strip("'\"") for r in val.split(",") if r.strip()]
        elif key == "summary":
            entry["summary"] = val.strip("'\"")
        elif key in ("date", "type", "severity", "component", "supersedes"):
            entry[key] = val.strip("'\"")
        elif key in ("uses", "harmful_uses"):
            try:
                entry[key] = int(val)
            except ValueError:
                entry[key] = 0

    return entry if "component" in entry else None


def compute_token_estimate(filepath: Path) -> int:
    """Estimate token count from file size (chars / 4)."""
    try:
        return len(filepath.read_text(encoding="utf-8", errors="replace")) // 4
    except OSError:
        return 0


def compute_retrieval_score(entry: dict) -> float:
    """Score = severity_weight × recency_factor.

    Time-weighted: critical learning from 30 days ago (2.67) beats fresh low (2.0),
    but 90-day-old medium (0.8) loses to fresh low (2.0).
    Ref: rules/memory-files.md — time-weighted relevance formula.
    """
    severity = SEVERITY_WEIGHTS.get(entry.get("severity", "low"), 1)
    try:
        days_since = (date.today() - date.fromisoformat(entry.get("date", "2026-01-01"))).days
    except (ValueError, TypeError):
        days_since = 0
    recency = 1 / (1 + days_since / 60)
    return round(severity * recency, 3)


def build_indexes() -> dict[str, list[dict]]:
    """Group learnings by component and write L2 index files. Returns by_component map."""
    if not LEARNINGS_DIR.exists():
        print("ERROR: learnings directory not found")
        return {}

    by_component: dict[str, list[dict]] = defaultdict(list)
    for f in sorted(LEARNINGS_DIR.glob("*.md")):
        if f.name.startswith(INDEX_PREFIX) or f.name == "critical-patterns.md":
            continue
        entry = parse_frontmatter(f)
        if entry:
            by_component[entry["component"]].append(entry)

    # Remove old index files
    for old in LEARNINGS_DIR.glob(f"{INDEX_PREFIX}*.md"):
        old.unlink()

    # Write new index files
    for component, entries in sorted(by_component.items()):
        entries.sort(key=lambda e: e.get("date", ""), reverse=True)

        lines = [
            f"# Component Index: {component}",
            f"",
            f"Auto-generated L2 index. {len(entries)} learnings.",
            f"",
            f"| Date | File | Severity | Score | Summary |",
            f"|------|------|----------|-------|---------|",
        ]

        for e in entries:
            date_str = e.get("date", "?")
            fname = e["file"]
            sev = e.get("severity", "?")
            score = compute_retrieval_score(e)
            summary = e.get("summary", "no summary")
            if len(summary) > 75:
                summary = summary[:72] + "..."
            lines.append(f"| {date_str} | [{fname}]({fname}) | {sev} | {score:.2f} | {summary} |")

        lines.append("")
        lines.append("## Tags in this component")
        lines.append("")
        all_tags: set[str] = set()
        for e in entries:
            all_tags.update(e.get("tags", []))
        lines.append(", ".join(sorted(all_tags)))
        lines.append("")

        index_path = LEARNINGS_DIR / f"{INDEX_PREFIX}{component}.md"
        index_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  {index_path.name}: {len(entries)} entries")

    return by_component


def build_manifest(by_component: dict[str, list[dict]]) -> None:
    """Write block-manifest.json — the page table for context selection.

    Structure:
    {
      "generated": "YYYY-MM-DD",
      "total_blocks": N,
      "blocks": {
        "<filename>": {
          "id": "filename",
          "component": "...",
          "date": "YYYY-MM-DD",
          "type": "...",
          "severity": "...",
          "tags": [...],
          "summary": "...",
          "uses": N,
          "harmful_uses": N,
          "supersedes": "filename or null",
          "related": [...],
          "token_estimate": N,
          "retrieval_score": N.NNN,
          "active": true/false   # false if superseded by another entry
        }
      },
      "superseded_ids": ["filename", ...],
      "tag_index": {
        "<tag>": ["filename", ...]
      },
      "component_index": {
        "<component>": ["filename", ...]
      }
    }
    """
    all_entries: list[dict] = []
    for entries in by_component.values():
        all_entries.extend(entries)

    # Collect superseded IDs
    superseded: set[str] = set()
    for e in all_entries:
        sup = e.get("supersedes", "")
        if sup:
            superseded.add(sup)

    # Build block records
    blocks: dict[str, dict] = {}
    tag_index: dict[str, list[str]] = defaultdict(list)
    component_index: dict[str, list[str]] = defaultdict(list)

    for e in all_entries:
        fpath = LEARNINGS_DIR / e["file"]
        token_est = compute_token_estimate(fpath)
        score = compute_retrieval_score(e)
        is_active = e["file"] not in superseded

        block = {
            "id": e["file"],
            "component": e.get("component", "general"),
            "date": e.get("date", ""),
            "type": e.get("type", ""),
            "severity": e.get("severity", "low"),
            "tags": e.get("tags", []),
            "summary": e.get("summary", ""),
            "uses": e.get("uses", 0),
            "harmful_uses": e.get("harmful_uses", 0),
            "supersedes": e.get("supersedes", "") or None,
            "related": e.get("related", []),
            "token_estimate": token_est,
            "retrieval_score": score,
            "active": is_active,
        }
        blocks[e["file"]] = block

        if is_active:
            for tag in e.get("tags", []):
                tag_index[tag].append(e["file"])
            component_index[e.get("component", "general")].append(e["file"])

    # Sort component_index entries by retrieval_score descending
    for comp in component_index:
        component_index[comp].sort(
            key=lambda fid: blocks[fid]["retrieval_score"], reverse=True
        )
    for tag in tag_index:
        tag_index[tag].sort(
            key=lambda fid: blocks[fid]["retrieval_score"], reverse=True
        )

    manifest = {
        "generated": date.today().isoformat(),
        "total_blocks": len(blocks),
        "active_blocks": sum(1 for b in blocks.values() if b["active"]),
        "blocks": blocks,
        "superseded_ids": sorted(superseded),
        "tag_index": dict(sorted(tag_index.items())),
        "component_index": dict(sorted(component_index.items())),
    }

    MANIFEST_FILE.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n  {MANIFEST_FILE.name}: {manifest['active_blocks']} active blocks, "
          f"{len(manifest['tag_index'])} tags, {len(manifest['component_index'])} components")


if __name__ == "__main__":
    print("Building component indexes...")
    by_component = build_indexes()
    print("\nBuilding block manifest...")
    build_manifest(by_component)
    print("\nDone.")
