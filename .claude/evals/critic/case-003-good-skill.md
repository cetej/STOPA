---
id: critic-003
skill: critic
title: Does not over-penalize a well-formed skill
eval-tags: [quality_review, file_operations]
ideal_steps: 7
ideal_tool_calls: 5
max_acceptable_steps: 13
fixture: inline
---

# Eval Case: Does not over-penalize a well-formed skill

Tests that `/critic` gives a fair assessment (PASS or WARN, not FAIL) to a properly constructed skill. Validates anti-false-positive behavior.

## Fixture

Write this content to `.harness/eval-fixtures/critic-003-fixture.md` before invocation:

```markdown
---
name: handoff
description: Use when capturing findings from completed sessions (especially remote/mobile) into persistent memory. Trigger on 'handoff', 'capture findings'. Do NOT use for active session checkpoints (/checkpoint).
argument-hint: [source — session description, findings text, or 'from clipboard']
user-invocable: true
allowed-tools: Read, Write, Glob, Grep
model: haiku
effort: low
maxTurns: 6
disallowedTools: Agent, Bash, Edit
---

# Handoff — Session Findings Capture

You capture knowledge from completed work sessions into persistent memory files.

## Error Handling

- Source text is empty or too short (<50 chars): Ask user to provide more context
- Memory file doesn't exist: Create it with appropriate structure
- Memory file over 400 lines: Archive old entries first, then append

## Process

### Step 1: Parse source
Read the provided findings. Extract: decisions made, patterns discovered, problems encountered, solutions applied.

### Step 2: Categorize
Classify each finding by type: decision, learning, bug_fix, architecture, workflow.

### Step 3: Write to memory
- Decisions -> `.claude/memory/decisions.md`
- Learnings -> `.claude/memory/learnings/<date>-<desc>.md` with YAML frontmatter
- Bugs -> `docs/TROUBLESHOOTING.md` (if exists)

### Step 4: Confirm
Output a summary of what was captured and where it was written.

## Output Format

```
## Handoff Summary
- Decisions captured: N -> decisions.md
- Learnings captured: N -> learnings/
- Bugs documented: N -> TROUBLESHOOTING.md
```

## Rules

1. Never overwrite existing memory entries — always append or create new files
2. Always include date in learnings filenames
3. Keep entries concise — max 20 lines per learning
```

## Invocation

```
/critic .harness/eval-fixtures/critic-003-fixture.md
```

## Assertions

| # | Type | Check | Expected |
|---|------|-------|----------|
| A1 | contains | Verdict is "PASS" or "WARN" (not "FAIL") | true |
| A2 | contains | Output has "What's Good" or positive feedback section | true |
| A3 | range | Weighted average score >= 3.0 | true |
| A4 | not_contains | Output does not flag "vague description" or "missing error handling" | true |

## Scoring

- 4 assertions pass: PASS
- 2-3 assertions pass: PARTIAL
- 0-1 assertions pass: FAIL

## Why This Matters

A critic that FAIL-s good code is as problematic as one that PASS-es bad code. This tests calibration — the critic should recognize quality when it sees it.
