---
name: Process Reward Models (PRMs)
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mom-taro-research]
tags: [orchestration, multi-agent, evaluation, reinforcement-learning]
---

# Process Reward Models (PRMs)

> Step-level scoring modely, které hodnotí každý krok procesu zvlášť (na rozdíl od outcome-only reward) — umožňují per-role evaluaci v multi-agent systémech.

## Key Facts

- Step-level scoring per role: Planner PRM (plan_coherence, assumption_validity), Executor PRM (tool_fit, parameter_correctness), Orchestrator PRM (agent_assignment, budget_efficiency) (ref: sources/mom-taro-research.md)
- Lightweight inference-time funkce — nevyžadují RL training, použitelné jako heuristiky
- arXiv:2502.10325 — formalizace step-level scoring pro role-differentiated evaluaci
- Kombinace s Best-of-N: PRM vybírá nejlepšího kandidáta bez nutnosti full critic per kandidát

## Relevance to STOPA

Navrhovaná Phase 2 implementace role-specific critic: přidat `role:` parametr do critic invokace, pak postupně implementovat per-role PRM evaluátory jako Python funkce v /critic skill.

## Mentioned In

- [MoM + TARo Research Brief](../sources/mom-taro-research.md)
