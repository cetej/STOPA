---
title: "Second Brain Gap Analysis — STOPA Knowledge Compounding"
slug: second-brain-gap-analysis
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 6
claims_extracted: 4
---

# Second Brain Gap Analysis — STOPA Knowledge Compounding

> **TL;DR**: Analýza tří mezer v STOPA knowledge systému inspirovaná Karpathy/Spisak Second Brain vzorem. Klíčová zjištění: 60 research výstupů (~900 KB) leží mimo memory graf jako mrtvá data. Řešení: `/ingest` skill (Gap 1), Research→Memory Bridge (Gap 2), Knowledge Graph Visualization (Gap 3). Celková prioritizace: Gap 1 → Gap 2 → Backfill → Vizualizace.

## Key Claims

1. 60 research reportů × ~15 KB = ~900 KB nevyužitých znalostí mimo memory graf — STOPA je nikdy nekonzultuje, neindexuje, nepropojuje — `[verified]` (měřitelný stav systému)
2. Ingest pipeline ve 4 fázích (Normalize → Extract → Cross-Reference → Store) s Haiku sub-agentem pro extrakci umožní každý nový zdroj automaticky obohacovat knowledge graf za ~$0.02 per source — `[argued]`
3. Research→Memory Bridge na konci `/deepresearch` workflow (auto-ingest výstupu) způsobí compounding efekt: každý nový research staví na extrahovaných poznatcích z předchozích — `[argued]`
4. concept-graph.json (547 KB) je silný datový zdroj bez vizualizace — interaktivní HTML graf (D3.js/Cytoscape) nebo Mermaid fallback v `/compile` umožní procházení znalostní báze — `[asserted]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Ingest Pipeline (/ingest skill) | concept | new |
| Research-Memory Bridge | concept | new |
| Knowledge Graph Visualization | concept | new |
| Karpathy Wiki Pattern | concept | existing |
| D3.js | tool | new |
| Obsidian | tool | new |

## Relations

- Ingest Pipeline `feeds` Research-Memory Bridge
- Research-Memory Bridge `extends` deepresearch skill
- Knowledge Graph Visualization `renders` concept-graph.json
- Ingest Pipeline `implements` Karpathy Wiki Pattern
- D3.js `enables` Knowledge Graph Visualization
