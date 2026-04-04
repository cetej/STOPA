---
name: autoresearch
variant: compact
description: Condensed autoresearch for repeat invocations within session. Use full SKILL.md for first invocation.
---

# AutoResearch — Compact (Session Re-invocation)

Hypothesis-driven experiment loop: propose → implement → measure → keep/revert.

## Four Roles (strict separation)

| Role | Mutable? |
|------|----------|
| Target file | YES — edited each iteration |
| Eval command | LOCKED — never modify (invalidates history) |
| Hypotheses | Read-only direction |
| Git + TSV log | Memory — commits wins, reverts losses |

## Experiment Loop (per iteration)

```
1. Review: read TSV + git log + traces
2. Hypothesize: ONE named hypothesis with rationale + expected effect
3. Implement: single-file mutation only
4. Commit: before running eval
5. Run eval: extract scalar metric (spot-check first if >30s)
6. Evaluate: improved vs best-so-far? → keep / discard / crash
7. Reward hacking check: LOC creep >30%, churn cycling, metric spike >3x
8. Log to TSV
9. Exit check: budget | plateau (6 discards) | solved | crash loop
10. Batch ASSESS (every ceil(budget/3)):
    PROCEED → exit to synthesis
    REFINE → narrow focus on best approach
    PIVOT → rescue agent + new hypotheses
    ABORT → failure analysis
```

## Critical Rules

- One hypothesis per iteration — no bundling
- Never modify eval script
- Single-file mutation — split multi-file changes
- Confound isolation: structural changes separate from prompt changes
- 3 crashes in row → STOP
- Forced PROCEED after 2 consecutive PIVOTs

## Budget Tiers

| Tier | Experiments | Literature |
|------|-----------|-----------|
| quick | 3-5 | skip |
| standard | 8-12 | 2-3 searches |
| deep | 15-20 | full scout |
| industrial | 50-100+ | minimal |
