---
name: xRouter
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mom-taro-discovery-2]
tags: [routing, reinforcement-learning, cost-optimization, orchestration]
---
# xRouter

> RL-trained cost-aware orchestration system that optimizes LLM model selection on the cost-performance Pareto frontier; avoids need for preference labels.

## Key Facts

- RL-based: state = task embedding + budget remaining; action = model + strategy + tool; reward = quality/cost ratio (ref: sources/mom-taro-discovery-2.md)
- Scales to >2 model tiers and handles continuous model zoo without preference data (ref: sources/mom-taro-discovery-2.md)
- Paper: arXiv:2510.08439 (ref: sources/mom-taro-discovery-2.md)
- Naturally balances Pareto frontier instead of binary strong/weak (ref: sources/mom-taro-discovery-2.md)

## Relevance to STOPA

Preferred over RouteLLM when STOPA routes across 3+ model tiers (Haiku/Sonnet/Opus) — avoids preference data requirement and handles heterogeneous task distribution better.

## Mentioned In

- [Adaptive Model Routing in LLM Agent Systems](../sources/mom-taro-discovery-2.md)
