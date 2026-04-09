---
title: "The Art of Scaling Reinforcement Learning Compute for LLMs"
slug: scalerl-scaling-rl-compute-llms
source_type: url
url: "https://arxiv.org/abs/2510.13786"
date_ingested: 2026-04-08
date_published: "2025-10"
entities_extracted: 3
claims_extracted: 7
---

# The Art of Scaling Reinforcement Learning Compute for LLMs

> **TL;DR**: 400K GPU-hour study establishing sigmoidal compute-performance curves for RL training. Three core principles: (1) not all recipes reach the same ceiling — loss type and batch size shift asymptote A, (2) early small-compute performance is UNRELIABLE predictor of scale performance, (3) most design choices affect efficiency B, not ceiling A. ScaleRL recipe (CISPO + curriculum + FP32 head) achieves A=0.61 vs GRPO's 0.52.

## Key Claims

1. RL compute-performance follows sigmoidal curve: R = R0 + (A-R0) / (1+(Cmid/C)^B); asymptote A varies by recipe — `verified` (400K GPU-hours, reproducible with ±0.015)
2. Early small-compute performance is unreliable: methods superior at low compute may underperform at scale — `verified` (cross-recipe ablations)
3. Most design choices (normalization, curriculum, off-policy) primarily modulate efficiency B, not ceiling A — `verified` (16K GPU-hour leave-one-out experiments)
4. CISPO is far more robust to hyperparameters than DAPO/GRPO: εmax {4,5,8} → minimal variance vs DAPO's 0.05-0.09 shift — `verified`
5. FP32 precision at LM head: dramatic improvement 0.52→0.61 asymptote — `verified`
6. Larger batch sizes (2048 vs 768): identical entropy but substantially better final performance — `verified`
7. Scout 17Bx16 MoE: A=0.71 vs 8B's 0.61, requires 6× less RL compute for equivalent — `verified`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [ScaleRL](../entities/scalerl.md) | concept | new |
| [Sigmoidal Scaling Curves](../entities/sigmoidal-scaling-curves.md) | concept | new |
| [GRPO](../entities/grpo.md) | concept | updated |

## Relations

- ScaleRL `extends` GRPO — uses CISPO instead of GRPO's loss, adds curriculum filtering
- ScaleRL `uses` Sigmoidal Scaling Curves — core predictive framework
- ScaleRL `competes_with` DAPO — DAPO less robust to hyperparameters

## Cross-References

- Related learnings: `2026-04-08-direction-magnitude-decoupling-optimization.md` (RLSD also improves over GRPO)
- Related entities: grpo.md, rlsd.md, gdpo.md
- Contradictions: none
