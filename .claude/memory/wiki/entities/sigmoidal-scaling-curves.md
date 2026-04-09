---
name: Sigmoidal Scaling Curves
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [scalerl-scaling-rl-compute-llms]
tags: [scaling-laws, compute-efficiency, prediction, optimization]
---

# Sigmoidal Scaling Curves

> Compute-performance model for RL training: R = R0 + (A-R0) / (1+(Cmid/C)^B), where A = asymptotic ceiling, B = scaling efficiency, Cmid = half-gain compute. Enables predicting final performance from partial training runs.

## Key Facts

- Three parameters characterize any RL recipe: A (ceiling), B (efficiency), Cmid (half-gain point) (ref: sources/scalerl-scaling-rl-compute-llms.md)
- Different recipes converge to DIFFERENT asymptotes — more compute doesn't fix a bad recipe (ref: sources/scalerl-scaling-rl-compute-llms.md)
- Extrapolation from 50% compute accurately predicts final performance within ±0.02 (ref: sources/scalerl-scaling-rl-compute-llms.md)
- Most design choices shift B (efficiency) not A (ceiling) — focus optimization effort on what shifts A (ref: sources/scalerl-scaling-rl-compute-llms.md)
- Early performance is unreliable: method X beating method Y at low compute may lose at scale (ref: sources/scalerl-scaling-rl-compute-llms.md)

## Relevance to STOPA

This model applies to STOPA's iterative optimization skills. /autoloop and /autoresearch could fit sigmoidal curves to score trajectories across iterations — if the predicted asymptote A is below the target, switching approaches early saves compute. The "early performance is unreliable" finding means STOPA shouldn't pick the approach that wins first 2 iterations — give each approach enough iterations to reveal its ceiling.

## Mentioned In

- [The Art of Scaling RL Compute for LLMs](../sources/scalerl-scaling-rl-compute-llms.md)
