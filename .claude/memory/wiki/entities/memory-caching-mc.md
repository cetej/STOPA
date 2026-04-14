---
name: Memory Caching (MC)
type: concept
first_seen: 2026-04-13
last_updated: 2026-04-13
sources: [memory-caching-rnns-growing-memory]
tags: [architecture, memory, rnn, inference, long-context]
---

# Memory Caching (MC)

> Technika cachování checkpointů hidden states RNN po segmentech. Paměť roste se sekvencí — O(NL) interpolace mezi O(L) RNN a O(L²) Transformer. 4 varianty s různým trade-off recall vs compute.

## Key Facts

- Sekvence se dělí na segmenty S(1)...S(N); na konci každého segmentu se cachuje memory state M(i) (ref: sources/memory-caching-rnns-growing-memory.md)
- Retrieval: online memory + forward pass přes všechny cached memories → output per token (ref: sources/memory-caching-rnns-growing-memory.md)
- 4 varianty: Residual Memory, Gated Residual Memory (GRM), Memory Soup, Sparse Selective Caching (SSC) (ref: sources/memory-caching-rnns-growing-memory.md)
- GRM: input-dependent gating γ(i)_t moduluje příspěvek každého segmentu; context-aware — nemůže být pre-computed (ref: sources/memory-caching-rnns-growing-memory.md)
- Memory Soup: averaging parametrů cached memory modulů (inspirace weight souping) (ref: sources/memory-caching-rnns-growing-memory.md)
- SSC: MoE-style router vybírá top-k relevantních cached memories → efektivnější než full scan (ref: sources/memory-caching-rnns-growing-memory.md)
- Segment size 1 + gated MC = matematický ekvivalent gated global softmax attention (ref: sources/memory-caching-rnns-growing-memory.md)
- Logaritmické segmentování: O(L log L) komplexita, ale nižší rozlišení pro vzdálenou minulost (ref: sources/memory-caching-rnns-growing-memory.md)
- Titans+GRM: 52.55 avg (760M), DLA+GRM: 55.96 (1.3B) — překonává Transformer++ (ref: sources/memory-caching-rnns-growing-memory.md)
- Autoři: Google Research (Ali Behrouz et al.)

## Relevance to STOPA

MC princip je analogický STOPA checkpoint systému: cachujeme komprimovaný stav (memory/session) na segmentových hranicích a při retrieval kombinujeme online kontext s historickými checkpointy. GRM gating odpovídá relevance-weighted memory retrieval v STOPA hybrid-retrieve. Logaritmické vs konstantní segmentování = trade-off mezi granularitou a compute — přenositelné na design memory compaction strategie.

## Mentioned In

- [Memory Caching: RNNs with Growing Memory](../sources/memory-caching-rnns-growing-memory.md)
