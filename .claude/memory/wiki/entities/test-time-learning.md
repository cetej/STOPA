---
name: Test-Time Learning
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [memory-intelligence-agent-mia]
tags: [agent-learning, inference, memory, continuous-learning, rl-training]
---

# Test-Time Learning

> Mechanism enabling a model component (typically a Planner or reasoner) to update its parameters continuously during inference without interrupting the active reasoning workflow.

## Key Facts

- In MIA: Planner uses test-time learning to evolve search strategies on-the-fly during inference (ref: sources/memory-intelligence-agent-mia.md)
- Enables agents to adapt to new question distributions without full retraining (ref: sources/memory-intelligence-agent-mia.md)
- Complementary to offline RL training: TTL handles distribution shift at inference time (ref: sources/memory-intelligence-agent-mia.md)
- Combined with unsupervised self-evolution (peer-review-style: logic + credibility + validity reviewers) — no labels needed (ref: sources/memory-intelligence-agent-mia.md)

## Relevance to STOPA

Test-time learning is the theoretical basis for STOPA skills like /self-evolve and /autoloop — agents that improve within a session based on execution feedback. MIA demonstrates this can work at inference time for parametric memory, not just prompt-level iteration.

## Mentioned In

- [Memory Intelligence Agent (MIA)](../sources/memory-intelligence-agent-mia.md)
