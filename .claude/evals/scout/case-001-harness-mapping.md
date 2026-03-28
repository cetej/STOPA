---
id: scout-001
skill: scout
title: Maps the harness infrastructure in STOPA
eval-tags: [codebase_search, file_operations]
ideal_steps: 5
ideal_tool_calls: 4
max_acceptable_steps: 10
fixture: live-repo
---

# Eval Case: Maps the harness infrastructure in STOPA

Tests that `/scout` correctly discovers and reports the harness system structure when pointed at `.claude/harnesses/`.

## Fixture

`live-repo` — STOPA repository itself. Known structure:
- `.claude/harnesses/_engine.md` (shared engine)
- `.claude/harnesses/skill-audit/HARNESS.md` (skill audit harness)
- `.claude/harnesses/skill-audit/template.md` (report template)
- `.claude/harnesses/eval-runner/HARNESS.md` (eval runner — may or may not exist at eval time)

## Invocation

```
/scout .claude/harnesses/
```

## Assertions

| # | Type | Check | Expected |
|---|------|-------|----------|
| A1 | contains | Output contains "Scout Report" heading | true |
| A2 | contains | Output mentions `_engine.md` | true |
| A3 | contains | Output mentions `skill-audit` | true |
| A4 | contains | Output describes file relationships or structure | true |
| A5 | not_contains | Output does not use Write or Edit tools (read-only) | true |

## Scoring

- 5 assertions pass: PASS
- 3-4 assertions pass: PARTIAL
- 0-2 assertions pass: FAIL

## Why This Matters

Scout's core value is discovering unknown structure. If it can't map the harness system (3-5 files, clear hierarchy), it fails at its primary job.
