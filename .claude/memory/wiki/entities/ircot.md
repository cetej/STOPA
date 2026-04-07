---
name: IRCoT
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [rag-multidoc-research]
tags: [rag, multi-hop, reasoning, retrieval]
---

# IRCoT

> Interleaved Retrieval with Chain-of-Thought — seminal paper alternating CoT and retrieval at sentence level; each CoT step can trigger retrieval, each result conditions next CoT step.

## Key Facts

- Paper: arXiv:2212.10509 (Trivedi et al., ACL 2023) (ref: sources/rag-multidoc-research.md)
- +21 retrieval improvement, +15 QA improvement on HotpotQA/2WikiMultihop/MuSiQue (ref: sources/rag-multidoc-research.md)
- Seminal work for iterative/agentic retrieval paradigm (ref: sources/rag-multidoc-research.md)
- More expensive than HippoRAG: 10-30× higher cost on same benchmarks (ref: sources/rag-multidoc-research.md)

## Relevance to STOPA

Reference architecture for iterative retrieval in deepresearch skill. Establishes that multi-step retrieval consistently outperforms single-step. HippoRAG is preferred for cost-effectiveness.

## Mentioned In

- [RAG Multi-Document Research](../sources/rag-multidoc-research.md)
