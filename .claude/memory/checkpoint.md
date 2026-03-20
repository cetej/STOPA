# Session Checkpoint

**Saved**: 2026-03-20 (late evening, Session 4)
**Task**: Czech Language Corrector — Sessions 1-4 complete
**Branch**: main
**Progress**: ALL TASKS COMPLETE (Variant A + Variant B + Integration)

## What Was Done — Session 4: Integration

11. **B3: Protected terms bridge** — `ngm_terminology/corrector/protected_terms.py`
   - `get_protected_terms(chain_db, domains, max_per_domain)` → `set[str]`
   - Reads from TermDB (flat), NormalizedTermDB (multi-domain), SpeciesDB
   - Filters: max 5 words per term, lowercase, splits multi-word terms
   - E2E: 5444 terms total, 500 geography, 1709 biology

12. **B4: NG-ROBOT Phase 4.5** — `document_processor.py`
   - Import CzechCorrector + ChainTermDB with graceful fallback (`CZECH_CORRECTOR_AVAILABLE`)
   - Post-Phase 4 hook: runs `_run_czech_corrector()` after FactChecker
   - Auto-applies typography fixes to `current_content`
   - Stores suggestions (anglicisms, false friends) in `_corrector_suggestions`
   - Injects suggestions into Phase 5 via `_format_corrector_suggestions()` as extra context
   - Saves `4.5_czech_corrector.md` output file

13. **B5: ADOBE-AUTOMAT** — `backend/routers/translate.py`
   - Import CzechCorrector with graceful fallback
   - Typography auto-fix loop on each `elem.czech` after translate_batch()
   - Returns `typo_corrected` count in response

14. **E2E test** — Real article (demence/káva, 14K chars)
   - 16 auto-fixes (typography: quotes, dashes, number spacing)
   - 3 suggestions (false friends: aktuální, aktuálně, list)
   - All 4 capabilities active (typography, spellcheck, morphology, rules_db)

## Complete Feature Summary

### Variant A (Prompt Quick Wins) — Sessions 1-2
- A1: Czech guardrails in Phase 1 master prompt
- A2: Czech quality section in Phase 7 SEO prompt
- A3: CorrectorRulesDB (222 rules, 7 tables in SQLite)
- A4: Rules injection into Phase 5 prompt

### Variant B (Hybrid Corrector) — Sessions 3-4
- B1: CzechCorrector package (5 modules + protected_terms)
- B2: Dependencies (MorphoDiTa, pyspellchecker, LINDAT Korektor API)
- B3: Protected terms bridge (TermDB → corrector)
- B4: NG-ROBOT Phase 4.5 integration
- B5: ADOBE-AUTOMAT integration
- E2E: Tested on real article

## Known Issues / Future Work

| # | Item | Priority | Notes |
|---|------|----------|-------|
| 1 | GitHub remote pro terminology-db | low | Jen lokální git, push na GitHub |
| 2 | Spelling check zapnutí | low | LINDAT Korektor API pomalé, potřebuje caching |
| 3 | Měření dopadu Phase 4.5 na Phase 5 output | medium | Zpracovat článek s/bez a porovnat tokeny |
| 4 | Rozšíření CorrectorRulesDB | ongoing | 222 pravidel = základ, přidávat z reálných chyb |
| 5 | Variant C (full NLP) | future | UDPipe, Stanza, GECCC corpus |

## Key Context

- ngm-terminology v2.2.0 with CzechCorrector
- Corrector package: `terminology-db/ngm_terminology/corrector/` (6 modules)
- Protected terms: `corrector/protected_terms.py` — bridge to TermDB
- NG-ROBOT: Phase 4.5 in `document_processor.py` (post-Phase 4 hook)
- ADOBE-AUTOMAT: Typography fix in `backend/routers/translate.py`
- MorphoDiTa model: `terminology-db/models/czech-morfflex2.0-pdtc1.0-220710/`
- CorrectorRulesDB: 222 rules in 7 tables
