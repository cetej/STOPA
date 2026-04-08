---
name: Flow Map Language Models
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [flow-map-language-models]
tags: [language-model, inference, diffusion, architecture, generation]
---

# Flow Map Language Models (FMLM)

> Continuous flow formulation over one-hot token embeddings that enables one-step language generation, outperforming 8-step discrete diffusion models in quality.

## Key Facts

- Continuous flows over one-hot embeddings outperform discrete diffusion in both quality and speed (ref: sources/flow-map-language-models.md)
- FLM (flow model) matches SOTA discrete diffusion on LM1B and OpenWebText (ref: sources/flow-map-language-models.md)
- FMLM (distilled one-step variant) exceeds 8-step quality of recent few-step discrete diffusion LMs (ref: sources/flow-map-language-models.md)
- Trained via simple cross-entropy objectives preserving simplex geometry (ref: sources/flow-map-language-models.md)
- Three flow map distillation strategies compared (ref: sources/flow-map-language-models.md)

## Relevance to STOPA

Low direct relevance. Advances in one-step LM inference could reduce latency for future model generations used in orchestration, but no immediately transferable pattern for skill/memory/agent design.

## Mentioned In

- [Flow Map Language Models](../sources/flow-map-language-models.md)
