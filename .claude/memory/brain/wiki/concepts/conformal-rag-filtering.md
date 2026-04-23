---
title: Conformal RAG — Statistical Guarantees for Context Filtering
category: concepts
tags: [rag, context-engineering, statistical-methods, retrieval, filtering]
sources: [arXiv:2511.17908]
updated: 2026-04-23
---

# Conformal RAG — Statistical Guarantees for Context Filtering

**Paper**: arXiv:2511.17908  
**Authors**: Debashish Chakraborty, Eugene Yang, Daniel Khashabi, Dawn Lawrie, Kevin Duh  
**Datasets**: NeuCLIR, RAGTIME (ARGUE F1 evaluation)

## Core Principle

**Conformal Prediction** applied to RAG context filtering: instead of heuristically filtering retrieved chunks, use statistical coverage guarantees — ensure a specified fraction of relevant snippets are retained with provable probability.

## What Conformal Prediction Enables

| Approach | Guarantee | Mechanism |
|----------|-----------|-----------|
| Standard RAG | None — top-K heuristic | Retrieve K chunks regardless of relevance |
| Threshold filtering | None — arbitrary cutoff | Filter by similarity score threshold |
| **Conformal RAG** | Statistical coverage guarantee | Calibrated rejection threshold from held-out data |

"Model-agnostic and principled approach" — works with any embedding model or LLM scorer.

## Quantitative Results

| Metric | Result |
|--------|--------|
| Context reduction | 2-3× vs unfiltered retrieval |
| Coverage target | Consistently achieved |
| Factual accuracy | Stable or improved under strict filtering |

## Two Scoring Functions

1. **Embedding-based**: cosine similarity between query and retrieved chunk
2. **LLM-based**: small model scores relevance — higher quality, higher compute

## STOPA Relevance

2BRAIN hybrid-retrieve.py currently uses RRF (Reciprocal Rank Fusion) without statistical guarantees — keeps top-N regardless of quality. Conformal RAG suggests:

- Replace fixed `--top 8` in hybrid-retrieve.py with coverage-guarantee-based cutoff
- The calibration set = STOPA's own labeled retrieval examples from outcomes/
- Prevents "context contamination" (CAG problem) with principled rather than heuristic filtering

Practical upgrade path: calibrate conformal threshold on STOPA's existing learning retrieval successes/failures tracked in outcomes/.

## Related Concepts

→ [context-awareness-gate.md](context-awareness-gate.md)  
→ [context-engineering.md](context-engineering.md)  
→ [adr-context-strategies.md](adr-context-strategies.md)  
→ [knowledge-compounding.md](knowledge-compounding.md)
