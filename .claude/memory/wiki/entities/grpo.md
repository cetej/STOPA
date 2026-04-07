---
name: GRPO (Group Relative Policy Optimization)
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [beyond-mode-research]
tags: [reinforcement-learning, fine-tuning, rlvr, deepseek]
---
# GRPO (Group Relative Policy Optimization)

> RL training objective used in DeepSeek-R1 and Multi-Answer RL that eliminates the value model by normalizing rewards within a group of K sampled outputs; enables RLVR without a separate critic network.

## Key Facts

- Eliminates value model by normalizing reward across K outputs in the same group (ref: sources/beyond-mode-research.md)
- Used in DeepSeek-R1 (arXiv:2501.12948) at scale; adopted in Multi-Answer RL for diversity training (ref: sources/beyond-mode-research.md)
- Implementation: TRL + DeepSpeed stack; requires 4× A100 for 8B model training (ref: sources/beyond-mode-research.md)
- Key advantage over PPO: cheaper to run (no separate value model inference) (ref: sources/beyond-mode-research.md)

## Relevance to STOPA

Technical foundation if STOPA ever needs RL fine-tuning for a specialized model (e.g., ORAKULUM forecasting model). GRPO is the standard choice for RLVR tasks.

## Mentioned In

- [Reaching Beyond the Mode — Multi-Answer RL and Uncertainty Quantification](../sources/beyond-mode-research.md)
