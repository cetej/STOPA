---
name: In-Place TTT
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [in-place-ttt-mlp-fast-weights]
tags: [inference, continuous-learning, long-context, model-architecture, weight-adaptation]
---

# In-Place TTT

> Framework enabling LLMs to dynamically update their own weights during inference by repurposing existing MLP projection matrices as "fast weights" — no new layers, no retraining required.

## Key Facts

- Repurposes the final projection matrix (W_down) of MLP blocks as adaptable fast weights — drop-in compatible with any transformer (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Drop-in enhancement on Qwen3-4B: +4.4 accuracy at 64k tokens, +2.2 at 128k tokens (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Full-pretrain RULER-16k benchmark: 6.58 → 19.99 (full attention mode), 5.07 → 7.57 (sliding window) (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Optimal chunk size: 1024 tokens — balances efficiency and performance (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Uses LM-aligned objective (next-token prediction via 1D convolution + projection) instead of generic reconstruction — Theorem 1 proves it increases correct token logits by ≥ λ_lr·c²_norm·c_align (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Supports context parallelism via parallel scan algorithm — scales to modern hardware (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Outperforms Gated Linear Attention and DeltaNet at 500M/1.5B scale on sliding-window perplexity 2k-32k (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Compatible with position extrapolation (YaRN) for 256k+ context (ref: sources/in-place-ttt-mlp-fast-weights.md)

## Relevance to STOPA

When selecting models for STOPA's deep-tier iterative agents (autoloop, autoresearch, self-evolve) on tasks with > 64k context, prefer models with In-Place TTT support — they show 3-12× improvement on long-context benchmarks. This is the strongest inference-time adaptation signal currently available.

## Mentioned In

- [In-Place TTT: LLM Weight Adaptation at Inference](../sources/in-place-ttt-mlp-fast-weights.md)
