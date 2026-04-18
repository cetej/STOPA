---
title: "TriAttention — AlphaSignal Practitioner Summary"
slug: triattention-alphsignal-practitioner
source_type: url
url: "https://alphasignal.ai/"
date_ingested: 2026-04-18
date_published: "2026-04-18"
entities_extracted: 3
claims_extracted: 5
---

# TriAttention — AlphaSignal Practitioner Summary

> **TL;DR**: Practitioner evaluation of TriAttention by AlphaSignal — adds deployment instructions, budget-accuracy tradeoff table, AMD/MLX ports, and a "Worth Watching" (not production-ready) verdict. Contradicts prior entity entry that marked vLLM integration as PRODUCTION-READY.

## Key Claims

1. TriAttention at 3,072-token KV budget matches Full Attention exactly on AIME25 (40.8% vs 40.8%) at 2.5× throughput — `verified`
2. At 1,024-token budget: 1.2pp accuracy drop (68.4% vs 69.6% on MATH-500) with 6.3× throughput — `verified`
3. Calibration data quality is irrelevant: Google homepage HTML achieves 46.2% AIME24 vs curated ShareGPT 46.7% (0.5pp diff) — `verified` (paper ablation Table F)
4. Prefix caching (`--enable-prefix-caching`) MUST be disabled; incompatible with KV compression — `verified` (deployment requirement)
5. R-KV and SnapKV collapse at reasoning depth: 61% at depth 14 → 31% at depth 16; TriAttention maintains accuracy — `verified`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [TriAttention](../entities/triattention.md) | tool | updated |
| [AlphaSignal](../entities/alphsignal-ai.md) | company | new |
| [R-KV](../entities/r-kv.md) | concept | new |

## Relations

- AlphaSignal `reviews` TriAttention — practitioner verdict: Worth Watching
- R-KV `competes_with` TriAttention — query-window-based baseline, collapses at depth >14
- R-KV `extends` SnapKV — adds recurrence but inherits post-RoPE instability

## Cross-References

- Related learnings: `2026-04-09-triattention-pre-rope-kv-compression.md` (prior arXiv learning, uses=6)
- Related wiki articles: `pipeline-engineering.md` (covers TriAttention), `memory-architecture.md` (retrieval depth knob)
- WARNING: Contradicts entity `triattention.md` line "vLLM plugin: PRODUCTION-READY" — AlphaSignal rates "Worth Watching / evaluate before production commit"
