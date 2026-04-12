---
name: Soft Entropy Estimator
type: tool
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [learning-is-forgetting-llm-lossy-compression]
tags: [information-theory, llm-analysis, measurement, entropy, compression]
---

# Soft Entropy Estimator

> Memory-efficient entropy estimator for LLM representations using cosine similarity + softmax over random reference points on the unit sphere; scales to 32B models in a single forward pass.

## Key Facts

- Algorithm: normalize embeddings to unit sphere, compute softmax over cosine similarities to m=100 random reference points, compute Shannon entropy of resulting distribution (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Temperature calibration via von Mises-Fisher KL divergence: `ε*(m,d) ≈ 1/√(2d·log m)` — same √d scaling as transformer self-attention (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Single forward pass, memory-efficient — prior methods (dimension-wise binning, clustering) intractable at OLMo2 32B (5120-dim × 64 layers × 512 ctx) (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Robust: m=100 vs m=50 gives same results; works across C4, Tulu, MMLU data distributions (ref: sources/learning-is-forgetting-llm-lossy-compression.md)
- Code: https://github.com/hcoxec/soft_h (Conklin 2025, PhD thesis University of Edinburgh)

## Relevance to STOPA

Enables practical model selection metric (optimality) without benchmark eval — potential integration into /budget or /status for cheap model quality estimates when multiple model options are available.

## Mentioned In

- [Learning is Forgetting: LLM Training As Lossy Compression](../sources/learning-is-forgetting-llm-lossy-compression.md)
