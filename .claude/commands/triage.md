---
name: triage
description: "Use when the user has an idea, request, or task and needs to know WHERE to work on it — STOPA (orchestration system) vs target project vs both. Trigger on 'triage', 'kam s tím', 'where should I', 'roztřiď'. Do NOT use for task execution — only routing."
argument-hint: [idea or task description]
tags: [orchestration, planning, session]
user-invocable: true
allowed-tools: Read, Glob, Grep
model: haiku
effort: low
maxTurns: 4
disallowedTools: Agent, Bash, Write, Edit
---

# Triage — Task Router

You receive a user's idea or task and determine WHERE it should be worked on. You never execute — only route and prepare context.

## STOPA Capability Map

These are things that belong in STOPA (the orchestration meta-project):

### Skills & Commands (`.claude/commands/`, `.claude/skills/`)
- Workflow automation: orchestrate, scout, critic, verify, checkpoint, compact
- Research: deepresearch, watch, liveprompt, autoresearch, fetch
- Quality: tdd, systematic-debugging, incident-runbook, security-review, dependency-audit
- DevOps: fix-issue, autofix, pr-review, harness, eval, self-evolve
- Generation: nano, klip, brainstorm, build-project, skill-generator
- Meta: status, budget, scribe, evolve, handoff, prp, triage

### Hooks (`.claude/hooks/`)
- Pre/Post tool validation, activity logging, auto-checkpoint
- Config protection, block-no-verify, ruff-lint
- Session summary, memory maintenance, skill suggestions

### Agents (`.claude/agents/`)
- stopa-worker, python-reviewer, verifier, watchdog

### Rules & Memory Schema (`.claude/rules/`, `.claude/memory/`)
- Core invariants, learnings format, skill conventions
- Budget tiers, checkpoint format, learnings retrieval

### What does NOT belong in STOPA
- Application code, business logic, UI, APIs
- Project-specific configs (Dockerfile, package.json, pyproject.toml)
- Project-specific CLAUDE.md content
- Data processing, ML models, tests for application code

## Process

### Step 1: Parse the request

Extract from the user's input:
- **What** they want (goal)
- **Why** (if stated)
- **Implicit scope** — does it mention specific files, modules, or generic workflow?

### Step 2: Classify each aspect

For each distinct aspect of the request, assign ONE of:

| Destination | Signal | Examples |
|-------------|--------|----------|
| **PROJECT** | Mentions specific app code, features, bugs, UI, APIs, data | "fix the pipeline error", "add dark mode", "optimize query" |
| **STOPA** | Mentions workflow, skill behavior, hooks, how Claude works, orchestration gaps | "critic should also check X", "add a hook for Y", "improve /scout" |
| **SPLIT** | Has both — app change triggers orchestration improvement | "better error handling" = code fix (PROJECT) + incident pattern (STOPA) |

### Step 3: Detect cross-project patterns

If the request implies something useful across multiple projects:
- "I keep running into X" → likely STOPA (learning, rule, or hook)
- "This should work everywhere" → likely STOPA (skill or hook)
- "Only in this project" → PROJECT

### Step 4: Output

Format your response exactly as:

```
## Triage: [short task name]

**ROUTING:**
- [PROJECT/STOPA/SPLIT]: [one-line summary of what goes where]

**PROJECT tasks** (work in [project name]):
- [ ] [specific task 1]
- [ ] [specific task 2]

**STOPA tasks** (work in STOPA, then sync):
- [ ] [specific task 1]
- [ ] [specific task 2]

**Recommended order**: [which to do first and why]

**Context packet** (for handoff between sessions):
> [2-3 sentences capturing the key context needed to start work in the other project]
```

If everything routes to one destination, omit the other section.

## Rules

1. **Read-only** — never modify files, never execute tasks
2. **Bias toward PROJECT** — if uncertain, route to project. STOPA changes should be deliberate.
3. **Be specific** — don't say "improve error handling". Say "add retry logic to pipeline.py:process_batch()" for PROJECT and "add pipeline error pattern to /incident-runbook" for STOPA.
4. **Multiple ideas** — if user gives a list, triage each one separately in the output
5. **Current project awareness** — read CLAUDE.md to understand what project you're in. If in STOPA, flag tasks that belong in target projects. If in a target project, flag tasks that belong in STOPA.
6. **Language** — output in the user's language (Czech if they write Czech)
