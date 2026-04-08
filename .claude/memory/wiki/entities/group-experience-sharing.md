---
name: Group Experience Sharing
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [group-evolving-agents-gea]
tags: [orchestration, multi-agent, memory, evolution]
---

# Group Experience Sharing

> Mechanismus v GEA kde každý agent přistupuje k agregovaným evolučním trasám groupmates (code patches, execution logs, failure outcomes) — brání ztrátě cenných objevů v izolovaných větvích.

## Key Facts

- Bez sdílení: beneficiální objevy v izolovaných větvích zanikají při prořezávání evolučního stromu (ref: sources/group-evolving-agents-gea.md)
- Se sdílením: GEA integruje tools ze 17 vs 9 ancestor agentů — ~2× diverzita toolsetů (ref: sources/group-evolving-agents-gea.md)
- Sdílí se: applied code patches, execution logs, failure outcomes — vše co tvoří evoluční trajektorii (ref: sources/group-evolving-agents-gea.md)
- Analogie k STOPA: learnings/ directory + RCL outcomes/ jsou statické sdílení; GEA dělá totéž dynamicky během evoluce (ref: sources/group-evolving-agents-gea.md)

## Relevance to STOPA

Validuje design learnings/ + outcomes/ jako sdílené paměti, ale odhaluje gap: STOPA agenti v jedné session nesdílí mezivýsledky dynamicky. `/orchestrate` farm tier by mohl implementovat shared workspace (findings ledger) pro group experience sharing.

## Mentioned In

- [GEA: Group-Evolving Agents](../sources/group-evolving-agents-gea.md)
