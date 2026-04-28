---
skill: koder
date: 2026-04-27
task: "Fix three PREKLAD bugs: silent done guard, EN header passthrough, RTT metadata pollution"
outcome: success
project: PREKLAD
task_file: "koder-queue/urgent-preklad-bug-fix"
files_changed:
  - preklad/api/jobs.py
  - preklad/exporter/docx_writer.py
  - preklad/parser/rtt_parser.py
  - preklad/parser/models.py
  - tests/test_validation_guards.py
exit_reason: completed
---

## What Was Done

- Bug 1 (silent done guard): Added _validate_translation_output() and _validate_cz_docx() in jobs.py. Checks orchestrator status, final_cz_text length >=50, Czech char ratio >=5%, line_mapping non-empty when body_lines exist. Opens written DOCX and re-checks. Failure → status=failed with specific Czech error.
- Bug 2 (EN header passthrough): Added _resolve_header_field() in docx_writer.py. Looks up CZ from line_mapping via LineEntry role. No CZ found → [NEPŘELOŽENO] prefix. Never silent EN passthrough.
- Bug 3 (metadata pollution): Added _is_metadata_line() exporter filter + RTT_TITLE_COLON_RE parser skip. Parser now skips "Dept : Story Slug" embedded numbered lines. Exporter also filters story/issue-meta/word-count patterns. Added role="metadata" to LineEntry Literal.
- Tests: 13 new tests in tests/test_validation_guards.py.

## Verification

182/182 tests pass. E2E on rainbow_lizards.pdf:
- "0626 mini feature" in DOCX: False
- "word count" in DOCX: False
- "The Grid : Rainbow Lizards" in DOCX: False
- Untranslated EN headline in DOCX: False
- First substantive paragraph: "MOHOU NAS TYTO DUHOVE JESTĚRKY NAUCIT NECO O EVOLUCI?"
- Czech char ratio: 7.7%
- Server /health: OK
