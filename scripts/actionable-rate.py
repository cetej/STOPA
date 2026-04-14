#!/usr/bin/env python3
"""
Actionable Rate Calculator for /watch → ingest → learnings pipeline.

Parses news.md Action Items table and calculates:
- actionable_rate = items with acted=yes / total active items
- breakdown by urgency tier
- stale items (no action after 14+ days)

Usage:
    python scripts/actionable-rate.py              # summary
    python scripts/actionable-rate.py --detail      # per-item breakdown
    python scripts/actionable-rate.py --json        # machine-readable output
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NEWS_PATH = Path(__file__).parent.parent / ".claude" / "memory" / "news.md"


def parse_action_items(text: str) -> list[dict]:
    """Parse the Action Items markdown table into structured records."""
    items = []
    # Match table rows: | # | Item | Urgency | Acted | Evidence | Next Step |
    pattern = re.compile(
        r"^\|\s*(\d+\w?)\s*\|"       # item number
        r"\s*(.*?)\s*\|"              # item description
        r"\s*(HIGH|MED|LOW|INFO|PARKED)\s*\|"  # urgency
        r"\s*\*{0,2}(yes|no)\*{0,2}\s*\|"     # acted (with optional bold)
        r"\s*(.*?)\s*\|"              # evidence
        r"\s*(.*?)\s*\|",             # next step
        re.IGNORECASE,
    )

    for line in text.splitlines():
        m = pattern.match(line.strip())
        if m:
            items.append({
                "id": m.group(1).strip(),
                "item": re.sub(r"\*{1,2}", "", m.group(2)).strip()[:80],
                "urgency": m.group(3).strip().upper(),
                "acted": m.group(4).strip().lower() == "yes",
                "evidence": m.group(5).strip().replace("—", "").strip(),
                "next_step": m.group(6).strip()[:60],
            })
    return items


def parse_resolved_items(text: str) -> int:
    """Count resolved items (all are acted by definition)."""
    count = 0
    in_resolved = False
    for line in text.splitlines():
        if "## Resolved" in line:
            in_resolved = True
            continue
        if in_resolved and line.startswith("## "):
            in_resolved = False
        if in_resolved and line.startswith("|") and not line.startswith("| #") and not line.startswith("|---"):
            count += 1
    return count


def calculate_metrics(items: list[dict], resolved_count: int) -> dict:
    """Calculate actionable rate and breakdown metrics."""
    total = len(items)
    acted = sum(1 for i in items if i["acted"])
    not_acted = total - acted

    by_urgency = {}
    for urg in ["HIGH", "MED", "LOW", "INFO", "PARKED"]:
        urg_items = [i for i in items if i["urgency"] == urg]
        urg_acted = sum(1 for i in urg_items if i["acted"])
        if urg_items:
            by_urgency[urg] = {
                "total": len(urg_items),
                "acted": urg_acted,
                "rate": round(urg_acted / len(urg_items) * 100, 1),
            }

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "active_items": total,
        "acted": acted,
        "not_acted": not_acted,
        "actionable_rate": round(acted / total * 100, 1) if total else 0,
        "resolved_count": resolved_count,
        "by_urgency": by_urgency,
        "target_rate": 50.0,
        "gap": round(50.0 - (acted / total * 100 if total else 0), 1),
    }


def print_summary(metrics: dict, items: list[dict]) -> None:
    """Print human-readable summary."""
    print("=" * 50)
    print("  WATCH → INGEST → LEARNINGS: Actionable Rate")
    print("=" * 50)
    print()
    print(f"  Active items:    {metrics['active_items']}")
    print(f"  Acted on:        {metrics['acted']}")
    print(f"  Not acted:       {metrics['not_acted']}")
    print(f"  Resolved (arch): {metrics['resolved_count']}")
    print()
    print(f"  >>> ACTIONABLE RATE: {metrics['actionable_rate']}% <<<")
    print(f"  >>> TARGET:          {metrics['target_rate']}% <<<")
    print(f"  >>> GAP:             {metrics['gap']}pp <<<")
    print()

    print("  By urgency:")
    for urg, data in metrics["by_urgency"].items():
        bar = "#" * data["acted"] + "." * (data["total"] - data["acted"])
        print(f"    {urg:6s}  [{bar}]  {data['acted']}/{data['total']} ({data['rate']}%)")
    print()

    # Top candidates for action (HIGH urgency, not acted)
    high_unacted = [i for i in items if i["urgency"] == "HIGH" and not i["acted"]]
    if high_unacted:
        print("  HIGH urgency, NOT acted (priority candidates):")
        for i in high_unacted:
            print(f"    #{i['id']}: {i['item'][:60]}")
        print()


def print_detail(items: list[dict]) -> None:
    """Print per-item breakdown."""
    print(f"{'#':>4s}  {'Acted':5s}  {'Urg':6s}  Item")
    print("-" * 70)
    for i in items:
        mark = "YES" if i["acted"] else "  -"
        print(f"  {i['id']:>3s}  {mark:5s}  {i['urgency']:6s}  {i['item'][:55]}")


def main() -> None:
    if not NEWS_PATH.exists():
        print(f"ERROR: {NEWS_PATH} not found", file=sys.stderr)
        sys.exit(1)

    text = NEWS_PATH.read_text(encoding="utf-8")
    items = parse_action_items(text)
    resolved = parse_resolved_items(text)

    if not items:
        print("ERROR: No action items parsed from news.md", file=sys.stderr)
        print("Check that the table format matches: | # | Item | Urgency | Acted | Evidence | Next Step |")
        sys.exit(1)

    metrics = calculate_metrics(items, resolved)

    if "--json" in sys.argv:
        metrics["items"] = items
        print(json.dumps(metrics, indent=2, ensure_ascii=False))
    elif "--detail" in sys.argv:
        print_detail(items)
        print()
        print(f"Actionable rate: {metrics['actionable_rate']}% (target: {metrics['target_rate']}%)")
    else:
        print_summary(metrics, items)


if __name__ == "__main__":
    main()
