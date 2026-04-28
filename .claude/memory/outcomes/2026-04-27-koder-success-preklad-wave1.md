---
skill: koder
date: 2026-04-27
task: "PREKLAD Wave 1 — project scaffold, prompts port, termdb client, pipeline modules"
outcome: success
project: "PREKLAD"
task_file: "wave1-bootstrap"
files_changed:
  - C:/Users/stock/Documents/000_NGM/PREKLAD/pyproject.toml
  - C:/Users/stock/Documents/000_NGM/PREKLAD/README.md
  - C:/Users/stock/Documents/000_NGM/PREKLAD/CLAUDE.md
  - C:/Users/stock/Documents/000_NGM/PREKLAD/.env.example
  - C:/Users/stock/Documents/000_NGM/PREKLAD/.gitignore
  - C:/Users/stock/Documents/000_NGM/PREKLAD/inbox/.gitkeep
  - C:/Users/stock/Documents/000_NGM/PREKLAD/preklad/__init__.py
  - C:/Users/stock/Documents/000_NGM/PREKLAD/preklad/parser/__init__.py
  - C:/Users/stock/Documents/000_NGM/PREKLAD/preklad/pipeline/__init__.py
  - C:/Users/stock/Documents/000_NGM/PREKLAD/preklad/termdb/__init__.py
  - C:/Users/stock/Documents/000_NGM/PREKLAD/preklad/termdb/client.py
  - C:/Users/stock/Documents/000_NGM/PREKLAD/preklad/exporter/__init__.py
  - C:/Users/stock/Documents/000_NGM/PREKLAD/preklad/api/__init__.py
  - C:/Users/stock/Documents/000_NGM/PREKLAD/preklad/pipeline/glossary_enforcer.py
  - C:/Users/stock/Documents/000_NGM/PREKLAD/preklad/pipeline/czech_corrector.py
  - C:/Users/stock/Documents/000_NGM/PREKLAD/prompts/master_translator_v1.md
  - C:/Users/stock/Documents/000_NGM/PREKLAD/prompts/phase5_czech_context.md
  - C:/Users/stock/Documents/000_NGM/PREKLAD/prompts/phase6_critic.md
  - C:/Users/stock/Documents/000_NGM/PREKLAD/prompts/phase8_domain_critic.md
  - C:/Users/stock/Documents/000_NGM/STOPA/.claude/memory/state.md
  - C:/Users/stock/Documents/000_NGM/STOPA/.claude/memory/intermediate/orchestrate-plan.md
exit_reason: "completed"
---

## What Was Done

- Created full PREKLAD project structure (10 directories, 19 files)
- Copied test fixtures: rainbow_lizards.pdf (199KB) and okavango.docx (407KB)
- Ported glossary_enforcer.py from ADOBE-AUTOMAT — adapted interface from ADOBE-AUTOMAT's TextElement-based API to simpler `enforce_glossary(text, term_pairs) -> (str, list[Fix])` signature
- Implemented czech_corrector.py from scratch (no source to port — CzechCorrector is in closed ngm_terminology package) — deterministic rules from NG-ROBOT 00_MASTER_v42.2.6.md
- Created termdb client using actual schema (terms/translations/domains/aliases tables) with lru_cache
- Wrote 4 prompt files: master_translator_v1.md (RTT-aware extension of NG-ROBOT master), phase5_czech_context.md (1:1 port), phase6_critic.md (Self-Refine, new), phase8_domain_critic.md (domain expert, new)
- Initialized git repo, staged all tracked files
- Updated STOPA state.md: previous task moved to History, new preklad-bootstrap task set as Active
- Created orchestrate-plan.md for Wave 2-4 agents

## Verification

- `python -c "import ast; ast.parse(...)"` passed on all 3 Python files
- `TermdbClient(termdb.db).get_protected_terms_cached(limit=10)` → 10 terms loaded, no exception
- rainbow_lizards.pdf: 202886 bytes (>100KB) ✓
- okavango.docx: 416710 bytes (>50KB) ✓
- PREKLAD/.git/ exists ✓
- All 4 prompt files in prompts/ ✓
- STOPA state.md has task_id: preklad-bootstrap ✓
- orchestrate-plan.md at STOPA/.claude/memory/intermediate/ ✓

## What Failed (if any)

- czech_corrector.py: 3 syntax error attempts caused by curly quotes (U+201C, U+201D) inside Python string literals. Root cause: the Write tool inserted typographic curly quotes which Python parser interprets as part of string syntax. Fixed by rewriting constants using plain ASCII + Unicode character U+201E/U+201C explicitly assigned to named constants at module level. Resolution: 3rd attempt succeeded.
