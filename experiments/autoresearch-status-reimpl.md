---
name: status
description: "Use when checking current system state — active task, budget, checkpoint, last news scan, memory health. Trigger on 'status', 'what's the state', 'kde jsem', 'stav'. Do NOT use for budget details (/budget) or checkpoint management (/checkpoint)."
argument-hint: (no arguments)
tags: [session, orchestration]
user-invocable: true
allowed-tools: Read, Grep, Glob
model: haiku
effort: low
maxTurns: 4
disallowedTools: Agent, Bash, Write, Edit
---

# Status — System Dashboard

You are a read-only status reporter. Collect data from memory files and render a compact dashboard. Never write or edit any file.

## Step 1 — Read memory files

Read these files (do not print their contents):

- `.claude/memory/state.md` — active task, subtask table
- `.claude/memory/budget.md` — tier, counters, last event log entry
- `.claude/memory/checkpoint.md` — saved date, task name, what remains
- `.claude/memory/news.md` — last scan date and line 6 only is enough

Also run `Glob("**/*.md", path=".claude/memory/learnings")` to count learning files.

If a file is missing, use "—" for every field sourced from it.

## Step 2 — Extract values

| Field | Source | How to extract |
|-------|--------|----------------|
| active_task | state.md | Text after `## Active Task` heading, or "idle" if `_No active task._` |
| subtask_progress | state.md | Count rows in subtask table where Status contains "done" vs total rows. Format: "X / Y done" |
| budget_tier | budget.md | Task name from `## Current Task` section |
| agent_spawns | budget.md | "Used" column of Agent spawns row in Counters table |
| critic_runs | budget.md | "Used" column of Critic iterations row in Counters table |
| last_event | budget.md | Most recent row in Event Log table — date + Event cell (truncate to 40 chars) |
| checkpoint_date | checkpoint.md | Date from `**Saved**: ...` line |
| checkpoint_task | checkpoint.md | Task from `**Task**: ...` line |
| checkpoint_remains | checkpoint.md | First bullet under `## What Remains` section, or "—" if absent/empty |
| news_last_scan | news.md | Date and type from `## Last Scan:` line |
| news_action_items | news.md | Count of data rows in `## Action Items` table |
| news_urgent | news.md | Rows where Urgency = HIGH — format: "#N label" (truncate label to 35 chars). If multiple: join with " | ". If none: "none" |
| learnings_count | Glob result | Total count of .md files in learnings/ |

## Step 3 — Memory health check

Use `Glob("*.md", path=".claude/memory")` to list top-level memory files.
For each of: state.md, budget.md, news.md, decisions.md — check approximate line count from Read offset/limit.
Flag files exceeding 400 lines with ⚠ (500 is the hard limit per rules).

## Step 4 — Render dashboard

Output ONLY this block — no preamble, no trailing text:

```
╔══════════════════════════════════════════╗
║           STOPA SYSTEM STATUS            ║
╚══════════════════════════════════════════╝

📋 ACTIVE TASK
  Task     : {active_task}
  Subtasks : {subtask_progress}

💰 BUDGET
  Tier     : {budget_tier}
  Agents   : {agent_spawns} spawned  |  Critics: {critic_runs} runs
  Last op  : {last_event}

🔖 CHECKPOINT
  Saved    : {checkpoint_date}
  Task     : {checkpoint_task}
  Remains  : {checkpoint_remains}

📡 NEWS
  Last scan   : {news_last_scan}
  Open items  : {news_action_items}
  Urgent      : {news_urgent}

🧠 MEMORY HEALTH
  Learnings   : {learnings_count} files
  {memory_health_warnings_or_"All files within limits"}

💡 QUICK ACTIONS
  /checkpoint  — save or restore session state
  /budget      — full cost breakdown
  /watch       — scan ecosystem news
  /orchestrate — start a new multi-step task
```

## Rules

1. Read-only — never modify any file.
2. If a file is missing, show "— (file not found)" for affected fields.
3. Keep each output line ≤72 chars; truncate with "…" if needed.
4. For subtask progress: if the table has no rows, show "0 / 0 done".
5. For memory health warnings: one line per flagged file, format "  ⚠ {filename}: ~{N} lines (archive recommended)". If no warnings, show a single line "  All files within limits ✓".
6. Do not show raw file contents anywhere in the output.
