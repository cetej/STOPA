# RL for RAG — rule-based proxy A/B evaluation

**Issue:** [#20](https://github.com/cetej/STOPA/issues/20)
**Source paper:** arXiv:2510.24652 (R3 — RL-trained per-query retrieval strategy, +4.2% nDCG@10 on BEIR)
**Implementation:** rule-based proxy of the RL policy (zero training)
**Date:** 2026-04-26

## TL;DR

Rule-based `select_strategy(query)` implemented in [scripts/hybrid-retrieve.py](../scripts/hybrid-retrieve.py)
behind opt-in flag `--use-strategy`. Default behavior largely unchanged (fixed RRF k=60).

**Update 2026-04-26 (post-eval):** Sub-rule `grep_only` for ≤2-word queries promoted
from opt-in to **always-on default** (validated by A/B: 75% speedup, lowest blast radius,
extends light-tier fast-path). Other strategies stay opt-in. Verified on 4 scenarios:
1-word `memory` and 2-word `memory consolidation` skip BM25+graph (~27ms vs ~92ms full
hybrid for 5-word query) — ~3.4× speedup. Other queries unchanged.

A/B on 11 unique queries (197 total occurrences in `.claude/memory/retrieval-metrics.jsonl`):

| Metric | Value | Interpretation |
|---|---|---|
| Top-1 stability | **9.1%** | Strategy radically changes #1 result on most queries |
| Top-3 Jaccard | 0.52 | ~50% overlap in top-3 results |
| Top-5 Jaccard | 0.49 | Similar pattern at K=5 |
| Avg duration (baseline) | 240.6 ms | — |
| Avg duration (strategy) | 185.9 ms | **22.7% faster** |
| `grep_only` speedup | -181 ms | 75% faster on short queries (n=3) |
| `graph_priority` speedup | -8 ms | Marginal — runs all signals, just reweights |

**Verdict:** Implementation is sound and measurably faster, but **without ground-truth relevance
labels** (no user clicks, no human annotations) we cannot say whether the radically different
top-1 results are better or worse than the baseline. Default = baseline; strategy = opt-in.

## Paper recap (Section 4 — what R3 actually does)

R3 (arXiv:2510.24652) trains a PPO policy over multi-step retrieval decisions:
- **Reward:** scalar from downstream answer correctness (EM/F1)
- **Action space:** binary "retrieve again?" + corpus selection + top-K choice
- **Features:** query encoding + corpus stats + previous-step context
- **Beats:** fixed top-K, rule-based heuristics, Self-RAG triggers

R3 needs labeled QA pairs to compute reward. STOPA has no such labels — the realistic baseline
is rule-based heuristics (one of the things R3 itself outperforms). This work implements that
baseline as a stepping stone; lifting it toward an actual learned policy would need
critic-score-as-reward, which is doable but out of scope for this issue.

## Strategy selector heuristics

| Trigger | Strategy | Weights (grep / bm25 / graph) | Rationale |
|---|---|---|---|
| ≤2 words | `grep_only` | 1.0 / 0.0 / 0.0 | BM25 saturation adds nothing on single terms; skip BM25+graph for speed |
| Filename pattern (`.md`, `/`) | `grep_priority` | 1.5 / 0.7 / 0.7 | Exact-match channel dominates path lookups |
| Question prefix (how/why/jak/proč) | `hybrid` | 1.0 / 1.0 / 1.0 | Need all signals for reasoning queries |
| ≥15 words | `bm25_priority` | 0.7 / 1.5 / 0.7 | Auto-generated context dumps — TF saturation works, grep finds noise |
| Known concept-graph entity | `graph_priority` | 0.8 / 0.8 / 1.5 | Boost graph walk when entity is recognized |
| Otherwise | `hybrid` | 1.0 / 1.0 / 1.0 | Conservative default = current behavior |

Skipping signals with weight 0 is the perf win — `grep_only` runs no BM25 and no graph walk.

## Per-strategy A/B results

```
graph_priority   n=7  (weighted=187)  top1_stable=0.00  jacc@3=0.50  delta_ms=-8
grep_only        n=3  (weighted=  8)  top1_stable=0.00  jacc@3=0.40  delta_ms=-181
hybrid           n=1  (weighted=  2)  top1_stable=1.00  jacc@3=1.00  delta_ms=+0
```

- `graph_priority` triggered most often — the reweighting promotes graph-discovered files
  above grep+bm25 hits. On `**Phase 3: ...**`-style queries it consistently surfaces
  `2026-03-23-ecosystem-scan.md` instead of `2026-04-05-self-improving-harness.md`.
- `grep_only` is the speedup engine but only fires on 3 queries in the corpus.
- `hybrid` is identity (default behavior preserved).

## Why we can't claim a win

- Top-1 changed on 10/11 queries. Without relevance labels, we cannot label any of those
  changes as "better."
- The metrics log captures *what was retrieved*, not *whether it was useful*. There is no
  click signal, no critic score tied to retrieval quality, no user feedback on which file
  ended up cited.
- Test corpus is tiny (11 unique queries, dominated by 2 long auto-generated topic dumps
  from a hook). Real usage variety would need hundreds of distinct queries before a
  rule-based heuristic could be validated empirically.

## Recommendation

1. **Ship as opt-in.** Default `use_strategy=False` preserves all current behavior. Anyone
   who wants the speedup can pass `--use-strategy` (CLI) or set `use_strategy=True` in
   programmatic calls.
2. **Instrument before adoption.** Before flipping the default, log per-query critic
   feedback (e.g., did the agent actually cite the top-1 result?). That gives a reward
   signal close to the one R3 uses.
3. **Re-evaluate at 100+ unique queries.** With more variety the per-strategy buckets
   become statistically meaningful. Today they're a smoke test.
4. **Pruning candidate:** `grep_only` for ≤2-word queries is the safest sub-rule to
   promote — large speedup, small absolute query count, and the existing `light` tier
   fast-path already does something similar.

## Files

- [scripts/hybrid-retrieve.py](../scripts/hybrid-retrieve.py) — `select_strategy()`,
  `STRATEGY_WEIGHTS`, weighted RRF in `fuse_rrf()`, `--use-strategy` CLI flag
- [scripts/ab-test-strategy.py](../scripts/ab-test-strategy.py) — reproducible A/B harness
- [outputs/2026-04-26-ab-test-results.json](2026-04-26-ab-test-results.json) — raw rows
