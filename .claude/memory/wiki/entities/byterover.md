---
name: ByteRover
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [byterover-memory-analysis]
tags: [memory, retrieval, agent-memory, markdown, hierarchical]
---

# ByteRover

> AI agent memory system achieving SOTA without vector embeddings; uses hierarchical Context Tree (4-level) + 5-tier progressive retrieval + importance scoring with recency decay.

## Key Facts

- Paper: arXiv:2604.01599 (Andy Nguyen et al., 2026-04-02) (ref: sources/byterover-memory-analysis.md)
- SOTA: LoCoMo 96.1% (+6.2pp over HonCho), LongMemEval-S 92.8% (ref: sources/byterover-memory-analysis.md)
- Core thesis: "The system that stores knowledge does not understand it" — same LLM curates and reasons (ref: sources/byterover-memory-analysis.md)
- 5-tier retrieval: Hash Cache (0ms) → Fuzzy Cache (50ms) → BM25 (100ms) → Optimized LLM (<5s) → Full Agentic (8-15s) (ref: sources/byterover-memory-analysis.md)
- Ablation: tiered retrieval = most critical component (−29.4pp without it) (ref: sources/byterover-memory-analysis.md)
- Importance score: BM25 relevance + normalized importance + recency decay exp(−Δt/30) (ref: sources/byterover-memory-analysis.md)
- Validates STOPA: markdown-on-disk > vector DB; write-time quality control; recency decay (ref: sources/byterover-memory-analysis.md)

## Relevance to STOPA

Direct comparator and upgrade source for STOPA memory system. Key adoptable ideas: keyword index cache (Tier 1), topic clustering (2-level hierarchy), exponential decay with hysteresis, formal curation operations (ADD/UPDATE/MERGE/ARCHIVE/PROMOTE).

## Mentioned In

- [ByteRover vs STOPA Memory Analysis](../sources/byterover-memory-analysis.md)
