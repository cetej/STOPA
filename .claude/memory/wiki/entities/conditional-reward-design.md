---
name: Conditional Reward Design
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [gdpo-multi-reward-rl-optimization]
tags: [rl-training, multi-reward, reward-shaping, priority]
---

# Conditional Reward Design

> A reward engineering pattern where easier/secondary rewards are gated on the achievement of harder/primary rewards, preventing models from gaming easy objectives while ignoring hard ones.

## Key Facts

- Core mechanism: `R_length = 1 if length ≤ L AND R_correct = 1, else 0` — length reward activates only when correctness is achieved (ref: sources/gdpo-multi-reward-rl-optimization.md)
- Addresses priority ordering failure: weight adjustment alone is insufficient when objective difficulties diverge substantially — model optimizes easier reward regardless of weights (ref: sources/gdpo-multi-reward-rl-optimization.md)
- DeepSeek-R1-7B with conditional rewards: +4.4% AIME accuracy, 16.9% fewer length violations vs unconditioned multi-reward (ref: sources/gdpo-multi-reward-rl-optimization.md)
- More effective than weight-based priority for hard/easy objective pairs; weight tuning remains useful for fine-grained control after difficulty gaps are resolved (ref: sources/gdpo-multi-reward-rl-optimization.md)

## Relevance to STOPA

Pattern applicable to STOPA's /autoloop and optimization skills when running multi-metric improvement loops: gate style/format rewards on correctness to prevent reward gaming.

## Mentioned In

- [GDPO: Group reward-Decoupled Normalization Policy Optimization](../sources/gdpo-multi-reward-rl-optimization.md)
