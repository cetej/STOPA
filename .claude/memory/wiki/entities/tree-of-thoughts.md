---
name: Tree of Thoughts
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoa-prompt-techniques, ai-planning-framework-web-agents]
last_updated: 2026-04-26
tags: [reasoning, planning, search]
---

# Tree of Thoughts

> Yao et al. 2023 (arXiv:2305.10601) — deliberate search over thought tree s LLM evaluation na každém uzlu. 4.4k GitHub stars.

## Key Facts

- GPT-4+ToT: 74% vs 4% CoT na Game of 24 (ref: sources/egoa-prompt-techniques.md)
- Mechanismus: generuj N thought candidates, evaluuj každý, prune slabé, expand silné
- Umožňuje backtracking — na rozdíl od lineárního CoT
- 21× více citací než Graph of Thoughts (Graph of Thoughts claims +62% quality, -31% cost vs ToT)

## Relevance to STOPA

LATS (92.7% HumanEval) rozšiřuje ToT o MCTS + Reflexion. STOPA deep tier orchestrace s branching by měl implementovat ToT-inspired explorace: spusť 2-3 přístupy paralelně (fork agents), evaluuj výsledky /critic, implementuj nejlepší.

- BFS/DFS atribuce: ToolTree §6 (2026, ICLR) explicitně označuje ToT jako canonical zdroj BFS/DFS pro LLM thought trees — potvrzuje prioritu (ref: sources/ai-planning-framework-web-agents.md)
- Shahnovsky & Dror (2026) BFS/DFS taxonomie je derivativní od ToT — nevzniká nová taxonomie (ref: sources/ai-planning-framework-web-agents.md)

## Mentioned In

- [EgoAlpha/prompt-in-context-learning Research Brief](../sources/egoa-prompt-techniques.md)
- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)
