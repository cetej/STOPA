---
title: "The Missing Knowledge Layer in Cognitive Architectures for AI Agents"
arxiv: "2604.11364"
fetched: 2026-04-21
source: https://arxiv.org/abs/2604.11364
authors: [Michaël Roynard (LAAS-OASIS)]
tags: [cognitive-architecture, knowledge-layer, memory, persistence-semantics, coala]
---

# Raw Extraction

## Key Concepts
- CoALA and JEPA lack explicit Knowledge layer with distinct persistence semantics
- Four-layer decomposition: Knowledge / Memory / Wisdom / Intelligence
- Persistence semantics: indefinite supersession / Ebbinghaus decay / evidence-gated revision / ephemeral inference

## Main Claims
- Applying cognitive decay to factual information (facts don't decay like memories) = architectural error
- Using identical update mechanics for facts and experiences = conflation error
- Eight convergence points across existing frameworks point to same gap
- Companion Python + Rust implementations demonstrate feasibility

## Proposed Layers
| Layer | Persistence Semantics |
|-------|----------------------|
| Knowledge | Indefinite supersession |
| Memory | Ebbinghaus decay |
| Wisdom | Evidence-gated revision |
| Intelligence | Ephemeral inference |

## Methodology
- Survey of persistence semantics across frameworks
- BEAM benchmark evaluation
- arXiv:2604.11364
