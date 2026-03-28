#!/usr/bin/env python3
"""Build L2 component index files from learnings YAML frontmatter.

Generates .claude/memory/learnings/index-<component>.md files.
These serve as the middle layer (L2) in the hierarchical retrieval:
  L1: critical-patterns.md (always-read, top 10)
  L2: index-<component>.md (keyword-routed, per-component)
  L3: individual learning files (read on demand)

Run during /scribe maintenance or after adding new learnings.
"""
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LEARNINGS_DIR = Path(".claude/memory/learnings")
INDEX_PREFIX = "index-"


def parse_frontmatter(filepath: Path) -> dict | None:
    """Parse YAML frontmatter from a learning file."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None

    entry = {"file": filepath.name}
    for line in lines[1:12]:
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
        elif key == "summary":
            entry["summary"] = val.strip("'\"")
        elif key in ("date", "type", "severity", "component"):
            entry[key] = val

    return entry if "component" in entry else None


def build_indexes():
    """Group learnings by component and write index files."""
    if not LEARNINGS_DIR.exists():
        print("ERROR: learnings directory not found")
        return

    # Collect entries by component
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
        # Sort by date descending (newest first)
        entries.sort(key=lambda e: e.get("date", ""), reverse=True)

        lines = [
            f"# Component Index: {component}",
            f"",
            f"Auto-generated L2 index. {len(entries)} learnings.",
            f"",
            f"| Date | File | Severity | Summary |",
            f"|------|------|----------|---------|",
        ]

        for e in entries:
            date = e.get("date", "?")
            fname = e["file"]
            sev = e.get("severity", "?")
            summary = e.get("summary", e.get("tags", ["no summary"])[0] if e.get("tags") else "no summary")
            # Truncate summary for table
            if len(summary) > 80:
                summary = summary[:77] + "..."
            lines.append(f"| {date} | [{fname}]({fname}) | {sev} | {summary} |")

        lines.append("")
        lines.append("## Tags in this component")
        lines.append("")
        # Collect all tags
        all_tags = set()
        for e in entries:
            all_tags.update(e.get("tags", []))
        lines.append(", ".join(sorted(all_tags)))
        lines.append("")

        index_path = LEARNINGS_DIR / f"{INDEX_PREFIX}{component}.md"
        index_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"  {index_path.name}: {len(entries)} entries")

    print(f"\nDone. {len(by_component)} component indexes generated.")


if __name__ == "__main__":
    build_indexes()
