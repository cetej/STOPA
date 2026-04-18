---
name: TriAttention
type: tool
first_seen: 2026-04-09
last_updated: 2026-04-18
sources: [triattention-kv-compression, triattention-alphsignal-practitioner]
tags: [attention, kv-cache, compression, long-reasoning, efficiency, llm-architecture, vllm]
---

# TriAttention

> Trigonometric KV cache compression for long-context LLM reasoning — vLLM env-var integration. 2.5× throughput, 10.7× memory reduction vs Full Attention. Worth Watching — not production-ready yet.

## Key Facts

- Core insight: pre-RoPE Q/K vectors cluster around fixed centers ("Q/K Concentration"), enabling trigonometric importance scoring (ref: sources/triattention-kv-compression.md)
- Benchmark (AIME25, Qwen3-8B, 32K tokens): 2.5× throughput, 10.7× KV cache reduction at matched accuracy (ref: sources/triattention-kv-compression.md)
- **Budget-accuracy tradeoff**: 3,072 budget → 2.5× speed, 0pp loss; 1,024 budget → 6.3× speed, 1.2pp loss on MATH-500 (ref: sources/triattention-alphsignal-practitioner.md)
- **vLLM integration: EVALUATION-READY** — two env vars, no code changes. `--enable-prefix-caching false` required (incompatible) (ref: sources/triattention-alphsignal-practitioner.md)
- **MLX support: EXPERIMENTAL** (Apple Silicon, Apr 9 2026); AMD ROCm/HIP port Apr 11 + TurboQuant stacking = ~6.8× effective KV reduction
- Calibration data quality: irrelevant — Google homepage HTML (46.2%) ≈ curated ShareGPT (46.7%) on AIME24 (0.5pp diff)
- KV budget: configurable via `TRIATTN_RUNTIME_KV_BUDGET`, default 2048 tokens
- **Known limitations**: no dedicated GPU kernel (compute overhead), prefix caching incompatible, only 3 verified model families
- Code: https://github.com/WeianMao/triattention
- Authors: Weian Mao, Song Han (MIT), Yukang Chen (NVIDIA), Bohan Zhuang (ZJU)

## Relevance to STOPA

STOPA already supports vLLM as local inference backend. TriAttention plugin enables long-reasoning (30K+ tokens) on consumer GPUs with Qwen3-8B/DeepSeek-R1 — direct upgrade path for deep-tier local inference.

## Mentioned In

- [TriAttention: Efficient Long Reasoning with Trigonometric KV Compression](../sources/triattention-kv-compression.md)
- [TriAttention — AlphaSignal Practitioner Summary](../sources/triattention-alphsignal-practitioner.md)
