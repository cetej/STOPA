---
branch: main
last_update: 2026-04-23T11:00:00
---

# Shared Memory — Task State

## Active Task

**Chase Context-Engineering Patterns: Align Evals & Agent Attribution** (Harrison Chase 5 patterns integration) — **COMPLETE**

Příprava:
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

## Phase 4 Artifacts (Evidence)

| File | Purpose | Verification |
|------|---------|--------------|
| `.claude/hooks/trace-capture.py` | Agent attribution in traces | Lines 81, 143–144 read/write `agent_type` |
| `.claude/skills/annotate/SKILL.md` | Retrospective annotation skill | 217 lines, 6 phases, sync'd to commands/ |
| `.claude/commands/annotate.md` | Sync copy (core-invariant #2) | Byte-identical to SKILL.md |
| `scripts/validate-trace.py` | Trace JSONL validator | PASS: 5/5 records, 1 subagent, 1 error record |
| `.traces/sessions/test-trace-2026-04-23.jsonl` | Test fixture | 5 records, includes `agent: critic` |
| `.claude/memory/annotations.jsonl` | Annotation store | 3 records: skip/bad/good |
| `.claude/evals/annotated/case-001/` | Generated eval case | input.md + expected.md + eval.md |

## Session Files (Phase 1 Completion)

| File | Status | Notes |
|------|--------|-------|
| .claude/hooks/session-summary.sh | ✅ FIXED | line 35: `Skill[: ]` regex pattern |
| .claude/hooks/outcome-writer.py | ✅ FIXED | added `_record_failure_inline()` |
| .claude/settings.json | ✅ MODIFIED | deactivated 25 low-value hooks (82→57) |
| .claude/archive/skills/ | ✅ CREATED | 20 dead skills moved |
| .claude/archive/commands/ | ✅ CREATED | 20 command files moved |
| .claude/memory/raw/archive/ | ✅ CREATED | 602 old captures archived |
| outputs/stopa-restructure-plan.md | ✅ SAVED | Full 3-phase plan with metrics |
