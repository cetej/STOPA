---
name: Czech Language Corrector Plan
description: Czech grammar/style corrector — Sessions 1-3 done. Variant A complete (Phase 1+5+7 guardrails, 222-rule SQLite DB). Variant B skeleton done (CzechCorrector with MorphoDiTa, Korektor API, typography). Next: Session 4 (integration).
type: project
---

# Czech Language Corrector — Progress

**Started**: 2026-03-20
**Status**: Sessions 1-3 complete, Session 4 pending
**Approach**: Variant A (quick wins) → Variant B (hybrid corrector)
**Full plan**: `STOPA/.claude/memory/czech_corrector_plan.md`

## Completed

### Variant A (all 4 tasks)
- **A1**: Czech guardrails in Phase 1 master prompt (`00_MASTER_v42.2.5.md`)
- **A2**: Czech quality section in Phase 7 SEO prompt (`claude_processor.py`)
- **A3**: CorrectorRulesDB — 222 rules in 7 SQLite tables (`corrector_rules.db`)
- **A4**: `format_corrector_rules_for_prompt()` wired into Phase 5

### Variant B skeleton
- **Dependencies**: ufal.morphodita + pyspellchecker installed
- **MorphoDiTa model**: czech-morfflex2.0-pdtc1.0-220710 downloaded (95 MB)
- **CzechCorrector package**: `ngm_terminology/corrector/` with 5 modules
  - morpho.py (lemmatization, POS, form generation)
  - spellcheck.py (LINDAT Korektor API + pyspellchecker fallback)
  - typography.py (deterministic: quotes, dashes, numbers, units, dates, prepositions)
  - corrector.py (main orchestrator, graceful degradation)
- **ngm-terminology v2.2.0**

## Pending (Session 4)
- B3: Protected terms bridge (TermDB → Corrector contract)
- B4: NG-ROBOT Phase 4.5 (new phase between FactChecker and LanguageContextOptimizer)
- B5: ADOBE-AUTOMAT correct_czech() after translate_batch()
- E2E test on real article

**Why:** Pipeline produces non-Czech expressions (anglicisms, calques, false friends) because Phase 1 had no Czech quality rules, and Phase 5 catches them too late with limited tools.

**How to apply:** When working on NG-ROBOT translation quality or ADOBE-AUTOMAT translation, reference this plan. CzechCorrector is in ngm-terminology package — import via `from ngm_terminology.corrector import CzechCorrector`.
