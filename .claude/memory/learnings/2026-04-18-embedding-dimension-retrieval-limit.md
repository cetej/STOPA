---
date: 2026-04-18
type: architecture
severity: medium
component: memory
tags: [retrieval, embedding, bm25, theory, hybrid-retrieve]
summary: "Weller et al. (ICLR 2026, arXiv:2508.21038) prove single-vector embeddings cannot retrieve all top-k document combos beyond dimension threshold: d ≥ log(C(n,k)) / log(1 + 1/γ). BM25 scores 97.8% recall@2 on LIMIT-small where SOTA embeddings score 54.3%. STOPA's grep+BM25+graph hybrid is theoretically grounded — avoid embedding-only retrieval on heterogeneous corpora."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
maturity: draft
valid_until:
skill_scope: [orchestrate, scout]
related: [2026-04-18-retrieval-depth-knob-complexity-interpolation.md, 2026-04-05-bm25-memory-search.md]
verify_check: "Glob('scripts/memory-search.py') → 1+ matches"
model_gate:
impact_score: 0.0
task_context:
  task_class: research
  complexity: low
  tier: light
---

## Detail

Theoretical bound (Weller et al., ICLR 2026):

For a corpus of n documents and retrieval size k, any single-vector embedding model of dimension d can only retrieve a bounded number of top-k subsets. Full coverage requires:

```
d ≥ log(C(n,k)) / log(1 + 1/γ)
```

Where γ is the margin parameter. Practically: 500k documents need d≥512 to cover all top-2 combinations.

**Benchmark evidence (LIMIT dataset):**

| Model type | Recall@2 (LIMIT-small) | Recall@2 (50k docs) |
|-----------|----------------------|---------------------|
| BM25 | 97.8% | — |
| SOTA neural embeddings | 54.3% | ~30% |
| Cross-encoders | substantially better | substantially better |
| Multi-vector (ColBERT) | substantially better | substantially better |

In-domain training = minimal improvement → intrinsic limit, not domain shift.

**STOPA implication**: `scripts/memory-search.py` uses BM25 (not embeddings) — this is not just pragmatic (zero GPU dependencies) but theoretically correct for a heterogeneous learnings corpus with diverse relevance criteria.
