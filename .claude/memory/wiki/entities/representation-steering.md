---
name: Representation Steering
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [mechanistic-steering-refusal-circuits]
tags: [safety, interpretability, steering, activation, mechanistic]
---

# Representation Steering

> Technique for modifying LLM behavior by injecting or adding vectors to residual stream activations at inference time, without retraining.

## Key Facts

- Three main methods: Difference-in-Means (DIM, non-learning), Next Token Prediction (NTP), Preference Optimization (PO) — ref: sources/mechanistic-steering-refusal-circuits.md
- All three methods leverage circuits with ≥90% overlap despite low cosine similarities (0.10–0.42) between their vectors — ref: sources/mechanistic-steering-refusal-circuits.md
- Steering operates primarily through OV (output-value) circuit; QK (query-key) circuit largely bypassed — ref: sources/mechanistic-steering-refusal-circuits.md
- Steering vectors can be sparsified 90–99% while retaining most performance (gradient-based approach outperforms random/bottom-k) — ref: sources/mechanistic-steering-refusal-circuits.md
- ~10–11% of model edges suffice to recover 85% of steered behavior (highly targeted) — ref: sources/mechanistic-steering-refusal-circuits.md

## Relevance to STOPA

STOPA's calm-steering hook uses Anthropic emotion vectors for behavioral modification — this paper confirms the mechanistic basis: steering is consistent, targeted, and works through OV circuits. Sparsification findings mean minimal overhead.

## Mentioned In

- [What Drives Representation Steering?](../sources/mechanistic-steering-refusal-circuits.md)
