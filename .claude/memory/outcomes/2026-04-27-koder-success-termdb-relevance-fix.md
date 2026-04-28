---
skill: koder
date: 2026-04-27
task: "Fix termdb pipeline: drop is_primary filter, add relevance-aware article lookup"
outcome: success
project: PREKLAD
task_file: (inline task)
files_changed:
  - preklad/termdb/client.py
  - preklad/pipeline/phase16_glossary.py
  - preklad/pipeline/orchestrator.py
  - tests/test_termdb_relevance.py
exit_reason: completed
---

## What Was Done

- client.py: Removed is_primary=1 filter from _get_terms_cached(). Query uses ORDER BY t.id ASC, tr.is_primary DESC + Python dedup (first row per canonical_name = primary when available, fallback to any). ~150K iNaturalist is_primary=0 records now included. Added lookup_by_canonical() for direct Latin->cs lookups. Added lookup_terms_for_article() which extracts Latin binomials (regex) from article text and does a single IN-clause DB query — no subsampling, no top-N cap.
- phase16_glossary.py: Full rewrite. Pass 1 detects Latin binomials in CZ text, calls lookup_by_canonical, finds preceding Czech noun phrase (10-word lookback, sentence-boundary-aware), replaces if word overlap < 50% and phrase looks species-like. Pass 2 runs legacy enforce_glossary. Added isinstance(cs_canonical, str) guard. New artifacts: latin_binomials_found, canonical_lookups. enforce() signature extended with en_text= and article_terms= kwargs (backward compatible).
- orchestrator.py: Wires lookup_terms_for_article before Phase 1; builds term_table from article-relevant terms only (no max cap). Falls back to get_protected_terms_cached(limit=500) if empty. Passes en_text and article_terms to Phase 1.6.
- tests/test_termdb_relevance.py: 22 new tests covering is_primary=0 inclusion, Latin binomial detection, multi-species no-cap, stopword filtering, Phase 1.6 enforcement, and live DB tests against real termdb.

## Verification

22/22 new tests pass. 179/180 non-LLM tests pass (1 pre-existing failure in test_exporter.py::TestEdgeCases::test_empty_line_mapping from pre-existing docx_writer.py modification — confirmed unrelated by isolated stash test). git commit 22a35b5 on PREKLAD master.

## What Failed (if any)

None from this task. Pre-existing exporter test failure exists but is not caused by these changes.
