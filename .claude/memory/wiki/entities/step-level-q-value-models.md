---
name: Step-Level Q-Value Models
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mom-taro-discovery-2]
tags: [routing, decision-theory, reinforcement-learning, orchestration]
---
# Step-Level Q-Value Models

> MCTS-trained critics that assign expected utility (Q-values) to each agent action at each step, enabling decision-theoretic stopping policies rather than fixed circuit breakers.

## Key Facts

- Q-values trained via MCTS rollouts + annotated trajectory rewards; at inference: sample candidates → pick max Q-value action (ref: sources/mom-taro-discovery-2.md)
- Generalizes across similar tasks: Q-values learned on one task transfer to similar tasks (ref: sources/mom-taro-discovery-2.md)
- Paper: arXiv:2409.09345 — "Enhancing Decision-Making for LLM Agents via Step-Level Q-Value Models" (ref: sources/mom-taro-discovery-2.md)
- Key insight: routes only when marginal benefit > cost, rather than "always use strong model for all steps" (ref: sources/mom-taro-discovery-2.md)

## Relevance to STOPA

Could replace fixed 3-fix circuit breakers with a learned stopping policy: train on failure logs to compute P(success | error_class, attempt_N). Stop early if Q-value < 0.1 instead of counting to 3.

## Mentioned In

- [Adaptive Model Routing in LLM Agent Systems](../sources/mom-taro-discovery-2.md)
