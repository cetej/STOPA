---
title: "On the Theoretical Limitations of Embedding-Based Retrieval"
slug: embedding-retrieval-theoretical-limits
source_type: url
url: "https://arxiv.org/pdf/2508.21038"
date_ingested: 2026-04-18
date_published: "2026 (ICLR 2026)"
authors: "Weller et al. (Google DeepMind + Johns Hopkins University)"
entities_extracted: 2
claims_extracted: 6
---

# On the Theoretical Limitations of Embedding-Based Retrieval

> **TL;DR**: Formal proof that single-vector embeddings cannot retrieve all top-k document combinations beyond a dimension threshold. BM25 achieves 97.8% recall@2 on the new LIMIT benchmark where SOTA embeddings manage only 54.3%. Cross-encoders and multi-vector models close the gap.

## Key Claims

1. For embedding dimension d, retrievable top-k subsets are bounded: d ≥ log(C(n,k)) / log(1 + 1/γ) — `verified`
2. BM25 achieves 97.8% recall@2 on LIMIT-small vs 54.3% for SOTA neural embeddings — `verified`
3. SOTA embedding models achieve ~30% recall@2 on 50k-document LIMIT corpus — `verified`
4. 500k documents require dimension ≥512 for all top-2 combinations (free embedding experiment) — `verified`
5. In-domain training provides minimal improvement — intrinsic representational limits, not domain shift — `verified`
6. Cross-encoders and multi-vector models handle LIMIT substantially better than single-vector embeddings — `verified`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [LIMIT Dataset](../entities/limit-dataset.md) | tool | new |
| [Single-Vector Embedding Limitation](../entities/single-vector-embedding-limitation.md) | concept | new |

## Relations

- LIMIT-Dataset `created_by` Weller et al. — introduced in this paper
- BM25 `competes_with` single-vector-embeddings — 97.8% vs 54.3% on LIMIT-small
- cross-encoders `supersedes` single-vector-embeddings — for diverse relevance definitions
- multi-vector-models `supersedes` single-vector-embeddings — handle LIMIT substantially better

## Cross-References

- Related learnings: `2026-04-18-retrieval-depth-knob-complexity-interpolation.md` (BM25 complexity hierarchy), `2026-04-05-bm25-memory-search.md` (STOPA BM25 implementation)
- Related wiki articles: [memory-architecture](../memory-architecture.md)
- Contradictions: none
