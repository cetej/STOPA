---
task_id: preklad-bootstrap
goal: "Bootstrap PREKLAD project: RTT PDF/DOCX → structured CZ DOCX with FastAPI+HTMX UI"
type: feature
task_style: structured
status: done
branch: main
locked_at: 2026-04-27
completed_at: 2026-04-27T18:00:00
result: "MVP scaffold complete. 5 commits in PREKLAD. 108/108 tests pass. 4/6 SC verified (sc-3/sc-5 require ANTHROPIC_API_KEY for live translation). Latest commit: 92aeaee."
---

# Shared Memory — Task State

## Active Task

**Goal**: PREKLAD — translation-only pipeline for NG-ROBOT RTT files

**Tier**: deep
**Verifiability**: METRIC

### Success Criteria (locked Phase 1.95)

- sc-1: `python -c "import preklad"` succeeds
- sc-2: `python -m preklad.api.app` starts FastAPI on :8000, GET /health returns 200
- sc-3: Upload rainbow_lizards.pdf → CZ DOCX produced, parses with python-docx, non-empty body
- sc-4: Upload okavango.docx → Phase 0 detects long+backgrounder, line-parser splits correctly, full pipeline runs
- sc-5: Side-by-side EN|CZ DOCX downloadable, contains paragraph pairs
- sc-6: UI loads at /, drag&drop works, no console errors, anti-slop visual identity verified

### Wave Plan

| Wave | Agents | Files |
|------|--------|-------|
| 1 | scaffold (DONE after this run) | structure, configs, refs port, termdb client, fixtures |
| 2 | parser, pipeline, exporter | parser/*, pipeline/phase*.py + orchestrator, exporter/* |
| 3 | api, ui | api/*, ui/templates/*, ui/static/* |
| 4 | verify | end-to-end test on both fixtures |

## History

### Chase Context-Engineering Patterns: Align Evals & Agent Attribution (COMPLETE, 2026-04-23)

Harrison Chase 5 patterns integration:
- [x] Phase 1 complete: sensors fixed, hooks pruned, skills archived (commit 890f00b)
- [x] Phase 2 complete: KODER agent, task queue, handoff protocol (commit 09b251a)
- [x] Phase 3.1: Retrospektivní audit — 27 active items mapped, 5 acted (18.5% baseline)
- [x] Phase 3.2: news.md upgraded — `Acted | Evidence` sloupce v Action Items tabulce
- [x] Phase 3.3: `scripts/actionable-rate.py` — metrika calculator (summary/detail/json)
- [x] Phase 3.4: watch skill updated — auto-tagging nových findings s acted=no
- [x] Phase 3.5: actionable_rate 18.5% → 51.9% (target 50% ✅)
- [x] Phase 4.1: Sync invariant fixed — `.claude/commands/annotate.md` created as identical copy of `.claude/skills/annotate/SKILL.md` (verified via diff)
- [x] Phase 4.2: Agent attribution implementation — `trace-capture.py` reads `agent_type` from PostToolUse event (lines 81, 143–144), writes `record["agent"]` only for subagents
- [x] Phase 4.3: Trace validation — `scripts/validate-trace.py` created (ASCII-safe output), test trace validated: 5/5 records parse, subagent attribution `critic` detected, error record (seq=3) has output_full
- [x] Phase 4.4: End-to-end annotation workflow tested — `annotations.jsonl` (3 records: skip/bad/good), `.claude/evals/annotated/case-001/` generated with input.md + expected.md + eval.md for `bad` verdict on seq=3 (pytest blind run)
- [x] Phase 4.5: Documentation — Phase 4 complete, ready for commit + distribution

Phase 4 Artifacts:
| File | Purpose | Verification |
|------|---------|--------------|
| `.claude/hooks/trace-capture.py` | Agent attribution in traces | Lines 81, 143–144 read/write `agent_type` |
| `.claude/skills/annotate/SKILL.md` | Retrospective annotation skill | 217 lines, 6 phases, sync'd to commands/ |
| `.claude/commands/annotate.md` | Sync copy (core-invariant #2) | Byte-identical to SKILL.md |
| `scripts/validate-trace.py` | Trace JSONL validator | PASS: 5/5 records, 1 subagent, 1 error record |
| `.traces/sessions/test-trace-2026-04-23.jsonl` | Test fixture | 5 records, includes `agent: critic` |
| `.claude/memory/annotations.jsonl` | Annotation store | 3 records: skip/bad/good |
| `.claude/evals/annotated/case-001/` | Generated eval case | input.md + expected.md + eval.md |
