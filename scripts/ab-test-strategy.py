#!/usr/bin/env python3
"""ab-test-strategy.py — A/B test rule-based strategy vs fixed-RRF baseline.

Loads queries from retrieval-metrics.jsonl, runs each through hybrid_search()
twice (use_strategy=False vs True), compares:
  - Top-1 stability: same #1 result?
  - Top-K Jaccard overlap: how similar are the result sets?
  - Duration delta: time saved/lost
  - Per-strategy breakdown

No ground truth available — this is an agreement + perf comparison, not nDCG.
The hypothesis: if disagreement is small AND perf improves, strategy is safe to adopt.
"""
import json
import statistics
import sys
import time
from collections import defaultdict
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
METRICS = ROOT / ".claude" / "memory" / "retrieval-metrics.jsonl"
HR_PATH = ROOT / "scripts" / "hybrid-retrieve.py"
OUT_PATH = ROOT / "outputs" / "2026-04-26-rl-rag-eval.md"


def load_module(path: Path, name: str):
    spec = spec_from_file_location(name, str(path))
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_unique_queries() -> list[tuple[str, int]]:
    """Return (query, occurrence_count) pairs from the metrics log."""
    seen: dict[str, int] = {}
    for line in METRICS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        q = entry.get("query", "").strip()
        if q:
            seen[q] = seen.get(q, 0) + 1
    return sorted(seen.items(), key=lambda x: -x[1])


def jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def run_one(hr, query: str, use_strategy: bool) -> dict:
    t0 = time.perf_counter()
    results = hr.hybrid_search(
        query=query, task_tier="standard", top_n=8,
        debug=False, use_gate=True, use_strategy=use_strategy,
    )
    dt_ms = (time.perf_counter() - t0) * 1000
    return {
        "files": [r.filename for r in results],
        "top_score": results[0].rrf_score if results else 0.0,
        "duration_ms": dt_ms,
        "strategy": hr.select_strategy(query) if use_strategy else "fixed",
    }


def main():
    hr = load_module(HR_PATH, "hr")

    queries = load_unique_queries()
    print(f"Loaded {len(queries)} unique queries from metrics log\n")

    # Per-query comparison
    rows = []
    by_strategy: dict[str, list[dict]] = defaultdict(list)

    for q, count in queries:
        a = run_one(hr, q, use_strategy=False)  # baseline
        b = run_one(hr, q, use_strategy=True)   # strategy

        top1_same = (a["files"][:1] == b["files"][:1])
        top3_jacc = jaccard(a["files"][:3], b["files"][:3])
        top5_jacc = jaccard(a["files"][:5], b["files"][:5])
        top8_jacc = jaccard(a["files"][:8], b["files"][:8])
        delta_ms = b["duration_ms"] - a["duration_ms"]

        row = {
            "query": q[:80],
            "count": count,
            "strategy": b["strategy"],
            "top1_same": top1_same,
            "top3_jacc": round(top3_jacc, 2),
            "top5_jacc": round(top5_jacc, 2),
            "top8_jacc": round(top8_jacc, 2),
            "a_dur_ms": round(a["duration_ms"]),
            "b_dur_ms": round(b["duration_ms"]),
            "delta_ms": round(delta_ms),
            "a_top": a["files"][0] if a["files"] else "—",
            "b_top": b["files"][0] if b["files"] else "—",
        }
        rows.append(row)
        by_strategy[b["strategy"]].append(row)

    # Aggregate metrics
    n = len(rows)
    weighted_n = sum(r["count"] for r in rows)

    def agg(field, weighted=False):
        if weighted:
            total = sum(r[field] * r["count"] for r in rows)
            return total / weighted_n
        return sum(r[field] for r in rows) / n

    summary = {
        "n_queries": n,
        "n_weighted": weighted_n,
        "top1_stability": round(sum(1 for r in rows if r["top1_same"]) / n, 3),
        "top1_stability_weighted": round(
            sum(r["count"] for r in rows if r["top1_same"]) / weighted_n, 3
        ),
        "avg_top3_jacc": round(agg("top3_jacc"), 3),
        "avg_top5_jacc": round(agg("top5_jacc"), 3),
        "avg_top8_jacc": round(agg("top8_jacc"), 3),
        "weighted_top3_jacc": round(agg("top3_jacc", weighted=True), 3),
        "avg_a_dur_ms": round(agg("a_dur_ms"), 1),
        "avg_b_dur_ms": round(agg("b_dur_ms"), 1),
        "avg_delta_ms": round(agg("delta_ms"), 1),
        "speedup_pct": round(
            100 * (agg("a_dur_ms") - agg("b_dur_ms")) / agg("a_dur_ms"), 1
        ) if agg("a_dur_ms") > 0 else 0.0,
    }

    print("=" * 70)
    print("AGGREGATE")
    print("=" * 70)
    for k, v in summary.items():
        print(f"  {k:30} {v}")

    print()
    print("=" * 70)
    print("PER-STRATEGY BREAKDOWN")
    print("=" * 70)
    for strat, rs in sorted(by_strategy.items()):
        n_strat = len(rs)
        weight_strat = sum(r["count"] for r in rs)
        avg_jacc = sum(r["top3_jacc"] for r in rs) / n_strat
        avg_delta = sum(r["delta_ms"] for r in rs) / n_strat
        stable = sum(1 for r in rs if r["top1_same"]) / n_strat
        print(f"  {strat:18} n={n_strat:2} (weighted={weight_strat:3}) "
              f"top1_stable={stable:.2f}  jacc@3={avg_jacc:.2f}  "
              f"delta_ms={avg_delta:+.0f}")

    print()
    print("=" * 70)
    print("PER-QUERY DETAIL")
    print("=" * 70)
    for r in sorted(rows, key=lambda x: -x["count"]):
        marker = "OK" if r["top1_same"] else "DIFF"
        print(f"  [{marker:4}] strat={r['strategy']:16} n={r['count']:3} "
              f"jacc@3={r['top3_jacc']:.2f}  jacc@5={r['top5_jacc']:.2f}  "
              f"delta={r['delta_ms']:+5d}ms  q={r['query'][:50]!r}")
        if not r["top1_same"]:
            print(f"           A_top: {r['a_top']}")
            print(f"           B_top: {r['b_top']}")

    # Persist results to JSON for further analysis
    out_json = ROOT / "outputs" / "2026-04-26-ab-test-results.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps({
        "summary": summary,
        "per_strategy": {
            s: {"n": len(rs), "weighted": sum(r["count"] for r in rs)}
            for s, rs in by_strategy.items()
        },
        "rows": rows,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nDetailed results: {out_json}")


if __name__ == "__main__":
    main()
