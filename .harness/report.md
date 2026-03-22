# Skill Audit Report

**Generated**: 2026-03-22
**Skills audited**: 15
**Overall health**: 3.9/5

---

## Summary Table

| Skill | Description Quality | Tools Permission | Integration | Overall |
|-------|-------------------|-----------------|-------------|---------|
| youtube-transcript | 5/5 | ok | 2/5 | 3/5 |
| autoloop | 5/5 | ok | 4/5 | 4/5 |
| budget | 4/5 | ok ✓ exemplary | 5/5 | 5/5 |
| checkpoint | 5/5 | ok | 5/5 | 5/5 |
| dependency-audit | 4/5 | ok | 3/5 | 4/5 |
| incident-runbook | 5/5 | ok ✓ explicit disallow | 2/5 | 4/5 |
| orchestrate | 5/5 | ok | 5/5 | 5/5 |
| project-init | 5/5 | ok | 2/5 | 4/5 |
| scout | 4/5 | ⚠ no disallowed list | 4/5 | 4/5 |
| scribe | 4/5 | ok | 4/5 | 4/5 |
| skill-generator | 5/5 | ok | 4/5 | 4/5 |
| verify | 5/5 | ok ✓ explicit disallow | 2/5 | 4/5 |
| watch | 4/5 | ⚠ over-permissioned | 4/5 | 4/5 |
| critic | 5/5 | ok | 5/5 | 5/5 |
| harness | 5/5 | ok | 4/5 | 5/5 |

---

## Top Issues

### HIGH — Integration gaps in utility skills

**Affected**: `verify`, `youtube-transcript`, `incident-runbook`, `project-init`

These skills operate in isolation — they don't read shared memory for context or write findings back. This breaks the COMPOUND loop: insights from these skills are lost.

| Skill | Missing read | Missing write |
|-------|-------------|--------------|
| verify | budget.md | state.md (result), learnings.md (failures) |
| youtube-transcript | checkpoint.md (context) | learnings.md (workarounds) |
| incident-runbook | learnings.md (project patterns) | runbook.md (blocked by disallow — by design) |
| project-init | — | — (by design, bootstrap) |

**Fix**: Add a "After Completion" section to `verify` and `youtube-transcript` that writes findings to shared memory.

---

### MEDIUM — Scout has no enforcement of read-only mandate

**Affected**: `scout`

Scout's instructions say "never modify anything" but `disallowedTools` is empty. This relies on Claude following text instructions rather than hard constraints. Both `verify` and `incident-runbook` use explicit disallow lists for the same purpose — scout should too.

**Fix**: Add `disallowedTools: Write, Edit, Bash` to scout's frontmatter.

---

### MEDIUM — watch has unnecessary tool permissions

**Affected**: `watch`

`watch` has no `disallowedTools` despite having no use for `Bash`, `Glob`, or `Grep` in its workflow. It only needs Read/Write/Edit (for news.md) + WebSearch/WebFetch + Agent.

**Fix**: Add `disallowedTools: Bash, Glob, Grep` to watch's frontmatter.

---

### MEDIUM — Overlap risk: autoloop ↔ skill-generator

Both can trigger on "improve skill X". The distinction (iterative optimization with scoring vs. one-shot structural update) is not visible in either description.

**Fix**: Add to `autoloop`: "Do NOT use when /skill-generator is sufficient for a one-shot improvement." Add to `skill-generator`: "For iterative automated optimization with M5 scoring, use /autoloop."

---

### LOW — Harness doesn't read learnings.md at start

**Affected**: `harness`

The harness engine runs phases mechanically but doesn't apply accumulated learnings at Phase 0. Orchestrate reads learnings.md before every task.

**Fix**: Add to harness Phase 0: "Read `.claude/memory/learnings.md` — apply relevant patterns to phase execution."

---

### LOW — budget skill missing user-facing trigger phrases

**Affected**: `budget`

Description says "auto-invoked by orchestrator" but doesn't give users explicit phrases to invoke it themselves ("check budget", "how much have I spent", "set budget limit").

**Fix**: Add explicit user trigger to description.

---

## Recommendations

**Priority 1 — Quick fixes (low effort, high impact)**

1. **scout**: Add `disallowedTools: Write, Edit, Bash` — enforce read-only via constraint, not text
2. **watch**: Add `disallowedTools: Bash, Glob, Grep` — remove unused tool permissions
3. **verify**: Add "After Completion" section: write result to state.md, failures to learnings.md
4. **harness**: Add learnings.md read at Phase 0

**Priority 2 — Description improvements**

5. **autoloop ↔ skill-generator**: Add cross-exclusion language to both descriptions
6. **scout ↔ orchestrate**: Add "read-only only — for multi-step changes use /orchestrate" to scout
7. **watch**: Tighten trigger phrases — "what's new" is too generic
8. **budget**: Add user-facing trigger phrases to description

**Priority 3 — Integration improvements**

9. **youtube-transcript**: Add learnings.md write for discovered workarounds (e.g., yt-dlp anti-bot fixes)
10. **incident-runbook**: Add learnings.md read at start for project-specific patterns
11. **dependency-audit**: Add budget awareness before running web searches
12. **autoloop**: Add /critic suggestion after loop completion

---

## Detailed Findings

### Description Audit

**Score 5/5** (12 skills): youtube-transcript, autoloop, checkpoint, incident-runbook, orchestrate, project-init, skill-generator, verify, critic, harness + 2 more

**Score 4/5** (3 skills):
- `budget` — good but missing explicit user-facing triggers
- `scout` — overlap risk with orchestrate; missing 'read-only only' emphasis
- `dependency-audit` — missing 'before upgrading' trigger; overlap with watch not fully resolved
- `watch` — generic 'what's new' trigger; scope not explicit enough

**Overlap pairs identified**:
- `orchestrate` ↔ `harness` — distinction is good but subtle
- `autoloop` ↔ `skill-generator` — both trigger on 'improve skill X'
- `scout` ↔ `orchestrate` — both can fire on 'before multi-file change'
- `verify` ↔ `critic` — both evaluate quality, but execution vs analysis distinction is clear
- `watch` ↔ `dependency-audit` — ecosystem vs project scope is clear

---

### Tools Audit

**Exemplary patterns** (skills others should copy):
- `budget`: minimal Read/Write/Edit — gold standard for least privilege
- `incident-runbook`: explicit `disallowedTools: Agent, Write, Edit` — enforces diagnosis-only mandate
- `verify`: explicit `disallowedTools: Write, Edit` — enforces observe-only mandate
- `critic`: explicit `disallowedTools: Write, Edit` — enforces report-only mandate

**Issues**:
- `scout`: missing disallowed list despite "read-only" mandate (medium risk)
- `watch`: has Bash/Glob/Grep in allowed list but never uses them (low risk)

**Justified broad permissions** (orchestrators/coordinators):
- `orchestrate`, `harness`, `autoloop`, `checkpoint` — all have broad tools for good reasons

---

### Integration Audit

**Score 5/5** (3 skills): `budget`, `checkpoint`, `orchestrate`, `critic`
> These define the integration reference standard.

**Score 4/5** (6 skills): `autoloop`, `scout`, `scribe`, `skill-generator`, `watch`, `harness`
> Good integration, minor gaps.

**Score 3/5** (1 skill): `dependency-audit`
> Reads/writes memory but missing budget awareness.

**Score 2/5** (4 skills): `youtube-transcript`, `incident-runbook`, `project-init`, `verify`
> Low integration — ranges from intentional (project-init, incident-runbook) to fixable (verify, youtube-transcript).

**Key pattern**: Skills that are "utility tools" (youtube-transcript, incident-runbook) deliberately have low integration. Skills that are "system tools" (orchestrate, critic, budget) have maximum integration. This is the right design — but `verify` should be a system tool (it validates work products) and needs its integration upgraded.

---

*Generated by skill-audit harness v1.0*
