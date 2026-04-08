---
title: "RLP: Reinforcement as a Pretraining Objective"
slug: rlp-reinforcement-pretraining
source_type: url
url: "https://arxiv.org/abs/2510.01265"
date_ingested: 2026-04-08
date_published: "2025-10-02"
entities_extracted: 1
claims_extracted: 4
---

# RLP: Reinforcement as a Pretraining Objective

> **TL;DR**: RL doesn't have to wait for post-training. RLP integrates reinforcement learning into pretraining by treating chain-of-thought as exploratory actions, rewarded by information gain (next-token log-likelihood improvement). +19% on small models, +23% scientific reasoning on 12B.

## Key Claims

1. RL integrated into pretraining yields larger reasoning gains than post-training-only RL — `verified` (19% improvement Qwen3-1.7B, 42.81%→61.32% Nemotron-Nano-12B)
2. Information gain (log-likelihood improvement conditioned on reasoning chain) provides dense reward signal without needing external verifiers — `argued`
3. Models that learn reasoning during pretraining develop more robust reasoning capabilities than those fine-tuned post-hoc — `argued`
4. Largest gains appear on reasoning-intensive benchmarks (AIME25, MMLU-Pro) — `verified`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [RLP](../entities/rlp.md) | concept | new |

## Relations

- RLP `extends` GRPO — both use group-relative rewards, but RLP applies during pretraining
- RLP `contradicts` standard RLHF pipeline — challenges assumption that RL belongs only in post-training
- RLP `uses` information gain as reward signal — no verifier needed

## Cross-References

- Related entities: [grpo.md](../entities/grpo.md), [gdpo.md](../entities/gdpo.md), [conditional-reward-design.md](../entities/conditional-reward-design.md)
- Related learnings: `2026-04-07-multi-reward-normalization-collapse.md` (reward design)
- Contradictions: none
