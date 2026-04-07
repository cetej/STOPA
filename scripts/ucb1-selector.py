#!/usr/bin/env python3
"""UCB1 Strategy Selector for autoloop optstate.

Reads optstate JSON, computes UCB1 scores per strategy category,
outputs ranked strategy recommendations. ASI-Evolve integration (arXiv:2603.29640).

Usage:
    python scripts/ucb1-selector.py [optstate_path] [--c FLOAT] [--top N] [--json]

Arguments:
    optstate_path  Path to optstate JSON (default: .claude/memory/optstate/autoloop.json)
    --c FLOAT      Exploration constant (default: 1.41 = sqrt(2), Auer et al. 2002)
    --top N        Return top N strategies (default: 3)
    --json         Output raw JSON (default: human-readable)
"""
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_OPTSTATE = Path(".claude/memory/optstate/autoloop.json")
C_DEFAULT = math.sqrt(2)

# Canonical strategy categories mapped to mutation keyword patterns
STRATEGY_CATEGORIES = {
    "fix_crashes": ["crash", "error", "fix", "broken", "repair", "bug"],
    "exploit_success": ["variant", "extend", "improve", "similar", "refine", "tweak"],
    "explore_new": ["new approach", "different", "untried", "novel", "alternative"],
    "combine": ["combine", "merge", "both", "hybrid", "mix"],
    "simplify": ["simplify", "remove", "reduce", "less", "clean", "minimal"],
    "radical": ["radical", "rewrite", "opposite", "complete", "from scratch", "rethink"],
}

# Default priority order (fallback when no data)
DEFAULT_ORDER = ["fix_crashes", "exploit_success", "explore_new", "combine", "simplify", "radical"]


def categorize_mutation(text: str) -> str | None:
    """Map a mutation description string to a strategy category."""
    text_lower = text.lower()
    for category, keywords in STRATEGY_CATEGORIES.items():
        if any(kw in text_lower for kw in keywords):
            return category
    return None


def build_strategy_stats(change_ledger: list) -> dict[str, dict]:
    """Build per-strategy win/play counts from change_ledger entries."""
    stats: dict[str, dict] = defaultdict(lambda: {"plays": 0, "wins": 0.0})

    for entry in change_ledger:
        mutations = entry.get("mutations", [])
        outcome = entry.get("outcome", "failure")

        # Score: success=1.0, partial=0.5, failure=0.0
        reward = {"success": 1.0, "partial": 0.5}.get(outcome, 0.0)

        for mutation in mutations:
            category = categorize_mutation(mutation)
            if category:
                stats[category]["plays"] += 1
                stats[category]["wins"] += reward

    return dict(stats)


def ucb1_score(wins: float, plays: int, total_plays: int, c: float) -> float:
    """Compute UCB1 score. Unplayed strategies return inf (explore first)."""
    if plays == 0:
        return float("inf")
    avg_reward = wins / plays
    exploration = c * math.sqrt(math.log(total_plays) / plays)
    return avg_reward + exploration


def rank_strategies(stats: dict, total_plays: int, c: float, top: int) -> list[dict]:
    """Rank all strategy categories by UCB1 score."""
    ranked = []
    for category in STRATEGY_CATEGORIES:
        s = stats.get(category, {"plays": 0, "wins": 0.0})
        score = ucb1_score(s["wins"], s["plays"], max(total_plays, 1), c)
        ranked.append({
            "strategy": category,
            "score": round(score, 3) if score != float("inf") else None,
            "plays": s["plays"],
            "wins": round(s["wins"], 1),
            "avg_reward": round(s["wins"] / s["plays"], 3) if s["plays"] > 0 else None,
        })

    # Sort: None (inf/unplayed) first, then by score descending
    ranked.sort(key=lambda x: (x["score"] is not None, -(x["score"] or 0)))
    return ranked[:top]


def main() -> None:
    optstate_path = DEFAULT_OPTSTATE
    c = C_DEFAULT
    top = 3
    output_json = False

    # Parse args
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--c" and i + 1 < len(args):
            c = float(args[i + 1])
            i += 2
        elif args[i] == "--top" and i + 1 < len(args):
            top = int(args[i + 1])
            i += 2
        elif args[i] == "--json":
            output_json = True
            i += 1
        elif not args[i].startswith("--"):
            optstate_path = Path(args[i])
            i += 1
        else:
            i += 1

    # Load optstate
    if not optstate_path.exists():
        result = {
            "ranked": [
                {"rank": k + 1, "strategy": s, "score": None, "plays": 0, "wins": 0, "avg_reward": None}
                for k, s in enumerate(DEFAULT_ORDER[:top])
            ],
            "total_plays": 0,
            "data_source": str(optstate_path),
            "c": round(c, 3),
            "status": "no_data_default",
        }
        print(json.dumps(result, indent=2))
        return

    try:
        optstate = json.loads(optstate_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(json.dumps({"error": f"Cannot read optstate: {e}"}))
        return

    change_ledger = optstate.get("change_ledger", [])
    if len(change_ledger) < 3:
        result = {
            "ranked": [
                {"rank": k + 1, "strategy": s, "score": None, "plays": 0, "wins": 0, "avg_reward": None}
                for k, s in enumerate(DEFAULT_ORDER[:top])
            ],
            "total_plays": len(change_ledger),
            "data_source": str(optstate_path),
            "c": round(c, 3),
            "status": "insufficient_data",
        }
        print(json.dumps(result, indent=2))
        return

    # Compute UCB1
    stats = build_strategy_stats(change_ledger)
    total_plays = sum(s["plays"] for s in stats.values())
    ranked = rank_strategies(stats, total_plays, c, top)

    # Add rank numbers
    for k, entry in enumerate(ranked):
        entry["rank"] = k + 1

    result = {
        "ranked": ranked,
        "total_plays": total_plays,
        "data_source": str(optstate_path),
        "c": round(c, 3),
        "status": "ok",
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
