---
id: scout-002
skill: scout
title: Inventories the skills directory and reports coverage
eval-tags: [codebase_search, file_operations]
ideal_steps: 4
ideal_tool_calls: 3
max_acceptable_steps: 8
fixture: live-repo
---

# Eval Case: Inventories the skills directory and reports coverage

Tests that `/scout` can enumerate skills and provide a meaningful overview of the skill system.

## Fixture

`live-repo` — STOPA repository. Known: `.claude/skills/` contains 15+ skill subdirectories, each with a `SKILL.md`.

## Invocation

```
/scout .claude/skills/
```

## Assertions

| # | Type | Check | Expected |
|---|------|-------|----------|
| A1 | contains | Output contains "Scout Report" heading | true |
| A2 | count | Output references at least 10 skill names | >= 10 |
| A3 | contains | Output mentions at least one skill by name (critic, scout, verify, orchestrate) | true |
| A4 | contains | Output describes patterns or conventions observed | true |

## Scoring

- 4 assertions pass: PASS
- 2-3 assertions pass: PARTIAL
- 0-1 assertions pass: FAIL

## Why This Matters

Skill inventory is a common pre-task step. Scout must handle directories with many subdirectories efficiently and report a useful summary, not just a file listing.
