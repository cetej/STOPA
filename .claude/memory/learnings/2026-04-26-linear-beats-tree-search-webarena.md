---
date: 2026-04-26
type: best_practice
severity: high
component: orchestration
tags: [orchestration, planning, search, evaluation, budget]
summary: "Na WebArena (noisy web actions) AgentOccam (linear, 45.7%) bije všechny tree-search baselines. Zavést search do orchestrace až když linear pipeline dosáhla plateau. Tree search pomáhá pouze u typed I/O (tool planning)."
source: external_research
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.85
maturity: draft
verify_check: "manual"
skill_scope: [orchestrate]
task_context:
  task_class: research
  complexity: medium
  tier: standard
---

# Linear Well-Tuned Beats Naive Tree Search (WebArena domain)

## Finding

Plan-MCTS (arXiv:2602.14083) Table 1 WebArena leaderboard:
- AgentOccam (linear, GPT-4-Turbo): **45.7%** — nejsilnější baseline
- Plan-MCTS (plan-space MCTS): 39.2%
- WebPilot (MCTS multi-agent): 37.2%
- Koh 2024 Best-First Search: **19.2%** — nejhorší search method

## Doménová závislost

- Noisy action space (web GUI, arbitrary HTML) → linear bije tree search
- Typed I/O (API tool calls, structured schemas) → ToolTree +3-10pp přes greedy

## STOPA pravidlo

**Prerequisite pro zavedení search do `/orchestrate`:** dokažte že linear pipeline je v plateau (opakované běhy, stable score, marginal improvement).

STOPA's linear orchestration pipeline je architekturálně správně. Nevylepšovat zavedením MCTS bez empirické evidence plateau.

## Evidence

- arXiv:2602.14083 Table 1 — přímý read v reading agentovi deepresearch pipeline
