---
title: "How AI Aggregation Affects Knowledge"
slug: acemoglu-ai-aggregation-knowledge
source_type: url
url: "https://arxiv.org/abs/2604.04906"
date_ingested: 2026-04-09
date_published: "2026-04-06"
entities_extracted: 3
claims_extracted: 5
---

# How AI Aggregation Affects Knowledge

> **TL;DR**: Acemoglu et al. (MIT) formalize endogenous feedback loops in AI aggregation via extended DeGroot model. Three key results: fast aggregator updates amplify bias (model collapse parallel), majority-weighted training degrades minority dimensions, and a single global aggregator necessarily worsens at least one knowledge dimension vs local specialized ones.

## Key Claims

1. Fast-updating aggregator (low ρ) prevents beneficial learning across diverse environments — `[verified]` (Theorem 2, formal proof)
2. Majority-weighted training data worsens learning, degradation monotonically increases with network segregation — `[verified]` (Proposition 2)
3. Minority-weighted correction helps only at intermediate segregation, fails at extremes — `[verified]` (Proposition 3)
4. Local topic-specific aggregators improve learning; consolidating into global necessarily worsens ≥1 dimension — `[verified]` (Theorem 3, Proposition 4)
5. Endogenous feedback loop: aggregator trains on beliefs shaped by own output, amplifying rather than correcting errors — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Daron Acemoglu](../entities/daron-acemoglu.md) | person | new |
| [DeGroot model](../entities/degroot-model.md) | concept | new |
| [endogenous feedback loop](../entities/endogenous-feedback-loop.md) | concept | new |

## Relations

- DeGroot model `extended_by` Acemoglu — AI aggregator node added to classical social learning
- endogenous feedback loop `causes` model collapse — parallel mechanism via belief-training-feedback cycle
- local aggregators `outperform` global aggregators — for specialized/multidimensional knowledge (Theorem 3)

## Cross-References

- Related learnings: `2026-03-30-write-time-gating-salience.md` (write-time gating = upstream defense against aggregation bias)
- Related wiki: [memory-architecture](../memory-architecture.md) (STOPA's learning pipeline IS the aggregation loop described)
- Implementation: circular validation detection in `learning-admission.py`, `skill_scope:` field, inverse frequency graduation
