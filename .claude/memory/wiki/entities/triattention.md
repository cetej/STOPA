---
name: TriAttention
type: tool
first_seen: 2026-04-09
last_updated: 2026-04-09
sources: [triattention-kv-compression]
tags: [attention, kv-cache, compression, long-reasoning, efficiency, llm-architecture, vllm]
---

# TriAttention

> Trigonometric KV cache compression for long-context LLM reasoning — vLLM plugin ready. 2.5× throughput, 10.7× memory reduction vs Full Attention.

## Key Facts

- Core insight: pre-RoPE Q/K vectors cluster around fixed centers ("Q/K Concentration"), enabling trigonometric importance scoring (ref: sources/triattention-kv-compression.md)
- Benchmark (AIME25, Qwen3-8B, 32K tokens): 2.5× throughput, 10.7× KV cache reduction at matched accuracy (ref: sources/triattention-kv-compression.md)
- **vLLM plugin: PRODUCTION-READY** — `triattention.vllm.plugin:register_triattention_backend`, pre-calibrated for Qwen3-8B and DeepSeek-R1 variants
- **MLX support: EXPERIMENTAL** (Apple Silicon, merged Apr 7 2026)
- SGLang: not yet (on roadmap)
- KV budget: configurable, default 2048 tokens
- Code: https://github.com/WeianMao/triattention
- Authors: Weian Mao, Song Han (MIT), Yukang Chen (NVIDIA), Bohan Zhuang (ZJU)

## Relevance to STOPA

STOPA already supports vLLM as local inference backend. TriAttention plugin enables long-reasoning (30K+ tokens) on consumer GPUs with Qwen3-8B/DeepSeek-R1 — direct upgrade path for deep-tier local inference.

## Mentioned In

- [TriAttention: Efficient Long Reasoning with Trigonometric KV Compression](../sources/triattention-kv-compression.md)
