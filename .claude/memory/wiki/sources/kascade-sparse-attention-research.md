---
title: "Kascade & Sparse Attention — Implementace a Inspirace"
slug: kascade-sparse-attention-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 8
claims_extracted: 5
---
# Kascade & Sparse Attention — Implementace a Inspirace

> **TL;DR**: Kascade (Microsoft Research, arXiv:2512.16391) achieves 4.1x decode speedup via cross-layer top-k index reuse — but requires H100 GPUs. Practical alternatives for consumer hardware: SpargeAttn (RTX 3090+, pip-installable), FlexAttention (PyTorch stable), FlashInfer. Key architectural insight transferable to STOPA: "anchor layer" pattern (one agent does full scan, others reuse findings) directly validates Findings Ledger / Root Context Provider patterns.

## Key Claims

1. Kascade achieves 4.1x decode / 2.2x prefill speedup over FlashAttention-3 on H100 at 10% top-k sparsity, with only 2.5% accuracy degradation on reasoning tasks — `[verified]`
2. Cross-layer attention similarity >0.98 means neighboring transformer layers share ~98% of important tokens — the core insight enabling index reuse — `[verified]`
3. SpargeAttn (ICML 2025) is the most practical training-free alternative for RTX 3090/4090: pip-installable, no custom CUDA — `[verified]`
4. The Kascade anchor-layer pattern is directly analogous to STOPA's Findings Ledger: one agent performs full context scan (anchor), others reuse indexed findings (reuse) — `[argued]`
5. FlexAttention (PyTorch stable) allows cross-layer reuse via `block_mask` caching with zero extra dependencies — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Kascade | paper | new |
| SpargeAttn | tool | new |
| FlexAttention | tool | new |
| FlashInfer | tool | new |
| IndexCache | tool | new |
| MInference | tool | new |
| NSA (Native Sparse Attention) | concept | new |
| SnapKV | concept | new |

## Relations

- Kascade `implements` cross-layer top-k reuse
- SpargeAttn `is_alternative_to` Kascade (consumer GPU)
- FlexAttention `enables` cross-layer reuse (PyTorch-native)
- IndexCache `ports` Kascade pattern (no custom CUDA)
- Kascade anchor-layer `validates` STOPA Findings Ledger pattern
