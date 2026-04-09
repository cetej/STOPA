---
title: "Thinking Mid-training: Reinforcement Learning of Interleaved Reasoning"
slug: thinking-midtraining-meta-ai
source_type: url
url: "https://facebookresearch.github.io/RAM/blogs/thinking_midtraining/"
date_ingested: 2026-04-08
date_published: "2026-04"
entities_extracted: 3
claims_extracted: 5
---

# Thinking Mid-training: Reinforcement Learning of Interleaved Reasoning

> **TL;DR**: Meta AI inserts a new training phase between pretraining and post-training — "thinking mid-training" — that teaches models to reason via interleaved thought generation + RL refinement. Llama-3-8B achieves 9× gains mid-training alone, 3.2× vs direct post-training when combined with RL post-training.

## Key Claims

1. Mid-training with interleaved thoughts yields 9× improvement over base model on math reasoning — `verified`
2. Combining mid-training + RL post-training gives 3.2× vs direct RL post-training on base model — `verified`
3. RL mid-training (8.7B tokens) more efficient than extended SFT (10.5B tokens) for same task — `verified`
4. Pretraining data lacks explicit reasoning traces; annotator model can insert interleaved thoughts at semantically appropriate positions — `argued`
5. Reasoning capabilities benefit from native training earlier in pipeline, not just post-hoc tuning — `argued`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Thinking Mid-training](../entities/thinking-mid-training.md) | concept | new |
| [DrGRPO](../entities/drgrpo.md) | concept | new |
| [RLP](../entities/rlp.md) | concept | updated |

## Relations

- `thinking-mid-training` `extends` `RLP` — both move RL earlier in training pipeline; RLP = pretraining phase, thinking-mid = dedicated intermediate phase
- `thinking-mid-training` `uses` `DrGRPO` — RL variant for binary reward optimization on thought quality
- `thinking-mid-training` `created_by` Meta AI RAM team

## Cross-References

- Related learnings: `rlp-reinforcement-pretraining.md` (same "front-load RL" family)
- Related wiki articles: [orchestration-multi-agent](../orchestration-multi-agent.md) — curriculum-hints pattern analogy
- Related entities: [RLP](../entities/rlp.md), [llamafirewall](../entities/llamafirewall.md) (Meta AI connection)
- Contradictions: none detected
