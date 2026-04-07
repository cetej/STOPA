---
name: StructRAG
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [rag-multidoc-research]
tags: [rag, structured-retrieval, task-adaptive]
---

# StructRAG

> Alibaba DAMO task-adaptive RAG that routes to optimal structure format per query (table, graph, algorithm, catalog, chunk); reconstructs documents into the selected format at inference time.

## Key Facts

- Paper: arXiv:2410.08815 (Li et al., Alibaba DAMO) (ref: sources/rag-multidoc-research.md)
- SOTA on knowledge-intensive benchmarks (ref: sources/rag-multidoc-research.md)
- Router selects optimal format at inference time (inference-time structuring vs GraphRAG's index-time) (ref: sources/rag-multidoc-research.md)
- Limitation: router requires a trained model — format selection without task-specific supervision is open (ref: sources/rag-multidoc-research.md)

## Relevance to STOPA

Relevant for STOPA's deepresearch skill when querying over heterogeneous knowledge bases. The task-adaptive routing principle aligns with STOPA's context engineering approach — different query types need different retrieval structures.

## Mentioned In

- [RAG Multi-Document Research](../sources/rag-multidoc-research.md)
