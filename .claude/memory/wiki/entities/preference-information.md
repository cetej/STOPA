---
name: Preference Information
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [learning-is-forgetting-llm-lossy-compression]
tags: [alignment, rlhf, model-selection, evaluation, information-theory]
---

# Preference Information

> I(Z; preference) — mutual information between model representations and preferred/rejected response pairs; measures how well a model distinguishes good from bad outputs.

## Key Facts

- Strongest performance predictor in the paper: **r = 0.76, p < 0.001** across 47 models (vs. optimality at r=0.52) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Measured using Tulu preference dataset (prompt + preferred/rejected pairs, 10K samples, max 512 ctx) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Dissociation: compression optimality predicts knowledge/reasoning (MMLU-Pro, BBH, MATH, GPQA, MuSR); preference info predicts instruction following (IFEval, r=0.39) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Post-training (RLHF/DPO) consistently increases I(Z;preference) while barely changing complexity — confirms post-training = alignment editing, not relearning (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Proxy for alignment quality measurable without behavioral evaluation (no prompting, no decoding needed) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)

## Relevance to STOPA

Enables alignment quality check without running behavioral evals — relevant for model selection when choosing between base vs. instruction-tuned variants in orchestration tier decisions.

## Mentioned In

- [Learning is Forgetting: LLM Training As Lossy Compression](../sources/learning-is-forgetting-llm-lossy-compression.md)
