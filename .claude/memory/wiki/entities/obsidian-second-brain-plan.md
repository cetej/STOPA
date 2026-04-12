---
name: Obsidian Second Brain Plan
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [claude-obsidian-llm-wiki-tutorial]
tags: [knowledge-management, memory, planning]
---

# Obsidian Second Brain Plan

> Plán integrace Obsidian s STOPA knowledge systémem. Uživatel se kloní k variantě D (separátní personal vault). Odloženo — zatím bez termínu.

## Analyzované varianty

| Varianta | Popis | Verdict |
|----------|-------|---------|
| A: Viewer na STOPA | Obsidian otevře `.claude/memory/wiki/` přímo | Rychlé, ale graph view nefunguje bez `[[wiki links]]` |
| B: Export skript | Periodický `export-to-obsidian.py` s konverzí na Obsidian formát | Nejlepší poměr effort/hodnota pro vizualizaci STOPA |
| C: Plný Karpathy Wiki | Nový vault = primární KB, STOPA sekundární | Nedoporučeno — split brain, STOPA už je Karpathy implementace |
| **D: Personal second brain** | **Separátní vault pro osobní/non-tech (knihy, zdraví, cíle)** | **Preferovaná varianta uživatele** |

## Varianta D — detail

- Obsidian vault pro osobní témata (ne STOPA/tech)
- STOPA = work/tech, Obsidian = personal
- Karpathy pattern čistě pro jednu doménu
- Effort: ~3-4h setup (vault, CLAUDE.md schema, první ingest)
- Prereq: mít osobní zdroje k naplnění (knihy, journal, podcasts)

## Status

**ODLOŽENO** — uživatel chce implementovat později. Při aktivaci: začít variantou D.
