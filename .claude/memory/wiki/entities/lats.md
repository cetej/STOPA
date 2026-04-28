---
name: LATS
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoa-prompt-techniques, ai-planning-framework-web-agents]
last_updated: 2026-04-26
tags: [orchestration, planning, reasoning, mcts]
---

# LATS

> Zhou et al. 2023 (arXiv:2310.04406) — Language Agent Tree Search: Monte Carlo Tree Search kombinovaný s LLM reasoning a self-reflection.

## Key Facts

- 92.7% pass@1 HumanEval (GPT-4) — nejvyšší v performance hierarchii (ref: sources/egoa-prompt-techniques.md)
- Performance hierarchie: LATS > Reflexion > ReAct > ToT > Self-Consistency > CoT
- Kombinuje MCTS branching s Reflexion self-reflection na každém uzlu
- Nejblíže k akademickému ekvivalentu STOPA deep tier orchestrace s branching

## Relevance to STOPA

Inspirace pro STOPA deep tier: branch exploration před lineárním 3-fix escalation. LATS-lite verze = zkus 2-3 různé přístupy paralelně (fork agents), vyhodnoť výsledky, pak implementuj nejlepší — odpovídá Best-of-N rollout vzoru.

- MCTS tree search efektivní na tool planning (+3-10pp), ale UNDERPERFORMUJE na WebArena vs linear AgentOccam (39.2% Plan-MCTS vs 45.7% AgentOccam) — doménová závislost (ref: sources/ai-planning-framework-web-agents.md)
- ToolTree §6: LATS citován jako kanonický "MCTS pro language agenty" (ref: sources/ai-planning-framework-web-agents.md)

## Mentioned In

- [EgoAlpha/prompt-in-context-learning Research Brief](../sources/egoa-prompt-techniques.md)
- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)
