---
name: AgentRewardBench
type: paper
first_seen: 2026-04-26
last_updated: 2026-04-26
sources: [ai-planning-framework-web-agents]
tags: [evaluation, web-agents, trajectory, benchmark]
---

# AgentRewardBench

> Lù et al. — benchmark 1,302 trajektorií × 5 benchmarků × 4 agentů pro evaluaci automatických evaluátorů web agentů; zavádí 3-otázkové expert annotation schema.

## Key Facts

- 3-otázkové anotační schema: success / side effects / repetitiveness (ne binární) (ref: sources/ai-planning-framework-web-agents.md)
- Rule-based WebArena evaluators underreport success vs expert annotations (ref: sources/ai-planning-framework-web-agents.md)
- 12 LLM judges testováno; "no single LLM excels across all benchmarks" (ref: sources/ai-planning-framework-web-agents.md)
- Pokrývá 5 benchmarků: WebArena, VisualWebArena, WorkArena, AssistantBench, WebVoyager (ref: sources/ai-planning-framework-web-agents.md)

## Relevance to STOPA

3-otázkové schema (success/side-effects/repetitiveness) by mělo nahradit binární good/bad labeling v `/annotate` Align Evals — richer annotation = lepší eval dataset pro /self-evolve.

## Mentioned In

- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)
