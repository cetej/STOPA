# Session Checkpoint

**Saved**: 2026-03-20 (late evening session)
**Task**: Czech Language Corrector — Sessions 2+3 complete
**Branch**: main
**Progress**: 7/8 tasks complete (Variant A done, Variant B skeleton done)

## What Was Done This Session

### Session 2: A2 + A4 (Variant A complete)

5. **A2: Phase 7 Czech quality** — Added `🇨🇿 KVALITA ČEŠTINY` section to SEOMetadataGenerator prompt (`claude_processor.py:5099`). Covers anglicisms, typography, word order, FAQ-specific rules. Applies to all generated texts (titles, PEREX, V KOSTCE, FAQ, alt texts, meta description).

6. **A4: Corrector rules in Phase 5** — Three changes to `claude_processor.py`:
   - Import `CorrectorRulesDB` with graceful fallback (`CORRECTOR_AVAILABLE` flag)
   - New function `format_corrector_rules_for_prompt()` (~line 1247) — follows `format_termdb_for_prompt()` pattern
   - Phase 5 `check_language_and_context()` auto-appends 222 rules from DB after knowledge base
   - Output: ~1639 chars of structured markdown tables

### Session 3: Variant B prototype (CzechCorrector)

7. **Dependencies installed** — `ufal.morphodita` v1.11.3, `pyspellchecker` v0.9.0
8. **MorphoDiTa model downloaded** — czech-morfflex2.0-pdtc1.0-220710 (95 MB) from LINDAT to `terminology-db/models/`
9. **CzechCorrector package** — `ngm_terminology/corrector/` with 5 modules:
   - `__init__.py` — exports CzechCorrector, CorrectionResult
   - `corrector.py` — main orchestrator class (graceful degradation per component)
   - `morpho.py` — MorphoDiTa wrapper (lemmatize, tag_text, get_forms, auto-discovery of model)
   - `spellcheck.py` — LINDAT Korektor REST API (primary) + pyspellchecker fallback
   - `typography.py` — deterministic fixes (quotes, dashes, numbers, units, dates, prepositions)
10. **Version bumped** to v2.2.0

### Test Results
- Typography: 6/6 auto-fixes on realistic text (quotes, dashes, numbers, units, %, dates)
- Anglicism detection: 3/3 (implementovat, fokusovat, signifikantní)
- False friend detection: 2/2 (aktuální, aktuálně)
- MorphoDiTa: lemmatization + POS tagging + form generation all working

## What Remains

| # | Item | Priority | Effort | Notes |
|---|------|----------|--------|-------|
| 1 | B3: Protected terms bridge | medium | low | get_protected_terms(chain_db, domains) → terms corrector must not modify |
| 2 | B4: NG-ROBOT Phase 4.5 integration | medium | medium | New phase between FactChecker and LanguageContextOptimizer |
| 3 | B5: ADOBE-AUTOMAT integration | low | low | correct_czech() call after translate_batch() |
| 4 | E2E test on real article | medium | low | Run full pipeline on sample article |
| 5 | git init terminology-db | low | trivial | Not a git repo yet |

## Key Context

- ngm-terminology v2.2.0 with CzechCorrector (MorphoDiTa + Korektor + CorrectorRulesDB)
- Corrector package: `terminology-db/ngm_terminology/corrector/`
- MorphoDiTa model: `terminology-db/models/czech-morfflex2.0-pdtc1.0-220710/`
- CorrectorRulesDB: `terminology-db/ngm_terminology/corrector_rules.db` (222 rules, 7 tables)
- Phase 5 + Phase 7 in NG-ROBOT updated with Czech quality rules
- pyspellchecker has NO Czech dictionary — using LINDAT Korektor REST API instead
- terminology-db has NO git repo

## Resume Prompt

> Resume work on Czech Language Corrector. Read: `STOPA/.claude/memory/czech_corrector_plan.md`, `STOPA/.claude/memory/checkpoint.md`.
>
> Sessions 1-3 complete. Variant A (all 4 tasks) + Variant B skeleton done. Next: **Session 4 — integration**: Protected terms bridge, NG-ROBOT Phase 4.5, ADOBE-AUTOMAT integration, E2E test.
>
> Work in: terminology-db (`C:\Users\stock\Documents\000_NGM\terminology-db`) for the module, NG-ROBOT (`C:\Users\stock\Documents\000_NGM\NG-ROBOT`) for integration, ADOBE-AUTOMAT (`C:\Users\stock\Documents\000_NGM\ADOBE-AUTOMAT`) for translate integration.
