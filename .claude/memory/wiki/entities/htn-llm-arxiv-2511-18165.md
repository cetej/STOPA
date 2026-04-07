---
name: HTN+LLM (arXiv:2511.18165)
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [vertical-scaling-report]
tags: [orchestration, planning]
---
# HTN+LLM (arXiv:2511.18165)

> Paper o hybridním HTN (Hierarchical Task Network) plánování s LLM — čistě LLM hierarchické plánování má 1% syntaktickou validitu, hybridní enforcement je nutný.

## Key Facts

- arXiv: 2511.18165
- Klíčový finding: čistě LLM hierarchické plánování = 1% syntaktická validita
- Závěr: hybridní enforcement (HTN constraints + LLM flexibility) je nutný pro spolehlivé hierarchické plánování (ref: sources/vertical-scaling-report.md)
- Relevantní pro Fázi C STOPA vertikálního škálování

## Relevance to STOPA

Validuje nutnost strukturovaných constraints ve vertikálním škálování — samotný LLM bez enforcement pravidel na hierarchii nestačí. Fáze C musí zahrnout hybridní enforcement mechanismus.

## Mentioned In

- [Vertikální škálování STOPA orchestrace — Technická zpráva](../sources/vertical-scaling-report.md)
