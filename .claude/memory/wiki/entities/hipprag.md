---
name: HippoRAG
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [rag-multidoc-research]
tags: [rag, knowledge-graph, retrieval, multi-hop]
---

# HippoRAG

> Ohio State University RAG system using OpenIE triples as index + Personalized PageRank for retrieval; +20% on multi-hop QA at 10-30× lower cost than IRCoT.

## Key Facts

- Paper: arXiv:2405.14831 (Gutiérrez et al., OSU, NeurIPS 2024) (ref: sources/rag-multidoc-research.md)
- +20% on multi-hop QA (MuSiQue, 2WikiMHQA, HotpotQA) (ref: sources/rag-multidoc-research.md)
- 10-30× cheaper than iterative IRCoT (ref: sources/rag-multidoc-research.md)
- HippoRAG 2 (ICML 2025): adds non-parametric continual learning — knowledge added without parameter updates (ref: sources/rag-multidoc-research.md)
- Lighter approach than GraphRAG: OpenIE triples + PPR vs full KG + community detection (ref: sources/rag-multidoc-research.md)

## Relevance to STOPA

Cost-effective alternative to GraphRAG for multi-hop knowledge retrieval. HippoRAG 2's continual learning is relevant for STOPA's growing knowledge base — can add new facts without retraining.

## Mentioned In

- [RAG Multi-Document Research](../sources/rag-multidoc-research.md)
