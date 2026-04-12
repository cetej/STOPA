---
name: Circuit Interchangeability
type: concept
first_seen: 2026-04-12
last_updated: 2026-04-12
sources: [mechanistic-steering-refusal-circuits]
tags: [interpretability, steering, mechanistic, safety]
---

# Circuit Interchangeability

> Empirical finding that different steering methodologies activate functionally overlapping circuits (≥90%) in transformer models, despite low vector cosine similarity.

## Key Facts

- DIM, NTP, and PO steering methods exhibit near 100% circuit overlap between smaller and larger circuits — ref: sources/mechanistic-steering-refusal-circuits.md
- Low cosine similarity (0.10–0.42) between steering vectors belies high circuit overlap — mechanistic equivalence despite surface-level dissimilarity — ref: sources/mechanistic-steering-refusal-circuits.md
- Different methods converge on statistically significant shared dimension subsets across sparsity levels (hypergeometric test p < 0.05) — ref: sources/mechanistic-steering-refusal-circuits.md

## Relevance to STOPA

Mixing steering approaches (calm-steering via Anthropic emotion vectors + heartbeat steering) won't produce conflicting mechanisms — they converge to the same underlying circuits. Validates STOPA's multi-hook steering strategy.

## Mentioned In

- [What Drives Representation Steering?](../sources/mechanistic-steering-refusal-circuits.md)
