---
name: ToolTree
type: paper
first_seen: 2026-04-26
last_updated: 2026-04-26
sources: [ai-planning-framework-web-agents]
tags: [planning, tool-use, mcts, evaluation]
---

# ToolTree

> Yang et al. (2026, ICLR) — dual-feedback MCTS s bidirectional pruning pro tool planning; +10pp nad SOTA; dokazuje doménovou závislost tree search efektivity.

## Key Facts

- +10pp průměrně nad SOTA tool planning na GTA, m&m, ToolBench benchmarks (ref: sources/ai-planning-framework-web-agents.md)
- Tree search beats greedy by +3-10pp na tool planning (typed I/O) — ale NE na web navigaci (noisy actions) (ref: sources/ai-planning-framework-web-agents.md)
- §6 explicitně atribuuje: BFS/DFS → Yao 2023 Tree of Thoughts; Best-First → Koh 2024 (ref: sources/ai-planning-framework-web-agents.md)
- Framing literatury: greedy (CoT, ReAct) vs search (ToT BFS/DFS, Best-First, A*, MCTS) (ref: sources/ai-planning-framework-web-agents.md)

## Relevance to STOPA

Doménová závislost: STOPA skills pro tool planning (API calls, structured I/O) jsou kandidáti pro tree-search enhancement; skills pro noisy GUI/web tasks nejsou. Klíč: typed I/O = early pruning funguje.

## Mentioned In

- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)
