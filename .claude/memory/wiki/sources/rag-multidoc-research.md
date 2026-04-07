---
title: "Proč naive RAG selhává na agregačních dotazech — Research Brief"
slug: rag-multidoc-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 10
claims_extracted: 5
---

# Proč naive RAG selhává na agregačních dotazech — Research Brief

> **TL;DR**: Naive RAG achieves near-zero results on aggregation queries (1.51 F1 on GlobalQA corpus-level aggregation). Four concurrent failure modes: bounded-K retrieval, fixed chunking destroying attribute bindings, dense embedding failures on complex filters, and LLM arithmetic weakness. Symbolic-hybrid approaches (GraphRAG, HippoRAG, IRCoT) substantially improve results.

## Key Claims

1. Naive RAG achieves 1.51 F1 on corpus-level aggregation (GlobalQA); best system GlobalRAG achieves 6.63 F1 — still far from practical. — `[verified]`
2. GraphRAG achieves 72-83% win rate over naive RAG on global comprehensiveness questions (p<0.001). — `[verified]`
3. HippoRAG: +20% on multi-hop QA, 10-30× cheaper than iterative IRCoT. — `[verified]`
4. FRAMES benchmark: single-step RAG = 0.40, multi-step pipeline = 0.66 (+65%) on 824 multi-hop questions. — `[verified]`
5. PAL (LLM writes Python, interpreter executes): Codex+PAL outperforms PaLM-540B by 15pt on GSM8K — symbolic computation > language-only reasoning. — `[verified]`

## Relations

- GraphRAG `uses` Louvain community detection for indexing
- HippoRAG `uses` Personalized PageRank for retrieval
- IRCoT `interleaves` CoT reasoning with retrieval
- OLLA `applies` stratified semantic sampling to aggregate over unstructured text
- Lost in the Middle `documents` U-shaped position bias in LLM context processing

## Entities

| Entity | Type | Status |
|--------|------|--------|
| GraphRAG | tool | new |
| HippoRAG | paper | new |
| IRCoT | paper | new |
| OLLA | paper | new |
| GlobalQA | concept | new |
| FRAMES benchmark | concept | new |
| StructRAG | paper | new |
| PAL | paper | new |
| BeamAggR | paper | new |
| LazyGraphRAG | tool | new |
