# Session Checkpoint

**Saved**: 2026-03-20 (afternoon session)
**Task**: BioLib terminology audit + NG-ROBOT & ADOBE-AUTOMAT integration
**Branch**: main
**Progress**: 4/4 tasks complete

## What Was Done This Session

1. **BioLib termdb.db audit** — 244,887 termínů v 6 doménách (biology 218K, geography 19.7K, chemistry 4K, medicine 2.8K, astronomy 126, geology 68). Schema mismatch identifikován — flat vs normalized.

2. **ngm-terminology v2.0.0** — Nové moduly:
   - `normalized_db.py` — NormalizedTermDB (read-only, normalizované schema)
   - `chain.py` — ChainTermDB (řetězí více DB, zápis do flat)
   - `config.py` — `find_multi_domain_db()` pro BIOLIB/termdb.db
   - Zpětně kompatibilní — starý TermDB beze změn

3. **NG-ROBOT integrace** — `claude_processor.py`:
   - `_multi_db` + `_chain_db` inicializace (246K+ termínů celkem)
   - `detect_article_domains()` — mapuje témata z 0_analysis.json na termdb domény
   - `format_termdb_for_prompt(article_domains=...)` — injektuje doménově relevantní termíny + preferované kategorie
   - Upraveno v `auto_agent.py` i `ngrobot.py`

4. **ADOBE-AUTOMAT integrace** — `translation_service.py`:
   - `_build_term_hints()` — batch-překládá EN texty z elementů přes NormalizedTermDB
   - Inject glosáře do system promptu před překladem
   - E2E test: Alps→Alpy, Mediterranean Sea→Středozemní moře, calcium→vápník

## What Remains (for next session)

| # | Item | Priority | Effort | Notes |
|---|------|----------|--------|-------|
| 1 | Autoloop Fáze 3 implementation | high | high | Build referenční dataset, composite score, autoloop na TermVerifier |
| 2 | git commit + push all 3 projects | medium | trivial | STOPA (uncommitted), NG-ROBOT, ADOBE-AUTOMAT, terminology-db |
| 3 | termdb.db empty domains | low | medium | physics + idioms importers, geology needs more terms |
| 4 | NG-ROBOT: chain_db pro translate i v batch | low | low | batch_translate na ChainTermDB pro species pre-resolve |

## Key Context

- ngm-terminology v2.0.0 editable install v `C:\Users\stock\Documents\000_NGM\terminology-db\`
- BIOLIB/termdb.db: 244K termínů, normalizované schema (terms→translations→aliases→sources)
- NG-ROBOT/terminology.db: 1665 termínů, flat schema (en/cz/lat)
- ChainTermDB řetězí obě — dotaz na obě, zápis do flat
- ADOBE-AUTOMAT: glosář auto-inject do Claude překladového promptu

## Git State

- Branch: main
- Uncommitted changes in: terminology-db, NG-ROBOT, ADOBE-AUTOMAT
- STOPA: clean (changes only in memory/checkpoint)

## Resume Prompt

> Resume work on STOPA / NG-ROBOT. Read: `CLAUDE.md`, `.claude/memory/checkpoint.md`.
>
> Previous session: ngm-terminology v2.0.0 (NormalizedTermDB + ChainTermDB), integrated 244K+ terms into NG-ROBOT (detect_article_domains + format_termdb_for_prompt) and ADOBE-AUTOMAT (batch term hints in translation_service.py).
>
> Remaining: **Autoloop Fáze 3** — build referenční dataset, composite quality score for TermVerifier. Work in NG-ROBOT context (`C:\Users\stock\Documents\000_NGM\NG-ROBOT`), TermVerifier at `claude_processor.py:2621`.
