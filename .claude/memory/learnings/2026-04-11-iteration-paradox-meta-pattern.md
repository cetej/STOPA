---
date: 2026-04-11
type: best_practice
severity: high
component: orchestration
tags: [autoloop, autoresearch, self-evolve, iteration, optimization, meta-pattern]
summary: "Iteration Paradox: iteruj s bounded refinement, ale nevěř prvním výsledkům. Udržuj diverzitu (high-temp sampling), dej každému přístupu 5+ iterací, odhadni strop (sigmoidal fit), používej regression gate. RL post-training ničí diverzitu potřebnou pro exploraci."
source: auto_pattern
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 1.00
skill_scope: [autoloop, autoresearch, self-evolve]
related: [2026-04-08-iterative-refinement-beats-long-cot.md, 2026-04-08-early-iteration-performance-unreliable.md, 2026-04-08-inference-time-sampling-beats-rl-for-diversity.md, 2026-04-10-eggroll-evolutionary-optimization.md, 2026-04-03-autoagent-overfitting-guard.md]
verify_check: "manual"
---

## Meta-pattern: Iteration Paradox

Consolidated from /dreams 2026-04-11 — 5 learnings with seemingly contradictory advice resolved into coherent protocol.

### The Paradox

- PDR paper: iterative refinement beats long CoT (+11% AIME)
- ScaleRL paper: early iteration results are UNRELIABLE predictors of scale
- Sampling paper: RL post-training kills diversity needed for exploration
- EGGROLL: sigma regimes determine mutation optimality
- AutoAgent: overfitting guard needed against metric gaming

### Resolution Protocol

1. **Iterate with bounded context** (PDR) — never grow context unboundedly
2. **Maintain diversity** — use high-temp sampling, not RL-tuned models for exploration
3. **Don't trust early winners** — give each approach minimum 5 iterations before comparing
4. **Estimate ceiling** — fit sigmoidal curve after 5+ iterations; if predicted asymptote < target, switch approach
5. **Regression gate** — fixed failures become permanent tests, bar only goes up
6. **Overfitting guard** — "would this change still be worthwhile without this exact eval case?"
7. **Sigma management** (EGGROLL) — small mutations early (refine), larger late (explore)

### When to Apply

Every iterative optimization skill: /autoloop, /autoresearch, /self-evolve, /prompt-evolve.
