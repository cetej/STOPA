---
name: PAL
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [rag-multidoc-research]
tags: [symbolic-reasoning, code-generation, llm-tools]
---

# PAL

> Program-Aided Language Models — LLM generates Python program as reasoning step, Python interpreter executes deterministic computation; smaller model+PAL outperforms larger language-only model.

## Key Facts

- Paper: arXiv:2211.10435 (Gao et al., CMU, ICML 2023) (ref: sources/rag-multidoc-research.md)
- Codex+PAL > PaLM-540B by 15pt on GSM8K (ref: sources/rag-multidoc-research.md)
- Principle: separate language (program generation) from computation (interpreter execution) (ref: sources/rag-multidoc-research.md)
- Foundational pattern for symbolic computation layers in RAG (ref: sources/rag-multidoc-research.md)

## Relevance to STOPA

Foundational pattern for any STOPA skill that requires numeric computation, counting, or aggregation. The same principle applies to OLLA (semantic stratified sampling) and any agent needing reliable arithmetic.

## Mentioned In

- [RAG Multi-Document Research](../sources/rag-multidoc-research.md)
