---
name: AgentOccam
type: tool
first_seen: 2026-04-26
last_updated: 2026-04-26
sources: [ai-planning-framework-web-agents]
tags: [web-agents, planning, baseline]
---

# AgentOccam

> Well-engineered linear web agent baseline (GPT-4-Turbo) — drží 45.7% na WebArena, nejsilnější publikovaný výsledek na GPT-4-Turbo tieru, bez tree search.

## Key Facts

- 45.7% WebArena success rate — bije Plan-MCTS (39.2%), WebPilot (37.2%), Branch-and-Browse (35.8%) (ref: sources/ai-planning-framework-web-agents.md)
- Linear baseline bez search-based backtracking (ref: sources/ai-planning-framework-web-agents.md)
- Vanilla Best-First (Koh 2024) dosahuje jen 19.2% — o 26.5pp méně než AgentOccam (ref: sources/ai-planning-framework-web-agents.md)
- Popsán jako "well-engineered" bez specifické architectural detail v Plan-MCTS paper (ref: sources/ai-planning-framework-web-agents.md)

## Relevance to STOPA

Empirický důkaz: "linear well-tuned > naive tree search." Prerequisite pro zavedení search do `/orchestrate`: dokažte že lineární varianta je v plateaus. STOPA's linear orchestration pipeline je pravděpodobně blíže AgentOccam než tree-search.

## Mentioned In

- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)
