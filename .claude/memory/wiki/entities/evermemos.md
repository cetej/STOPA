---
name: EverMemOS
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [idea-file-research]
tags: [memory, orchestration, research]
---

# EverMemOS

> SOTA systém na LoCoMo benchmarku pro dlouhodobou agentní paměť implementující 3-fázový lifecycle: Ingest (MemCells) → Consolidate → Reflect.

## Key Facts

- arXiv:2601.02163 (ref: sources/idea-file-research.md)
- 3-fázový memory lifecycle: Ingest (atomické MemCells) → Consolidate (asynchronní syntéza) → Reflect (cross-temporal pattern detection) (ref: sources/idea-file-research.md)
- SOTA na LoCoMo benchmarku pro long-context memory (ref: sources/idea-file-research.md)
- Fáze 3 (Reflect) je nejméně implementovaná napříč ekosystémem — žádná open-source implementace s verifikovatelným cross-temporal pattern detection nebyla nalezena (ref: sources/idea-file-research.md)

## Relevance to STOPA

Přímá inspirace pro STOPA memory architecture upgrade. STOPA implementuje fáze 1 (ingest do learnings/) a fáze 2 (/compile pro consolidaci), ale fáze 3 (reflection/cross-temporal pattern detection) chybí. EverMemOS MemCells pattern odpovídá STOPA learnings/ individual YAML files.

## Mentioned In

- [Idea File Research](../sources/idea-file-research.md)
