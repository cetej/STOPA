---
# Machine-readable checkpoint (NLAH path-addressable)
saved: "2026-04-04"
session_id: null
task_ref: null  # e.g. "state.md#task-nlah-impl"
branch: main
progress:
  completed: []   # subtask IDs: ["st-1", "st-3"]
  in_progress: [] # subtask IDs: ["st-2"]
  blocked: []     # subtask IDs with reason
artifacts_modified: []
resume:
  next_action: null
  blockers: []
  decisions_pending: []
  failed_approaches: []
---

# Session Checkpoint

**Saved**: 2026-04-04
**Task**: Agent-Skills Patterns Adoption — Phase 2 COMPLETE
**Branch**: main

## Co je hotovo (Phase 1 + Phase 2)

- `.claude/rules/skill-files.md` — `phase:` field + 3 body sekce spec
- `.claude/rules/skill-tiers.md` — Lifecycle Phase Mapping + Required Sections by Tier
- `/skill-generator` template aktualizovan
- **48/48 skills** ma `phase:` tag
- **37/37 skills** ma Anti-Rationalization Defense (`Rationalization | Why Wrong | Do Instead`)
- **37/37 commands/** synced s skills/
- **Tier 1 (7/7):** triage, orchestrate, scout, critic, checkpoint, scribe, status — AR + RF + VC
- **Tier 2 (22/22):** vsechny maji AR
- **Tier 4 (2/2):** tdd, systematic-debugging — AR + RF
- **Skill-generator (1/1):** AR v template

## Co zbyva

### SHOULD: Tier 2 — Red Flags + VC pro klicove skills
security-review, dependency-audit, harness, eval — doporucuji RF + VC

### SHOULD: Tier 4 — Verification Checklist
tdd, systematic-debugging — chybi VC

### NICE: Tier 3 — AR RECOMMENDED (11 skills)
nano, klip, autoloop, project-init, watch, sweep, compact, budget, browse, youtube-transcript, self-evolve

## Co NEdělat
- Nemen description field — MUSI zustat "Use when..."
- Nemen existujici AR obsah — jen pridavej k skillum co AR nemaji
- Nepridavej sekce ke skill-generator template (uz tam jsou)

## Resume Prompt

Phase 2 hotova. Vsech 22 Tier 2 skills ma Anti-Rationalization Defense tabulky. Celkem 37 skills pokryto (Tier 1+2+4). Zbyva: Tier 3 (NICE-TO-HAVE, 11 skills), Red Flags + Verification Checklists pro klicove Tier 2 skills, commit.
