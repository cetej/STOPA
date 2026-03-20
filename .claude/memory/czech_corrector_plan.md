---
name: Czech Corrector Implementation Plan
description: Architecture plan for Czech language corrector module — Variant A (quick win) → Variant B (hybrid corrector). Pipeline audit findings, available resources, integration points.
type: project
---

# Czech Language Corrector — Implementation Plan

**Created**: 2026-03-20
**Status**: approved, implementation started
**Approach**: Variant A (quick wins) → Variant B (hybrid corrector)

## Why: Identified Problems

### Pipeline weak points (NG-ROBOT)
1. **Phase 1 (Translation)** — Master prompt (703 lines) has ZERO Czech language rules. Only structural formatting (title lengths, slugs, hyperlinks). Main injection point for anglicisms, calques, false friends.
2. **Phase 2 (Completeness)** — Re-translates missing sections with same absence of Czech quality constraints.
3. **Phase 5 (LanguageContextOptimizer)** — Main quality gate but overloaded: 11 categories in single pass, Sonnet with thinking=OFF, effort=medium. KB = 7 markdown files (~345 lines total). No structured DB.
4. **Phase 7 (SEO)** — Generates new Czech text (FAQ, V KOSTCE) with NO post-correction.
5. **ArticleWriter** — Original Czech articles bypass Phase 5 entirely.
6. **Chunked articles** — Phase 1 chunks 2+ get condensed system prompt, further reducing quality.

### ADOBE-AUTOMAT
- `translation_service.py` SYSTEM_PROMPT hardcodes Czech typographic rules (exonyms, dates, quotes)
- No post-translation Czech quality check
- Typography rules duplicated between ADOBE-AUTOMAT and NG-ROBOT Phase 5

## Variant A: Quick Wins (this session + next)

### A1. Czech guardrails in Phase 1 translation prompt
- **File**: `NG-ROBOT/projects/1-PREKLAD-FORMAT/00_MASTER_v42.2.5.md`
- **Action**: Add a dedicated Czech language quality section covering:
  - Avoid anglicisms and calques (implementovat→zavést, fokusovat→soustředit)
  - Czech word order (verb-second tendency, adjective placement)
  - No nominalization chains (English pattern: "The implementation of the investigation...")
  - Czech quotes „", em-dashes –, non-breaking spaces before units
  - False friends list (top 30 from Phase 5 KB)
- **Impact**: Prevention > correction. Fixing at source is cheaper than fixing downstream.

### A2. Post-correction on Phase 7 (SEO texts)
- **File**: `NG-ROBOT/claude_processor.py` (SEOMetadataGenerator)
- **Action**: Add Czech quality instruction to SEO prompt (titles, FAQ, V KOSTCE must follow same Czech rules)
- **Impact**: Currently generated with no Czech quality guidance

### A3. Structured rules database (foundation for Variant B)
- **File**: `terminology-db/ngm_terminology/corrector_rules.db` (new SQLite)
- **Action**: Convert Phase 5's 7 markdown KB files into structured SQLite tables:
  - `false_friends` (en, wrong_cz, correct_cz, example)
  - `anglicisms` (en_pattern, cz_replacement, category)
  - `collocations` (wrong, correct, explanation)
  - `typography_rules` (pattern, replacement, context)
- **Impact**: Single source of truth for both NG-ROBOT and ADOBE-AUTOMAT

### A4. Feed rules DB into Phase 5 prompt
- **Action**: `format_corrector_rules_for_prompt()` — similar to `format_termdb_for_prompt()`
- **Impact**: Phase 5 gets structured, queryable data instead of raw markdown

## Variant B: Hybrid Corrector (next sessions)

### Architecture
```
ngm-terminology/
  ngm_terminology/
    corrector/
      __init__.py          # CzechCorrector class
      morpho.py            # MorphoDiTa wrapper (lemmatizace, POS tagging)
      spellcheck.py        # Hunspell + Korektor wrapper
      rules.py             # Rules DB access (SQLite from A3)
      typography.py        # Deterministic typography fixes
      style.py             # Anglicism/calque detection
      protected_terms.py   # Bridge to TermDB ("don't touch these terms")
```

### Dependencies
```
pip install ufal.morphodita   # ~200 KB + 25 MB Czech model
pip install pyspellchecker    # Hunspell wrapper
# Korektor: binary download from LINDAT or REST API
```

### Workflow in pipeline
1. **Pre-check (before LLM)**: Hunspell + MorphoDiTa → identify correction candidates
2. **Rule-based fixes**: Typography, known false friends, anglicisms from DB → auto-fix without LLM
3. **LLM correction**: Only complex cases (style, word order, register) → pass pre-filtered issue list to LLM

### Integration points
- **NG-ROBOT**: New Phase 4.5 (between FactChecker and LanguageContextOptimizer)
  - Input: Phase 4 output + protected terms from TermDB
  - Output: Pre-corrected text + remaining issues list for Phase 5
- **ADOBE-AUTOMAT**: After `translate_batch()`, before `write_back_to_termdb()`
  - `correct_czech(elements, protected_terms)` call
- **Distribution**: Via `pip install ngm-terminology` (existing infrastructure)

### Key contract: Protected Terms
- Before correction, load canonical TermDB entries for the article
- These are OFF-LIMITS for synonym substitution or base-form "correction"
- Corrector may only adjust their declension, not replace them
- Implementation: `get_protected_terms(chain_db, article_domains) → dict`

## Available Czech NLP Resources

### Essential (Variant B)
| Resource | What | License | Size | Python |
|----------|------|---------|------|--------|
| MorphoDiTa + MorfFlex CZ 2.1 | Morphology, lemmatization, POS | CC BY-NC-SA | 25 MB | `ufal.morphodita` |
| Hunspell cs_CZ | Fast spell check | GPL | ~5 MB | `pyspellchecker` |
| Korektor | Statistical spell+grammar | BSD/CC BY-NC-SA | ~100 MB | subprocess/REST |

### Extended (Variant C, later)
| Resource | What | License | Size | Python |
|----------|------|---------|------|--------|
| UDPipe czech-pdt | Dependency parsing | CC BY-NC-SA | ~50 MB | `ufal.udpipe` |
| Stanza Czech | Neural NLP (best accuracy) | Apache 2.0 | ~300 MB | `stanza` |
| GECCC corpus | 83K error-correction sentences | CC BY-SA 4.0 | ~20 MB | M2 format |
| Czech Wikipedia | Language model data | CC BY-SA | ~2 GB | WikiExtractor |

### LINDAT REST APIs (prototyping, free, no key)
- MorphoDiTa: `http://lindat.mff.cuni.cz/services/morphodita/`
- UDPipe: `https://lindat.mff.cuni.cz/services/udpipe/`
- Korektor: `https://lindat.mff.cuni.cz/services/korektor/`
- NameTag: `http://lindat.mff.cuni.cz/services/nametag/`

## Overlap with TermDB

TermDB and corrector are **complementary**:
- TermDB = bilingual lookup (EN→CZ), domain-specific terms
- Corrector = Czech-internal rules (grammar, style, typography)
- Overlap: declension of translated terms, geographic exonyms, typography (currently duplicated in 3 places)
- Resolution: "protected terms" contract + centralize typography rules in corrector DB

## Cost/Benefit Estimates

| Variant | Effort | Token savings/article | New dependencies | Maintenance |
|---------|--------|----------------------|------------------|-------------|
| A (prompts) | 2-3 days | ~0 (better quality, same cost) | None | Low |
| B (hybrid) | 1-2 weeks | ~10-20% Phase 5 tokens | MorphoDiTa, Hunspell | Medium |
| C (full NLP) | 3-5 weeks | Could replace Phase 5 | +UDPipe, Stanza, GECCC | High |

## Session Plan

### Session 1 (current): A1 + A3 start
- [x] Audit + research (done)
- [ ] Add Czech guardrails to Phase 1 master prompt
- [ ] Start rules SQLite DB (convert false_friends + anglicisms from KB)

### Session 2: A2 + A3 complete + A4
- [ ] Phase 7 post-correction
- [ ] Complete rules DB (collocations, typography)
- [ ] `format_corrector_rules_for_prompt()` integration

### Session 3: Variant B prototype
- [ ] Install MorphoDiTa + Hunspell
- [ ] `CzechCorrector` class skeleton
- [ ] morpho.py + spellcheck.py wrappers
- [ ] Integration test on sample article

### Session 4: Variant B integration
- [ ] Protected terms bridge
- [ ] NG-ROBOT Phase 4.5 integration
- [ ] ADOBE-AUTOMAT integration
- [ ] E2E test on real article
