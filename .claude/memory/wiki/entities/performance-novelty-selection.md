---
name: Performance-Novelty Selection
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [group-evolving-agents-gea]
tags: [orchestration, multi-agent, evolution, exploration]
---

# Performance-Novelty Selection

> Kritérium pro výběr parent agentů v GEA kombinující task success rate s diversitou přes cosine distance: score(i) = αᵢ · √nov(i).

## Key Facts

- Vzorec: `score(i) = αᵢ · √nov(i)` — výkon je primární (αᵢ), novita poskytuje mírné explorační zkreslení (ref: sources/group-evolving-agents-gea.md)
- Novita měřena cosine distance od ostatních kandidátů — brání konvergenci k jediné evoluční větvi (ref: sources/group-evolving-agents-gea.md)
- Odmocnina u nov(i) záměrně snižuje váhu diversity — exploitace dominuje, explorace je ochranný mechanismus (ref: sources/group-evolving-agents-gea.md)

## Relevance to STOPA

Kandidát na rozšíření UCB1 selektoru v ASI-Evolve integraci (viz `reference_asi_evolve.md` v auto-memory). UCB1 řeší exploration/exploitation trade-off globálně; Performance-Novelty řeší totéž na úrovni agent identity/diversity.

## Mentioned In

- [GEA: Group-Evolving Agents](../sources/group-evolving-agents-gea.md)
