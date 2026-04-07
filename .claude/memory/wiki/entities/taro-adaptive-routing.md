---
name: TARo (Token-level Adaptive Routing)
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mom-taro-research]
tags: [orchestration, routing, cost-optimization]
---

# TARo (Token-level Adaptive Routing)

> Rai et al. (arXiv:2603.18411) — adaptivní per-token routing překonává fixní interpolaci; router trénovaný na malých modelech funguje na velkých bez retrainingu (weak-to-strong transfer).

## Key Facts

- +8.4% na MATH500 vs. fixní interpolaci (ref: sources/mom-taro-research.md)
- Weak-to-strong transfer: router trénovaný na 3B/8B funguje na 14B/70B bez retrainingu
- Naučí se abstraktní vlastnosti problému (complexity, domain), ne model-specific artefakty
- Potvrzeno across architecture families
- Trénink na 1K vzorcích — velmi sample-efficient

## Relevance to STOPA

Přímo aplikovatelné na STOPA: místo fixed light/standard/deep tier při startu tasku → per-subtask heuristic router. Slibný pattern: haiku-first difficulty estimation (spusť přes haiku, pokud uspěje s confidence → keep, jinak eskaluj na sonnet/opus).

## Mentioned In

- [MoM + TARo Research Brief](../sources/mom-taro-research.md)
