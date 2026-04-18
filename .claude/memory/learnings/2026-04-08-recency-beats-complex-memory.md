---
date: 2026-04-08
type: architecture
severity: medium
component: memory
tags: [context, recency, sliding-window, memory-design, retrieval]
summary: "Simple sliding-window recency (last N items) matches/beats complex memory accumulation in time-sensitive tasks. More history can hurt real-time perception even when it helps recall."
source: external_research
maturity: draft
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.00
related: [2026-04-18-retrieval-depth-knob-complexity-interpolation.md, 2026-04-08-living-memory-over-static-retrieval.md]
verify_check: "manual"
---

## Learning

SimpleStream (arXiv:2604.02317) shows that feeding only the N most recent items to a model beats 13 complex memory mechanisms on streaming benchmarks.

**Pattern**: For tasks where recency matters more than history (real-time perception, streaming analysis, live fetch), a sliding window of the last N context items often outperforms elaborate retrieval. Complex memory adds value primarily for tasks requiring long-range recall.

**STOPA application**: When designing skill context strategies, distinguish task type:
- Recency-dominant (real-time, streaming, live) → sliding window of recent N interactions/results
- History-dominant (research, debugging, refactoring) → retrieval-augmented memory (BM25, hybrid)

**Tradeoff**: Adding more history improves recall metrics but degrades real-time perception metrics. Design context loading to match task type, not to maximize total context loaded.

> Updated 2026-04-18: MC complexity model (arXiv:2602.24281) provides formal backing — tier=light (grep only) = O(1) access = N=1 segment config. Recency-dominant tasks map to the lowest complexity tier, confirming this learning's rule with theoretical grounding.
