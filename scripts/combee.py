#!/usr/bin/env python3
"""combee.py — √n Hierarchical Aggregation for Parallel Prompt Learning.

Implements the Combee pattern (arXiv:2604.04247):
  1. Parallel Scan Aggregation — tree-based merge in √n subgroups
  2. Augmented Shuffling — duplicate + shuffle to prevent high-value loss
  3. Dynamic Batch Size Controller — power-law plateau detection

Usage in STOPA skills:
  - self-evolve: parallel eval grading across N test cases
  - autoloop: population mode candidate evaluation
  - evolve: batch learning processing at scale

Standalone test:
    python scripts/combee.py --demo
"""
import math
import random
import sys
from typing import Any, Callable, TypeVar

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

T = TypeVar("T")


def sqrt_partition(items: list[T], min_group: int = 2) -> list[list[T]]:
    """Partition items into √n subgroups for hierarchical aggregation.

    Returns list of subgroups, each with roughly √n items.
    Ensures minimum group size to avoid degenerate single-item groups.
    """
    n = len(items)
    if n <= min_group:
        return [items]

    k = max(min_group, int(math.sqrt(n)))
    # Distribute items evenly across k groups
    groups: list[list[T]] = [[] for _ in range(k)]
    for i, item in enumerate(items):
        groups[i % k].append(item)

    # Remove empty groups (shouldn't happen but be safe)
    return [g for g in groups if g]


def augmented_shuffle(items: list[T], p: int = 2) -> list[T]:
    """Duplicate each item p times and shuffle.

    Combee augmented shuffling: gives each high-value item multiple
    chances to survive aggregation. Default p=2 (paper default).
    """
    augmented = []
    for item in items:
        augmented.extend([item] * p)
    random.shuffle(augmented)
    return augmented


def hierarchical_aggregate(
    items: list[T],
    merge_fn: Callable[[list[T]], T],
    shuffle_p: int = 2,
    min_group: int = 2,
) -> T:
    """Two-level hierarchical aggregation with augmented shuffling.

    1. Augment + shuffle items (p duplicates each)
    2. Partition into √n subgroups
    3. Level 1: merge each subgroup → intermediate results
    4. Level 2: merge intermediates → final result

    Args:
        items: List of items to aggregate (e.g., reflections, eval results)
        merge_fn: Function that merges a list of items into one
        shuffle_p: Augmentation factor (default 2)
        min_group: Minimum items per subgroup (default 2)

    Returns:
        Single aggregated result
    """
    if len(items) <= min_group:
        return merge_fn(items)

    # Step 1: Augment and shuffle
    shuffled = augmented_shuffle(items, p=shuffle_p)

    # Step 2: Partition into √n groups
    groups = sqrt_partition(shuffled, min_group=min_group)

    # Step 3: Level 1 — merge each subgroup
    intermediates = [merge_fn(group) for group in groups]

    # Step 4: Level 2 — merge intermediates
    return merge_fn(intermediates)


def dynamic_batch_size(
    delay_samples: dict[int, float],
    tau: float = 0.016,
) -> int:
    """Find optimal batch size where marginal improvement drops below τ.

    Fits power-law: T_epoch(bs) = A * bs^(-α)
    Returns plateau_bs = (α*A/τ)^(1/(α+1))

    Args:
        delay_samples: {batch_size: per_iteration_delay_seconds}
        tau: marginal improvement threshold (default 1.6% = 0.016)

    Returns:
        Optimal batch size (clamped to sampled range)
    """
    if len(delay_samples) < 2:
        return max(delay_samples.keys()) if delay_samples else 1

    # Sort by batch size
    sizes = sorted(delay_samples.keys())
    delays = [delay_samples[s] for s in sizes]

    # Estimate epoch time = delay * (N_total / bs)
    # For relative comparison, use delay / bs as proxy
    # Fit log-linear: log(delay/bs) = log(A) + (-α-1) * log(bs)
    import numpy as np  # noqa: delayed import for optional dependency

    x = np.log(np.array(sizes, dtype=float))
    y = np.log(np.array(delays, dtype=float) / np.array(sizes, dtype=float))

    # Simple linear regression
    n = len(x)
    slope = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x)**2)
    intercept = (np.sum(y) - slope * np.sum(x)) / n

    alpha = -(slope + 1)  # from the power-law fit
    A = math.exp(intercept)

    if alpha <= 0 or A <= 0:
        return sizes[-1]  # fallback to largest sampled

    # Plateau batch size
    plateau = (alpha * A / tau) ** (1.0 / (alpha + 1))
    # Clamp to sampled range
    return max(sizes[0], min(sizes[-1], int(round(plateau))))


# ── Convenience for STOPA skills ──────────────────────────────────────

def aggregate_eval_results(
    results: list[dict[str, Any]],
    key: str = "score",
) -> dict[str, Any]:
    """Merge eval results using hierarchical aggregation.

    Each result is a dict with at least {case_id, score, passed}.
    Returns aggregated stats preserving per-case detail.
    """
    if not results:
        return {"pass_rate": 0.0, "mean_score": 0.0, "cases": []}

    def merge(items: list[dict]) -> dict:
        # Deduplicate by case_id (augmented shuffle creates dupes)
        # Items may be raw eval results OR intermediate aggregation dicts
        seen: dict[str, dict] = {}
        for item in items:
            # If item is an intermediate result from Level 1, unpack its cases
            if "cases" in item and isinstance(item.get("cases"), list):
                for case in item["cases"]:
                    cid = case.get("case_id", id(case))
                    if cid not in seen or case.get(key, 0) > seen[cid].get(key, 0):
                        seen[cid] = case
            else:
                cid = item.get("case_id", id(item))
                if cid not in seen or item.get(key, 0) > seen[cid].get(key, 0):
                    seen[cid] = item
        unique = list(seen.values())

        scores = [r.get(key, 0) for r in unique]
        passed = sum(1 for r in unique if r.get("passed", False))
        return {
            "pass_rate": passed / len(unique) if unique else 0.0,
            "mean_score": sum(scores) / len(scores) if scores else 0.0,
            "cases": unique,
        }

    if len(results) <= 4:
        return merge(results)

    return hierarchical_aggregate(results, merge)


def aggregate_candidate_scores(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Rank population candidates by z-score normalization.

    Each candidate: {id, metric, cost (optional)}.
    Returns candidates sorted by z-score, highest first.
    """
    if not candidates:
        return []

    metrics = [c["metric"] for c in candidates]
    mean = sum(metrics) / len(metrics)
    std = max(0.01, (sum((m - mean) ** 2 for m in metrics) / len(metrics)) ** 0.5)

    for c in candidates:
        c["z_score"] = (c["metric"] - mean) / std

    return sorted(candidates, key=lambda c: -c["z_score"])


# ── Demo / self-test ──────────────────────────────────────────────────

def _demo():
    """Demonstrate hierarchical aggregation vs flat."""
    print("=== Combee √n Aggregation Demo ===\n")

    # Simulate 20 eval results
    results = [
        {"case_id": f"case_{i}", "score": random.uniform(0.3, 1.0), "passed": random.random() > 0.3}
        for i in range(20)
    ]

    # Flat aggregation
    flat_scores = [r["score"] for r in results]
    flat_mean = sum(flat_scores) / len(flat_scores)
    flat_pass = sum(1 for r in results if r["passed"]) / len(results)

    # Hierarchical aggregation
    hier = aggregate_eval_results(results)

    print(f"Items: {len(results)}")
    print(f"√n partition size: {int(math.sqrt(len(results)))}")
    print(f"\nFlat:         mean_score={flat_mean:.3f}  pass_rate={flat_pass:.3f}")
    print(f"Hierarchical: mean_score={hier['mean_score']:.3f}  pass_rate={hier['pass_rate']:.3f}")
    print(f"Cases preserved: {len(hier['cases'])}/{len(results)}")

    # Population ranking demo
    print("\n=== Population Candidate Ranking ===\n")
    candidates = [
        {"id": "A_structural", "metric": 0.82},
        {"id": "B_content", "metric": 0.91},
        {"id": "C_simplify", "metric": 0.78},
    ]
    ranked = aggregate_candidate_scores(candidates)
    for c in ranked:
        print(f"  {c['id']}: metric={c['metric']:.2f}  z_score={c['z_score']:+.2f}")

    print("\nDone.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Combee √n Hierarchical Aggregation")
    parser.add_argument("--demo", action="store_true", help="Run demo")
    args = parser.parse_args()

    if args.demo:
        _demo()
    else:
        parser.print_help()
