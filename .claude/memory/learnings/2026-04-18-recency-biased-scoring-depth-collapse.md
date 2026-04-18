---
date: 2026-04-18
type: architecture
severity: high
component: memory
tags: [retrieval, kv-cache, recency-bias, depth, long-horizon, hybrid-retrieve, attention]
summary: "Recency-biased retrieval (scoring tokens/learnings by recent-query relevance) collapses at depth >14 in DFS reasoning: R-KV/SnapKV drop from 61% to 31%. Position-independent scoring (TriAttention pre-RoPE; graph walk) maintains accuracy. STOPA: BM25 alone suffers same failure on long-session retrieval — graph walk compensates."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.7
maturity: draft
valid_until:
skill_scope: [orchestrate, scout]
related: [2026-04-18-retrieval-depth-knob-complexity-interpolation.md, 2026-04-09-triattention-pre-rope-kv-compression.md]
verify_check: "manual"
model_gate:
impact_score: 0.0
failure_class:
---

## Recency-Biased Retrieval Depth Collapse

**Pattern**: Retrieval methods that score importance using a narrow recent-query window fail at reasoning depth. Concrete evidence from TriAttention paper:

| Method | Depth 14 accuracy | Depth 16 accuracy |
|--------|------------------|------------------|
| R-KV (recency-biased) | 61% | 31% (−50%) |
| SnapKV (recency-biased) | ~50% | ~30% |
| TriAttention (position-independent) | ~60% | ~60% (stable) |

**Root cause**: Post-RoPE query rotation makes importance scores position-unstable. Recent queries score recent tokens high, distant tokens (needed for backtracking in DFS) get pruned.

**STOPA analog**:
- BM25 over current task description = recency-biased (query shifts each session → old learnings score low)
- Graph walk = position-independent (follows conceptual edges regardless of learning age)
- Risk: on long multi-session tasks (deepresearch, build-project), BM25-only retrieval prunes early-session-critical learnings just like R-KV prunes DFS backtrack tokens

**Mitigation (already implemented)**: hybrid-retrieve.py uses BM25 + graph walk. For `tier=deep` tasks, graph walk is mandatory. Ensure graph walk doesn't get disabled when BM25 returns 3+ results on long-horizon tasks.

**Reference**: arXiv:2604.04921 + AlphaSignal practitioner analysis (2026-04-18)
