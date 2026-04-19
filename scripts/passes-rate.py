#!/usr/bin/env python3
"""
Passes Rate Calculator — feature-level completion metric across registered projects.

Reads ~/.claude/memory/projects.json for project registry, then scans each
project's docs/feature-list.json (if present) and calculates:
- passes_rate per project = features passes:true / total features
- global passes_rate = sum(passed) / sum(total)
- stale projects (feature-list.json not updated in 30+ days)

Inspired by Anthropic Claude Code harness: feature-list.json as ground truth
prevents agents from "declaring victory too early" on multi-session projects.

Usage:
    python scripts/passes-rate.py              # summary table
    python scripts/passes-rate.py --detail     # per-feature breakdown
    python scripts/passes-rate.py --json       # machine-readable
    python scripts/passes-rate.py --project X  # single project
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_REGISTRY = Path.home() / ".claude" / "memory" / "projects.json"
STALE_DAYS = 30


def load_registry(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"ERROR: registry {path} invalid JSON: {e}", file=sys.stderr)
        return []
    return data.get("projects", [])


def load_feature_list(project_path: Path) -> dict | None:
    fl_path = project_path / "docs" / "feature-list.json"
    if not fl_path.exists():
        return None
    try:
        data = json.loads(fl_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"_invalid": True, "_path": str(fl_path)}
    data["_mtime"] = fl_path.stat().st_mtime
    data["_path"] = str(fl_path)
    return data


def calc_project_stats(project: dict) -> dict:
    name = project.get("name", "?")
    path = Path(project.get("path", ""))
    stats = {
        "name": name,
        "path": str(path),
        "status": project.get("status", "unknown"),
        "has_feature_list": False,
        "total": 0,
        "passed": 0,
        "rate": 0.0,
        "stale_days": None,
        "features": [],
    }

    if not path.exists():
        stats["error"] = "path not found"
        return stats

    fl = load_feature_list(path)
    if fl is None:
        return stats

    stats["has_feature_list"] = True

    if fl.get("_invalid"):
        stats["error"] = f"feature-list.json invalid JSON: {fl['_path']}"
        return stats

    features = fl.get("features", [])
    stats["total"] = len(features)
    passed = [f for f in features if f.get("passes") is True]
    stats["passed"] = len(passed)
    stats["rate"] = stats["passed"] / stats["total"] if stats["total"] else 0.0

    mtime = fl.get("_mtime", 0)
    if mtime:
        age = (datetime.now(timezone.utc).timestamp() - mtime) / 86400
        stats["stale_days"] = round(age, 1)

    stats["features"] = [
        {
            "id": f.get("id", "?"),
            "category": f.get("category", "?"),
            "description": f.get("description", "")[:80],
            "passes": bool(f.get("passes", False)),
        }
        for f in features
    ]
    return stats


def print_summary(all_stats: list[dict]) -> None:
    harness_projects = [s for s in all_stats if s["has_feature_list"]]
    no_harness = [s for s in all_stats if not s["has_feature_list"]]

    print("=" * 72)
    print("PASSES RATE — feature completion across registered projects")
    print("=" * 72)

    if harness_projects:
        total_feat = sum(s["total"] for s in harness_projects)
        total_pass = sum(s["passed"] for s in harness_projects)
        global_rate = total_pass / total_feat if total_feat else 0.0

        print(f"\nGlobal: {total_pass}/{total_feat} features pass ({global_rate:.1%})")
        print(f"Harness-adopted: {len(harness_projects)}/{len(all_stats)} projects\n")

        print(f"{'Project':<20} {'Status':<10} {'Passed/Total':<15} {'Rate':<8} {'Stale':<8}")
        print("-" * 72)
        for s in sorted(harness_projects, key=lambda x: x["rate"]):
            stale = f"{s['stale_days']}d" if s["stale_days"] is not None else "-"
            marker = " !" if s["stale_days"] and s["stale_days"] > STALE_DAYS else ""
            err = f" [ERR: {s['error']}]" if "error" in s else ""
            print(
                f"{s['name']:<20} {s['status']:<10} "
                f"{s['passed']}/{s['total']:<14} {s['rate']:.1%}   {stale:<6}{marker}{err}"
            )
    else:
        print("\nNo projects have docs/feature-list.json yet.")
        print("Run `/project-init <path> --harness` on a project to enable tracking.\n")

    if no_harness:
        print(f"\nProjects without harness ({len(no_harness)}):")
        for s in no_harness:
            err = f"  [{s['error']}]" if "error" in s else ""
            print(f"  - {s['name']}{err}")

    print()


def print_detail(all_stats: list[dict]) -> None:
    print_summary(all_stats)
    print("=" * 72)
    print("PER-FEATURE BREAKDOWN")
    print("=" * 72)
    for s in all_stats:
        if not s["has_feature_list"] or "error" in s:
            continue
        print(f"\n{s['name']} — {s['passed']}/{s['total']} ({s['rate']:.1%})")
        for f in s["features"]:
            mark = "[x]" if f["passes"] else "[ ]"
            print(f"  {mark} {f['id']:<6} {f['category']:<15} {f['description']}")


def print_json(all_stats: list[dict]) -> None:
    harness = [s for s in all_stats if s["has_feature_list"]]
    total_feat = sum(s["total"] for s in harness)
    total_pass = sum(s["passed"] for s in harness)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "global": {
            "total_features": total_feat,
            "passed_features": total_pass,
            "rate": total_pass / total_feat if total_feat else 0.0,
            "harness_adopted_projects": len(harness),
            "total_projects": len(all_stats),
        },
        "projects": all_stats,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Passes rate across registered projects")
    parser.add_argument("--detail", action="store_true", help="per-feature breakdown")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--project", help="filter to single project by name")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY,
                        help=f"registry path (default: {DEFAULT_REGISTRY})")
    args = parser.parse_args()

    projects = load_registry(args.registry)
    if args.project:
        projects = [p for p in projects if p.get("name", "").lower() == args.project.lower()]
        if not projects:
            print(f"ERROR: project '{args.project}' not in registry", file=sys.stderr)
            return 1

    all_stats = [calc_project_stats(p) for p in projects]

    if args.json:
        print_json(all_stats)
    elif args.detail:
        print_detail(all_stats)
    else:
        print_summary(all_stats)
    return 0


if __name__ == "__main__":
    sys.exit(main())
