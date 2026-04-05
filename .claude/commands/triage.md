---
name: triage
description: "Use when the user has an idea, request, or task and needs to know WHERE to work on it, or when the right skill is ambiguous. Trigger on 'triage', 'kam s tím', 'where should I', 'roztřiď', 'not sure which skill'. Do NOT use for task execution — only routing and skill selection."
argument-hint: [idea or task description]
tags: [orchestration, planning, session]
phase: define
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

<!-- CACHE_BOUNDARY -->

## Process

### Step 1: Parse the request

Extract from the user's input:
- **What** they want (goal)
- **Why** (if stated)
- **Implicit scope** — does it mention specific files, modules, or generic workflow?

### Step 1.5: Self-Discover Reasoning Module Selection (arXiv:2402.03620)

Before routing to a skill, identify which **reasoning modules** the task requires. Self-Discover shows that dynamically composing reasoning structures from atomic modules outperforms fixed approaches by +32% at 10-40× less compute than Self-Consistency.

Atomic reasoning modules available:
- **Step-by-step** — decomposition, sequential logic → /orchestrate, /systematic-debugging
- **Comparison** — evaluate alternatives side-by-side → /council, /deepresearch (comparison scale)
- **Search** — find information in codebase or web → /scout, /deepresearch
- **Verification** — prove correctness with evidence → /verify, /critic
- **Generation** — create new artifacts → /nano, /klip, /build-project
- **Reflection** — evaluate own work quality → /critic, /self-evolve, /autoreason

**Classify**: Which 1-2 modules does this task primarily need? This narrows skill selection and informs the recommended approach. Include the module(s) in Step 4 output as `**Reasoning modules:** [module1, module2]`.

### Step 2: Classify each aspect

For each distinct aspect of the request, assign ONE of:

| Destination | Signal | Examples |
|-------------|--------|----------|
| **PROJECT** | Mentions specific app code, features, bugs, UI, APIs, data | "fix the pipeline error", "add dark mode", "optimize query" |
| **STOPA** | Mentions workflow, skill behavior, hooks, how Claude works, orchestration gaps | "critic should also check X", "add a hook for Y", "improve /scout" |
| **SPLIT** | Has both — app change triggers orchestration improvement | "better error handling" = code fix (PROJECT) + incident pattern (STOPA) |

### Step 2b: Classify query type (StructRAG-inspired)

Assign ONE query type based on the task's nature — this determines the optimal representace and skill:

| Query Type | Signal | Optimal Representace | Primary Skill(s) |
|-----------|--------|---------------------|-------------------|
| `explore` | "jak funguje", "co je", "prozkoumej", "ukaž kód" | Codebase traversal | /scout |
| `build` | "přidej", "implementuj", "vytvoř", "postav" | Task decomposition | /orchestrate, /build-project |
| `fix` | "oprav", "nefunguje", "bug", "error", "spadlo" | Root cause tree | /fix-issue, /systematic-debugging, /incident-runbook |
| `research` | "zjisti", "porovnej", "overview", "prozkoumej web" | Evidence table | /deepresearch, /watch |
| `review` | "zkontroluj", "review", "audit", "kvalita" | Multi-perspective | /critic, /pr-review, /security-review |
| `generate` | "vygeneruj", "obrázek", "video", "prezentace" | Media pipeline | /nano, /klip |
| `meta` | "vylepši skill", "evolve", "status", "hook" | Self-referential | /self-evolve, /evolve, /skill-generator |

**Disambiguation rules:**
- "prozkoumej" + local codebase → `explore` (/scout); "prozkoumej" + external topic → `research` (/deepresearch)
- "nefunguje" + known error → `fix` (/systematic-debugging); "nefunguje" + sudden crash → `fix` (/incident-runbook)
- If task spans 2 types: pick the PRIMARY type, note the secondary in output

### Step 3: Detect cross-project patterns

If the request implies something useful across multiple projects:
- "I keep running into X" → likely STOPA (learning, rule, or hook)
- "This should work everywhere" → likely STOPA (skill or hook)
- "Only in this project" → PROJECT

### Step 4: Output

Format your response exactly as:

```
## Triage: [short task name]

**ROUTING:** [PROJECT/STOPA/SPLIT] — [one-line summary]
**Query type:** [explore | build | fix | research | review | generate | meta]
**Recommended skill:** /skill-name — [one-line reason why this skill fits]

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

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I already know which skill fits, no need to triage" | Assumption bias — the obvious skill may not be the best. Triage catches cross-project routing and multi-skill compositions. | Run triage anyway — it takes <30s and prevents wasted effort on wrong skill. |
| "This is too simple for triage, just do it directly" | Simple-looking tasks often span multiple projects or need orchestration. Skipping triage means skipping routing. | If in doubt, triage. The cost of wrong routing is a wasted session. |
| "The user said which skill to use, so I'll skip triage" | User may not know the full skill catalog or that their task crosses project boundaries. | Triage confirms user's choice AND checks for project routing — both matter. |

## Red Flags

STOP and re-evaluate if any of these occur:
- Starting orchestrate or fix-issue without knowing which project to work in
- Editing files in STOPA when the task belongs to a target project (or vice versa)
- Running a skill that doesn't match the task's actual needs
- Ignoring project routing entirely and working in the wrong directory

## Verification Checklist

- [ ] Task routed to correct project (STOPA vs target vs both)
- [ ] Recommended skill(s) identified with rationale
- [ ] If multi-project: split plan documented before execution
- [ ] User informed of routing decision (not silently assumed)

## Rules

1. **Read-only** — never modify files, never execute tasks
2. **Bias toward PROJECT** — if uncertain, route to project. STOPA changes should be deliberate.
3. **Be specific** — don't say "improve error handling". Say "add retry logic to pipeline.py:process_batch()" for PROJECT and "add pipeline error pattern to /incident-runbook" for STOPA.
4. **Multiple ideas** — if user gives a list, triage each one separately in the output
5. **Current project awareness** — read CLAUDE.md to understand what project you're in. If in STOPA, flag tasks that belong in target projects. If in a target project, flag tasks that belong in STOPA.
6. **Language** — output in the user's language (Czech if they write Czech)
