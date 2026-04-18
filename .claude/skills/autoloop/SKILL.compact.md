---
name: autoloop
variant: compact
description: Condensed autoloop for repeat invocations within session. Use full SKILL.md for first invocation.
---

# AutoLoop — Compact (Session Re-invocation)

Karpathy loop: constrain scope → define metric → iterate → keep/revert → compound gains.

## Two Modes

| Mode | Trigger | Metric |
|------|---------|--------|
| File | Target is file path | Built-in scorer or LLM-as-judge |
| Metric | `verify:<command>` | External command output |

## Iteration Loop (SEPL: ρ→σ+ι→ε→κ)

```
1. Review (ρ):    read file + TSV + git log + traces
2. Modify (σ+ι):  ONE atomic change (if needs "and" → split)
3. Commit:        git commit before verification
4. Verify (ε):    run metric (spot-check first if 5+ cases)
5. Guard (ε):     regression check if guard: configured
6. Decide (κ):    improved → keep | same/worse → discard | crash → recover
7. Log to TSV:    operator Z — trace
8. Exit check:    adaptive plateau (3→6 discards with exploration ramp)
                  or budget | max score | crash loop
```

## Adaptive Plateau (key differentiator)

| Consecutive discards | Action |
|---------------------|--------|
| 3 | exploration_weight 1.4 — try radical experiments |
| 4 | 1.7 — combine two near-misses |
| 5 | 2.0 — try opposite of all prior keeps |
| 6 | 2.0 — one last radical attempt |
| 7 | HARD STOP |

If `escalate:true` and 3 discards → trigger Escalation Phase instead.

## Critical Rules

- One change per iteration — atomic
- Never modify eval/guard files
- Confound isolation: structural ≠ prompt changes
- Simplicity override: barely improved (+<0.1%) but complex → discard
- Git is memory — read log before each iteration
- Late-phase recovery at 70% budget: revisit pruned paths
- Reward hacking: LOC >30% growth, churn cycling, spike >3x → pause

## Report

Baseline → Best (+delta) | Median (kept) | Keeps/Discards/Crashes | Exit reason
Pareto frontier if cost_metric tracked.
