---
name: Fast Weights
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [in-place-ttt-mlp-fast-weights]
tags: [model-architecture, inference, weight-adaptation, continuous-learning]
---

# Fast Weights

> Model weights that can be rapidly updated during inference (as opposed to slow weights updated only during training), enabling the model to adapt to incoming context within a forward pass.

## Key Facts

- In In-Place TTT: W_down (MLP final projection) serves as fast weight — updated chunk-by-chunk during inference (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Pre-trained weights are preserved alongside fast weight updates — no catastrophic forgetting (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Performance scales consistently with fast weight state size — larger capacity → better results (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Negligible throughput and memory overhead on modern hardware (ref: sources/in-place-ttt-mlp-fast-weights.md)
- Conceptually distinct from LoRA adapters: fast weights update in real-time during inference, not fine-tuned offline (ref: sources/in-place-ttt-mlp-fast-weights.md)

## Relevance to STOPA

Fast weights are the implementation mechanism behind In-Place TTT. Understanding this pattern helps evaluate future model releases: models advertised as "TTT-compatible" or "in-context learning via fast weights" should be prioritized for STOPA's long-context iterative skills.

## Mentioned In

- [In-Place TTT: LLM Weight Adaptation at Inference](../sources/in-place-ttt-mlp-fast-weights.md)
