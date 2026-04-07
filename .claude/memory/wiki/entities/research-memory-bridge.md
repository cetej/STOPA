---
name: Research-Memory Bridge
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [second-brain-gap-analysis]
tags: [memory, research, orchestration, knowledge-management]
---

# Research-Memory Bridge

> Automatické propojení mezi `/deepresearch` výstupy a memory grafem — hook na konci deepresearch workflow spustí ingest pipeline, čímž každý research report automaticky obohacuje knowledge graf.

## Key Facts

- Problém: `/compile` pracuje jen s `learnings/`, ne s `outputs/` — research výstupy jsou izolované (ref: sources/second-brain-gap-analysis.md)
- Úroveň A (automatická): hook po `/deepresearch` → ingest pipeline → 3-5 learnings, entity pages, concept-graph update, source page (ref: sources/second-brain-gap-analysis.md)
- Úroveň B (periodická syntéza): nová fáze v `/compile` — skenuje `outputs/`, clusteruje podle tématu, generuje synthesis pages (ref: sources/second-brain-gap-analysis.md)
- Compounding efekt: Research N staví na extrahovaných entitách z Research 1..N-1 — retrieval je lepší (ref: sources/second-brain-gap-analysis.md)
- Effort Úroveň A: modifikace `/deepresearch` (~50 řádků) + závislost na `/ingest` (ref: sources/second-brain-gap-analysis.md)
- Effort Úroveň B: nová fáze v `/compile` (~150 řádků) (ref: sources/second-brain-gap-analysis.md)
- Backfill cíl: 30+/60 existujících outputs propojit s memory grafem (50%+) (ref: sources/second-brain-gap-analysis.md)

## Relevance to STOPA

Fáze 2 implementačního plánu (po `/ingest`). Nejvyšší compounding hodnota — každý nový research automaticky staví na předchozích a přispívá do sdíleného grafu.

## Mentioned In

- [Second Brain Gap Analysis](../sources/second-brain-gap-analysis.md)
