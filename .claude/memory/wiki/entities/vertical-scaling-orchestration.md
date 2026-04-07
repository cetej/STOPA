---
name: Vertical Scaling (Orchestration)
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [vertical-scaling-report, vertical-scaling-explained]
tags: [orchestration, planning]
---
# Vertical Scaling (Orchestration)

> Rozšíření STOPA orchestrace o tři abstrakční úrovně (mikro/mezo/makro) — agenti vidí kontext nad i pod sebou, což zabraňuje vertikální nekonzistenci, mezo bottleneck a emergence problémům.

## Key Facts

- Tři úrovně: Mikro (řádky, funkce), Mezo (API kontrakty, moduly), Makro (architektura, ADR, business rules)
- Informace proudí nahoru jako summaries, dolů jako constraints
- Fáze A (teď): 3-level scout output, +0% tokeny
- Fáze B (2026-04-21): /telescope skill, +10-20% tokeny
- Fáze C (2026-05-18): plná integrace, +25-40% tokeny
- Break-even: 1 z 8 úkolů s cross-level problémem → vyplatí se finančně ($1.55 úspora)
- Tři typy zachycených problémů: vertikální nekonzistence, mezo bottleneck, emergence (ref: sources/vertical-scaling-report.md, sources/vertical-scaling-explained.md)

## Relevance to STOPA

Klíčový roadmap item pro Q2 2026. Fáze A implementována v aktuální session. Scheduled reminders pro Fáze B (2026-04-21) a C (2026-05-18) existují.

## Mentioned In

- [Vertikální škálování STOPA orchestrace — Technická zpráva](../sources/vertical-scaling-report.md)
- [Vertikální škálování orchestrace — Co to je a jak to funguje](../sources/vertical-scaling-explained.md)
