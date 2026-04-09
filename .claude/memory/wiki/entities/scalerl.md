---
name: ScaleRL
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [scalerl-scaling-rl-compute-llms]
tags: [rl-training, scaling-laws, policy-optimization, compute-efficiency]
---

# ScaleRL

> Best-practice RL training recipe for LLMs achieving highest asymptotic performance (A=0.61 on 8B, A=0.71 on Scout MoE) through CISPO loss, FP32 LM head, curriculum filtering, and batch-level normalization.

## Key Facts

- Recipe: CISPO loss + FP32 LM head + prompt-level averaging + batch-level normalization + No-Positive-Resampling (filter ≥90% pass rate prompts) + zero-variance exclusion (ref: sources/scalerl-scaling-rl-compute-llms.md)
- A=0.61 on 8B dense (vs GRPO ~0.52); Scout 17Bx16 MoE: A=0.71 (ref: sources/scalerl-scaling-rl-compute-llms.md)
- CISPO is far more robust to hyperparameters than DAPO/GRPO: εmax across {4,5,8} → minimal variance (ref: sources/scalerl-scaling-rl-compute-llms.md)
- FP32 at LM head: single biggest gain, 0.52→0.61 asymptote (ref: sources/scalerl-scaling-rl-compute-llms.md)
- Validated by 100K GPU-hour run matching predicted asymptote within ±0.02 (ref: sources/scalerl-scaling-rl-compute-llms.md)
- No-Positive-Resampling curriculum: filter out problems the model already solves reliably — focus compute on hard problems (ref: sources/scalerl-scaling-rl-compute-llms.md)

## Relevance to STOPA

ScaleRL's No-Positive-Resampling maps directly to STOPA's /self-evolve: stop iterating on eval cases the skill already passes reliably, focus compute on failing/flaky cases. The sigmoidal curve model suggests /autoloop should fit performance trajectory and predict asymptote early — if the ceiling is low, switch approaches instead of burning iterations.

## Mentioned In

- [The Art of Scaling RL Compute for LLMs](../sources/scalerl-scaling-rl-compute-llms.md)
