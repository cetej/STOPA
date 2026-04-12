---
title: "What Drives Representation Steering? A Mechanistic Case Study on Steering Refusal"
slug: mechanistic-steering-refusal-circuits
source_type: url
url: "https://arxiv.org/pdf/2604.08524v1"
date_ingested: 2026-04-12
date_published: "2026-04"
entities_extracted: 3
claims_extracted: 5
---

# What Drives Representation Steering? A Mechanistic Case Study on Steering Refusal

> **TL;DR**: Different steering methodologies (DIM, NTP, PO) all activate ≥90% overlapping circuits in transformer models. Refusal steering works through OV (output-value) circuits, not QK. Steering vectors can be compressed 90–99% with minimal loss — mechanistic basis for efficient behavioral intervention.

## Key Claims

1. Different steering methods (DIM, NTP, PO) use circuits with ≥90% overlap despite low cosine similarity (0.10–0.42) — `verified`
2. Refusal steering bypasses QK circuit; freezing attention scores drops performance only 8.75% — `verified`
3. ~10–11% of model edges suffice to recover 85% of steered refusal behavior — `verified`
4. Steering vectors sparsifiable 90–99% while retaining ~90% attack success rate (gradient-based) — `verified`
5. OV circuit decomposition reveals semantically interpretable concepts even when steering vector lacks interpretability — `argued`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Representation Steering](../entities/representation-steering.md) | concept | new |
| [OV Circuit](../entities/ov-circuit.md) | concept | new |
| [Circuit Interchangeability](../entities/circuit-interchangeability.md) | concept | new |

## Relations

- Representation Steering `uses` OV Circuit — steering ignores QK, works through output-value path
- Circuit Interchangeability `part_of` Representation Steering — all methods converge mechanistically
- This paper `extends` Anthropic emotion vectors research — provides mechanistic explanation for why steering works

## Cross-References

- Related learnings: `2026-03-30-society-of-thought-orchestration.md` (mentions steering feature 30939), `2026-04-08-heartbeat-mid-run-steering.md` (behavioral steering in STOPA)
- Related wiki articles: [general-security-environment](../general-security-environment.md) (Anthropic emotion vectors)
- Contradictions: none detected
