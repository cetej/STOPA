"""Retrieval metrics dashboard — Phase C ADR 0016 re-evaluation support.

Reads `.claude/memory/retrieval-metrics.jsonl` and reports:
- Miss rate (queries returning 0 results)
- Latency distribution (p50, p95, max)
- Signal composition (which retrieval paths contribute)

Council verdict thresholds (for July 2026 re-evaluation):
- Miss rate > 8% → upgrade to vector index (Qdrant/LanceDB)
- p95 latency > 300ms → upgrade to vector index

Usage:
    python scripts/retrieval-metrics-report.py
    python scripts/retrieval-metrics-report.py --since 2026-04-21
    python scripts/retrieval-metrics-report.py --json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STOPA_ROOT = Path(__file__).resolve().parent.parent
METRICS_FILE = STOPA_ROOT / ".claude" / "memory" / "retrieval-metrics.jsonl"

# Council thresholds — keep in sync with outputs/adr-0016-phase-c-council.md
THRESHOLD_MISS_RATE = 0.08
THRESHOLD_P95_LATENCY_MS = 300


def load_entries(since: str | None) -> list[dict]:
    if not METRICS_FILE.exists():
        return []
    entries = []
    cutoff = None
    if since:
        try:
            cutoff = datetime.fromisoformat(since)
        except ValueError:
            print(f"WARN: could not parse --since '{since}', ignoring")
    for line in METRICS_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if cutoff:
            try:
                ts = datetime.fromisoformat(e.get("ts", ""))
                if ts < cutoff:
                    continue
            except ValueError:
                continue
        entries.append(e)
    return entries


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    sorted_v = sorted(values)
    idx = int(len(sorted_v) * pct / 100)
    idx = min(idx, len(sorted_v) - 1)
    return sorted_v[idx]


def compute_stats(entries: list[dict]) -> dict:
    if not entries:
        return {"total": 0}

    misses = sum(1 for e in entries if e.get("miss"))
    latencies = [e.get("duration_ms", 0) for e in entries]
    signal_freq = Counter()
    tier_dist = Counter()
    for e in entries:
        for sig in e.get("signals", []):
            signal_freq[sig] += 1
        tier_dist[e.get("task_tier", "unknown")] += 1

    return {
        "total": len(entries),
        "misses": misses,
        "miss_rate": round(misses / len(entries), 4),
        "latency_p50_ms": int(percentile(latencies, 50)),
        "latency_p95_ms": int(percentile(latencies, 95)),
        "latency_max_ms": max(latencies) if latencies else 0,
        "signal_freq": dict(signal_freq.most_common()),
        "tier_dist": dict(tier_dist.most_common()),
        "first_ts": entries[0].get("ts"),
        "last_ts": entries[-1].get("ts"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--since", help="ISO date/datetime to filter from (e.g. 2026-04-21)")
    parser.add_argument("--json", action="store_true", help="machine-readable JSON output")
    args = parser.parse_args()

    entries = load_entries(args.since)
    stats = compute_stats(entries)

    if args.json:
        stats["thresholds"] = {
            "miss_rate": THRESHOLD_MISS_RATE,
            "p95_latency_ms": THRESHOLD_P95_LATENCY_MS,
            "miss_breach": stats.get("miss_rate", 0) > THRESHOLD_MISS_RATE,
            "latency_breach": stats.get("latency_p95_ms", 0) > THRESHOLD_P95_LATENCY_MS,
        }
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return 0

    if stats["total"] == 0:
        print("No retrieval metrics logged yet.")
        print(f"(Expected at: {METRICS_FILE})")
        return 0

    print(f"Retrieval metrics — {stats['total']} queries ({stats['first_ts']} → {stats['last_ts']})")
    print()
    print(f"  Miss rate:   {stats['miss_rate']*100:.2f}% ({stats['misses']}/{stats['total']})  {'⚠️ BREACH' if stats['miss_rate'] > THRESHOLD_MISS_RATE else 'OK'} (threshold {THRESHOLD_MISS_RATE*100:.0f}%)")
    print(f"  Latency p50: {stats['latency_p50_ms']} ms")
    print(f"  Latency p95: {stats['latency_p95_ms']} ms  {'⚠️ BREACH' if stats['latency_p95_ms'] > THRESHOLD_P95_LATENCY_MS else 'OK'} (threshold {THRESHOLD_P95_LATENCY_MS} ms)")
    print(f"  Latency max: {stats['latency_max_ms']} ms")
    print()
    print("  Signal frequency:")
    for sig, cnt in stats["signal_freq"].items():
        pct = cnt / stats["total"] * 100
        print(f"    {sig:<12} {cnt:>4} ({pct:.1f}%)")
    print()
    print("  Tier distribution:")
    for tier, cnt in stats["tier_dist"].items():
        pct = cnt / stats["total"] * 100
        print(f"    {tier:<10} {cnt:>4} ({pct:.1f}%)")

    # Council decision trigger
    if stats["miss_rate"] > THRESHOLD_MISS_RATE or stats["latency_p95_ms"] > THRESHOLD_P95_LATENCY_MS:
        print()
        print("  🔴 DECISION TRIGGER: breach detected — evaluate vector index upgrade (Qdrant/LanceDB).")
        print("     See outputs/adr-0016-phase-c-council.md for Phase C re-evaluation plan.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
