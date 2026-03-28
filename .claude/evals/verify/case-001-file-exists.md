---
id: verify-001
skill: verify
title: Verifies that the harness engine file exists and is substantive
eval-tags: [file_operations, codebase_search]
ideal_steps: 7
ideal_tool_calls: 5
max_acceptable_steps: 12
fixture: live-repo
---

# Eval Case: Verifies that the harness engine file exists and is substantive

Tests that `/verify` can confirm a known-good file passes L1 (Exists) and L2 (Substantive) checks.

## Fixture

`live-repo` — `.claude/harnesses/_engine.md` is a real file with ~100+ lines of harness engine spec.

## Invocation

```
/verify .claude/harnesses/_engine.md
```

## Assertions

| # | Type | Check | Expected |
|---|------|-------|----------|
| A1 | contains | Output contains "Verification Report" | true |
| A2 | contains | Output shows PASS result (file exists and is substantive) | true |
| A3 | contains | Output references L1 or "Exists" level | true |
| A4 | contains | Output provides evidence (file size, content excerpt, or line count) | true |

## Scoring

- 4 assertions pass: PASS
- 2-3 assertions pass: PARTIAL
- 0-1 assertions pass: FAIL

## Why This Matters

The most basic verify check — does a known file exist and contain real content? If this fails, the entire verification ladder is broken.
