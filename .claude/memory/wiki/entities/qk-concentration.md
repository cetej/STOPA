---
name: Q/K Concentration
type: concept
first_seen: 2026-04-09
last_updated: 2026-04-09
sources: [triattention-kv-compression]
tags: [attention, kv-cache, llm-architecture, theory]
---

# Q/K Concentration

> Pre-RoPE query and key vectors in transformer attention cluster around fixed centers, causing attention patterns to favor specific token distances via a trigonometric relationship — the theoretical foundation of TriAttention.

## Key Facts

- Observation: pre-RoPE Q and K vectors form stable clusters around fixed centers, independent of position (ref: sources/triattention-kv-compression.md)
- Consequence: attention scores follow a trigonometric pattern based on positional distance and vector norms — making key importance predictable without computing full attention (ref: sources/triattention-kv-compression.md)
- Contrast with post-RoPE: post-RoPE attention scores rotate with position and are unstable estimators — all prior KV compression methods that rely on them have this flaw (ref: sources/triattention-kv-compression.md)
- Used by TriAttention to compress KV cache via positional-distance-based importance scoring (ref: sources/triattention-kv-compression.md)

## Relevance to STOPA

Theoretical grounding for why position-aware KV compression is feasible. If this property holds broadly across model families, it validates the pre-RoPE analysis approach as a general method for efficient long-context inference.

## Mentioned In

- [TriAttention: Efficient Long Reasoning with Trigonometric KV Compression](../sources/triattention-kv-compression.md)
