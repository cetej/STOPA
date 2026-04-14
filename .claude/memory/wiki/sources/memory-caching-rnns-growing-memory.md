---
title: "Memory Caching: RNNs with Growing Memory"
slug: memory-caching-rnns-growing-memory
source_type: url
url: "https://arxiv.org/abs/2602.24281"
date_ingested: 2026-04-13
date_published: "2026-02"
entities_extracted: 2
claims_extracted: 5
---

# Memory Caching: RNNs with Growing Memory

> **TL;DR**: Cachování checkpointů hidden states po segmentech umožňuje RNN paměti růst se sekvencí (O(NL) interpolace mezi O(L) RNN a O(L²) Transformer). 4 varianty (Residual, Gated Residual, Memory Soup, Sparse Selective). GRM varianta nejlepší — Titans+GRM uzavírá gap s Transformery na recall tasks. Matematicky: segment=1 + gated MC = gated global attention.

## Key Claims

1. Fixní paměť RNN = hlavní důvod selhání na recall-intensive tasks; MC to řeší cachováním memory checkpointů — `[argued]`
2. Komplexita O(NL) kde 1≤N≤L — plynulá interpolace RNN↔Transformer — `[verified]`
3. GRM (Gated Residual Memory) konzistentně nejlepší varianta — input-dependent gating pro selektivní retrieval z cached segmentů — `[verified]`
4. Titans+GRM: 52.55 avg (760M/30B) vs Transformer++ 49.64; na 1.3B/100B tokens: DLA+GRM 55.96 vs Transformer++ 53.19 — `[verified]`
5. Segment size 1 + gated MC matematicky ekvivalentní gated global softmax attention — MC jako principiální zobecnění attention — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Memory Caching (MC)](../entities/memory-caching-mc.md) | concept | new |
| [Titans](../entities/titans.md) | tool | existing (check) |

## Relations

- Memory Caching `extends` RNN — adds cached hidden state checkpoints
- Memory Caching `interpolates` between RNN and Transformer — O(NL) complexity
- GRM `uses` input-dependent gating — selective cached memory retrieval
- Memory Caching `inspired_by` weight souping (Memory Soup variant)

## Cross-References

- Related wiki sources: [in-place-ttt-mlp-fast-weights](in-place-ttt-mlp-fast-weights.md) (TTT: weight adaptation at inference — related memory paradigm)
- Related learnings: none directly
- Contradictions: none
