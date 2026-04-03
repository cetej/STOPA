---
category: claude-code-orchestration
severity: high
last_updated: 2026-04-03
---

# Claude Code / Orchestration — Runbook

## Skill not triggering

**Symptom:** User invokes a skill by description but Claude doesn't use it
**Cause:** `description:` field doesn't contain trigger keywords, or summarizes workflow instead of trigger conditions
**Fix:**
1. Check `description:` starts with "Use when..."
2. Ensure trigger keywords match user's likely phrasing
3. Verify skill is listed in `skill-tiers.md`

**Prevention:** Rule in `skill-files.md` — description = trigger conditions only, never workflow summary

---

## Agent loop (same agent 3x)

**Symptom:** Orchestrator keeps spawning the same sub-agent for the same subtask
**Cause:** Circuit breaker not firing, or agent output not matching expected format
**Fix:**
1. Circuit breaker should fire at 3x same agent on same subtask
2. If not firing: check orchestrate skill's loop detection logic
3. Manual stop: tell orchestrator to STOP and report current state

---

## Memory file > 500 lines

**Symptom:** Memory file getting unwieldy, slow retrieval
**Cause:** Accumulated entries without archival
**Fix:**
1. Move old entries to `*-archive.md`
2. Never delete — only archive (audit trail rule)
3. Run `/scribe maintenance` to automate

---

## Checkpoint stale

**Symptom:** Checkpoint references tasks/state that no longer exists
**Cause:** Multiple sessions since last checkpoint, project evolved
**Fix:**
1. Check date in checkpoint.md
2. If > 2 sessions old: run `/scout` to re-map instead of trusting checkpoint
3. Update or clear checkpoint after re-scouting
