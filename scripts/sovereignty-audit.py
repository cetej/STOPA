#!/usr/bin/env python3
"""
V5: Memory Sovereignty Audit

Scans all memory locations and reports ownership status:
  ✅ Git-tracked (we own it)
  ⚠️  Auto-memory only (Anthropic-controlled format, not in git)
  ❌ Server-only (compaction state, conversation history — no local copy)

Usage:
  python scripts/sovereignty-audit.py
  python scripts/sovereignty-audit.py --verbose
  python scripts/sovereignty-audit.py --json
"""

import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --- Configuration ---

STOPA_ROOT = Path(__file__).resolve().parent.parent
GIT_MEMORY = STOPA_ROOT / ".claude" / "memory"
GIT_LEARNINGS = GIT_MEMORY / "learnings"

AUTO_MEMORY_BASE = Path.home() / ".claude" / "projects"
STOPA_AUTO = AUTO_MEMORY_BASE / "C--Users-stock-Documents-000-NGM-STOPA" / "memory"

# Known project auto-memory directories
PROJECT_DIRS = {
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

# Server-only items we know exist but can't access
SERVER_ONLY = [
    "Conversation history (server-side, no export API)",
    "Compaction summaries (server-side, opaque)",
    "Tool result cache (ephemeral, per-session)",
    "Model attention/context state (inference-time only)",
]


def scan_git_memory() -> dict:
    """Scan git-tracked memory files."""
    result = {"files": [], "total_size": 0, "count": 0}

    if not GIT_MEMORY.exists():
        return result

    for f in sorted(GIT_MEMORY.rglob("*.md")):
        rel = f.relative_to(STOPA_ROOT)
        size = f.stat().st_size
        result["files"].append({"path": str(rel), "size": size})
        result["total_size"] += size
        result["count"] += 1

    for f in sorted(GIT_MEMORY.rglob("*.json")):
        rel = f.relative_to(STOPA_ROOT)
        size = f.stat().st_size
        result["files"].append({"path": str(rel), "size": size})
        result["total_size"] += size
        result["count"] += 1

    for f in sorted(GIT_MEMORY.rglob("*.jsonl")):
        rel = f.relative_to(STOPA_ROOT)
        size = f.stat().st_size
        result["files"].append({"path": str(rel), "size": size})
        result["total_size"] += size
        result["count"] += 1

    return result


def scan_auto_memory() -> dict:
    """Scan all auto-memory directories."""
    result = {"projects": {}, "total_size": 0, "total_files": 0}

    if not AUTO_MEMORY_BASE.exists():
        return result

    for project_name, dir_name in PROJECT_DIRS.items():
        mem_dir = AUTO_MEMORY_BASE / dir_name / "memory"
        if not mem_dir.exists():
            continue

        project_files = []
        project_size = 0
        for f in sorted(mem_dir.rglob("*")):
            if f.is_file():
                size = f.stat().st_size
                project_files.append({"name": f.name, "size": size})
                project_size += size

        result["projects"][project_name] = {
            "files": project_files,
            "count": len(project_files),
            "size": project_size,
        }
        result["total_size"] += project_size
        result["total_files"] += len(project_files)

    # Scan for unknown project dirs
    for d in sorted(AUTO_MEMORY_BASE.iterdir()):
        if not d.is_dir():
            continue
        name = d.name
        if name not in PROJECT_DIRS.values():
            mem_dir = d / "memory"
            if mem_dir.exists():
                count = sum(1 for f in mem_dir.rglob("*") if f.is_file())
                if count > 0:
                    result["projects"][f"UNKNOWN:{name}"] = {
                        "files": [],
                        "count": count,
                        "size": 0,
                    }

    return result


def find_auto_only(git_mem: dict, auto_mem: dict) -> list:
    """Find auto-memory files that have no git-tracked equivalent."""
    git_names = {Path(f["path"]).name for f in git_mem["files"]}

    auto_only = []
    for project, data in auto_mem["projects"].items():
        for f in data["files"]:
            if f["name"] not in git_names and f["name"] != "MEMORY.md":
                auto_only.append(
                    {"project": project, "file": f["name"], "size": f["size"]}
                )
    return auto_only


def find_git_only(git_mem: dict, auto_mem: dict) -> list:
    """Find git-tracked files with no auto-memory equivalent (good — we own these)."""
    auto_names = set()
    for data in auto_mem["projects"].values():
        for f in data["files"]:
            auto_names.add(f["name"])

    git_only = []
    for f in git_mem["files"]:
        name = Path(f["path"]).name
        if name not in auto_names:
            git_only.append(f)
    return git_only


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}K"
    else:
        return f"{size_bytes / (1024 * 1024):.1f}M"


def print_report(git_mem: dict, auto_mem: dict, auto_only: list, verbose: bool):
    """Print human-readable sovereignty report."""

    print("=" * 60)
    print("  MEMORY SOVEREIGNTY AUDIT")
    print("=" * 60)
    print()

    # --- Git-tracked (owned) ---
    print(f"✅ GIT-TRACKED (we own)")
    print(f"   {git_mem['count']} files, {format_size(git_mem['total_size'])}")
    if verbose:
        # Group by subdirectory
        by_dir: dict[str, int] = {}
        for f in git_mem["files"]:
            parts = Path(f["path"]).parts
            key = "/".join(parts[:3]) if len(parts) > 3 else "/".join(parts[:2])
            by_dir[key] = by_dir.get(key, 0) + 1
        for d, count in sorted(by_dir.items()):
            print(f"     {d}: {count} files")
    print()

    # --- Auto-memory (vendor-controlled) ---
    print(f"⚠️  AUTO-MEMORY (Anthropic-controlled, not in git)")
    print(f"   {auto_mem['total_files']} files across {len(auto_mem['projects'])} projects, {format_size(auto_mem['total_size'])}")
    for project, data in sorted(auto_mem["projects"].items()):
        print(f"     {project}: {data['count']} files ({format_size(data['size'])})")
    print()

    # --- Auto-only (at risk) ---
    if auto_only:
        print(f"⚠️  AUTO-ONLY FILES (no git backup — at risk)")
        print(f"   {len(auto_only)} files exist ONLY in auto-memory:")
        for entry in auto_only[:15]:
            print(f"     [{entry['project']}] {entry['file']} ({format_size(entry['size'])})")
        if len(auto_only) > 15:
            print(f"     ... and {len(auto_only) - 15} more")
    else:
        print("✅ No auto-only files — everything is mirrored in git")
    print()

    # --- Server-only (no access) ---
    print(f"❌ SERVER-ONLY (zero ownership)")
    for item in SERVER_ONLY:
        print(f"     {item}")
    print()

    # --- Summary ---
    total_owned = git_mem["count"]
    total_at_risk = len(auto_only)
    total_lost = len(SERVER_ONLY)
    total = total_owned + total_at_risk + total_lost

    pct_owned = (total_owned / total * 100) if total > 0 else 0

    print("-" * 60)
    print(f"  SOVEREIGNTY SCORE: {pct_owned:.0f}% owned")
    print(f"    ✅ Owned:   {total_owned} items")
    print(f"    ⚠️  At risk: {total_at_risk} items (mirror with mirror-automemory.py)")
    print(f"    ❌ Lost:    {total_lost} items (server-side, no mitigation yet)")
    print("-" * 60)

    # --- Recommendations ---
    print()
    print("RECOMMENDATIONS:")
    if total_at_risk > 0:
        print(f"  1. Run `python scripts/mirror-automemory.py` to backup {total_at_risk} at-risk files")
    if total_at_risk == 0:
        print("  1. Auto-memory mirror is up to date ✅")
    print("  2. Add mirror-automemory.py to /sweep or scheduled task")
    print("  3. Monitor Anthropic for PostCompaction hook API (compaction defense)")
    print("  4. Consider memory-export.py for full portable backup (V3)")


def main():
    parser = argparse.ArgumentParser(description="Memory Sovereignty Audit")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed file listings")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    git_mem = scan_git_memory()
    auto_mem = scan_auto_memory()
    auto_only = find_auto_only(git_mem, auto_mem)

    if args.json:
        report = {
            "git_tracked": {"count": git_mem["count"], "size": git_mem["total_size"]},
            "auto_memory": {
                "total_files": auto_mem["total_files"],
                "total_size": auto_mem["total_size"],
                "projects": {k: {"count": v["count"], "size": v["size"]} for k, v in auto_mem["projects"].items()},
            },
            "auto_only": auto_only,
            "server_only": SERVER_ONLY,
            "sovereignty_pct": round(git_mem["count"] / (git_mem["count"] + len(auto_only) + len(SERVER_ONLY)) * 100),
        }
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        print_report(git_mem, auto_mem, auto_only, args.verbose)


if __name__ == "__main__":
    main()
