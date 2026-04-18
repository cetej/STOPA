---
name: LIMIT Dataset
type: tool
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [embedding-retrieval-theoretical-limits]
tags: [retrieval, benchmark, embedding, evaluation]
---

# LIMIT Dataset

> Synthetic benchmark designed to expose fundamental retrieval failures of single-vector embedding models via simple attribute-preference queries.

## Key Facts

- Created by Weller et al. (Google DeepMind + Johns Hopkins) as part of arXiv:2508.21038 (ICLR 2026) (ref: sources/embedding-retrieval-theoretical-limits.md)
- Two scales: LIMIT-small (46 docs) and LIMIT-large (50k docs) (ref: sources/embedding-retrieval-theoretical-limits.md)
- Despite task simplicity, SOTA embeddings achieve only ~30% recall@2 on 50k-doc version (ref: sources/embedding-retrieval-theoretical-limits.md)
- BM25 achieves 97.8% recall@2 on LIMIT-small vs 54.3% for SOTA neural embeddings (ref: sources/embedding-retrieval-theoretical-limits.md)
- Training on in-domain examples provides minimal improvement — intrinsic representational limits, not domain shift (ref: sources/embedding-retrieval-theoretical-limits.md)

## Relevance to STOPA

Provides empirical evidence that BM25-based retrieval (used in STOPA's `scripts/memory-search.py`) is not just a pragmatic zero-dependency choice but theoretically justified for heterogeneous corpora with diverse relevance criteria.

## Mentioned In

- [On the Theoretical Limitations of Embedding-Based Retrieval](../sources/embedding-retrieval-theoretical-limits.md)
