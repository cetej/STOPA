---
name: Ingest Pipeline
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [second-brain-gap-analysis]
tags: [memory, knowledge-management, orchestration, research]
---

# Ingest Pipeline

> 4-fázový proces zpracování externích zdrojů do strukturovaných memory artefaktů: Normalize → Extract → Cross-Reference → Store. Implementováno jako `/ingest` skill.

## Key Facts

- Motivace: 60 research výstupů (~900 KB) v `outputs/` leží mimo memory graf — systém je nikdy nekonzultuje (ref: sources/second-brain-gap-analysis.md)
- Fáze 1 Normalize: URL → `/fetch`, soubor → Read, research output → `outputs/*.md` (ref: sources/second-brain-gap-analysis.md)
- Fáze 2 Extract (Haiku sub-agent): entity extraction, claim extraction (s evidence level), relation extraction — max 15 entit, 10 claims, 10 relací per zdroj (ref: sources/second-brain-gap-analysis.md)
- Fáze 3 Cross-Reference: grep existujících learnings/wiki, detekce nová/update/kontradikce, aktualizace concept-graph.json (ref: sources/second-brain-gap-analysis.md)
- Fáze 4 Store: source summary → `wiki/sources/`, entity pages → `wiki/entities/`, learnings → `learnings/` (přes salience gate) (ref: sources/second-brain-gap-analysis.md)
- Token cost: ~$0.02 per source (Haiku extraction), amortizuje se přes lepší retrieval (ref: sources/second-brain-gap-analysis.md)
- Auto-trigger po `/deepresearch` (opt-out `--no-ingest`); backfill existujících outputs jako batch session (ref: sources/second-brain-gap-analysis.md)

## Relevance to STOPA

Základ pro knowledge compounding. Bez ingest pipeline knowledge systém roste jen z learnings/ (manuální zápis), ne z research výstupů. Fáze 1 implementačního plánu.

## Mentioned In

- [Second Brain Gap Analysis](../sources/second-brain-gap-analysis.md)
