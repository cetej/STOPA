---
title: "Vertikální škálování orchestrace — Co to je a jak to funguje"
slug: vertical-scaling-explained
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 5
claims_extracted: 3
---
# Vertikální škálování orchestrace — Co to je a jak to funguje

> **TL;DR**: Přístupné vysvětlení vertikálního škálování pro nontechnické čtenáře. Tři úrovně abstrakce (mikro/mezo/makro) řeší tři kategorie chyb: vertikální nekonzistence, mezo bottleneck a emergence. Analogie zedník-elektrikář-instalatér bez koordinace.

## Key Claims

1. Tři abstrakční úrovně (mikro/mezo/makro) umožňují zachytit různé kategorie chyb, které single-level agent nevidí — vertikální nekonzistence, mezo bottleneck, emergence — `[argued]`
2. Informace proudí nahoru jako summaries (mikro→mezo→makro) a dolů jako constraints (makro→mezo→mikro) — bidirektionální tok je klíčový — `[argued]`
3. Fáze A (3-level scout) nezpůsobuje token overhead (+0%) — benefit je pouze kontextový, bez nákladů — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Vertical Scaling (orchestration) | concept | new |
| 3-Level Scout | concept | new (also in vertical-scaling-report) |
| Cross-Level Critic | concept | new |
| Mezo Bottleneck | concept | new |
| Level-Tagged Subtasks | concept | new |

## Relations

- Vertical Scaling `requires` 3-Level Scout
- Cross-Level Critic `validates` level-tagged subtasks
- Mezo Bottleneck `detected-by` 3-Level Scout
- Vertical Scaling `prevents` emergence problems
- Level-Tagged Subtasks `enable` Cross-Level Critic
