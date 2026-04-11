---
name: Attention Matching (AM) Framework
type: concept
first_seen: 2026-04-11
last_updated: 2026-04-11
sources: [latent-briefing-kv-cache-compaction]
tags: [kv-cache, attention, compression, inference]
---

# Attention Matching (AM) Framework

> KV cache compaction framework that finds a compact cache producing nearly identical attention outputs via token selection, bias correction (NNLS), and value reconstruction (ridge regression).

## Key Facts

- Zweiger et al. (2026): given KV cache size S, find compact cache size t < S with softmax(Q·C1ᵀ+β)·C2 ≈ softmax(Q·Kᵀ)·V (ref: sources/latent-briefing-kv-cache-compaction.md)
- Three steps per (layer,head): token selection (top-t by attention score), beta via NNLS (bias corrections), C2 via ridge regression (value reconstruction) (ref: sources/latent-briefing-kv-cache-compaction.md)
- Original: 320 serialized solves for Qwen3-14B (40 layers × 8 KV heads), 30+s on A100 (ref: sources/latent-briefing-kv-cache-compaction.md)
- Latent Briefing's shared global mask batches all 320 solves → ~1.7s (ref: sources/latent-briefing-kv-cache-compaction.md)

## Relevance to STOPA

Foundational compression technique. Complementary to TriAttention (pre-RoPE importance scoring) — AM operates on full attention outputs while TriAttention exploits geometric structure. Both reduce KV cache cost for long-context inference.

## Mentioned In

- [Latent Briefing: KV Cache Compaction for Multi-Agent Systems](../sources/latent-briefing-kv-cache-compaction.md)
