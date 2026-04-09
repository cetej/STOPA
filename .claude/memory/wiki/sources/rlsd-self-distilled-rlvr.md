---
title: "Self-Distilled RLVR: Reliable Self-Evolution for LLMs"
slug: rlsd-self-distilled-rlvr
source_type: url
url: "https://arxiv.org/abs/2604.03128"
date_ingested: 2026-04-08
date_published: "2026-04"
entities_extracted: 3
claims_extracted: 6
---

# Self-Distilled RLVR

> **TL;DR**: OPSD (on-policy self-distillation) fails due to information leakage — teacher sees reference answers, student doesn't. RLSD fixes this by decoupling: environment rewards control update DIRECTION, teacher differences modulate MAGNITUDE. Result: +4.69% over base, +2.32% over GRPO on multimodal reasoning, 2× convergence speed.

## Key Claims

1. OPSD fails due to irreducible information leakage: KL decomposes as L_OPSD = L* + I(Y_t; R|X, Y<t), the mutual info term can't be optimized away — `argued` (Theorem 1, KL decomposition proof)
2. Impossibility trilemma: distribution-matching with shared params can't simultaneously achieve stability + improvement + leakage-free — `argued` (Theorem 3)
3. RLSD achieves leakage immunity via 3 structural isolations: directional, support, magnitude-bounded — `argued` (Theorem 5)
4. RLSD outperforms GRPO by +2.32% avg across 5 multimodal benchmarks (Qwen3-VL-8B); MathVision +3.91pp — `verified`
5. At 200 steps RLSD surpasses GRPO at 400 steps → 2× convergence acceleration — `verified`
6. RLSD maintains 15-20% higher entropy than GRPO throughout training, preventing premature mode collapse — `verified`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [RLSD](../entities/rlsd.md) | concept | new |
| [GRPO](../entities/grpo.md) | concept | updated |
| [Information Leakage in Self-Distillation](../entities/opsd-information-leakage.md) | concept | new |

## Relations

- RLSD `extends` GRPO — uses GRPO framework, replaces uniform advantages with clipped teacher-modulated advantages
- RLSD `supersedes` OPSD — fixes leakage while retaining dense credit assignment
- RLSD `uses` GRPO — same base framework, no auxiliary networks

## Cross-References

- Related learnings: `2026-04-08-inference-time-sampling-beats-rl-for-diversity.md` (diversity/entropy preservation)
- Related wiki: skill-evaluation.md (credit assignment in iterative optimization)
- Related entities: grpo.md, gdpo.md (multi-reward RL), diversity-collapse.md
- Contradictions: none
