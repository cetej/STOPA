---
title: "Pro-AI Bias in Large Language Models"
slug: pro-ai-bias-llms
source_type: url
url: "https://arxiv.org/abs/2601.13749"
date_ingested: 2026-04-13
date_published: "2026-01-20"
entities_extracted: 1
claims_extracted: 3
---

# Pro-AI Bias in LLMs

> **TL;DR**: LLMs systematically favor AI/ML solutions in recommendation tasks across diverse domains, even when not mentioned in query. Proprietary models show near-deterministic AI preference. AI job salaries overestimated by ~10pp. Structural analog to commercial persuasion — emergent training bias, not injected objective.

## Key Claims

1. LLMs disproportionately recommend AI-related options in advice-seeking queries; proprietary models near-deterministic — `[verified]`
2. AI job salary overestimation ~10pp vs matched non-AI jobs — `[verified]`
3. "Artificial Intelligence" has highest similarity across positive/negative/neutral framings in open-weight models — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Pro-AI Bias](../entities/pro-ai-bias.md) | concept | new |

## Relations

- `Pro-AI Bias` `analogous_to` `AI Commercial Persuasion` — emergent bias vs injected commercial objective
- `Pro-AI Bias` `detected_via` controlled counterfactual testing

## Cross-References

- Related: `ai-commercial-persuasion.md` — same structural phenomenon, different source (training data vs system prompt)
- Related: `selective-neglect-persuasion.md` — mechanism overlap (asymmetric treatment)
