# Council Verdict: Memory Architecture — Flat-file vs Vector DB

**Date**: 2026-04-01
**Method**: /council skill (5 advisors × haiku, 3 judges × sonnet, chairman synthesis)
**Question**: Should STOPA migrate from flat-file markdown memory to LanceDB vector database?

## Verdict: NEMIGROVAT

Unanimni konsenzus 5/5 advisors. Při 22-38 learnings je vector DB premature over-engineering.

## Pro migrace na LanceDB

| Výhoda | Kdy začne hrát roli | Reálnost |
|--------|---------------------|----------|
| Sémantické vyhledávání (fuzzy match) | 200+ learnings, synonym fallback nestačí | Nízká |
| Automatické shlukování souvisejících learnings | 500+ learnings | Střední |
| Cross-project memory search | Sdílená knowledge base | Střední |
| Sémantická deduplikace | Hodně duplicitních learnings | Nízká |

## Proti migraci

| Riziko | Dopad | Důkaz |
|--------|-------|-------|
| Scale mismatch — 22 learnings, grep 22ms | Nulový perf. gain | Měřeno |
| Ztráta git auditability — binary DB | Nelze diffnout memory změny | Git blame/log funguje na .md |
| Plugin distribuce se rozbije | Sync do NG-ROBOT přestane fungovat | Binary soubor nelze mergovat |
| Přepisování hooků (3-5 Python) | 2-4 týdny práce bez feature value | YAML frontmatter → DB queries |
| Embedding API dependency | Recurring cost + failure mode | Silent degradation |
| Silent failure mode vector search | Confidently wrong výsledky | Grep je binární (match/no match) |

## Náklady

| Položka | Markdown (status quo) | LanceDB migrace |
|---------|----------------------|-----------------|
| Infrastruktura | 0 | LanceDB + embedding model |
| API tokeny | 0 | ~100-500 tokenů/learning |
| Migrace hooků | 0 | 2-4 týdny |
| Distribuce | git sync | Nový mechanismus |
| Údržba | Archive rotation 30 min/m | Schema migration, index rebuild |
| Debug/audit | grep + cat | Specializované query |
| Windows | Bezproblémová | File locking, antivirus |

## Upgrade Path

| Fáze | Trigger | Akce | Effort |
|------|---------|------|--------|
| Teď | — | Automatizovat synonym fallback | 2h |
| Teď | — | Confidence decay + graduation triggers | 4h |
| Q3 2026 | 100+ learnings | SQLite FTS5 index jako shim | 1 den |
| Q4 2026 | 500+ learnings / 500ms grep / 20% miss rate | Zvážit LanceDB | 2-4 týdny |

## Council Leaderboard

| Rank | Persona | Avg Position | Top-2 | Confidence |
|------|---------|-------------|-------|------------|
| 1 | Data-Driven | 1.0 | 3/3 | 4 |
| 2 | Architect | 2.0 | 3/3 | 4 |
| 3 | User Advocate | 3.3 | 0/3 | 3 |
| 4 | Pragmatist | 3.7 | 0/3 | 4 |
| 5 | Skeptic | 5.0 | 0/3 | 2 |

## Dissent

Advisory C (Skeptic) varoval před confirmation bias — všichni souhlasí, což může být varovný signál. Doporučil měřit retrieval miss rate.

## Klíčové napětí

- Migrační threshold: 200 vs 300 vs 500 learnings (2.5× spread)
- SQLite FTS5 jako mezikrok — podprozkoumaná střední cesta
