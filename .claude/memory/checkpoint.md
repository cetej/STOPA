# Session Checkpoint

**Saved**: 2026-03-20 (Session 4 — final)
**Task**: Czech Language Corrector — ALL SESSIONS COMPLETE
**Branch**: main (pushed)
**Status**: Fully integrated, tested on 3 real articles

## Complete Feature Map

### Variant A (Prompt Quick Wins) — Sessions 1-2
- **A1**: Czech guardrails in Phase 1 master prompt (`00_MASTER_v42.2.5.md`)
- **A2**: Czech quality section in Phase 7 SEO prompt (`claude_processor.py:~5099`)
- **A3**: CorrectorRulesDB — 222 rules in 7 SQLite tables (`corrector_rules.db`)
- **A4**: Rules injection into Phase 5 prompt (`format_corrector_rules_for_prompt()`)

### Variant B (Hybrid Corrector) — Sessions 3-4
- **B1**: CzechCorrector package — 6 modules in `ngm_terminology/corrector/`
- **B2**: Dependencies — MorphoDiTa v1.11.3, pyspellchecker v0.9.0, LINDAT Korektor API
- **B3**: Protected terms bridge — `get_protected_terms(chain_db, domains)` → `set[str]`
- **B4**: NG-ROBOT Phase 4.5 — post-Phase 4 hook in `document_processor.py`
- **B5**: ADOBE-AUTOMAT — typography auto-fix in `backend/routers/translate.py`

### Fixes (Session 4 bonus)
- Typography: global protection for PMID, DOI, ISBN, URL, version numbers
- False friends: Czech homonym whitelist (list, host, most...), short word exact-match only
- git init terminology-db (local, no GitHub remote yet)

## E2E Test Results (3 articles)

| Article | Chars | Typo fixes | Suggestions | Phase 4.5 time | Pipeline cost |
|---------|-------|-----------|-------------|----------------|---------------|
| Humans Americas | 16,197 | 21 | 0 | 1.9s | $1.83 |
| Žraloci býčí | 14,949 | 7 | 3 | 1.8s | $1.20 |
| Fyzika deště | 13,463 | 2 | 1 | 1.8s | $1.15 |

Phase 4.5: $0 cost, ~1.8s, 100% precision on typography.

## Remaining Work

| # | Item | Priority | Effort |
|---|------|----------|--------|
| 1 | GitHub remote pro terminology-db | low | trivial |
| 2 | Spelling check — LINDAT Korektor caching | low | medium |
| 3 | Měření dopadu Phase 4.5 na Phase 5 output tokeny | medium | medium |
| 4 | Rozšíření CorrectorRulesDB z reálných chyb | ongoing | low |
| 5 | Variant C (UDPipe, Stanza, GECCC) | future | high |

## Key Paths

- Corrector package: `terminology-db/ngm_terminology/corrector/` (6 modules)
- CorrectorRulesDB: `terminology-db/ngm_terminology/corrector_rules.db`
- MorphoDiTa model: `terminology-db/models/czech-morfflex2.0-pdtc1.0-220710/`
- NG-ROBOT integration: `NG-ROBOT/document_processor.py` (_run_czech_corrector, _format_corrector_suggestions)
- ADOBE-AUTOMAT integration: `ADOBE-AUTOMAT/backend/routers/translate.py`
- Phase 1 prompt: `NG-ROBOT/projects/1-PREKLAD-FORMAT/00_MASTER_v42.2.5.md`
- Phase 5 KB: `NG-ROBOT/projects/5-JAZYK-KONTEXT/`
- Phase 7 prompt: `NG-ROBOT/claude_processor.py` SEOMetadataGenerator section

## Resume Prompt

> Czech Language Corrector je kompletní (Sessions 1-4). Variant A (prompt quick wins) + Variant B (hybrid MorphoDiTa corrector) integrovaný v NG-ROBOT (Phase 4.5) i ADOBE-AUTOMAT.
>
> Další práce: viz "Remaining Work" v `STOPA/.claude/memory/checkpoint.md`.
> Klíčové repozitáře: terminology-db (lokální git), NG-ROBOT + ADOBE-AUTOMAT + STOPA (GitHub pushed).
