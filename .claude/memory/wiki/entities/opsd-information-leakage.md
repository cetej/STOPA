---
name: Information Leakage in Self-Distillation
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [rlsd-self-distilled-rlvr]
tags: [rl-training, self-distillation, failure-mode, anti-pattern]
---

# Information Leakage in Self-Distillation (OPSD)

> When a teacher model has access to privileged information (reference answers) that the student doesn't, gradients carry r-dependent deviations whose variance accumulates to corrupt training — even though mean deviation is zero.

## Key Facts

- KL decomposition: L_OPSD = L* + I(Y_t; R|X, Y<t) — the mutual information term is irreducible, can't be optimized away (ref: sources/rlsd-self-distilled-rlvr.md)
- Zero-mean perturbation trap: per-sample gradient deviations E[delta] = 0, but Var[||delta||²] drives accumulating corruption (ref: sources/rlsd-self-distilled-rlvr.md)
- Impossibility trilemma: distribution-matching + shared params can't simultaneously achieve stability + improvement + leakage-free (ref: sources/rlsd-self-distilled-rlvr.md)
- All compression strategies fail: full-vocab, teacher's top-1, student's top-1 all show monotonically increasing leakage (ref: sources/rlsd-self-distilled-rlvr.md)
- OPSD performance peaks at 10-20 steps then systematically degrades (ref: sources/rlsd-self-distilled-rlvr.md)

## Relevance to STOPA

This is a general warning for STOPA's self-evolution patterns: when /self-evolve or /autoloop uses a "teacher" signal that has access to information the agent doesn't (e.g., ground-truth test results during optimization), the optimization can leak toward the specific test rather than the general goal. RLSD's fix — decouple direction from magnitude — is the mitigation.

## Mentioned In

- [Self-Distilled RLVR](../sources/rlsd-self-distilled-rlvr.md)
