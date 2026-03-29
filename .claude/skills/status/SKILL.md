---
name: status
description: Use when checking current system state — active task, budget, checkpoint, last news scan, memory health. Trigger on 'status', 'what's the state', 'kde jsem', 'stav'. Do NOT use for budget details (/budget) or checkpoint management (/checkpoint).
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

You are the status reporter. You read memory files and produce a compact, machine-parseable status snapshot.

## Process

### Step 1: Read memory files

Read these files (silently, don't show contents to user):
- `.claude/memory/state.md`
- `.claude/memory/budget.md`
- `.claude/memory/checkpoint.md`
- `.claude/memory/news.md` (first 10 lines only — just need the last scan date)
- `.claude/memory/eval-baseline.tsv` (last 3 lines only — for regression trend)
- `.claude/memory/performance/*.json` — Glob for files, read last 3 by filename sort (newest first)

If any file is missing, report that field as "n/a".

### Step 2: Extract key facts

From each file, extract ONLY:

| Source | Extract |
|--------|---------|
| state.md | Active task name + subtask progress (e.g., "3/5 done") or "none" |
| budget.md | Current tier + agent spawn count from Counters table |
| checkpoint.md | Saved date + task name + status line |
| news.md | Date of last scan (from most recent entry heading) |
| eval-baseline.tsv | Last 2 data rows: compute health_score delta, format trend arrow (↑ if delta > 0.1, ↓ if < -0.1, → if within ±0.1) |
| performance/*.json | Last 3 runs: skill name, delta, exit_reason |

### Step 3: Check memory health

Use Glob to list `.claude/memory/*.md` files. For each file, read the line count.
Flag any file with **more than 400 lines** as needing maintenance.

### Step 4: Output

Print exactly this format (no extra commentary, no markdown headers):

```
task:          <active task + progress, or "none">
budget:        <tier>, <N> agent spawns
checkpoint:    <date> — <task> (<status>)
last_watch:    <date> (<N days ago>)
eval_trend:    <health_score> <arrow> (<delta> vs <previous_date>)
perf_trend:    <skill1: +delta1> | <skill2: +delta2> | ... (last 3 runs, or "no data")
memory_health: <"ok" or list of warnings>
```

For `eval_trend`: read last 2 data rows from `eval-baseline.tsv`. Compute `delta = current_health_score - previous_health_score`. Arrow: `↑` if delta > 0.1, `↓` if delta < -0.1, `→` if within ±0.1. If fewer than 2 rows: `n/a (baseline not established)`. If file missing: `n/a`.

## Rules

1. **Read-only** — never modify any file
2. **Compact output** — no explanations, no suggestions, just the status block
3. **Missing data** — use "n/a" for any field where the source file doesn't exist
4. **Date math** — calculate "N days ago" from today's date for last_watch
