---
title: "How Well Do Agentic Skills Work in the Wild: Benchmarking LLM Skill Usage in Realistic Settings"
slug: benchmarking-llm-skill-usage-realistic-settings
source_type: url
url: "https://arxiv.org/abs/2604.04323"
date_ingested: 2026-04-07
date_published: "2026-04-06"
entities_extracted: 5
claims_extracted: 6
---

# How Well Do Agentic Skills Work in the Wild

> **TL;DR**: Skill benefits degrade consistently as conditions become more realistic — from 55.4% (force-loaded) to 38.4% (retrieved from 34K pool), only 3pp above no-skill baseline. Two bottlenecks: agents can't identify skills from metadata alone, and can't adapt general-purpose skills. Query-specific refinement recovers 57.7%→65.5% on Terminal-Bench 2.0.

## Key Claims

1. Pass rates approach no-skill baselines under most realistic retrieval conditions — `[verified]`
2. Only 49% of Claude trajectories loaded all curated skills when optional (vs 100% forced) — skill selection is the first bottleneck — `[verified]`
3. Agentic hybrid search: 56.8% Recall@3 vs 38.1% direct semantic search — iterative querying essential — `[verified]`
4. Query-specific refinement = multiplier on existing quality, not knowledge generator; requires coverage ≥3.83 — `[argued]`
5. Claude Opus 4.6: 57.7% → 65.5% on Terminal-Bench 2.0 with query-specific refinement — `[verified]`
6. Skill ecosystems must be calibrated per model capability — smaller models need simpler, more targeted skills — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [arXiv:2604.04323](../entities/arxiv-2604-04323.md) | paper | new |
| [SKILLS-BENCH](../entities/skills-bench.md) | concept | new |
| [Terminal-Bench 2.0](../entities/terminal-bench-2.md) | concept | new |
| [query-specific-refinement](../entities/query-specific-refinement.md) | concept | new |

## Relations

- arXiv:2604.04323 `extends` arXiv:2603.25723 (NLAH) — NLAH validates SKILL.md patterns; this paper benchmarks at scale
- query-specific-refinement `maps_to` self-evolve — STOPA's /self-evolve is the implementation
- SKILLS-BENCH `evaluates` skill-selection — covers the 49% voluntary load rate problem
- agentic-hybrid-search `instantiates` hybrid-retrieval — same BM25+dense combo as STOPA memory-search.py

## Cross-References

- Related learnings: `2026-04-07-agents-md-efficiency-validated` (NLAH paper), skill-files.md (description=trigger rule)
- Related wiki articles: [skill-design](../skill-design.md), [skill-evaluation](../skill-evaluation.md), [memory-architecture](../memory-architecture.md)
- Contradictions: none detected
