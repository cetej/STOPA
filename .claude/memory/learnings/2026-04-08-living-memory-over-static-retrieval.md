---
date: 2026-04-08
type: best_practice
severity: high
component: memory
tags: [memory, retrieval, agent-memory, living-memory, static-rag, evolution]
summary: "Living memory (evolving + compressed trajectories) beats static RAG by +31% avg across 11 benchmarks. Traditional long-context accumulation can underperform even no-memory baselines — more stored context ≠ better performance."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.95
related: [2026-03-30-write-time-gating-salience.md, 2026-04-08-recency-beats-complex-memory.md]
verify_check: "manual"
---

## Detail

MIA (arXiv:2604.04503) demonstrates that memory systems must evolve, not just accumulate. A 7B model with living memory (+31% avg) outperforms a 32B model without it by 18%. The critical mechanism is bidirectional conversion between parametric (model weights) and non-parametric (explicit files) memory, plus test-time learning that updates strategies during inference.

**Key implication for STOPA**: STOPA's write-time gating (filter before storing) is validated. Static accumulation of all trajectories is counterproductive. The memory-architecture.md rule "write-time gating over read-time filtering" has empirical backing from MIA's finding that long-context RAG collapses at high distractor ratios.

**Practical rule**: When designing STOPA memory for a new agent, prefer compressed trajectory storage with evolution hooks over append-only history. Recency + quality filtering > completeness.
