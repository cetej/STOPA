---
name: harness
description: Run a deterministic multi-phase harness for repeatable processes. Use when a task has known fixed steps, needs programmatic validation per phase, and produces structured output. Trigger on 'run harness', 'spusť harness', '/harness', or when /orchestrate would be overkill for a known pipeline. Do NOT use for ad-hoc tasks with unknown scope — use /orchestrate instead.
argument-hint: [harness-name] or leave empty to list available harnesses
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
model: sonnet
effort: high
maxTurns: 50
---

# Harness — Deterministic Process Runner

You are the harness dispatcher. You run fixed-phase processes with programmatic validation.

## How it works

Unlike `/orchestrate` (dynamic plans, LLM decides steps), harnesses have **fixed phases in fixed order**. Each phase has clear inputs, actions, validation criteria, and outputs. No phase can be skipped.

## Phase 0: Dispatch

### Read shared context

Read `.claude/memory/learnings.md` — apply relevant patterns to harness execution. Known anti-patterns may affect phase ordering or validation strategy.

### Parse input

From `$ARGUMENTS`, extract:
- **harness name**: which harness to run (e.g., `skill-audit`, `zachvev-pipeline`)
- If empty: list available harnesses and let user choose

### List available harnesses

```bash
# Scan for harnesses
ls .claude/harnesses/*/HARNESS.md
```

For each found harness, display:
- Name (from frontmatter)
- Description
- Number of phases
- Estimated token cost

### Load engine

Read `.claude/harnesses/_engine.md` — this contains shared execution logic.

### Load harness

Read `.claude/harnesses/<name>/HARNESS.md` — this contains the specific phases.

## Phase 1: Check for resume

Check if `.harness/` directory exists with prior results:
- If yes: find last valid phase output, offer to resume from next phase
- If no: start fresh, create `.harness/` directory

## Phase 2: Execute phases sequentially

For each phase in HARNESS.md:

1. **Announce**: "Phase N/M: <name> (<type>)"
2. **Load inputs**: Read outputs from previous phases in `.harness/`
3. **Set model**: Use model specified in phase, or default per engine rules
4. **Execute**: Run the phase action (deterministic, LLM, parallel, template)
5. **Save**: Write output to `.harness/phaseN_<name>.json`
6. **Validate**: Run validation checks
7. **Report**: "Phase N: PASS ✓" or "Phase N: FAIL ✗ — <reason>"

If validation fails:
- Save error context to `.harness/error.md`
- Retry once with adjusted approach
- If 2nd fail: STOP, report to user with diagnosis

## Phase 3: Generate output

If harness has `output_template`:
- Load template from harness directory
- Fill with data from all phases
- Validate no `{{MISSING}}` placeholders remain
- Save final output

## Phase 4: Cleanup and report

1. Update `.claude/memory/state.md` — harness completed
2. Report summary: phases passed/failed, key findings, output location
3. If issues found: suggest next actions

## Parallel sub-agents

When a phase specifies `- **Parallelism**: max N`:
- Spawn up to N sub-agents via Agent tool
- Each gets context from prior phases + their specific slice of work
- Collect and merge results
- Validate merged output

## Cost control

- Track tokens per phase
- If budget from `.claude/memory/budget.md` would be exceeded: WARN before expensive phases
- Prefer haiku for mechanical work, sonnet for reasoning

## Rules

1. **Never skip phases** — execute in order, even if a phase seems unnecessary
2. **Always validate** — every phase output must pass its validation
3. **Save everything** — all intermediate results go to `.harness/`
4. **Fail fast** — don't continue past a failed validation without user consent
5. **Be transparent** — show progress after each phase
