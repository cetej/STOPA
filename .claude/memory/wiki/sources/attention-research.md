---
title: "Attention Mechanism Innovations — Research Brief"
slug: attention-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 10
claims_extracted: 5
---

# Attention Mechanism Innovations — Research Brief

> **TL;DR**: None of the four studied techniques (XSA, AttnRes, Differential Attention, Value Residual Learning) have been confirmed in any production model as of Q1 2026. Production frontier is dominated by MLA (DeepSeek), GQA (de-facto standard), and experimental DSA. Differential Attention is the most mature of the four — V2 removes all production blockers and DEX adapter enables post-hoc conversion of existing models.

## Key Claims

1. MLA (DeepSeek V2/V3/R1) reduces KV cache from 213.5 GB to 7.6 GB and is strictly more expressive than GQA for identical KV budget. — `[verified]`
2. Differential Attention (ICLR 2025 Oral) V2 removes custom kernel requirement; tested at 30B MoE production scale. — `[verified]`
3. GQA is de-facto standard for all non-DeepSeek frontier models: Llama 3/4, Mistral, Qwen2.5, Gemma 2, Phi-4-Mini. — `[verified]`
4. Value Residual Learning (SVFormer): better than GQA at 64K tokens, combined SVFormer+GQA4 is best of both at long range. — `[verified]`
5. NSA (Native Sparse Attention, ACL 2025 Best Paper): sub-quadratic O(Lk) attention; DeepSeek V3.2-Exp is first production deployment. — `[verified]`

## Relations

- MLA `is used by` DeepSeek V2, V3, R1
- GQA `is standard for` Llama, Mistral, Qwen, Gemma, Phi
- Differential Attention `received` ICLR 2025 Oral designation
- DEX adapter `enables post-hoc conversion to` Differential Attention
- NSA `achieves` O(Lk) sub-quadratic complexity

## Entities

| Entity | Type | Status |
|--------|------|--------|
| MLA (Multi-Head Latent Attention) | concept | new |
| Differential Attention | concept | new |
| XSA (Exclusive Self-Attention) | concept | new |
| Value Residual Learning | concept | new |
| AttnRes | concept | new |
| NSA (Native Sparse Attention) | concept | new |
| GQA (Grouped Query Attention) | concept | new |
| DEX adapter | concept | new |
| iRoPE | concept | new |
| TransMLA | paper | new |
