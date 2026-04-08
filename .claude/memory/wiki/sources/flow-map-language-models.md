---
title: "Flow Map Language Models: One-step Language Modeling via Continuous Denoising"
slug: flow-map-language-models
source_type: url
url: "https://arxiv.org/abs/2602.16813"
date_ingested: 2026-04-08
date_published: "2026-02-18"
entities_extracted: 1
claims_extracted: 3
---

# Flow Map Language Models

> **TL;DR**: Continuous flows over one-hot token embeddings beat discrete diffusion for language generation. Distilled one-step model (FMLM) exceeds 8-step discrete diffusion quality. Challenges assumption that discrete noising is necessary for discrete modalities.

## Key Claims

1. Continuous flow matching over one-hot embeddings matches SOTA discrete diffusion on LM1B and OpenWebText — `verified`
2. One-step distilled model (FMLM) exceeds 8-step quality of recent few-step discrete diffusion LMs — `verified`
3. Continuous flow formulation enables learning a unique flow map that discrete methods cannot achieve — `argued`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Flow Map Language Models](../entities/flow-map-language-models.md) | concept | new |

## Relations

- FMLM `competes_with` discrete diffusion language models — continuous alternative with fewer steps
- FMLM `uses` flow map distillation — three strategies compared

## Cross-References

- Related learnings: none matched
- Related wiki articles: none (no existing diffusion/generation articles)
- Contradictions: none
