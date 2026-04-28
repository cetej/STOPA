---
date: 2026-04-09
type: best_practice
severity: medium
component: pipeline
tags: [kv-cache, attention, long-reasoning, efficiency, inference, llm-architecture]
summary: "Pre-RoPE Q/K vectors cluster around fixed centers (Q/K Concentration), enabling 10.7× KV cache compression and 2.5× throughput for long-reasoning via trigonometric importance scoring — bypassing the instability of post-RoPE attention scores used by prior methods."
source: external_research
uses: 8
successful_uses: 0
harmful_uses: 0
confidence: 1.00
maturity: validated
impact_score: 0.0
verify_check: "manual"
---

## TriAttention: Pre-RoPE KV Compression for Long Reasoning

**Pattern**: When estimating KV token importance for cache compression, use **pre-RoPE** vector space, not post-RoPE. Post-RoPE queries rotate with position → unstable importance scores. Pre-RoPE Q/K vectors cluster around fixed centers → stable trigonometric importance scoring from positional distance + vector norms.

**Results** (AIME25, Qwen3-8B, 32K tokens):
- 2.5× throughput vs Full Attention at matched accuracy
- 10.7× KV cache reduction at matched accuracy
- Competing baselines: ~50% accuracy at comparable efficiency

**Application for STOPA**: When selecting inference backends for long-reasoning deep-tier tasks (30K+ token chains), prefer frameworks that support TriAttention or similar pre-RoPE compression. At 10.7× memory reduction, long reasoning becomes viable on consumer GPUs where Full Attention causes OOM.

**Reference**: arXiv:2604.04921 (MIT, NVIDIA, ZJU)
**Code**: https://github.com/WeianMao/triattention
