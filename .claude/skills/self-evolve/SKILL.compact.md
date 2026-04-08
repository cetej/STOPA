---
name: self-evolve
variant: compact
description: Condensed self-evolve for repeat invocations within session. Use full SKILL.md for first invocation.
---

# Self-Evolve — Compact (Session Re-invocation)

Adversarial co-evolution: Curriculum (Haiku) generates hard cases, Executor (Sonnet) fixes skill.

## Setup

1. Read target `.claude/skills/<target>/SKILL.md`
2. Check `.claude/evals/<target>/` — need cases (or bootstrap:true)
3. Load meta params if meta:true (`.claude/memory/intermediate/self-evolve-meta/<target>.json`)
4. Load optstate (`.claude/memory/optstate/self-evolve.json`) — UCB1 strategy data
5. Create branch: `self-evolve/<target>`
6. Baseline eval → record pass_rate

## Co-Evolution Loop (per round)

| Step | Agent | Action |
|------|-------|--------|
| Grade | — | Run all eval cases, record pass_rate |
| Curriculum | Haiku | If <100%: FIX mode (target oldest failing). If 100%: ESCALATE (add 1-2 harder cases via UCB1 strategy) |
| Curriculum Critic | Sonnet | Score new cases ≥3/5 to accept. Max 2 retries. |
| Executor | Sonnet | Single atomic edit fixing failure. Read trace for WHERE it broke. |
| Critic Gate | /critic | Every 2 rounds. FAIL → git revert. |
| Re-Grade | — | Run all cases. Regression detection: net gain ≥2 to keep despite regressions. |
| UCB1 Update | — | Log strategy+outcome to optstate change_ledger |
| Heartbeat | — | Every 2 rounds: 2 consecutive discards → PAUSE, reflect, switch strategy |

## Circuit Breakers

- 3 consecutive reverts → STOP
- 20 eval cases reached → STOP
- Skill >500 lines → STOP
- Budget exhausted → normal exit
- Meta: 3 drops → disable meta, revert params

## Output

Report: baseline → final pass_rate, evolution log, skill diff, key findings.
Outcome record → `.claude/memory/outcomes/`.
Optstate update → `.claude/memory/optstate/self-evolve.json`.
User approves merge to main.
