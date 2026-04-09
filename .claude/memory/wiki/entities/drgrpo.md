---
name: DrGRPO
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [thinking-midtraining-meta-ai]
tags: [rl, training-methodology, grpo, reward-optimization]
---

# DrGRPO

> Variant of GRPO (Group Relative Policy Optimization) used in Meta's thinking mid-training pipeline; optimizes thought generation via binary LLM-judge rewards on suffix prediction quality.

## Key Facts

- Used in Stage 3 (RL mid-training) of the thinking mid-training pipeline — agent generates thoughts, LLM judge evaluates whether thoughts lead to accurate text completions (ref: sources/thinking-midtraining-meta-ai.md)
- Achieves result with 8.7B tokens vs SFT baseline requiring 10.5B — 17% more token-efficient (ref: sources/thinking-midtraining-meta-ai.md)
- Binary reward signal: does the interleaved thought improve downstream completion accuracy? — simpler than dense reward schemes (ref: sources/thinking-midtraining-meta-ai.md)

## Relevance to STOPA

Less directly relevant than thinking-mid-training itself. Useful context for understanding why RL > extended SFT for reasoning refinement — applicable when evaluating whether to use RL-tuned models (stronger reasoning, potentially better for iterative agent loops) vs SFT-only models at same tier.

## Mentioned In

- [Thinking Mid-training — Meta AI](../sources/thinking-midtraining-meta-ai.md)
