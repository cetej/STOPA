---
date: 2026-04-12
type: architecture
severity: medium
component: hook
tags: [steering, interpretability, mechanistic, calm-steering, safety]
summary: "Representation steering (refusal, behavior modification) works through OV circuit, not QK. Vectors are sparsifiable 90-99% with minimal loss. Different methods (DIM/NTP/PO) converge to ≥90% overlapping circuits — mechanistic equivalence despite surface dissimilarity."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
verify_check: "manual"
skill_scope: []
---

## Steering Vectors — Mechanistic Basis (arXiv:2604.08524)

**Finding**: Refusal steering (and by extension behavioral steering generally) operates through OV (output-value) attention circuits. Freezing all QK (query-key) attention scores drops steering performance by only 8.75% — the QK path is largely irrelevant.

**Sparsification**: Steering vectors can be compressed 90–99% using gradient-based sparsification while retaining ~90% performance. Different methods converge to statistically shared dimension subsets (hypergeometric p < 0.05).

**Circuit overlap**: DIM, NTP, and PO methods use circuits with ≥90% overlap despite cosine similarity of only 0.10–0.42. ~10–11% of model edges suffice for 85% of behavior recovery.

**How to apply**: STOPA's calm-steering hook and panic-detector operate via Anthropic emotion vectors — this confirms the mechanistic soundness. Multiple steering sources (calm-steering + heartbeat) converge to the same circuits and won't interfere. Steering interventions can be efficient/sparse.
