---
name: Route-to-Reason (RTR)
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mom-taro-discovery-2]
tags: [routing, reasoning-strategy, orchestration, cost-optimization]
---
# Route-to-Reason (RTR)

> Joint optimization of model selection AND reasoning strategy (CoT vs direct answer vs tool use vs delegation) under a budget constraint; extends RouteLLM to cover strategy-level routing.

## Key Facts

- Maintains 95%+ quality at 40-60% of baseline budget by dynamically selecting the optimal reasoning modality per step (ref: sources/mom-taro-discovery-2.md)
- Beats static model routing alone because easy questions benefit from weak model + direct answer over strong model + CoT (ref: sources/mom-taro-discovery-2.md)
- Paper: arXiv:2505.19435 (ref: sources/mom-taro-discovery-2.md)
- Budget slider maps directly to constraint parameter (ref: sources/mom-taro-discovery-2.md)

## Relevance to STOPA

Long-term upgrade for orchestrate skill: instead of hardcoded tier→model, RTR would learn per-subtask (model, strategy) allocation. Most impactful for mixed workflows where some subtasks need deep reasoning and others need direct answers.

## Mentioned In

- [Adaptive Model Routing in LLM Agent Systems](../sources/mom-taro-discovery-2.md)
