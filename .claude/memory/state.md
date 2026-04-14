---
branch: main
last_update: 2026-04-14T11:00:00
---

# Shared Memory — Task State

## Active Task

**Phase 3: Měřitelný feedback loop** (watch → ingest → actionable learnings)

Příprava:
- [x] Phase 1 complete: sensors fixed, hooks pruned, skills archived (commit 890f00b)
- [x] Phase 2 complete: KODER agent, task queue, handoff protocol (commit 09b251a)
- [x] Phase 3.1: Retrospektivní audit — 27 active items mapped, 5 acted (18.5% baseline)
- [x] Phase 3.2: news.md upgraded — `Acted | Evidence` sloupce v Action Items tabulce
- [x] Phase 3.3: `scripts/actionable-rate.py` — metrika calculator (summary/detail/json)
- [x] Phase 3.4: watch skill updated — auto-tagging nových findings s acted=no
- [ ] Phase 3.5: Zvýšit actionable_rate z 18.5% na 50% (cíl: konec dubna)

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
