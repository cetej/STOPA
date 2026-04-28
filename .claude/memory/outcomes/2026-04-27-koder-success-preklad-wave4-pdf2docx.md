---
skill: koder
date: 2026-04-27
task: "PREKLAD Wave 4: pdf2docx preprocessor + live E2E translation on rainbow_lizards.pdf"
outcome: success
project: PREKLAD
task_file: "(delegated from STOPA orchestrator)"
files_changed:
  - preklad/parser/pdf_to_docx.py
  - preklad/parser/rtt_parser.py
  - preklad/pipeline/orchestrator.py
  - preklad/config.py
  - pyproject.toml
  - tests/test_parser.py
  - scripts/e2e_test.py
  - .gitignore
exit_reason: completed
---

## What Was Done

- Added `pdf2docx>=0.5.8` to `pyproject.toml` dependencies and installed package
- Created `preklad/parser/pdf_to_docx.py` — converter module, creates `{stem}.converted.docx` sibling file
- Modified `parse_rtt()` in `rtt_parser.py` to use hybrid approach:
  - pdfplumber still extracts the line-numbered story body (preserves "N text" structure)
  - pdf2docx converts PDF separately to recover sidebar/text-box content (background notes)
  - `_extract_sidebar_notes_from_converted_docx()` splits packed notes string back into individual entries
  - Sidebar notes merged with any pdfplumber-found colon-style notes (deduplicated)
- Added `_extract_paragraphs_docx_file()` using zipfile XML traversal for pdf2docx-converted DOCX files (handles content in floating wp:anchor shapes)
- Fixed `orchestrator._get_en_text()` to reconstruct numbered-line format from `RTTDocument.body_lines` instead of falling back to `str(rtt_doc)`
- Fixed `config.py` `load_dotenv()` to use explicit project root path with `override=True` (was loading wrong empty .env)
- Added `*.converted.docx` to `.gitignore`
- Added `test_background_notes_extracted_via_pdf2docx` test asserting `len(notes) >= 3`
- Created `scripts/e2e_test.py` for future regression testing

## Verification

Parser test (45 tests, 0 failures):
```
Pytest: 45 passed
```

Notes detected after pdf2docx integration (was 0 before):
- [8] ROBERTO GARCÍA-ROA: Male. https://www.robertogarciaroa.com/
- [10] Ibiza wall lizards: Podarcis pityusensis
- [17] National Geographic Explorer Tobias Uller: Male. ...

E2E test: PASSED
- Phases run: ['phase0', 'phase1', 'phase1.6', 'czech_corrector']
- Status: done (short format, no full pipeline needed)
- CZ DOCX: 38561 bytes, 32 paragraphs, 152 Czech-specific chars
- SBS DOCX: 40224 bytes, 8 paragraphs, 2 tables
- Czech headline: "MOHOU NÁS TYTO DUHOVÉ JEŠTĚRKY NAUČIT NĚCO O EVOLUCI?"

Final commit: 4d7d479

## sc-3 and sc-5 verdict
- sc-3 (Rainbow -> CZ DOCX): PASS (38 kB, 152 Czech-specific chars, valid translation)
- sc-5 (Side-by-side EN|CZ): PASS (40 kB, 2 tables including body table and notes table)
