---
date: 2026-04-05
type: architecture
severity: high
component: memory
tags: [retrieval, search, ranking, bm25, learnings]
summary: "BM25-inspired memory-search.py replaces raw grep for learnings retrieval. IDF + term saturation + length normalization + metadata weights. 72 docs corpus, zero dependencies, synonym expansion. Ranked results vs unordered grep matches."
source: auto_pattern
confidence: 0.8
uses: 0
harmful_uses: 0
impact_score: 0.0
verify_check: "Glob('scripts/memory-search.py') → 1+ matches"
---

## BM25-Inspired Memory Retrieval

Implementován `scripts/memory-search.py` jako náhrada raw grep-first retrieval.

### Principy z BM25
- **IDF**: vzácné termy (pipeline=3.04) váží víc než běžné (harness=1.69)
- **Term frequency saturation**: 10 výskytů > 1, ale 100 už nepomáhá (k1=1.2)
- **Length normalization**: krátké focused learnings nebonusovány délkou (b=0.75)

### Kombinace s STOPA metadaty
BM25 score × metadata score (severity × source × confidence × impact × time_decay).
Výsledek: critical user_correction learning z minulého týdne > old medium auto_pattern.

### Unified retrieval
Prohledává learnings/ + critical-patterns.md + decisions.md + key-facts.md.
Jeden dotaz, seřazený výstup.

### Inspirace
LinkedIn post o BM25 vs vector search + Airweave (airweave-ai/airweave) hybrid retrieval.
Pro 72 dokumentů je BM25 scoring ideální — zero GPU, zero embeddings, zero dependencies.
