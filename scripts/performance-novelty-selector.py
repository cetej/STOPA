#!/usr/bin/env python3
"""Performance-Novelty Branch Selector for self-evolve group mode.

GEA-inspired (arXiv:2602.04837): ranks parallel evolution branches
by score = pass_rate × sqrt(novelty), where novelty is mean Jaccard
distance of each branch's changed-functions set from all others.

No embedding model needed — pure set operations on function names.

Usage:
    python scripts/performance-novelty-selector.py <trace_buffer_path> [--top N] [--json]

Arguments:
    trace_buffer_path  Path to shared trace buffer JSONL
                       (intermediate/gea-<target>/traces.jsonl)
    --top N            Return top N branches (default: 2)
    --json             Output raw JSON (default: human-readable)
    --round N          Only consider entries up to this round (default: all)

Trace buffer format (one JSON per line):
    {"branch": 1, "round": 3, "strategy": "adversarial",
     "patch_summary": "...", "files_changed": [...],
     "functions_changed": ["validate_input", "parse_args"],
     "outcome": "success", "pass_rate_delta": 0.08}
"""
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load_traces(path: Path, max_round: int | None = None) -> list[dict]:
    """Load JSONL trace buffer, optionally filtering by round."""
    traces = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            entry = json.loads(line)
            if max_round is not None and entry.get("round", 0) > max_round:
                continue
            traces.append(entry)
    return traces


def build_branch_profiles(traces: list[dict]) -> dict[int, dict]:
    """Aggregate per-branch stats from traces."""
    branches: dict[int, dict] = defaultdict(lambda: {
        "functions_changed": set(),
        "pass_rates": [],
        "outcomes": [],
        "strategies": [],
        "rounds": 0,
    })

    for entry in traces:
        bid = entry["branch"]
        b = branches[bid]
        b["functions_changed"].update(entry.get("functions_changed", []))
        if "pass_rate_delta" in entry:
            b["pass_rates"].append(entry["pass_rate_delta"])
        b["outcomes"].append(entry.get("outcome", "unknown"))
        b["strategies"].append(entry.get("strategy", "unknown"))
        b["rounds"] += 1

    return dict(branches)


def jaccard_distance(set_a: set, set_b: set) -> float:
    """Jaccard distance = 1 - |A∩B| / |A∪B|. Returns 1.0 if both empty."""
    if not set_a and not set_b:
        return 0.0
    union = set_a | set_b
    if not union:
        return 0.0
    return 1.0 - len(set_a & set_b) / len(union)


def compute_novelty(profiles: dict[int, dict]) -> dict[int, float]:
    """Mean Jaccard distance of each branch from all others."""
    branch_ids = list(profiles.keys())
    novelties = {}

    for bid in branch_ids:
        if len(branch_ids) < 2:
            novelties[bid] = 1.0
            continue

        distances = []
        for other_bid in branch_ids:
            if other_bid == bid:
                continue
            d = jaccard_distance(
                profiles[bid]["functions_changed"],
                profiles[other_bid]["functions_changed"],
            )
            distances.append(d)

        novelties[bid] = sum(distances) / len(distances) if distances else 0.0

    return novelties


def compute_pass_rate(profile: dict) -> float:
    """Estimate branch quality from outcome history."""
    outcomes = profile["outcomes"]
    if not outcomes:
        return 0.0
    score_map = {"success": 1.0, "partial": 0.5, "failure": 0.0, "unknown": 0.0}
    total = sum(score_map.get(o, 0.0) for o in outcomes)
    return total / len(outcomes)


def rank_branches(
    profiles: dict[int, dict],
    novelties: dict[int, float],
    top: int,
) -> list[dict]:
    """Rank branches by GEA score = pass_rate × sqrt(novelty + epsilon)."""
    epsilon = 0.01
    ranked = []

    for bid, profile in profiles.items():
        pr = compute_pass_rate(profile)
        nov = novelties.get(bid, 0.0)
        score = pr * math.sqrt(nov + epsilon)

        ranked.append({
            "branch": bid,
            "score": round(score, 4),
            "pass_rate": round(pr, 3),
            "novelty": round(nov, 3),
            "functions_changed": len(profile["functions_changed"]),
            "rounds": profile["rounds"],
            "outcomes": profile["outcomes"],
            "dominant_strategy": max(
                set(profile["strategies"]),
                key=profile["strategies"].count,
            ) if profile["strategies"] else None,
        })

    ranked.sort(key=lambda x: -x["score"])
    return ranked[:top]


def main() -> None:
    trace_path = None
    top = 2
    output_json = False
    max_round = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--top" and i + 1 < len(args):
            top = int(args[i + 1])
            i += 2
        elif args[i] == "--json":
            output_json = True
            i += 1
        elif args[i] == "--round" and i + 1 < len(args):
            max_round = int(args[i + 1])
            i += 2
        elif not args[i].startswith("--"):
            trace_path = Path(args[i])
            i += 1
        else:
            i += 1

    if trace_path is None:
        print(json.dumps({"error": "Usage: performance-novelty-selector.py <trace_buffer.jsonl> [--top N] [--json]"}))
        sys.exit(1)

    if not trace_path.exists():
        print(json.dumps({"error": f"Trace buffer not found: {trace_path}", "branches": []}))
        sys.exit(1)

    traces = load_traces(trace_path, max_round)
    if not traces:
        print(json.dumps({"error": "Empty trace buffer", "branches": []}))
        sys.exit(1)

    profiles = build_branch_profiles(traces)
    novelties = compute_novelty(profiles)
    ranked = rank_branches(profiles, novelties, top)

    # Add rank numbers
    for k, entry in enumerate(ranked):
        entry["rank"] = k + 1
        # Convert outcomes list to summary for cleaner output
        entry["outcome_summary"] = f"{entry['outcomes'].count('success')}W/{entry['outcomes'].count('failure')}L/{entry['outcomes'].count('partial')}P"
        del entry["outcomes"]

    result = {
        "ranked": ranked,
        "total_branches": len(profiles),
        "total_traces": len(traces),
        "data_source": str(trace_path),
        "formula": "score = pass_rate × sqrt(novelty + 0.01)",
    }

    if output_json:
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
