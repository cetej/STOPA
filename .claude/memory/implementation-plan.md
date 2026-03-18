# Implementation Plan — Orchestration System v2

**Created**: 2026-03-18
**Updated**: 2026-03-18 (přesun do STOPA)
**Status**: ACTIVE

---

## Přehled

Plán dalšího rozvoje orchestračního systému. Pyramid Flow specifické úkoly odstraněny — tady jen univerzální vylepšení.

---

## Track A: Vylepšení skills

### A1. Agent Teams → /orchestrate Phase 4
- **Co**: Integrovat nativní Agent Teams pro paralelní subtasky
- **Effort**: medium
- **Status**: DONE (2026-03-18)
- **Výsledek**: Konkrétní rozhodovací strom (1/2-3/4+ subtasků), wave execution pattern, pravidla pro parallel agents

### A2. Analytics API → /budget
- **Co**: Reálné metriky nákladů místo odhadů
- **Effort**: medium
- **Status**: DONE (2026-03-18)
- **Výsledek**: Token estimation formula, `claude usage` CLI integration, calibration report format

### A3. Hook konfigurace
- **Co**: TaskCompleted → připomínka /scribe, SessionStart → checkpoint check
- **Effort**: small
- **Status**: DONE (2026-03-18)
- **Výsledek**: 3 hooks (checkpoint-check, scribe-reminder, memory-maintenance) + .claude/settings.json

### A4. Plugin System
- **Co**: Zabalit orchestraci jako Claude Code plugin pro snadnou distribuci
- **Effort**: medium
- **Status**: DONE (2026-03-18)
- **Výsledek**: `stopa-orchestration/` plugin s manifestem, 9 skills, 3 hooks, README
- **Instalace**: `claude --plugin-dir ./stopa-orchestration` nebo `/plugin install github.com/cetej/STOPA/stopa-orchestration`
- **Ref**: https://code.claude.com/docs/en/plugins

---

## Track B: Robustnost a škálování

### B1. Vylepšit context health heuristiku
- **Co**: Lepší detekce velkého kontextu (proxy metriky jsou křehké)
- **Effort**: medium
- **Status**: DONE (2026-03-18)
- **Výsledek**: Bodový scoring systém (7 signálů), 3 úrovně (healthy/yellow/red), pravidla pro notifikaci

### B2. Memory archivace
- **Co**: Implementovat scribe maintenance — deduplikace, archivace starých decisions
- **Effort**: small
- **Status**: DONE (2026-03-18)
- **Výsledek**: memory-maintenance.sh hook (100/500 line thresholds), archive files, rozšířená scribe maintenance procedura

### B3. Sync skript vylepšení
- **Co**: Podpora více cílových projektů, selektivní sync, auto-detect změn
- **Effort**: medium
- **Status**: DONE (2026-03-18)
- **Výsledek**: Multi-target sync, --all flag, --skills-only/--memory-only/--hooks-only, KNOWN_TARGETS seznam, sync_file helper

### B4. Skill self-improvement loop
- **Co**: skill-generator zapisuje LEARNINGS.md, ale ten se nevyhodnocuje systematicky
- **Effort**: medium
- **Status**: DONE (2026-03-18)
- **Výsledek**: "improve-all"/"audit" mód v skill-generator — scanuje skills, porovnává s learnings, generuje report, auto-fix low severity

---

## Navrhované pořadí

```
Fáze 1 — Quick wins:
  A3 (hooks)
  B2 (memory archivace)

Fáze 2 — Core improvements:
  A1 (Agent Teams) ← paralelně s A2
  A2 (Analytics API)
  B1 (context heuristika)

Fáze 3 — Distribuce:
  B3 (sync vylepšení)
  A4 (plugin system)
  B4 (self-improvement loop)
```
