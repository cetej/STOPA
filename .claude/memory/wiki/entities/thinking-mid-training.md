---
name: Thinking Mid-training
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [thinking-midtraining-meta-ai]
tags: [rl, pretraining, reasoning, training-methodology, mid-training]
---

# Thinking Mid-training

> Intermediate training phase inserted between pretraining and post-training that explicitly teaches LLMs to reason via interleaved thought generation, supervised fine-tuning, and RL refinement.

## Key Facts

- Three-stage pipeline: (1) annotator inserts "thoughts" at semantically appropriate positions in pretraining corpus → (2) SFT mid-training on augmented data → (3) RL mid-training using LLM-judge binary rewards with DrGRPO (ref: sources/thinking-midtraining-meta-ai.md)
- Mid-training alone: **9× improvement** over base Llama-3-8B on math reasoning benchmarks (ref: sources/thinking-midtraining-meta-ai.md)
- Combined with RL post-training: **3.2× improvement** in average accuracy vs direct post-training on base model — GSM8K, MATH-500, AMC23, Olympiad, GPQA-Diamond (ref: sources/thinking-midtraining-meta-ai.md)
- RL mid-training more token-efficient than extended SFT: 8.7B tokens vs 10.5B tokens for better result (ref: sources/thinking-midtraining-meta-ai.md)
- Performance doubles vs mid-training on raw unannotated data — annotator quality is key, not just data volume (ref: sources/thinking-midtraining-meta-ai.md)
- Core thesis: "reasoning capabilities benefit from being trained as native behavior earlier in the training pipeline" (ref: sources/thinking-midtraining-meta-ai.md)

## Relevance to STOPA

Validates the "teach early, refine late" principle — analogous to STOPA's `curriculum-hints` in SKILL.md (structured reasoning sequence as injected context, not post-hoc reward signal). Confirms that front-loading reasoning structure (mid-training ≈ curriculum-hints at call time) outperforms adding it only at the end. Also relevant for model selection: models trained with mid-training will have stronger reasoning at lower tier, shifting budget-tier thresholds.

## Mentioned In

- [Thinking Mid-training — Meta AI](../sources/thinking-midtraining-meta-ai.md)
