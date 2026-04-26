---
source: arxiv.org/abs/2604.18234
date: 2026-04-25
type: paper
title: "Evaluating Multi-Hop Reasoning in RAG Systems: A Comparison of LLM-Based Retriever Evaluation Strategies"
arxiv: "2604.18234"
venue: "SynIRgy Workshop, ECIR 2026"
wiki: concepts/care-multihop-rag.md
---

# CARE — Context-Aware Retriever Evaluation

## Authors
Lorenz Brehme, Thomas Ströhle, Ruth Breu

## Key Concepts
- CARE: Context-Aware Retriever Evaluation framework
- Multi-hop relevance: documents irrelevant in isolation become essential when combined
- LLM-as-judge evaluation strategies for retriever quality
- Adapted single-hop benchmarks to multi-hop scenarios

## Main Claims
Standard RAG evaluation focuses on single-context retrieval; this misses the multi-hop case where individual chunks look irrelevant but together provide the answer. CARE evaluates relevance jointly, not per-chunk.

## Core Findings
- CARE consistently outperforms existing eval methods across HotPotQA, MuSiQue, SQuAD
- Larger models with extended context windows benefit most
- Compared LLM judges from OpenAI, Meta, Google
- Code: GitHub lorenzbrehme/CARE

## Entities
- HotPotQA, MuSiQue, SQuAD
- ECIR 2026 (SynIRgy workshop)
- arXiv: 2604.18234
