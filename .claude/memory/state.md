---
branch: main
last_update: 2026-04-14T11:00:00
---

# Shared Memory — Task State

## Active Task

**Phase 2: Rozdělit STOPA a KODER** (scheduler / execution split)

Příprava:
- [x] Phase 1 complete: sensors fixed, hooks pruned, skills archived (commit 890f00b)
- [x] Phase 2.1: KODER agent definition (`.claude/agents/koder.md`)
- [x] Phase 2.1: `/koder` dispatch skill (`.claude/skills/koder/SKILL.md`)
- [x] Phase 2.2: Task queue (``.claude/tasks/koder-queue/``) + template
- [x] Phase 2.2: Scheduled task `koder-queue-check` (denně 9:53 po-pá)
- [x] Phase 2.5: ADR 0015 — plugin upgrade path naplánován
- [ ] Phase 2.3: End-to-end test — vytvořit a dispatchnout testovací task
- [ ] Phase 2.3: Outcome reading integration (STOPA čte KODER outcomes)

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
