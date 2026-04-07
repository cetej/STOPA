---
name: SpargeAttn
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [kascade-sparse-attention-research]
tags: [sparse-attention, transformer, inference-optimization, consumer-gpu]
---
# SpargeAttn

> Training-free drop-in sparse attention (ICML 2025, Tsinghua ML Group); pip-installable, RTX 3090/4090 compatible; two-stage online filter predicts attention map to skip unnecessary matrix multiplications.

## Key Facts

- Install: `pip install ninja && python setup.py install`; requires Ampere/Ada GPU (RTX 3090+), CUDA >=12.0 (ref: sources/kascade-sparse-attention-research.md)
- Two-stage filter: predicts attention map → skips wasteful matmuls for sparse regions (ref: sources/kascade-sparse-attention-research.md)
- Paper: arXiv:2502.18137; ICML 2025 (ref: sources/kascade-sparse-attention-research.md)
- Windows fork: github.com/sdbds/SpargeAttn-for-windows (ref: sources/kascade-sparse-attention-research.md)
- Covers both prefill and decode phases (ref: sources/kascade-sparse-attention-research.md)

## Relevance to STOPA

Most accessible sparse attention implementation for RTX 4090 (STOPA dev hardware). Starting point for local LLM inference optimization before considering H100-only approaches.

## Mentioned In

- [Kascade & Sparse Attention — Implementace a Inspirace](../sources/kascade-sparse-attention-research.md)
