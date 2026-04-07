---
name: LATS
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoa-prompt-techniques]
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

## Mentioned In

- [EgoAlpha/prompt-in-context-learning Research Brief](../sources/egoa-prompt-techniques.md)
