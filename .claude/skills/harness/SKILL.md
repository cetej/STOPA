---
name: harness
description: Use when running a deterministic multi-step process that must complete reliably. Trigger on 'harness', 'run pipeline', 'deterministic process'. Do NOT use for exploratory tasks or one-shot edits.
argument-hint: <pipeline name or description> [--dry-run]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
model: sonnet
effort: high
maxTurns: 30
---

# Harness — Deterministic Process Runner

You run multi-step pipelines where each phase has explicit deliverables, success criteria, and rollback points. Inspired by Anthropic's harness design pattern (generator/evaluator separation).

## Core Principle

**Sprint contracts, not open-ended loops.** Each phase defines WHAT must be delivered, HOW to verify it, and WHAT to do if it fails.

## Shared Memory

1. Read `.claude/memory/budget.md` — check current tier and remaining budget
2. Grep `.claude/memory/learnings/` for the pipeline topic — past failures inform current run

## Process

### Phase 0: Define the Pipeline

Parse `$ARGUMENTS` to determine the pipeline. If not clear, ask the user.

Create a **Pipeline Contract**:

```markdown
## Pipeline: <name>
**Phases**: N
**Estimated cost**: <tier>
**Rollback strategy**: git branch / file backup

| Phase | Deliverable | Success Criteria | Timeout |
|-------|-------------|------------------|---------|
| 1 | ... | ... | N turns |
| 2 | ... | ... | N turns |
```

### Phase N: Execute

For each phase in the pipeline:

1. **Announce**: "Phase N: <deliverable>"
2. **Execute**: Do the work (directly or via Agent with model: haiku)
3. **Verify**: Check success criteria — not "looks good" but measurable checks
4. **Gate**:
   - PASS → proceed to next phase
   - FAIL → attempt ONE fix, then re-verify
   - FAIL twice → STOP, report to user, suggest rollback

### Final: Report

```markdown
## Harness Report: <pipeline>

| Phase | Status | Deliverable | Attempts |
|-------|--------|-------------|----------|
| 1 | PASS | ... | 1 |
| 2 | PASS | ... | 2 (1 retry) |
| 3 | FAIL | ... | 2 (stopped) |

**Result**: N/M phases completed
**Rollback**: <branch name or backup location>
```

## Anti-Leniency Protocol

The evaluator (verification step) MUST be strict:
- "It compiles" is NOT a pass criterion for code quality
- "No errors in output" is NOT sufficient — check for expected positive signals
- If success criteria are vague, make them concrete BEFORE executing

## Error Handling

- Phase timeout (too many turns without progress) → STOP that phase, report
- Budget exceeded mid-pipeline → checkpoint progress, ask user
- Git conflict or file lock → retry once with 2s delay, then report

## Circuit Breakers

- Same phase fails 2× → STOP
- Total pipeline exceeds budget tier → STOP
- Agent spawned 3× for same subtask → STOP

## Rules

1. **Contract first** — never start executing without a pipeline contract
2. **Verify, don't trust** — every phase must have measurable success criteria
3. **Fail fast** — 2 failures = stop, don't burn tokens hoping
4. **Log everything** — each phase outcome recorded for learning
5. **Rollback ready** — always know how to undo the current phase
