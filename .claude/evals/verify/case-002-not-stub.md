---
id: verify-002
skill: verify
title: Verifies that the critic skill is substantive (not a stub)
eval-tags: [file_operations, codebase_search]
ideal_steps: 6
ideal_tool_calls: 4
max_acceptable_steps: 11
fixture: live-repo
---

# Eval Case: Verifies that the critic skill is substantive (not a stub)

Tests that `/verify` correctly identifies a fully-implemented skill file as substantive at L2, not flagging it as a stub.

## Fixture

`live-repo` — `.claude/skills/critic/SKILL.md` is a 200+ line skill with 4-phase pipeline, scoring rubric, anti-leniency protocol, etc.

## Invocation

```
/verify .claude/skills/critic/SKILL.md
```

## Assertions

| # | Type | Check | Expected |
|---|------|-------|----------|
| A1 | contains | Output contains "Verification Report" | true |
| A2 | not_contains | Output does NOT flag as "STUB" | true |
| A3 | contains | Output shows PASS for this file | true |
| A4 | contains | Output references content evidence (mentions decomposed pipeline, phases, or scoring) | true |

## Scoring

- 4 assertions pass: PASS
- 2-3 assertions pass: PARTIAL
- 0-1 assertions pass: FAIL

## Why This Matters

L2 stub detection is a key verify capability. A well-implemented skill must not be flagged as a stub — this tests calibration of the stub detection heuristics.
