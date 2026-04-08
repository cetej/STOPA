---
name: diversity-collapse
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [reasoning-with-sampling]
tags: [rl-training, sampling, inference-time, anti-pattern]
---

# diversity-collapse

> Side effect of RL post-training (GRPO, PPO) where the model's output distribution narrows, causing repeated similar responses regardless of sampling temperature.

## Key Facts

- Occurs after reinforcement learning fine-tuning (GRPO, PPO, RLHF) — model converges to narrow high-reward region (ref: sources/reasoning-with-sampling.md)
- p-alpha-sampling avoids this: no training → original distribution preserved (ref: sources/reasoning-with-sampling.md)
- Manifests as: Pass@k diversity drops sharply after RL training (ref: sources/reasoning-with-sampling.md)
- Practical test: run same prompt 5× with temperature 0.8 — if outputs are near-identical, diversity collapse is present

## Relevance to STOPA

`/autoresearch` and `/autoloop` rely on generating diverse candidate solutions. Choosing RL-tuned models for these iterative skills risks diversity collapse and reduces the effective exploration space. Prefer base/lightly-tuned models or high temperature when exploration matters. This is the mechanism behind the "sampling > greedy for reasoning loops" principle.

## Mentioned In

- [Reasoning with Sampling (arXiv:2510.14901)](../sources/reasoning-with-sampling.md)
