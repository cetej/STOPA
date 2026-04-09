---
name: RLP
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [rlp-reinforcement-pretraining, thinking-midtraining-meta-ai]
tags: [rl, pretraining, reasoning, reward-design, training-methodology]
---

# RLP (Reinforcement as a Pretraining Objective)

> Method that integrates reinforcement learning into pretraining rather than applying it only during post-training. Chain-of-thought reasoning treated as exploratory actions, rewarded by information gain (log-likelihood improvement of next token when conditioned on reasoning chain).

## Key Facts

- Moves RL from post-training to pretraining phase — models learn to reason during pretraining, not as post-hoc enhancement (ref: sources/rlp-reinforcement-pretraining.md)
- Dense reward signal without verifier: measures how much a sampled reasoning chain improves next-token prediction accuracy (ref: sources/rlp-reinforcement-pretraining.md)
- Qwen3-1.7B-Base: +19% across 8 math/science benchmarks (ref: sources/rlp-reinforcement-pretraining.md)
- Nemotron-Nano-12B-v2: 42.81% → 61.32% overall, +23% on scientific reasoning (ref: sources/rlp-reinforcement-pretraining.md)
- ICLR 2026 camera ready (ref: sources/rlp-reinforcement-pretraining.md)

## Relevance to STOPA

RLP validates the "front-load quality" principle: embedding capability earlier in the pipeline (pretraining vs post-training) yields compounding gains. Analogous to STOPA's write-time gating (learning admission) vs read-time filtering — quality injected early compounds, quality filtered late leaks. Also relevant for understanding reasoning model capabilities when selecting models for orchestration tiers.

## Mentioned In

- [RLP — Reinforcement as a Pretraining Objective](../sources/rlp-reinforcement-pretraining.md)
- [Thinking Mid-training — Meta AI](../sources/thinking-midtraining-meta-ai.md)
