---
title: "TriAttention: Efficient Long Reasoning with Trigonometric KV Compression"
slug: triattention-kv-compression
source_type: url
url: "https://www.alphaxiv.org/abs/2604.04921"
date_ingested: 2026-04-09
date_published: "2026-04"
entities_extracted: 5
claims_extracted: 6
---

# TriAttention: Efficient Long Reasoning with Trigonometric KV Compression

> **TL;DR**: TriAttention compresses KV caches for long-context LLM reasoning by exploiting "Q/K Concentration" — the empirical observation that pre-RoPE query/key vectors cluster around fixed centers, enabling trigonometric importance scoring from positional distance + vector norms. Achieves 2.5× throughput and 10.7× memory reduction vs Full Attention on AIME25 with Qwen3-8B.

## Key Claims

1. Pre-RoPE Q/K vectors cluster around fixed centers ("Q/K Concentration"), causing attention patterns to favor specific token distances via trigonometric relationship — `argued` (theoretical analysis + empirical evidence)
2. TriAttention achieves 2.5× higher throughput than Full Attention at matched accuracy (AIME25, Qwen3-8B, 32K tokens) — `verified`
3. TriAttention reduces KV cache memory 10.7× while matching Full Attention accuracy — `verified`
4. Competing baselines achieve only ~50% of Full Attention accuracy at comparable efficiency levels — `verified`
5. Post-RoPE attention scores are unstable for importance estimation because they rotate with position — `argued`
6. TriAttention enables consumer GPU deployment where Full Attention causes OOM — `verified`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [TriAttention](../entities/triattention.md) | concept | new |
| [Q/K Concentration](../entities/qk-concentration.md) | concept | new |
| [Song Han](../entities/song-han.md) | person | new |
| [MLA (Multi-Head Latent Attention)](../entities/mla-multi-head-latent-attention.md) | concept | existing (complementary KV compression approach) |
| [NSA (Native Sparse Attention)](../entities/nsa-native-sparse-attention.md) | concept | existing (complementary sparse approach) |

## Relations

- TriAttention `competes_with` MLA — both compress KV cache, different mechanisms (trigonometric vs low-rank)
- TriAttention `competes_with` NSA — both address long-context efficiency, different layers (KV compression vs sparse attention)
- Q/K Concentration `part_of` TriAttention — the core theoretical insight enabling the compression
- Song Han `created_by` TriAttention — senior author (MIT)

## Cross-References

- Related learnings: none (first KV-compression-specific paper; complements attention-research.md)
- Related wiki articles: none directly (attention coverage is in entity pages only)
- Contradictions: none
