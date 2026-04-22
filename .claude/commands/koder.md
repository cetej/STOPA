---
name: koder
description: "Use when delegating a coding task to KODER execution agent. Trigger on 'assign to koder', 'koder fix', 'koder task'. NOT for strategic decisions or research — only execution tasks (code, tests, fixes, refactoring)."
user-invocable: true
phase: build
tags: [orchestration, code-quality, testing]
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Agent]
permission-tier: full-access
input-contract: "user → task description + target project → non-empty"
output-contract: "task file → markdown → .claude/tasks/koder-queue/<id>.md + dispatched agent"
---

# /koder — Dispatch Task to KODER

You create a task for KODER and optionally dispatch it immediately.

## Process

### Step 1: Parse Input

Parse `<args>`:
- If args contains a project name (NG-ROBOT, ADOBE-AUTOMAT, test1, ZACHVEV, POLYBOT, BONANZA, DANE, KARTOGRAF, MONITOR, GRAFIK): set as target project
- If no project specified: ask which project
- Remaining text = task description

### Step 2: Create Task File

Generate task ID: `T-<date>-<NNN>` where NNN is next sequential number.

Read `koder/templates/task-template.md` for format reference.

Write task file to `.claude/tasks/koder-queue/<id>.md` with:
- Filled YAML frontmatter (id, date, priority, project path, status: pending)
- Clear task description from user input
- Acceptance criteria (infer from task type, ask user if unclear)
- Context: grep relevant learnings, check recent failures for the project
- Constraints: default to light budget, no new deps; koder must follow `.claude/rules/code-editing-examples.md` Rule 3 — every diff line must trace to task requirements (no "while I'm here" improvements)

### Step 3: Dispatch (optional)

If user said "now", "run", "dispatch" or task is priority=critical:
- Spawn KODER agent with `subagent_type: "koder"`
- Pass task file content as prompt
- Update task status to `in_progress`

If not dispatching immediately:
- Report: "Task <id> created in queue. Run `/koder dispatch <id>` to execute."

### Step 4: Dispatch Subcommand

If args starts with "dispatch <id>":
- Read task file from queue
- Spawn KODER agent
- Update task status

If args starts with "list":
- Glob `.claude/tasks/koder-queue/*.md`
- Show table: id, project, priority, status, created date

If args starts with "done" or "review":
- Glob `.claude/memory/outcomes/*-koder-*.md` (last 5)
- Show outcomes summary table

## Project Path Map

| Name | Path |
|------|------|
| NG-ROBOT | C:/Users/stock/Documents/000_NGM/NG-ROBOT |
| ADOBE-AUTOMAT | C:/Users/stock/Documents/000_NGM/ADOBE-AUTOMAT |
| test1 | C:/Users/stock/Documents/test1 |
| ZACHVEV | C:/Users/stock/Documents/000_NGM/ZACHVEV |
| POLYBOT | C:/Users/stock/Documents/000_NGM/POLYBOT |
| BONANZA | C:/Users/stock/Documents/000_NGM/BONANZA |
| DANE | C:/Users/stock/Documents/000_NGM/DANE |
| KARTOGRAF | C:/Users/stock/Documents/000_NGM/KARTOGRAF |
| MONITOR | C:/Users/stock/Documents/000_NGM/MONITOR |
| GRAFIK | C:/Users/stock/Documents/000_NGM/GRAFIK |
| STOPA | C:/Users/stock/Documents/000_NGM/STOPA |

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll just do this task myself, it's simple" | KODER exists to build outcome history — every task through KODER generates measurable signal | Create the task file, dispatch KODER |
| "No need for acceptance criteria, it's obvious" | Vague criteria = unmeasurable outcomes = broken feedback loop | Write at least 2 specific, verifiable criteria |
| "I'll add some extra improvements to the task" | Scope creep makes outcomes unmeasurable and wastes budget | One task = one clear objective |

## Red Flags

STOP and re-evaluate if any of these occur:
- Task description is vague ("fix stuff in NG-ROBOT")
- No acceptance criteria defined
- Task requires strategic decisions (→ use STOPA orchestrate instead)
- Dispatching to wrong project path

## Rules

1. Every task gets a file in the queue — no verbal-only delegation
2. Acceptance criteria are mandatory — minimum 2 items
3. Don't mix multiple unrelated changes in one task
4. Reference relevant learnings when they exist
5. Default budget: light. Upgrade only for multi-file tasks.
