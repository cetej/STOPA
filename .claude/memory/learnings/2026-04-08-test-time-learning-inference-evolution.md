---
date: 2026-04-08
type: architecture
severity: medium
component: orchestration
tags: [test-time-learning, inference, agent-learning, self-evolve, continuous-learning]
summary: "Test-time learning (TTL) enables agent components to update strategies during inference without interrupting reasoning. Complements offline RL: TTL handles distribution shift; RL provides baseline competence."
source: external_research
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.00
related: [2026-04-08-living-memory-over-static-retrieval.md]
verify_check: "manual"
---

## Detail

MIA's Planner uses test-time learning to evolve its search strategy on-the-fly during inference. Combined with unsupervised self-evaluation (peer-review-style reviewers for logic, credibility, validity), this requires no labels.

**Relevance to STOPA**: /self-evolve and /autoloop implement session-level TTL through prompt iteration. MIA shows this pattern works at parametric level too. For STOPA, the actionable implication is that skills with repair loops (TDD, self-evolve) are validated — execution feedback is enough to improve within-session performance without full retraining. The "alternating training" insight (Executor first → Planner) also suggests that in multi-agent orchestration, capability-building should precede strategy-building.
