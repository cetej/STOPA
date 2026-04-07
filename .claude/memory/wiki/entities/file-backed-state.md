---
name: File-backed state module
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [nlah-research]
tags: [memory, orchestration, context-engineering]
---

# File-backed state module

> NLAH modul externalizující perzistentní stav přes soubory (externalized, path-addressable, compaction-stable) místo transient kontextu. +5.5% na OSWorld, nejsilnější modul pro computer-use tasks.

## Key Facts

- +5.5% na OSWorld, +1.6% na SWE-bench — nejsilnější single modul pro computer-use (ref: sources/nlah-research.md)
- Tři vlastnosti: Externalized (artefakty vs. transient kontext), Path-addressable (znovuotevření přes cestu), Compaction-stable (přežívá truncation a restart)
- Kanonická workspace struktura: TASK.md, SKILL.md, task_history.jsonl, artifacts/, children/
- Přímý ekvivalent STOPA .claude/memory/ systému

## Relevance to STOPA

Akademická validace STOPA memory/ systému. Potvrzuje, že file-backed state (state.md, checkpoint.md, memory/) je správný design. Path-addressable + compaction-stable properties jsou přesně důvod proč STOPA memory soubory fungují přes session restarts.

## Mentioned In

- [NLAH Research Brief](../sources/nlah-research.md)
