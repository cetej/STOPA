---
name: Path-Addressable State
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [nlah-implementation-plan]
tags: [memory, session, orchestration]
---

# Path-Addressable State

> Požadavek na strukturu paměťových artefaktů: externalized (na disku), path-addressable (konkrétní objekt adresovatelný přes cestu), compaction-stable (přežívá truncation). Druhý nejsilnější modul NLAH.

## Key Facts

- NLAH modul: +5.5% na OSWorld (computer-use), +1.6% na SWE-bench (ref: sources/nlah-implementation-plan.md)
- Tři požadavky: Externalized / Path-addressable / Compaction-stable (ref: sources/nlah-implementation-plan.md)
- STOPA stav: Externalized=A (`.claude/memory/` na disku), Path-addressable=C+ (learnings ano, state/checkpoint ne), Compaction-stable=A (ref: sources/nlah-implementation-plan.md)
- Navrhovaná oprava: structured state.md s anchor IDs (`active_task.subtasks[].id: st-1`) → odkaz `state.md#st-2` (ref: sources/nlah-implementation-plan.md)
- Structured checkpoint.md: YAML s `task_ref: state.md#task-nlah-impl`, `context.completed: [st-1, st-3]` místo prózy (ref: sources/nlah-implementation-plan.md)
- Auto-checkpoint hook (30 min interval nebo context >70%) jako P3 doplněk (ref: sources/nlah-implementation-plan.md)

## Relevance to STOPA

P1 priorita (2×3h = 6h total). Základ pro path-based agent handoffs a strojové parsování sessionů. Bez toho je každý "resume" závislý na LLM porozumění prózy místo přímého adresování.

## Mentioned In

- [NLAH Implementation Plan](../sources/nlah-implementation-plan.md)
