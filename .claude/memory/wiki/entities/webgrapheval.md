---
name: WebGraphEval
type: paper
first_seen: 2026-04-26
last_updated: 2026-04-26
sources: [ai-planning-framework-web-agents]
tags: [evaluation, web-agents, trajectory, graph]
---

# WebGraphEval

> Qian et al. — agreguje 4,768 trajektorií 6 agentů do directed action graph a zavádí strukturální metriky (necessity rate, step inflation, edge classification) nad WebArena.

## Key Facts

- 4,768 trajektorií → directed graph (40k uzlů, 45k hran) z 812 WebArena tasks (ref: sources/ai-planning-framework-web-agents.md)
- Necessity rate: 72.9–82.0% akcí je nezbytných (LLM-judged); step inflation mean 2.14× (ref: sources/ai-planning-framework-web-agents.md)
- Edge classification: Trap / Critical / Bottleneck / Normal — strukturální analýza failure modes (ref: sources/ai-planning-framework-web-agents.md)
- Klíčový finding: pouze 3.8% WebArena tasks solved by ALL 6 agents, 83.2% mixed outcomes — vyvrací single-reference-trajectory assumption (ref: sources/ai-planning-framework-web-agents.md)
- Temporal reward backpropagation γ=0.9 pro per-node value assignment (ref: sources/ai-planning-framework-web-agents.md)

## Relevance to STOPA

"83.2% mixed outcomes" finding je argument pro multi-run evaluation v STOPA `/eval` — single run nedokazuje robustnost. Step inflation 2.14× je baseline pro porovnání délky orchestrátorových trajektorií.

## Mentioned In

- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)
