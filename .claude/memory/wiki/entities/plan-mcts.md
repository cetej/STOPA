---
name: Plan-MCTS
type: paper
first_seen: 2026-04-26
last_updated: 2026-04-26
sources: [ai-planning-framework-web-agents]
tags: [planning, web-agents, mcts, orchestration]
---

# Plan-MCTS

> Wang et al. (2026) — MCTS v plan-space (ne action-space) pro web navigaci; zavádí ortogonální osu Action-Space vs Plan-Space jako klíčovější než výběr search policy.

## Key Facts

- Plan-space MCTS (subplan units) vs Action-space MCTS (atomic actions): plan-space systematicky vítězí bez ohledu na search algoritmus (ref: sources/ai-planning-framework-web-agents.md)
- WebArena leaderboard: Plan-MCTS 39.2%, ale AgentOccam (linear) 45.7% — best linear bije tree-search (ref: sources/ai-planning-framework-web-agents.md)
- Vanilla Best-First Search (Koh 2024): pouze 19.2% na WebArena — o 26pp pod AgentOccam (ref: sources/ai-planning-framework-web-agents.md)
- Token scaling: plan-space search se škáluje s rozpočtem; action-space search nikoli (ref: sources/ai-planning-framework-web-agents.md)
- AgentOccam (45.7%) je nejsilnější WebArena baseline — linear, bez search (ref: sources/ai-planning-framework-web-agents.md)

## Relevance to STOPA

Validuje STOPA's scout→orchestrate split jako plan-space thinking. Lekce: search granularity (subtask) > search policy (BFS/DFS). AgentOccam finding = argument pro "linear well-tuned first, then search."

## Mentioned In

- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)
