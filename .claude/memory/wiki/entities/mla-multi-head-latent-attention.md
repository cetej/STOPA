---
name: MLA (Multi-Head Latent Attention)
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [attention-research, triattention-kv-compression]
tags: [attention, llm-architecture, deepseek, kv-cache]
---

# MLA (Multi-Head Latent Attention)

> DeepSeek's low-rank joint KV compression mechanism that reduces KV cache from 213.5 GB to 7.6 GB (93.3% reduction) while being strictly more expressive than GQA.

## Key Facts

- First introduced in DeepSeek V2 (May 2024), used in V3 (Dec 2024) and R1 (ref: sources/attention-research.md)
- KV dim=512, Q dim=1536, decoupled RoPE dim=64 in V3 (ref: sources/attention-research.md)
- TransMLA (arXiv:2502.07864) proved MLA is strictly more expressive than GQA for identical KV budget (ref: sources/attention-research.md)
- Ant Group adopted TransMLA for Ling-2.5-1T (1 trillion parameters) (ref: sources/attention-research.md)
- TransMLA enables post-training GQA→MLA conversion (ref: sources/attention-research.md)

## Relevance to STOPA

Key architecture for understanding DeepSeek model family capabilities. Relevant when selecting models for STOPA agents — MLA models offer better long-context performance at lower memory cost.

## Mentioned In

- [Attention Mechanism Innovations](../sources/attention-research.md)
- [TriAttention: Efficient Long Reasoning with Trigonometric KV Compression](../sources/triattention-kv-compression.md) — complementary KV compression; TriAttention uses trigonometric scoring vs MLA's low-rank factorization
