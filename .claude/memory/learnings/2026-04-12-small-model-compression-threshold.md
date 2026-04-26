---
date: 2026-04-12
type: best_practice
severity: high
component: orchestration
tags: [model-selection, scaling, small-models, haiku, compression, capacity]
summary: "Models below ~1B parameters fail to enter the compression phase of IB training dynamics — they lack capacity to compress a given data complexity. This is a fundamental limit, not a training duration issue: SmolLM2 1.7B (11T tokens) also fails."
source: external_research
maturity: draft
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 0.86
impact_score: 0.0
related: [2026-04-11-compression-regime-maps-to-tiers.md]
verify_check: "manual"
skill_scope: [orchestrate, council]
---

## Detail

Conklin et al. (arXiv:2604.07569, ICLR 2026) show that LLM training follows a 2-phase trajectory:
1. Fitting: I(Y;Z) increases (model learns to predict)
2. Compression: I(X;Z) decreases (model compresses irrelevant input toward IB bound)

Models below a capacity threshold oscillate in Phase 1 and never achieve meaningful compression:
- OLMo2 1B: never reaches Phase 2
- SmolLM2 1.7B: same failure despite 11T training tokens
- Pythia 6.9B: still in expansion phase at end of training (undertrained)

OLMo2 7B and 32B both achieve clean Phase 2 compression.

**Implication for STOPA tier selection:** Haiku-class models have a fundamental representational limit — they cannot encode the same contextual structure as Sonnet/Opus-class models. For tasks requiring complex contextual reasoning (orchestration planning, multi-hop analysis), this is a capacity wall, not a prompt engineering problem.
