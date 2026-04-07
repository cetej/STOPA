---
name: GraphRAG
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [rag-multidoc-research]
tags: [rag, knowledge-graph, retrieval, microsoft]
---

# GraphRAG

> Microsoft's RAG system using entity-relationship graphs with Louvain community detection and pre-generated hierarchical community summaries for global sensemaking queries.

## Key Facts

- GitHub: https://github.com/microsoft/graphrag (32k stars, v3.0.8) (ref: sources/rag-multidoc-research.md)
- 72-83% win rate over naive RAG on comprehensiveness, 75-82% on diversity (p<0.001) (ref: sources/rag-multidoc-research.md)
- Tested on 1M-1.7M token corpora (ref: sources/rag-multidoc-research.md)
- Paper: arXiv:2404.16130 (Edge et al., Microsoft) (ref: sources/rag-multidoc-research.md)
- LazyGraphRAG variant: 0.1% of indexing cost, still wins in all 96 comparison pairs (ref: sources/rag-multidoc-research.md)

## Relevance to STOPA

Primary candidate for MONITOR and knowledge-intensive STOPA projects requiring global sensemaking over large document corpora. LazyGraphRAG makes it cost-feasible for smaller deployments.

## Mentioned In

- [RAG Multi-Document Research](../sources/rag-multidoc-research.md)
