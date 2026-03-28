---
id: critic-001
skill: critic
title: Catches deliberate flaws in a synthetic skill file
eval-tags: [quality_review, file_operations]
ideal_steps: 8
ideal_tool_calls: 5
max_acceptable_steps: 14
fixture: inline
---

# Eval Case: Catches deliberate flaws in a synthetic skill file

Tests that `/critic` identifies real problems in a poorly constructed SKILL.md — vague description, missing error handling, no memory integration, over-permissioned tools.

## Fixture

Write this content to `.harness/eval-fixtures/critic-001-fixture.md` before invocation:

```markdown
---
name: data-fetcher
description: This is a useful skill for fetching various kinds of data from different sources.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Agent, Glob, Grep
model: opus
effort: high
maxTurns: 25
---

# Data Fetcher

You fetch data. Do whatever the user asks.

## Process

1. Read the user's request
2. Fetch the data
3. Return the result

## Output

Return the data in a useful format.
```

## Invocation

```
/critic .harness/eval-fixtures/critic-001-fixture.md
```

## Assertions

| # | Type | Check | Expected |
|---|------|-------|----------|
| A1 | not_contains | Verdict is "PASS" | false — flaws should prevent PASS |
| A2 | contains | Output contains "WARN" or "FAIL" | true |
| A3 | contains | Output mentions severity level (high, medium, low) | true |
| A4 | contains | Output has milestone or scoring section | true |
| A5 | contains | Output flags description quality (vague, generic, "useful") | true |
| A6 | contains | Output flags over-permission (opus for simple task, too many tools) | true |

## Scoring

- 5-6 assertions pass: PASS
- 3-4 assertions pass: PARTIAL
- 0-2 assertions pass: FAIL

## Why This Matters

A critic that gives PASS to a vague, over-permissioned skill with no error handling is not doing its job. This is the most basic quality gate test.
