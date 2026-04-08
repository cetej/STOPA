---
name: checkpoint
description: Use when ending an active session to save progress for resumption in a new session. Trigger on 'checkpoint', 'save progress', 'continue later'. Do NOT use for capturing completed remote session findings (/handoff), recording a single decision (/scribe), or mid-task while work is still in flight.
context:
  - gotchas.md
argument-hint: [save / resume / status]
discovery-keywords: [save progress, resume later, session state, pokračuj, ulož stav, context save, pause work]
tags: [session, memory]
phase: ship
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
model: haiku
effort: low
maxTurns: 10
disallowedTools: Agent
---

# Checkpoint — Session Continuity Manager

You ensure work survives across session boundaries. You save structured snapshots that allow the next session to resume seamlessly.

## When Things Go Wrong

- **checkpoint.md is corrupted or malformed**: Recreate from state.md + git log. Don't try to parse broken markdown.
- **Git state is dirty when saving**: Include the dirty state in the checkpoint — it's important context for resume.
- **No active task to checkpoint**: Save a minimal checkpoint with git state and session notes only.

<!-- CACHE_BOUNDARY -->

## Input

Parse `$ARGUMENTS`:
- **"save"** (default) → Create checkpoint from current session state
- **"resume"** → Read checkpoint and present resume context to user
- **"status"** → Show whether a checkpoint exists and its age
- **"clear"** → Archive checkpoint to state.md history and clear it

## Save Checkpoint

### Step 1: Gather State

Collect from all available sources:

1. **Task state**: Read `.claude/memory/state.md` — active task, subtasks, status
2. **Budget state**: Read `.claude/memory/budget.md` — tier, counters, how much budget remains
3. **Recent decisions**: Read `.claude/memory/decisions.md` — last 3 entries
4. **Git state**: Run these commands:
   ```bash
   git branch --show-current
   git status --short
   git log --oneline -5
   git diff --stat
   ```
5. **Learnings this session**: Glob `.claude/memory/learnings/` for today's entries (pattern: `YYYY-MM-DD-*.md`)
6. **Implementation plan**: Read `.claude/memory/implementation-plan.md` if it exists

### Step 1.5: Trajectory Audit (ref: LH-Deception, arXiv:2510.03999)

Before determining what's done, run a lightweight trajectory audit on the current session.
Chains of deception (vagueness drift, scope narrowing, false completion) are invisible per-step — only detectable across the full session trajectory.

**Check 4 signals:**

| # | Signal | How to check | Flag if |
|---|--------|-------------|---------|
| 1 | **Vagueness drift** | Compare specificity of early vs late agent outputs in this session. Look for hedging: "should work", "looks fine", "mostly correct", "I believe" in later outputs | Late outputs significantly vaguer than early ones |
| 2 | **Scope narrowing** | Read `state.md` subtask list. Count completed vs total. Check if any were silently dropped (no explicit "deferred" or "blocked" note) | Subtasks disappeared without explanation |
| 3 | **False completion** | For each "done"/"hotovo"/"tests pass" claim in session, verify matching tool output exists (test run, build output, grep result) | Claims without tool evidence |
| 4 | **Pressure response** | Read `panic-episodes.jsonl` for this session. If yellow/red episodes exist, check agent behavior AFTER the episode — did quality improve or degrade? | Agent continued same pattern post-intervention |

**Scoring:**
- **CLEAN** (0 flags) → no action needed
- **REVIEW** (1 flag) → note in Session Detail Log, no resume prompt change
- **WARNING** (2+ flags) → add to Resume Prompt: `"⚠ Trajectory audit flagged: [signals]. Verify before continuing."`

**Rules:**
- This is informational only — never blocks checkpoint save
- Output goes under `## Trajectory Audit` in Session Detail Log (below truncation boundary)
- No sub-agent needed — pattern matching on session context + panic-episodes + state.md
- Takes <30 seconds — don't over-analyze, just flag obvious patterns

### Step 2: Determine What's Done, What Remains, and What Failed

From the task state:
- List completed subtasks (with one-line summaries)
- List remaining subtasks (with dependencies and method)
- Identify the **immediate next action** — the very first thing the next session should do
- **Collect failed approaches**: Check for:
  1. Panic detector episodes: Read `.claude/memory/intermediate/panic-episodes.jsonl` (if exists) — each entry = a failed approach cycle
  2. Git reverts/resets in this session: `git reflog --since="8 hours ago"` for evidence of rolled-back work
  3. Conversation context: recall any approach you abandoned with reasoning
  - Write each failure as: `- **{approach}**: {why it failed} → {lesson}`

### Step 3b: Git Cross-Reference

After determining what's done vs. remaining, cross-reference with actual git state:

1. Run `git log --oneline --since="8 hours ago"` to list commits from this session
2. Run `git status --short` to identify uncommitted changes
3. In the checkpoint, clearly separate:
   - **Committed work**: list of commits with one-line descriptions (proven, safe)
   - **Uncommitted WIP**: list of modified/untracked files (at risk if session crashes)
   - **Discrepancy check**: if state.md says "subtask X done" but no matching commit exists → flag it

This prevents the "I thought it was committed" problem where work exists only in context.


### Step 3: Write Checkpoint

Write to `.claude/memory/checkpoint.md` with **both** YAML frontmatter (machine-readable) and markdown body (human-readable):

```markdown
---
# Machine-readable checkpoint (NLAH path-addressable)
saved: "<YYYY-MM-DDTHH:MM>"
session_id: "<s-YYYYMMDD-slug>"
task_ref: "state.md#<task_id>"
branch: <current git branch>
progress:
  completed: ["st-1", "st-3"]   # subtask IDs from state.md frontmatter
  in_progress: ["st-2"]
  blocked: []
artifacts_modified:
  - <file paths changed this session>
keywords:
  - <3-8 confidence keywords: project names, technical terms, frameworks, ticket IDs>
resume:
  next_action: "<specific next step>"
  blockers: []
  decisions_pending: []
  failed_approaches: ["<approach that didn't work — why>"]
---

# Session Checkpoint

**Saved**: <date> <time (approximate)>
**Task**: <goal from state.md>
**Branch**: <current git branch>
**Progress**: <N/M subtasks complete>

## What Was Done This Session

<Bulleted list of completed work, with file paths where relevant>

## What Remains

| # | Subtask | Status | Depends on | Method |
|---|---------|--------|-----------|--------|
<Remaining subtasks from state.md>

## Immediate Next Action

<The single most important thing to do first. Be specific:
 file path, function name, what change to make.>

## Tried and Failed

<Approaches attempted this session that DID NOT WORK.
 For each, include: what was tried, why it failed, what we learned.
 This prevents the next session from repeating dead ends.
 If nothing failed, write "Nothing — all approaches worked.">

## Key Context

<Essential information the next session needs to understand WHY
 decisions were made. Keep to 5-10 bullet points max.
 Reference decisions.md entries if detailed rationale exists.>

## Resume Prompt

> <A complete, self-contained prompt that can be given to a fresh
>  Claude session. It should include:
>  1. The overall goal
>  2. Current state (what's done, what's not)
>  3. The immediate next action
>  4. Any critical constraints or decisions
>  5. Reference to files: CLAUDE.md, .claude/memory/state.md,
>     .claude/memory/checkpoint.md, .claude/memory/wiki/INDEX.md
>  Write in English (for Claude). Keep under 300 words.>

---
## Session Detail Log

> **TRUNCATION BOUNDARY** (CPR-inspired): Everything below this line
> is NEVER loaded during resume. It exists for audit/searchability only.
> The `/checkpoint resume` command reads content ABOVE this heading only.

### Git State

- Branch: <branch>
- Uncommitted changes: <yes/no — if yes, list files>
- Last commit: <hash + message>
- Recent commits (this session): <git log --oneline --since="8 hours ago">

### Budget State

- Tier: <tier>
- Agents: <used>/<limit>
- Critics: <used>/<limit>

### Files Changed Detail

<git diff --stat output or per-file summary>

### Learnings Written This Session

<list of learnings/*.md files created/updated>

### Trajectory Audit

Signals: <N>/4 detected | Score: CLEAN / REVIEW / WARNING

| Signal | Status | Evidence |
|--------|--------|----------|
| Vagueness drift | ✓/⚠ | <specifics or "No hedging pattern detected"> |
| Scope narrowing | ✓/⚠ | <N/M subtasks, dropped items or "All accounted for"> |
| False completion | ✓/⚠ | <unverified claims or "All claims have tool evidence"> |
| Pressure response | ✓/⚠ | <panic episodes + post-episode behavior or "No episodes"> |

<If WARNING: recommendation for next session>
```

### Step 4: Notify User

After saving, output:
```
Checkpoint saved. To resume in a new session, paste this:

<the resume prompt from above>
```

## Resume From Checkpoint

When invoked with "resume" (or auto-detected at session start):

1. Read `.claude/memory/checkpoint.md`
2. If empty or missing → report "No checkpoint found"
3. If exists:
   - **Truncation boundary** (CPR-inspired): Find `## Session Detail Log` heading.
     If found, read ONLY content ABOVE that heading for resume context.
     Content below is audit-only — never loaded during resume (~60% token savings).
     If heading not found (legacy checkpoint), read entire file (backward compatible).
   - Display summary: task, progress, immediate next action
   - Ask user: "Resume from checkpoint, or start fresh?"
   - If resume: read all referenced memory files to rebuild context
   - If fresh: run `clear` (archive and delete)

## Status Check

When invoked with "status":

1. Read `.claude/memory/checkpoint.md`
2. If missing → "No checkpoint exists"
3. If exists → show: task name, save date, progress fraction, immediate next action

## Clear Checkpoint

When invoked with "clear":

1. Read `.claude/memory/checkpoint.md`
2. Append summary to `.claude/memory/state.md` under completed tasks history
3. Delete content of checkpoint.md (write empty template)

## Context Health Heuristic

This skill can be called by `/orchestrate` when it suspects context is getting large.
The heuristic signals are:

1. **Subtask progress >70%** — most of the work is behind us, context is heavy
2. **Agent spawns ≥3** — each agent result added significant context
3. **Session has been running for many exchanges** — user and assistant have gone back and forth extensively
4. **Recall degradation** — orchestrator notices it can't remember early details accurately

When auto-triggered by orchestrate, save checkpoint silently and return a one-line status
to the orchestrator (don't interrupt the user's flow).

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "Context is small enough, no need to checkpoint" | Context size doesn't predict session continuity needs. A fresh session won't know what was decided or attempted. | Checkpoint whenever subtasks exist or 3+ agents were spawned — regardless of context size. |
| "I'll just finish quickly, no checkpoint needed" | Session limits are unpredictable. A crash or timeout loses all context without checkpoint. | Checkpoint before risky operations and at natural milestones. |
| "The git history is enough to resume" | Git history captures code changes, not decisions, failed approaches, or pending subtasks. | Checkpoint captures resume prompt, state, decisions, and what NOT to do — git doesn't. |

## Red Flags

STOP and re-evaluate if any of these occur:
- Session ending without any checkpoint when subtasks exist in state.md
- Checkpoint that doesn't contain a resume prompt for the next session
- Mixing completed work from previous sessions into a new checkpoint
- Checkpoint without mentioning what was already tried and failed

## Verification Checklist

- [ ] checkpoint.md contains clear resume prompt for next session
- [ ] All pending subtasks from state.md referenced in checkpoint
- [ ] Failed approaches documented (so next session doesn't retry them)
- [ ] Decision log (decisions.md) up to date before checkpoint
- [ ] Budget state captured if orchestration was active

## Rules

1. **Resume prompt is king** — it must be self-contained. A fresh session with only that prompt and access to the files should be able to continue.
2. **Be specific** — "continue implementing feature" is useless. "Edit `.claude/skills/orchestrate/SKILL.md` line 107, add context health check after subtask completion" is useful.
3. **Don't over-save** — one checkpoint file, always overwritten. Only the latest matters.
4. **Keep checkpoint under 100 lines** — it's a summary, not a full transcript.
5. **Git state matters** — always include branch and uncommitted changes. A session that starts on the wrong branch wastes time.
