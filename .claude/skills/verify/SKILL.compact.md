---
name: verify
variant: compact
description: Condensed verify for repeat invocations within session. Use full SKILL.md for first invocation.
---

# Verify — Compact (Session Re-invocation)

Prove things work on real data. Run real commands, show real output, report PASS/FAIL with evidence.

## Two Modes

| Mode | Trigger | Flow |
|------|---------|------|
| Standard | pipeline, api, last changes, file | Steps 1-6 below |
| Source verification | `--sources <file>` | Citation check: URL liveness + claim-source alignment |

## Verification Loop

1. **Understand target** — parse ARGUMENTS, determine scope
2. **Read context** — CLAUDE.md, state.md, existing tests. Form hypothesis: "I expect X because Y."
3. **Deterministic scan** — run ALL available checks (imports, type check, lint, tests, build, API health). Collect ALL results before interpreting.
4. **Atomic claim decomposition** — for complex changes (3+ files): list every discrete behavioral assertion, map each to one verifiable check
5. **Milestone extraction** — 3-7 milestones from user perspective, each with assignment goal (specific pass/fail criterion)
6. **Verification plan** — map milestones to levels: L1 Exists | L2 Substantive | L3 Wired | L4 Flows
7. **Execute** — milestone by milestone (M1 fully before M2). Capture: PASS/FAIL/STUB/SKIP with evidence.
8. **Report** — table with check | level | result | evidence

## Verification Levels

| Level | Check | Stub patterns to catch |
|-------|-------|------------------------|
| L1 | File/endpoint exists | — |
| L2 | Not a stub, real logic | `return []`, `return null`, `TODO`, `pass` |
| L3 | Imported and used, not orphaned | Missing route registration |
| L4 | Real data reaches output | Hardcoded empty responses |

## Circuit Breakers

- NEVER modify code — observe and report only
- NEVER claim "done" from exit code alone — verify output content
- NEVER skip L3-L4 because L2 passed (schema compliance != downstream utility)
- NEVER report PASS from a single test case
- If no deterministic checks exist: note as risk, proceed to milestones

## Report Format

```
## Verification Report
Target: <what>  Result: PASS / PARTIAL / FAIL
| # | Check | Level | Result | Evidence |
Issues Found: (list stubs and problems)
Recommendations: (suggested fixes, not implementations)
```

After completion: update state.md. If FAIL: write learning to `learnings/`.
