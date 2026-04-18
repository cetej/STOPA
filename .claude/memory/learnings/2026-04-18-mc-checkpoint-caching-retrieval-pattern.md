---
date: 2026-04-18
type: architecture
severity: medium
component: memory
tags: [memory, retrieval, checkpoints, compaction, architecture]
summary: "Memory Caching (MC) formalizes a universal pattern: segment long stream → compress state at boundary → cache checkpoint → gate retrieval by query. STOPA session checkpoints and hybrid-retrieve implement this implicitly. Formal design: use GRM-style query-dependent gating (query × cached-state similarity) when choosing which checkpoints to surface, not flat recency."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.7
maturity: draft
valid_until:
skill_scope: []
related: [2026-04-18-retrieval-depth-knob-complexity-interpolation.md, 2026-04-08-living-memory-over-static-retrieval.md, 2026-04-08-recency-beats-complex-memory.md]
verify_check: "manual"
model_gate:
impact_score: 0.0
task_context:
  task_class: research
  complexity: medium
  tier: standard
---

## Detail

Behrouz et al. (arXiv:2602.24281) prove that cachování hidden states na segmentových hranicích tvoří O(NL) memory s plynulou kontrolou mezi O(L) eficiencí RNN a O(L²) kapacitou Transformerů.

**Přenositelný vzor pro STOPA:**

| MC krok | STOPA analogie | Současný stav |
|---------|---------------|---------------|
| Segmentuj sekvenci | Chunk learnings dle tématu/komponentu | Grep-first (component tag) |
| Komprimuj stav | Checkpoint.md session summary | Implementováno |
| Cachuj checkpoint | learnings/ soubory | Implementováno |
| GRM gate (query × segment) | hybrid-retrieve RRF | Implementováno — ale bez explicitního query×chunk similarity |

**Optimalizační příležitost**: Současný hybrid-retrieve kombinuje grep + BM25 + graph váhami (RRF k=60). GRM insight: gating by měl být query-dependent (ne jen statické váhy). Kandidátní upgrade: přidat embedding similarity query × learning summary jako čtvrtý retrieval kanál.

**Ref**: brain/wiki/concepts/memory-caching-rnn.md (4 varianty + complexity tabulka)
