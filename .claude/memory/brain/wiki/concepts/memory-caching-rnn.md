# Memory Caching — RNNs with Growing Memory

**Source:** arXiv:2602.24281 (Behrouz et al., Google Research, 2026)
**Added:** 2026-04-15

## Core Idea

Technika pro překonání fixní paměti RNN: cachování checkpointů memory stavů na segmentových hranicích. Při zpracování tokenu model přistupuje k aktuálnímu stavu I ke všem cachovaným stavům z předchozích segmentů. Výsledek: laditelný knob mezi O(L) eficientou RNN a O(L²) kapacitou Transformerů.

## 4 varianty

| Varianta | Mechanismus | Vlastnost |
|----------|-------------|-----------|
| **Residual** | součet cachovaných stavů | kolabuje u lineárních modulů |
| **Gated Residual (GRM)** | context-aware gating (query×segment similarita) | konzistentně nejlepší |
| **Memory Soup** | interpolace parametrů (ne outputů) | jen pro non-lineární moduly |
| **Sparse Selective (SSC)** | MoE router, top-k segmentů | minimální overhead |

## Complexity interpolation

| Segment config | Komplexita | Analogie |
|----------------|-----------|----------|
| N=1 | O(L) | Klasický RNN |
| Equal segments | O(L²/C) | Balancovaný |
| Log segmenty | O(L log L) | Ultra-dlouhé sekvence |
| N=L | O(L²) | Full attention |

## Klíčové výsledky

- Titans + GRM: 100% needle-in-haystack na 16K, +0.8% language modeling
- Blíží se Transformerům na recall (SQuAD, NQ, SWDE) — gap výrazně zúžen
- SSC: minimální overhead oproti base RNN
- Post-training aplikace: cachování memory states za inference bez re-tréninku
- Log segmentace selhává na recall (příliš komprimuje vzdálenou minulost)

## Teoretický insight

Populární hybrid modely (attention + RNN) jsou matematicky ekvivalentní Memory Caching se segment size = 1. Paper formalizuje proč hybrid architektury empiricky fungují — jsou speciální případ MC na jednom konci complexity spektra.

## Abstraktní vzor: Checkpoint Caching

Paper formalizuje obecný vzor aplikovatelný mimo ML:

1. **Segmentuj** dlouhý stream na bloky
2. **Komprimuj** stav na hranicích do checkpointu
3. **Při dotazu** přistup k aktuálnímu stavu + selektivně k cachovaným checkpointům
4. **Gating** = query-dependent výběr relevantních checkpointů

Tento vzor je izomorfní s: session checkpointy (STOPA), git commits (kód), memory consolidation (neuroscience), progressive summarization (PKM).

## Connections

- Related: [[context-engineering]] — MC je hardware-level implementace context window škálování
- Related: [[second-brain]] — checkpoint caching je analogie k session checkpointům a progressive summarization
- Related: [[memfactory]] — MemFactory extract/update/retrieve ≈ MC segment/cache/gate
- Related: [[agent-memory-taxonomy]] — MC formalizuje "growing memory" rodinu z write-manage-read taxonomie
- Applied-in: STOPA checkpoint.md (save state at boundaries), hybrid retrieval (query-dependent gating přes RRF)
