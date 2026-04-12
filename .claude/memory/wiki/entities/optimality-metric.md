---
name: Optimality Metric (IB)
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [learning-is-forgetting-llm-lossy-compression]
tags: [model-selection, information-theory, benchmark, evaluation, compression]
---

# Optimality Metric (IB)

> I(Y;Z)/I(X;Z) — ratio of expressivity to complexity; measures how close a model's representations are to the Information Bottleneck bound.

## Key Facts

- Definition: `Optimality = I(Y;Z) / I(X;Z)` — "bits of expressivity per bit of complexity", approaches 1.0 at the IB bound (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Predicts aggregate benchmark performance at **r = 0.52, p < 0.001** (Spearman) across 47 open-weight models and 6 benchmarks (MMLU-Pro, BBH, MATH Level 5, GPQA, MuSR, IFEval) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Stronger predictor than complexity alone (r=−0.38) or expressivity alone (r=0.08) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Computed via single forward pass on C4 — substantially cheaper than benchmark eval suite (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Does NOT predict IFEval (instruction following, r=0.07) — that requires preference information instead (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Potential stopping criterion for pre-training: cease when distance to IB bound stops decreasing

## Relevance to STOPA

Cheap model quality signal: could inform tier selection (haiku/sonnet/opus) by measuring compression optimality at session start rather than relying solely on benchmark tables.

## Mentioned In

- [Learning is Forgetting: LLM Training As Lossy Compression](../sources/learning-is-forgetting-llm-lossy-compression.md)
