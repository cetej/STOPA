#!/usr/bin/env python3
"""
V2: Auto-Memory → Git Mirror

Copies valuable auto-memory files from ~/.claude/projects/*/memory/
into .claude/memory/auto-mirror/ (git-tracked).

This ensures we OWN all memory — not just what Claude Code stores
in its vendor-controlled directory.

Usage:
  python scripts/mirror-automemory.py                  # dry-run (default)
  python scripts/mirror-automemory.py --apply          # actually copy
  python scripts/mirror-automemory.py --apply --all    # mirror ALL projects (not just STOPA)
  python scripts/mirror-automemory.py --diff           # show content diff for changed files
"""

import argparse
import hashlib
import shutil
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- Configuration ---

STOPA_ROOT = Path(__file__).resolve().parent.parent
MIRROR_DIR = STOPA_ROOT / ".claude" / "memory" / "auto-mirror"

AUTO_MEMORY_BASE = Path.home() / ".claude" / "projects"
STOPA_AUTO = AUTO_MEMORY_BASE / "C--Users-stock-Documents-000-NGM-STOPA" / "memory"

# Projects to mirror (beyond STOPA)
ALL_PROJECTS = {
    "STOPA": "C--Users-stock-Documents-000-NGM-STOPA",
    "NG-ROBOT": "C--Users-stock-Documents-000-NGM-NG-ROBOT",
    "ADOBE-AUTOMAT": "C--Users-stock-Documents-000-NGM-ADOBE-AUTOMAT",
    "ZACHVEV": "C--Users-stock-Documents-000-NGM-ZACHVEV",
    "POLYBOT": "C--Users-stock-Documents-000-NGM-POLYBOT",
    "MONITOR": "C--Users-stock-Documents-000-NGM-MONITOR",
    "KARTOGRAF": "C--Users-stock-Documents-000-NGM-KARTOGRAF",
    "GRAFIK": "C--Users-stock-Documents-000-NGM-GRAFIK",
    "DANE": "C--Users-stock-Documents-000-NGM-DANE",
    "ORAKULUM": "C--Users-stock-Documents-000-NGM-ORAKULUM",
}

# Files to skip (not worth mirroring)
SKIP_FILES = {
    "MEMORY.md",  # Index file — auto-generated, CC-specific format
}

# Only mirror these file types
MIRROR_EXTENSIONS = {".md", ".json", ".yaml", ".yml", ".jsonl"}


def file_hash(path: Path) -> str:
    """SHA256 of file content for change detection."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def scan_auto_memory(project_name: str, dir_name: str) -> list[dict]:
    """Scan a project's auto-memory for mirrorable files."""
    mem_dir = AUTO_MEMORY_BASE / dir_name / "memory"
    if not mem_dir.exists():
        return []

    files = []
    for f in sorted(mem_dir.rglob("*")):
        if not f.is_file():
            continue
        if f.name in SKIP_FILES:
            continue
        if f.suffix not in MIRROR_EXTENSIONS:
            continue

        files.append({
            "source": f,
            "project": project_name,
            "name": f.name,
            "size": f.stat().st_size,
            "hash": file_hash(f),
        })

    return files


def get_mirror_path(project_name: str, filename: str) -> Path:
    """Target path in git-tracked mirror directory."""
    if project_name == "STOPA":
        return MIRROR_DIR / filename
    else:
        return MIRROR_DIR / project_name.lower() / filename


def classify_file(source_info: dict) -> str:
    """Classify what action is needed: new, updated, unchanged."""
    target = get_mirror_path(source_info["project"], source_info["name"])

    if not target.exists():
        return "new"

    target_hash = file_hash(target)
    if target_hash != source_info["hash"]:
        return "updated"

    return "unchanged"


def mirror_file(source_info: dict, dry_run: bool) -> str:
    """Copy file to mirror directory. Returns action taken."""
    target = get_mirror_path(source_info["project"], source_info["name"])
    action = classify_file(source_info)

    if action == "unchanged":
        return "unchanged"

    if dry_run:
        return f"would_{action}"

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_info["source"], target)
    return action


def show_diff(source_info: dict):
    """Show content difference between auto-memory and mirror."""
    target = get_mirror_path(source_info["project"], source_info["name"])
    if not target.exists():
        print(f"    [NEW — no existing mirror]")
        return

    source_lines = source_info["source"].read_text(encoding="utf-8", errors="replace").splitlines()
    target_lines = target.read_text(encoding="utf-8", errors="replace").splitlines()

    if source_lines == target_lines:
        print(f"    [identical]")
        return

    # Simple diff summary
    added = len(source_lines) - len(target_lines)
    if added > 0:
        print(f"    [+{added} lines]")
    elif added < 0:
        print(f"    [{added} lines]")
    else:
        print(f"    [same length, content changed]")


def update_mirror_index():
    """Write a MIRROR-INDEX.md file listing all mirrored files."""
    index_path = MIRROR_DIR / "MIRROR-INDEX.md"
    lines = [
        "# Auto-Memory Mirror Index",
        "",
        f"Last mirrored: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "This directory contains git-tracked copies of auto-memory files",
        "from `~/.claude/projects/*/memory/`. Purpose: memory sovereignty —",
        "ensuring we own all memory, not just what Claude Code stores in its",
        "vendor-controlled directory.",
        "",
        "Generated by `scripts/mirror-automemory.py`.",
        "",
        "## Files",
        "",
    ]

    if not MIRROR_DIR.exists():
        return

    for f in sorted(MIRROR_DIR.rglob("*.md")):
        if f.name == "MIRROR-INDEX.md":
            continue
        rel = f.relative_to(MIRROR_DIR)
        size_kb = f.stat().st_size / 1024
        lines.append(f"- `{rel}` ({size_kb:.1f}K)")

    for f in sorted(MIRROR_DIR.rglob("*.json")):
        rel = f.relative_to(MIRROR_DIR)
        size_kb = f.stat().st_size / 1024
        lines.append(f"- `{rel}` ({size_kb:.1f}K)")

    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}K"
    else:
        return f"{size_bytes / (1024 * 1024):.1f}M"


def main():
    parser = argparse.ArgumentParser(description="Auto-Memory → Git Mirror")
    parser.add_argument("--apply", action="store_true", help="Actually copy files (default: dry-run)")
    parser.add_argument("--all", action="store_true", help="Mirror ALL projects, not just STOPA")
    parser.add_argument("--diff", action="store_true", help="Show content diff for changed files")
    args = parser.parse_args()

    dry_run = not args.apply

    # Select projects to mirror
    if args.all:
        projects = ALL_PROJECTS
    else:
        projects = {"STOPA": ALL_PROJECTS["STOPA"]}

    # Scan
    all_files = []
    for project_name, dir_name in projects.items():
        files = scan_auto_memory(project_name, dir_name)
        all_files.extend(files)

    if not all_files:
        print("No auto-memory files found to mirror.")
        return

    # Classify and mirror
    stats = {"new": 0, "updated": 0, "unchanged": 0}

    print(f"{'[DRY RUN] ' if dry_run else ''}Auto-Memory Mirror")
    print(f"  Source: ~/.claude/projects/*/memory/")
    print(f"  Target: .claude/memory/auto-mirror/")
    print(f"  Projects: {', '.join(projects.keys())}")
    print(f"  Files found: {len(all_files)}")
    print()

    for f_info in all_files:
        action = classify_file(f_info)

        if action == "new":
            icon = "➕"
            stats["new"] += 1
        elif action == "updated":
            icon = "🔄"
            stats["updated"] += 1
        else:
            stats["unchanged"] += 1
            continue  # Don't print unchanged files

        target = get_mirror_path(f_info["project"], f_info["name"])
        rel_target = target.relative_to(STOPA_ROOT)
        print(f"  {icon} [{f_info['project']}] {f_info['name']} ({format_size(f_info['size'])}) -> {rel_target}")

        if args.diff and action in ("new", "updated"):
            show_diff(f_info)

        if not dry_run:
            mirror_file(f_info, dry_run=False)

    print()
    print(f"  New: {stats['new']}, Updated: {stats['updated']}, Unchanged: {stats['unchanged']}")

    if dry_run and (stats["new"] > 0 or stats["updated"] > 0):
        print(f"\n  Run with --apply to execute mirror.")
    elif not dry_run and (stats["new"] > 0 or stats["updated"] > 0):
        update_mirror_index()
        print(f"\n  Mirror complete. Index updated at .claude/memory/auto-mirror/MIRROR-INDEX.md")
        print(f"  Don't forget to `git add .claude/memory/auto-mirror/`")


if __name__ == "__main__":
    main()
