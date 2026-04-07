---
name: Cross-Level Critic
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [vertical-scaling-report, vertical-scaling-explained]
tags: [orchestration, review]
---
# Cross-Level Critic

> Rozšíření STOPA critic o validaci na třech úrovních — kontroluje nejen kód (mikro), ale i API kontrakty (mezo) a architektonickou konzistenci (makro).

## Key Facts

- Součást Fáze C vertikálního škálování (plánováno 2026-05-18)
- Tři úrovně kontroly: MIKRO (syntax, logic, edge cases), MEZO (contracts, deps, tests), MAKRO (ADR, arch, business rules)
- Level-tagged subtasks jsou prerekvizitou — critic potřebuje vědět, jaká úroveň se kontroluje
- Go/No-Go: nesmí způsobit false positives blokující práci (ref: sources/vertical-scaling-report.md)

## Relevance to STOPA

Rozšíří stávající /critic skill o cross-level awareness. Implementace závisí na úspěchu Fáze B (/telescope).

## Mentioned In

- [Vertikální škálování STOPA orchestrace — Technická zpráva](../sources/vertical-scaling-report.md)
- [Vertikální škálování orchestrace — Co to je a jak to funguje](../sources/vertical-scaling-explained.md)
