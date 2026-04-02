#!/usr/bin/env python3
"""Analyze ccusage JSON output — compute model splits, burn rates, trends.

Usage:
    python cost-analyzer.py daily <ccusage-daily.json>       # Parse daily data
    python cost-analyzer.py blocks <ccusage-blocks.json>     # Parse block data
    python cost-analyzer.py trend <ccusage-daily.json>       # 7-day trend analysis

Output: JSON with computed metrics.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


def parse_json_input(path: str) -> list[dict] | dict:
    """Read JSON file from ccusage output."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def compute_model_split(daily_data: list[dict]) -> list[dict]:
    """Compute cost percentage per model from daily records.

    Input: ccusage daily JSON (list of records with model, cost fields).
    Output: list of {model, cost, percentage} sorted by cost desc.
    """
    model_costs: dict[str, float] = {}
    for record in daily_data:
        model = record.get("model", "unknown")
        cost = float(record.get("cost", 0))
        model_costs[model] = model_costs.get(model, 0) + cost

    total = sum(model_costs.values())
    if total == 0:
        return []

    result = []
    for model, cost in sorted(model_costs.items(), key=lambda x: -x[1]):
        result.append({
            "model": model,
            "cost": round(cost, 4),
            "percentage": round((cost / total) * 100, 1),
        })
    return result


def compute_burn_rate(block_data: list[dict]) -> dict | None:
    """Compute burn rate from active billing block.

    Input: ccusage blocks JSON.
    Output: {block_start, elapsed_hours, cost_so_far, rate_per_hour, projected_5h}
    """
    if not block_data:
        return None

    # Last block is typically the active one
    active = block_data[-1]
    cost = float(active.get("cost", 0))
    start = active.get("start", "")

    try:
        start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        elapsed = (datetime.now(start_dt.tzinfo) - start_dt).total_seconds() / 3600
    except (ValueError, TypeError):
        elapsed = 1.0  # fallback

    if elapsed <= 0:
        elapsed = 0.1

    rate = cost / elapsed
    projected = rate * 5  # 5-hour block

    return {
        "block_start": start,
        "elapsed_hours": round(elapsed, 2),
        "cost_so_far": round(cost, 4),
        "rate_per_hour": round(rate, 4),
        "projected_5h": round(projected, 2),
    }


def compute_cache_efficiency(block_data: list[dict]) -> dict:
    """Compute cache read efficiency from block token data.

    Output: {cache_read_tokens, input_tokens, ratio, assessment}
    """
    total_cache_read = 0
    total_input = 0

    for block in block_data:
        total_cache_read += int(block.get("cache_read", 0))
        total_input += int(block.get("input", 0))

    total = total_cache_read + total_input
    ratio = (total_cache_read / total * 100) if total > 0 else 0

    if ratio >= 80:
        assessment = "good"
    elif ratio >= 60:
        assessment = "needs_attention"
    else:
        assessment = "broken"

    return {
        "cache_read_tokens": total_cache_read,
        "input_tokens": total_input,
        "ratio_percent": round(ratio, 1),
        "assessment": assessment,
    }


def compute_trend(daily_data: list[dict], days: int = 7) -> dict:
    """Compute daily cost trend over last N days.

    Output: {daily_costs: [{date, cost, delta}], direction, avg_daily}
    """
    # Group by date
    date_costs: dict[str, float] = {}
    for record in daily_data:
        date = record.get("date", "unknown")
        cost = float(record.get("cost", 0))
        date_costs[date] = date_costs.get(date, 0) + cost

    # Sort by date, take last N
    sorted_dates = sorted(date_costs.items())[-days:]

    result = []
    prev_cost = None
    for date, cost in sorted_dates:
        delta = round(cost - prev_cost, 4) if prev_cost is not None else 0
        result.append({"date": date, "cost": round(cost, 4), "delta": delta})
        prev_cost = cost

    # Overall direction
    if len(result) >= 2:
        first_half = sum(r["cost"] for r in result[: len(result) // 2])
        second_half = sum(r["cost"] for r in result[len(result) // 2 :])
        direction = "rising" if second_half > first_half * 1.1 else (
            "falling" if second_half < first_half * 0.9 else "stable"
        )
    else:
        direction = "insufficient_data"

    avg = sum(r["cost"] for r in result) / len(result) if result else 0

    return {
        "daily_costs": result,
        "direction": direction,
        "avg_daily": round(avg, 4),
    }


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    data_path = sys.argv[2]
    data = parse_json_input(data_path)

    if not isinstance(data, list):
        data = [data]

    if command == "daily":
        result = {
            "model_split": compute_model_split(data),
            "total_cost": round(sum(float(r.get("cost", 0)) for r in data), 4),
        }
    elif command == "blocks":
        result = {
            "burn_rate": compute_burn_rate(data),
            "cache_efficiency": compute_cache_efficiency(data),
        }
    elif command == "trend":
        result = compute_trend(data)
    else:
        print(f"ERROR: Unknown command '{command}'", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
