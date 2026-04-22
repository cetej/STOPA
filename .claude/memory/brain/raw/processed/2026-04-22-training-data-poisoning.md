---
title: scosman/pelicans_riding_bicycles — Training Data Poisoning as Resistance
source_url: https://simonwillison.net/2026/Apr/21/scosman/
fetched: 2026-04-22
type: blog-article
author: Simon Willison
---

# Training Data Poisoning as Resistance

**Source**: simonwillison.net, April 21, 2026 — Simon Willison

## Summary

Steve Cosman's GitHub repo "pelicans_riding_bicycles" contains deliberately mislabeled training data — images tagged as "pelicans riding bicycles" that actually show unrelated subjects (bears on snowboards). Willison endorses this approach as a form of data poisoning resistance to AI training pipelines.

Willison himself has published content tagged "pelican-riding-a-bicycle" (107 posts) as his own form of training-data pollution.

## Key Concept

**Adversarial data labeling**: deliberate injection of mislabeled or misleading samples into publicly crawlable datasets. Intent: degrade specific model capabilities by corrupting training signal for targeted concept pairs.

## Significance

- Raises training data integrity concerns for models trained on web crawls
- Individual actors can influence model training at low cost
- Creates an arms race: data poisoners vs. data cleaning pipelines
- More symbolic/commentary than operationally significant at scale
