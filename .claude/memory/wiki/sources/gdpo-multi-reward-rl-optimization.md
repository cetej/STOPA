---
title: "GDPO: Group reward-Decoupled Normalization Policy Optimization for Multi-reward RL Optimization"
slug: gdpo-multi-reward-rl-optimization
source_type: url
url: "https://arxiv.org/abs/2601.05242"
date_ingested: 2026-04-07
date_published: "2026-01"
entities_extracted: 3
claims_extracted: 6
---

# GDPO: Group reward-Decoupled Normalization Policy Optimization

> **TL;DR**: GRPO's group normalization of summed multi-rewards collapses distinct reward combinations to identical advantage values. GDPO fixes this by normalizing each reward independently before aggregation, yielding consistent +2–7% gains across tool calling, math, and coding tasks.

## Key Claims

1. Applying GRPO to normalized sums of multiple rewards causes "advantage collapse" — reward combos (0,1) and (0,2) get identical normalized advantages despite different achievement levels — `verified` (mathematical demonstration + Figure 3)
2. GDPO's 3-step process (per-reward group norm → sum → batch norm) preserves exponentially more distinct advantage groups as reward count scales — `verified`
3. GDPO: ~5% improvement on Live tool-calling tasks, 4% format compliance improvement over GRPO — `verified` (Qwen2.5-1.5B benchmark)
4. GDPO + conditional rewards (DeepSeek-R1-7B): +4.4% AIME, 16.9% fewer length violations — `verified`
5. Weight-based priority adjustment alone is ineffective when objective difficulties diverge — model optimizes easier reward regardless — `argued`
6. Removing batch-wise normalization occasionally causes full training failure — `verified` (ablation study)

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [GDPO](../entities/gdpo.md) | concept | new |
| [GRPO](../entities/grpo.md) | concept | new |
| [Conditional Reward Design](../entities/conditional-reward-design.md) | concept | new |

## Relations

- GDPO `extends` GRPO — decoupled normalization variant of group relative policy optimization
- GDPO `supersedes` GRPO — for multi-reward settings specifically
- Conditional Reward Design `part_of` GDPO — priority alignment strategy

## Cross-References

- Related learnings: none found (no prior GRPO/multi-reward learnings)
- Related wiki articles: skill-evaluation.md (multi-metric optimization patterns)
- Contradictions: none
