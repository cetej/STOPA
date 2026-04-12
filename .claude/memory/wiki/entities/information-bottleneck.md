---
name: Information Bottleneck
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [learning-is-forgetting-llm-lossy-compression]
tags: [theory, compression, llm-training, information-theory, model-selection]
---

# Information Bottleneck

> Framework formalizing learning as lossy compression: retain only information in X relevant to predicting Y, discard the rest.

## Key Facts

- IB objective: `F_β[p(Z|X)] = I(X;Z) - β · I(Y;Z)` — minimizes complexity (I(X;Z)) while maximizing expressivity (I(Y;Z)) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- β=0 → everything compressed to a point; β→∞ → lossless; optimal frontier is the IB bound (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Specific instance of Rate-Distortion Theory (Shannon 1948) where distortion = −I(Y;Z) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Empirically validated at LLM scale for first time: 75 models, 6 families, all converge to same IB bound region — suggests universal deep learning property (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Two-phase training trajectory predicted by IB: Phase 1 fitting (I(Y;Z)↑), Phase 2 compression (I(X;Z)↓), confirmed at OLMo2 7B/32B scale (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Originally validated on MNIST feed-forward networks (Shwartz-Ziv & Tishby 2017) — dispute by Saxe 2019 now resolved at LLM scale

## Relevance to STOPA

Provides theoretical grounding for model selection: Optimality = I(Y;Z)/I(X;Z) can be computed in a single forward pass on C4 and predicts benchmark performance at r=0.52 — cheaper than running eval suites.

## Mentioned In

- [Learning is Forgetting: LLM Training As Lossy Compression](../sources/learning-is-forgetting-llm-lossy-compression.md)
