---
name: Single-Vector Embedding Limitation
type: concept
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [embedding-retrieval-theoretical-limits]
tags: [retrieval, theory, embedding, architecture]
---

# Single-Vector Embedding Limitation

> Proven theoretical constraint: for embedding dimension d, the number of distinct top-k document subsets retrievable by any query is bounded by the dimension.

## Key Facts

- Formal bound: d ≥ log(C(n,k)) / log(1 + 1/γ), where n=corpus size, k=retrieval size, γ=margin parameter (ref: sources/embedding-retrieval-theoretical-limits.md)
- 500k documents require at least dimension 512 to represent all top-2 combinations (free embedding experiment) (ref: sources/embedding-retrieval-theoretical-limits.md)
- Constraint is intrinsic — cannot be overcome by in-domain training alone (ref: sources/embedding-retrieval-theoretical-limits.md)
- Cross-encoders and multi-vector models (e.g., ColBERT) handle diverse relevance substantially better (ref: sources/embedding-retrieval-theoretical-limits.md)
- Lexical models (BM25) fail on synonym versions but excel on exact-match tasks where embeddings fail (ref: sources/embedding-retrieval-theoretical-limits.md)

## Relevance to STOPA

Theoretically justifies STOPA's hybrid retrieval stack (grep + BM25 + graph) over single-vector embedding search. As STOPA's learnings corpus grows, embedding-only retrieval would hit dimension ceilings; BM25 + graph walk avoids this class of failure entirely.

## Mentioned In

- [On the Theoretical Limitations of Embedding-Based Retrieval](../sources/embedding-retrieval-theoretical-limits.md)
