---
title: Training Data Poisoning as Adversarial Resistance
category: concepts
tags: [ai-safety, training-data, adversarial-ml, data-integrity]
sources: [raw/processed/2026-04-22-training-data-poisoning.md]
updated: 2026-04-22
---

# Training Data Poisoning as Adversarial Resistance

**Source**: Simon Willison, simonwillison.net, April 21, 2026  
**Project**: scosman/pelicans_riding_bicycles (GitHub)

## Concept

Deliberate injection of mislabeled or misleading samples into publicly crawlable datasets. Images tagged "pelicans riding bicycles" depict unrelated subjects (bears on snowboards). Intent: degrade specific model capabilities by corrupting training signal for targeted concept pairs.

Willison endorses this as a form of resistance to AI training pipelines scraping public content without consent.

## Mechanism

Individual actors → publish mislabeled content on public web → AI training crawlers ingest it → targeted model capabilities degrade for poisoned concept pairs.

Low-cost to execute; difficult to detect at scale. Raises training data integrity concerns for any model trained on web crawls.

## Adversarial Dynamics

- Data poisoners vs. data cleaning pipelines
- Arms race: as cleaning improves, poisoning must become more subtle
- More symbolic/commentary than operationally significant at current scale
- 107+ posts tagged "pelican-riding-a-bicycle" on simonwillison.net alone

## Significance for 2BRAIN

Primarily a data integrity + AI safety signal. Affects trust assumptions about publicly sourced training data. For 2BRAIN's RAG pipeline: internal/curated sources are more trustworthy than public web crawl data.

## Related Concepts

→ [prompt-injection-defense.md](prompt-injection-defense.md)  
→ [kill-chain-canary.md](kill-chain-canary.md)
