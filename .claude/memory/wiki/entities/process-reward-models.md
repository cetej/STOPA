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
- **PRM vs ORM** (arXiv:2501.09686): PRM poskytuje dense step-wise rewards → credit assignment (ví KDE selhání nastalo), ORM jen sparse finální odměna → pozdní detekce chyb
- **Best-of-N + PRM**: generuj N kandidátů, score každý krok PRM-em, vyber nejlepšího — konzistentně překonává single-sample + iterativní opravy
- **Test-time scaling**: PRM-guided search umožňuje škálovat inference compute pro lepší výsledky (nový scaling zákon nezávislý na pretraining)

## Relevance to STOPA

1. **Step-level checkpoints v orchestrate**: haiku agent po každém subtasku ověří "splnil krok plán?" → PASS/WARN/FAIL → early kill při FAIL (šetří budget)
2. **Role-specific critic**: přidat `role:` parametr do critic invokace, per-role PRM evaluátory
3. **Best-of-N v autoloop**: paralelní kandidáti + lightweight PRM scoring místo lineární iterace
4. **Self-consistency voting**: deep tier = 3× critic run, majority vote (test-time scaling)

## Mentioned In

- [MoM + TARo Research Brief](../sources/mom-taro-research.md)
- [Reinforced Reasoning Survey](../concepts/reinforced-reasoning.md)
