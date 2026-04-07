---
name: Differential Attention
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [attention-research]
tags: [attention, llm-architecture, microsoft, iclr-2025]
---

# Differential Attention

> Microsoft Research attention mechanism that computes attention as the difference of two parallel softmax maps, canceling attention noise and producing sparser, more focused patterns.

## Key Facts

- Paper: arXiv:2410.05258 (Ye et al., Microsoft Research + Tsinghua, ICLR 2025 Oral ~2% acceptance) (ref: sources/attention-research.md)
- Mechanism: `Attn(X) = softmax(Q₁K₁ᵀ/√d)V₁ − λ·softmax(Q₂K₂ᵀ/√d)V₂` (ref: sources/attention-research.md)
- Claimed ~65% model size/tokens to reach comparable perplexity; better hallucination reduction (ref: sources/attention-research.md)
- V2 (Jan 2026): removes custom FlashAttention kernels, production-scale 30B MoE tests (ref: sources/attention-research.md)
- DEX adapter enables post-hoc injection into pretrained Llama/Mistral without retraining (ref: sources/attention-research.md)
- Status: academic-only — no confirmed production deployment (ref: sources/attention-research.md)

## Relevance to STOPA

Most mature of the four studied attention innovations. DEX adapter makes it practically adoptable without full retraining. Relevant when evaluating LLM architecture choices for STOPA-adjacent model work.

## Mentioned In

- [Attention Mechanism Innovations](../sources/attention-research.md)
