---
name: RLSD
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [rlsd-self-distilled-rlvr]
tags: [rl-training, self-distillation, credit-assignment, policy-optimization]
---

# RLSD (RLVR with Self-Distillation)

> Hybrid RL training method that decouples update direction (from environment rewards) and update magnitude (from teacher-student token differences), avoiding information leakage while achieving dense per-token credit assignment.

## Key Facts

- Decouples direction vs magnitude: sign(A) from environment, token-level weight w_t = (P_T/P_S)^sign(A) from teacher (ref: sources/rlsd-self-distilled-rlvr.md)
- Clipped credit assignment: clip(w_t, 1-eps, 1+eps) bounds teacher influence — trust region mechanism (ref: sources/rlsd-self-distilled-rlvr.md)
- +4.69% over base Qwen3-VL-8B, +2.32% over GRPO avg across 5 benchmarks; MathVision +3.91pp (ref: sources/rlsd-self-distilled-rlvr.md)
- 2× convergence speed: 200-step RLSD > 400-step GRPO (ref: sources/rlsd-self-distilled-rlvr.md)
- 15-20% higher entropy than GRPO — resists premature mode collapse (ref: sources/rlsd-self-distilled-rlvr.md)
- No auxiliary networks — drop-in replacement for GRPO's uniform advantages (ref: sources/rlsd-self-distilled-rlvr.md)
- Only needs ground-truth answer (not full reasoning traces like OPSD) (ref: sources/rlsd-self-distilled-rlvr.md)

## Relevance to STOPA

The direction-vs-magnitude decoupling pattern is transferable to STOPA's iterative optimization skills. In /autoloop and /self-evolve, the critic provides direction (pass/fail, better/worse), while the diff magnitude should come from token-level analysis of what changed. Currently STOPA treats all changes uniformly — RLSD suggests separating "which direction to go" from "how much to change each part."

## Mentioned In

- [Self-Distilled RLVR](../sources/rlsd-self-distilled-rlvr.md)
