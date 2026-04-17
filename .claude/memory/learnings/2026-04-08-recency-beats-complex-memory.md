---
date: 2026-04-08
type: architecture
severity: medium
component: memory
tags: [context, recency, sliding-window, memory-design, retrieval]
summary: "Simple sliding-window recency (last N items) matches/beats complex memory accumulation in time-sensitive tasks. More history can hurt real-time perception even when it helps recall."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.85
verify_check: "manual"
---

## Learning

SimpleStream (arXiv:2604.02317) shows that feeding only the N most recent items to a model beats 13 complex memory mechanisms on streaming benchmarks.

**Pattern**: For tasks where recency matters more than history (real-time perception, streaming analysis, live fetch), a sliding window of the last N context items often outperforms elaborate retrieval. Complex memory adds value primarily for tasks requiring long-range recall.

**STOPA application**: When designing skill context strategies, distinguish task type:
- Recency-dominant (real-time, streaming, live) → sliding window of recent N interactions/results
- History-dominant (research, debugging, refactoring) → retrieval-augmented memory (BM25, hybrid)

**Tradeoff**: Adding more history improves recall metrics but degrades real-time perception metrics. Design context loading to match task type, not to maximize total context loaded.
