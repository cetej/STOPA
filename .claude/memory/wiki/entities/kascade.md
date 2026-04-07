---
name: Kascade
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [kascade-sparse-attention-research]
tags: [sparse-attention, transformer, inference-optimization, microsoft-research]
---
# Kascade

> Microsoft Research paper (arXiv:2512.16391) introducing cross-layer top-k attention index reuse for sparse attention, achieving 4.1x decode / 2.2x prefill speedup over FlashAttention-3 on H100.

## Key Facts

- Core insight: neighboring transformer layers share >98% of important attention tokens — compute exact Top-k indices only at "anchor" layers, reuse at others (ref: sources/kascade-sparse-attention-research.md)
- Benchmarks (H100, 10% sparsity): 4.1x decode at 131K context, 2.66x prefill; AIME-24: 47.92% (vs Quest 7.50%, StreamingLLM 0%) (ref: sources/kascade-sparse-attention-research.md)
- H100-only requirement: uses TileLang, CUDA 12.8+, fp16; tested on 8B models only (ref: sources/kascade-sparse-attention-research.md)
- Does NOT reduce KV cache memory — only compute latency (ref: sources/kascade-sparse-attention-research.md)
- Head-aware remapping: each reuse layer head maps to most similar anchor head (not 1:1) — ablation shows 1-3% accuracy gain (ref: sources/kascade-sparse-attention-research.md)

## Relevance to STOPA

Anchor-layer pattern directly validates STOPA's Findings Ledger / Root Context Provider design: one agent does full scan (anchor), others reuse indexed findings. Empirical validation that context reuse is safe at 98% similarity threshold.

## Mentioned In

- [Kascade & Sparse Attention — Implementace a Inspirace](../sources/kascade-sparse-attention-research.md)
