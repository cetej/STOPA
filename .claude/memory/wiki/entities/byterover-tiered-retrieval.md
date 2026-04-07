---
name: 5-Tier Progressive Retrieval
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [byterover-memory-analysis]
tags: [memory, retrieval, caching, performance]
---

# 5-Tier Progressive Retrieval

> ByteRover's cascading retrieval architecture: Hash Cache (0ms) → Fuzzy Cache (50ms) → BM25 (100ms) → Optimized LLM (<5s) → Full Agentic (8-15s); ablation shows −29.4pp without it.

## Key Facts

- From ByteRover (arXiv:2604.01599) (ref: sources/byterover-memory-analysis.md)
- Tier 0: exact hash match (~0ms), Tier 1: Jaccard similarity ≥0.6 (~50ms) (ref: sources/byterover-memory-analysis.md)
- Tier 2: BM25 normalized ≥0.93 + gap ≥0.08 (~100ms) (ref: sources/byterover-memory-analysis.md)
- Tier 3: single LLM call 1024 tokens temp 0.3 (<5s) (ref: sources/byterover-memory-analysis.md)
- Tier 4: multi-turn reasoning 2048 tokens temp 0.5 (8-15s) fallback (ref: sources/byterover-memory-analysis.md)
- Most critical component: −29.4pp ablation impact (ref: sources/byterover-memory-analysis.md)

## Relevance to STOPA

STOPA should adopt a 3-tier simplified version: session cache (in-memory dict) → keyword index JSON → grep fallback. Full 5-tier with LLM calls is overkill for YAML-tagged learnings under 500 entries.

## Mentioned In

- [ByteRover vs STOPA Memory Analysis](../sources/byterover-memory-analysis.md)
