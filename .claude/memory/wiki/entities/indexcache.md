---
name: IndexCache
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [kascade-sparse-attention-research]
tags: [sparse-attention, inference-optimization, vllm, cross-layer-reuse]
---
# IndexCache

> Cross-layer attention reuse patch for vLLM/SGLang (arXiv:2603.12201, THUDM); F-layers compute full attention indices, S-layers copy the cache — no custom CUDA kernels required.

## Key Facts

- 1.82x prefill speedup; eliminates 75% of indexer compute (ref: sources/kascade-sparse-attention-research.md)
- No custom CUDA kernels — patch on vLLM/SGLang, theoretically more portable than Kascade (ref: sources/kascade-sparse-attention-research.md)
- Limitation: only tested on DeepSeek-V3.2 / GLM-5 models (ref: sources/kascade-sparse-attention-research.md)
- GitHub: github.com/THUDM/IndexCache; paper arXiv:2603.12201 (ref: sources/kascade-sparse-attention-research.md)

## Relevance to STOPA

Relevant if STOPA runs local inference with DeepSeek or GLM models. The no-custom-CUDA approach makes it more accessible than Kascade for deployment.

## Mentioned In

- [Kascade & Sparse Attention — Implementace a Inspirace](../sources/kascade-sparse-attention-research.md)
