---
name: GDPO
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [gdpo-multi-reward-rl-optimization]
tags: [rl-training, multi-reward, normalization, llm-optimization]
---

# GDPO

> Group reward-Decoupled Normalization Policy Optimization — fixes GRPO's advantage collapse in multi-reward RL training by normalizing each reward independently before aggregating.

## Key Facts

- GDPO decouples normalization: each reward gets independent group-wise normalization, THEN advantages sum, THEN batch-level normalization for stability (ref: sources/gdpo-multi-reward-rl-optimization.md)
- Direct GRPO with summed rewards causes "advantage collapse" — distinct reward combinations (e.g., (0,1) vs (0,2)) map to identical normalized advantages (-0.7071, +0.7071), erasing useful signal (ref: sources/gdpo-multi-reward-rl-optimization.md)
- Tool calling improvements: ~5% on Live tasks, 2.7% avg accuracy, 4% format compliance vs GRPO (ref: sources/gdpo-multi-reward-rl-optimization.md)
- Math reasoning (DeepSeek-R1-1.5B): +2.6% MATH, +6.7% AIME, 80% fewer length violations (ref: sources/gdpo-multi-reward-rl-optimization.md)
- Coding (3 rewards): +2.6–3.3% pass rate improvements; scales to 3+ reward objectives (ref: sources/gdpo-multi-reward-rl-optimization.md)
- Removing batch-wise normalization occasionally causes full training failure — it's load-bearing for stability (ref: sources/gdpo-multi-reward-rl-optimization.md)

## Relevance to STOPA

When STOPA skills optimize against multiple metrics simultaneously (e.g., /autoloop with quality + length constraints, /self-evolve with correctness + format), GDPO's decoupled normalization principle should inform reward aggregation design to avoid signal collapse.

## Mentioned In

- [GDPO: Group reward-Decoupled Normalization Policy Optimization](../sources/gdpo-multi-reward-rl-optimization.md)
