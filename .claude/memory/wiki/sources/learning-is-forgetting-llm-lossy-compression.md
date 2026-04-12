---
title: "Learning is Forgetting: LLM Training As Lossy Compression"
slug: learning-is-forgetting-llm-lossy-compression
source_type: url
url: "https://arxiv.org/abs/2604.07569"
date_ingested: 2026-04-12
date_published: "2026-04 (ICLR 2026)"
entities_extracted: 6
claims_extracted: 7
---

# Learning is Forgetting: LLM Training As Lossy Compression

> **TL;DR**: LLM training is formalized as lossy compression via the Information Bottleneck framework; optimality I(Y;Z)/I(X;Z) predicts benchmark performance (r=0.52) and preference info I(Z;pref) predicts alignment (r=0.76) without behavioral eval — first empirical validation at scale with 75 models.

## Key Claims

1. LLM training follows a 2-phase IB trajectory (fitting → compression); transition at loss saturation — `[verified]`
2. Optimality I(Y;Z)/I(X;Z) predicts aggregate benchmark performance at r=0.52, p<0.001 (47 models, 6 benchmarks) — `[verified]`
3. Preference information I(Z;pref) is the strongest predictor at r=0.76 — dissociates pre-training (knowledge) from post-training (instruction following) — `[verified]`
4. Models below a capacity threshold (≈1B params) fail to enter Phase 2 compression — `[verified]`
5. 75 models from 6 families converge to the same IB bound region — universal deep learning property — `[verified]`
6. IFEval not predicted by compression (r=0.07) but by preference info (r=0.39) — `[verified]`
7. Post-training increases preference info while minimally changing complexity — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Information Bottleneck](../entities/information-bottleneck.md) | concept | new |
| [Soft Entropy Estimator](../entities/soft-entropy-estimator.md) | tool | new |
| [Optimality Metric (IB)](../entities/optimality-metric.md) | concept | new |
| [Preference Information](../entities/preference-information.md) | concept | new |
| [Two-Phase LLM Training](../entities/two-phase-llm-training.md) | concept | new |
| [arXiv:2604.07569](../entities/arxiv-2604-07569.md) | paper | new |

## Relations

- `information-bottleneck` `inspired_by` `rate-distortion-theory` (Shannon 1948)
- `soft-entropy-estimator` created for `information-bottleneck` measurement at LLM scale
- `optimality-metric` `part_of` `information-bottleneck` — derived ratio
- `preference-information` `part_of` `information-bottleneck` — IB applied to alignment signal
- `two-phase-llm-training` `part_of` `information-bottleneck` — empirical prediction from IB theory

## Cross-References

- Related learnings: none found (first IB/lossy-compression content in memory)
- Related wiki articles: [general-security-environment](../general-security-environment.md) (scaling model selection), [skill-evaluation](../skill-evaluation.md) (model quality metrics)
- Contradictions: none detected
