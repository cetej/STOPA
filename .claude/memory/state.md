---
branch: main
last_update: 2026-04-14T11:00:00
---

# Shared Memory — Task State

## Active Task

**Phase 2: Rozdělit STOPA a KODER** (scheduler / execution split)

Příprava:
- [x] Phase 1 complete: sensors fixed, hooks pruned, skills archived
- [ ] Phase 2.1: Create KODER profile (new persona)
- [ ] Phase 2.2: Define handoff protocol (task queue system)
- [ ] Phase 2.3: Implement task distribution mechanism

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
