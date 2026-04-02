---
name: checkpoint
description: Use when ending a session or saving progress. Trigger on checkpoint, save progress, continue later. Do NOT use mid-task when work is incomplete.
context:
  - gotchas.md
argument-hint: [save / resume / status]
tags: [session, memory]
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

Write to `.claude/memory/checkpoint.md`:

```markdown
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

## Git State

- Branch: <branch>
- Uncommitted changes: <yes/no — if yes, list files>
- Last commit: <hash + message>

## Budget State

- Tier: <tier>
- Agents: <used>/<limit>
- Critics: <used>/<limit>

## Resume Prompt

> <A complete, self-contained prompt that can be given to a fresh
>  Claude session. It should include:
>  1. The overall goal
>  2. Current state (what's done, what's not)
>  3. The immediate next action
>  4. Any critical constraints or decisions
>  5. Reference to files: CLAUDE.md, .claude/memory/state.md,
>     .claude/memory/checkpoint.md
>  Write in English (for Claude). Keep under 300 words.>
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

## Rules

1. **Resume prompt is king** — it must be self-contained. A fresh session with only that prompt and access to the files should be able to continue.
2. **Be specific** — "continue implementing feature" is useless. "Edit `.claude/skills/orchestrate/SKILL.md` line 107, add context health check after subtask completion" is useful.
3. **Don't over-save** — one checkpoint file, always overwritten. Only the latest matters.
4. **Keep checkpoint under 100 lines** — it's a summary, not a full transcript.
5. **Git state matters** — always include branch and uncommitted changes. A session that starts on the wrong branch wastes time.
