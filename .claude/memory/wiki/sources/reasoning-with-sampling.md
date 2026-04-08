---
title: "Reasoning with Sampling: Your Base Model is Smarter Than You Think"
slug: reasoning-with-sampling
source_type: url
url: "https://arxiv.org/abs/2510.14901"
date_ingested: 2026-04-08
date_published: "2025-10"
entities_extracted: 4
claims_extracted: 5
---

# Reasoning with Sampling: Your Base Model is Smarter Than You Think

> **TL;DR**: MCMC sampling from p^α (sharpened power distributions) extracts latent reasoning from base models without any training. Results nearly match RL-trained GRPO on math reasoning and beat it on code. Key advantage: preserves generation diversity that RL destroys.

## Key Claims

1. Base models contain more latent reasoning capability than assumed — inference-time sampling unlocks it — `[argued]`
2. p^α MCMC achieves 74.8% MATH500 and 57.3% HumanEval vs GRPO 78.5% / 53.7% — `[verified]`
3. RL post-training (GRPO) causes diversity collapse — p-alpha-sampling preserves Pass@k diversity — `[verified]`
4. Method requires no verifier, no curated dataset, no hyperparameter tuning — `[verified]`
5. Token overhead ~8.84× standard inference — diversity and quality come at inference cost — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [p-alpha-sampling](../entities/p-alpha-sampling.md) | concept | new |
| [diversity-collapse](../entities/diversity-collapse.md) | concept | new |
| Aayush Karan | person | skipped (not STOPA-relevant) |
| Yilun Du | person | skipped (not STOPA-relevant) |

## Relations

- `p-alpha-sampling` `competes_with` GRPO — same reasoning benchmark results with different tradeoffs
- `p-alpha-sampling` `uses` Metropolis-Hastings MCMC — implementation mechanism
- `diversity-collapse` `caused_by` RL post-training — mechanism identified in paper

## Cross-References

- Related learnings: `2026-04-07-multi-reward-normalization-collapse.md` (RL reward shaping), `2026-04-06-osft-self-sharpening.md` (sampling from model's own distribution)
- Related wiki articles: `general-security-environment.md` (GDPO multi-reward section)
- Contradictions: none detected
