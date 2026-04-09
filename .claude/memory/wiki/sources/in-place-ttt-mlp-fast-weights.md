---
title: "In-Place Test-Time Training: Learning Fast Weights from the Context"
slug: in-place-ttt-mlp-fast-weights
source_type: url
url: "https://arxiv.org/abs/2604.06169"
date_ingested: 2026-04-08
date_published: "2026-04"
entities_extracted: 3
claims_extracted: 7
---

# In-Place Test-Time Training: Learning Fast Weights from the Context

> **TL;DR**: LLMs can update their own weights during inference by repurposing the MLP W_down matrix as "fast weights" — no new layers, no retraining. Drop-in on Qwen3-4B gives +4.4 accuracy at 64k tokens; full pretrain improves RULER-16k from 6.58 to 19.99.

## Key Claims

1. Existing MLP W_down matrices can serve as fast weights updated chunk-by-chunk during inference without architectural changes — `argued` + `verified` (Theorem 1 + benchmarks)
2. Qwen3-4B drop-in enhancement: +4.4 accuracy at 64k tokens, +2.2 at 128k, +2.2 at 256k (YaRN extrapolation) — `verified`
3. Full-pretrain RULER-16k: 6.58 → 19.99 (full attention), 5.07 → 7.57 (sliding window) — `verified`
4. Optimal chunk size is 1024 tokens (ablation: performance-efficiency peak) — `verified`
5. LM-aligned TTT objective (next-token prediction + 1D convolution) provably increases correct token logits ≥ λ_lr·c²_norm·c_align — `argued` (Theorem 1)
6. Outperforms Gated Linear Attention and DeltaNet at 500M/1.5B scale — `verified`
7. State size scales monotonically with fast weight capacity — `verified`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [In-Place TTT](../entities/in-place-ttt.md) | concept | new |
| [Fast Weights](../entities/fast-weights.md) | concept | new |
| [Test-Time Learning](../entities/test-time-learning.md) | concept | updated |

## Relations

- In-Place TTT `extends` Test-Time Learning — weight-level variant of inference-time adaptation
- In-Place TTT `uses` Fast Weights — core implementation mechanism
- In-Place TTT `competes_with` DeltaNet — outperforms at 500M/1.5B on perplexity benchmarks
- In-Place TTT `competes_with` Gated Linear Attention — same benchmark comparison

## Cross-References

- Related learnings: `2026-04-08-test-time-learning-inference-evolution.md`, `2026-04-08-living-memory-over-static-retrieval.md`
- Related wiki articles: memory-architecture.md (long-context management), orchestration-infrastructure.md (model selection)
- Related entities: mia.md (TTL in MIA Planner), thinking-token-budget.md (inference-time compute)
- Contradictions: none
