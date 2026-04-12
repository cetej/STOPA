---
date: 2026-04-08
type: best_practice
severity: medium
component: orchestration
tags: [model-selection, long-context, inference, test-time-training, iterative-skills]
summary: "In-Place TTT gives 3-12× improvement on long-context benchmarks (RULER-16k: 6.58→19.99) by updating MLP weights chunk-by-chunk during inference. When selecting models for STOPA deep-tier iterative tasks with >64k context, TTT-capable models dominate."
source: external_research
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 0.85
verify_check: "manual"
---

## Detail

In-Place TTT (arXiv:2604.06169) demonstrates that LLMs can update their own weights at inference time by repurposing MLP W_down matrices as "fast weights." No new layers, no retraining — drop-in enhancement.

**Numbers that matter:**
- Drop-in on Qwen3-4B: +4.4 accuracy at 64k, +2.2 at 128k
- Full pretrain RULER-16k: 6.58 → 19.99 (full attention), 5.07 → 7.57 (sliding window)
- Optimal chunk: 1024 tokens

**Application for STOPA:** When STOPA's /autoloop, /autoresearch, or /self-evolve operate at deep tier with >64k context, and TTT-capable models are available (future releases), they should be preferred over standard models. The improvement is not marginal — RULER-16k goes from near-random to strong performance.

**Watch for:** Model release notes mentioning "fast weights," "in-context weight update," or "TTT support" — these indicate In-Place TTT or equivalent capability.
