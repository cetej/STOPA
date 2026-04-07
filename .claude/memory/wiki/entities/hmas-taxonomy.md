---
name: HMAS Taxonomy
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [vertical-scaling-research]
tags: [multi-agent, orchestration, architecture, taxonomy]
---

# HMAS Taxonomy

> Hierarchical Multi-Agent Systems taxonomy defining 5 design axes; temporal layering (high-level planning vs low-level execution) is the key axis for vertical scaling.

## Key Facts

- Paper: arXiv:2508.12683 (ref: sources/vertical-scaling-research.md)
- 5 axes: Control hierarchy, Information flow, Role delegation, Temporal layering, Communication (ref: sources/vertical-scaling-research.md)
- Temporal layering: high-level agent on abstract state space (architecture, business intent) vs low-level on detailed actions (line edits, tests) (ref: sources/vertical-scaling-research.md)
- Hybrid architecture (hierarchical + decentralized) recommended as most scalable (ref: sources/vertical-scaling-research.md)

## Relevance to STOPA

Provides formal framework for STOPA's vertical scaling design. Temporal layering maps to micro/mezo/makro levels in /telescope skill. STOPA currently = hybrid (orchestrator controls, worker has autonomy).

## Mentioned In

- [Vertikální škálování Research](../sources/vertical-scaling-research.md)
