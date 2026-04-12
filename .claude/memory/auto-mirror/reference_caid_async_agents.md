---
name: CAID — Centralized Asynchronous Isolated Delegation
description: CMU framework for parallel coding agents using git worktree coordination — validates STOPA orchestrate parallelism limits
type: reference
---

# CAID (CMU, 2026-04)

Coordination framework for running multiple coding agents in parallel on complex SW engineering tasks.

## Key findings

- **Git worktree/commit/merge** = coordination primitive for multi-agent collaboration
- **+26.7%** absolute improvement on paper reproduction tasks vs single agent
- **+14.3%** on Python library development tasks
- **Optimal: 4 agents.** Performance improved 2→4, **degraded at 8** (integration overhead > parallelism benefit)
- **Delegation quality >> agent count** — imprecise task handoffs and underspecified subgoals are primary failure mode

## STOPA Validation

| CAID Finding | STOPA Status | Implication |
|-------------|-------------|-------------|
| Git worktree as primitive | `/orchestrate` uses isolation worktrees | Validated — correct architectural choice |
| 4 agents optimal, 8 degrades | `deep` tier = 5-8 agents | Consider tightening deep tier to 4-6 |
| Delegation quality matters most | Budget tier PŘED scouting | Validated — invest in plan quality, not agent count |
| Branch-and-merge with test verify | Sub-agents merge via structured integration | Add: test verification on merge step |
| Non-monotonic scaling | Circuit breaker at nesting >2 | Validated — more agents ≠ better |

## How to apply

- When orchestrating `deep` tier tasks: prefer 4 focused agents over 6-8 shallow ones
- Invest more tokens in delegation clarity (detailed subtask specs) than in agent count
- Always include test verification when merging sub-agent outputs
- CAID validates that STOPA's git-worktree isolation is the right abstraction

Paper: CMU (arXiv TBD)
