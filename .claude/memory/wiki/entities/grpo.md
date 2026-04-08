---
name: GRPO
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [gdpo-multi-reward-rl-optimization]
tags: [rl-training, policy-optimization, llm-optimization]
---

# GRPO

> Group Relative Policy Optimization — RL policy gradient method for LLMs normalizing rewards at group level; baseline for GDPO.

## Key Facts

- Applies group-level normalization to aggregated (summed) rewards across objectives (ref: sources/gdpo-multi-reward-rl-optimization.md)
- Critical flaw in multi-reward settings: distinct reward combinations collapse to identical advantage values, destroying inter-objective signal (ref: sources/gdpo-multi-reward-rl-optimization.md)
- GRPO without std normalization: theoretically more diverse but causes training instability — 0% format correctness in tool-calling experiments (ref: sources/gdpo-multi-reward-rl-optimization.md)
- Works acceptably for single-objective RL; problematic for 2+ reward objectives (ref: sources/gdpo-multi-reward-rl-optimization.md)

## Relevance to STOPA

GRPO's collapse limitation is context for any multi-reward optimization in STOPA skills (/autoloop optimizing correctness + length simultaneously).

## Mentioned In

- [GDPO: Group reward-Decoupled Normalization Policy Optimization](../sources/gdpo-multi-reward-rl-optimization.md)
