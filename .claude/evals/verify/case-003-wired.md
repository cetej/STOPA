---
id: verify-003
skill: verify
title: Verifies that the scout skill is wired (referenced by other components)
eval-tags: [codebase_search, file_operations]
ideal_steps: 8
ideal_tool_calls: 6
max_acceptable_steps: 13
fixture: live-repo
---

# Eval Case: Verifies that the scout skill is wired (referenced by other components)

Tests that `/verify` can trace L3 (Wired) — that scout is not orphaned but actively referenced by other skills, CLAUDE.md, or orchestration.

## Fixture

`live-repo` — `.claude/skills/scout/SKILL.md` is referenced in:
- `CLAUDE.md` (skill tiers)
- `.claude/rules/skill-tiers.md` (Tier 1)
- Other skills' handoff sections (e.g., orchestrate → scout)
- Eval cases in `.claude/evals/scout/`

## Invocation

```
/verify .claude/skills/scout/SKILL.md
```

## Assertions

| # | Type | Check | Expected |
|---|------|-------|----------|
| A1 | contains | Output contains "Verification Report" | true |
| A2 | contains | Output mentions L3 or "Wired" level | true |
| A3 | contains | Output cites at least one file that references scout | true |
| A4 | contains | Result is PASS or PARTIAL (scout IS wired) | true |

## Scoring

- 4 assertions pass: PASS
- 2-3 assertions pass: PARTIAL
- 0-1 assertions pass: FAIL

## Why This Matters

L3 Wired checks prevent orphaned code. If verify can't trace that a Tier 1 skill is actively used by the orchestration system, it misses the most important integration test.
