---
name: FlashInfer
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [kascade-sparse-attention-research]
tags: [sparse-attention, inference-optimization, vllm, mlsys]
---
# FlashInfer

> Production-grade attention library (MLSys 2025) with sm7.5-sm12.0 support; integrates with vLLM and SGLang via `--attention-backend FLASHINFER`; 28-30% latency reduction for long-context inference.

## Key Facts

- Install: `pip install flashinfer-python`; supports sm7.5-sm12.0 GPU architectures (ref: sources/kascade-sparse-attention-research.md)
- 28-30% latency reduction for long-context inference (ref: sources/kascade-sparse-attention-research.md)
- Built-in Sparse MLA for DeepSeek models (ref: sources/kascade-sparse-attention-research.md)
- vLLM integration: `--attention-backend FLASHINFER` flag (ref: sources/kascade-sparse-attention-research.md)
- MLSys 2025 paper (ref: sources/kascade-sparse-attention-research.md)

## Relevance to STOPA

Recommended backend for any vLLM-based local inference stack. Easy integration path — single flag switch, production-tested.

## Mentioned In

- [Kascade & Sparse Attention — Implementace a Inspirace](../sources/kascade-sparse-attention-research.md)
