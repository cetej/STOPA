# Provenance: arXiv:2603.12710 deepresearch

**Date:** 2026-04-26  
**Question:** Hluboký rozbor paperu Shahnovsky & Dror (2026) "AI Planning Framework for LLM-Based Web Agents" — taxonomie, 5 metrik, dataset, kritická evaluace metodologie + STOPA mapping  
**Scale:** comparison  
**Rounds:** 1 (discovery + reading + synthesis + verification + final brief)  
**Sources:** 17 consulted / 12 directly fetched / 3 transitive / 2 partial / 0 rejected  
**Verification:** DONE_WITH_CONCERNS — 6 issues raised, all addressed in final brief

## Research Files

| File | Agent | Purpose |
|------|-------|---------|
| outputs/.research/arxiv-2603.12710-research-paper.md | lead (WebFetch) | Direct paper extraction via Jina Reader |
| outputs/.research/webarena-discovery.md | discovery-webarena (Haiku) | URL ranking — WebArena context (5/5 calls) |
| outputs/.research/planning-discovery.md | discovery-planning (Haiku) | URL ranking — planning literature (5/5 calls) |
| outputs/.research/eval-frameworks-research.md | reader-eval (Sonnet) | 5 trajectory eval frameworks fetched + analyzed (8/8 calls) |
| outputs/.research/planning-taxonomy-research.md | reader-planning (Sonnet) | Planning taxonomy literature fetched + analyzed (7/8 calls) |
| outputs/.research/arxiv-2603.12710-synthesis.md | lead | Cross-branch synthesis with markers |
| outputs/.research/arxiv-2603.12710-verification.md | verifier | URL liveness + claim alignment + orphan + marker audit |
| outputs/.research/arxiv-2603.12710-claims.md | lead | Pre-final claim inventory checkpoint (Step 5.5) |
| outputs/arxiv-2603.12710-research.md | lead | **Final brief (deliverable)** |
| outputs/arxiv-2603.12710-research.provenance.md | lead | This file |

## Pipeline Stats

- Discovery phase: ~3 min (2 parallel Haiku agents, 10 searches total)
- Reading phase: ~6 min (2 parallel Sonnet agents, 15 fetches total)
- Synthesis: ~2 min (lead — flat merge, comparison scale)
- Verification: ~3 min (verifier sub-agent, URL checks + alignment + orphans)
- Final brief: ~3 min (lead — incorporating verifier corrections + STOPA mapping)
- **Total wall time:** ~17 min

## Uncertainty Summary

| Marker | Count |
|--------|-------|
| [VERIFIED] | 26 |
| [INFERRED] | 3 |
| [SINGLE-SOURCE] | 1 |
| [UNVERIFIED] | 2 |

**Unverified rate:** 6.3% — well under 30% threshold.

## Verifier Concerns Resolved

1. ✅ WebJudge "85%" → uvedeno jako range 83.6%-87% across model variants
2. ✅ Bilenko 6-dimension structure → opraveno na top-level dimensions (Core / Cognitive / Learning / Multi-Agent / Environments / Evaluation), ne sub-components
3. ✅ AgentOccam vs tree-search citation → změněno z [7] (ToolTree) na [6] (Plan-MCTS) — wrong source originally
4. ✅ GPT-5-mini name → marked [UNVERIFIED] in final brief
5. ✅ Yao 2023 / Koh 2024 transitive citations → marker změněn z [VERIFIED] na [INFERRED]
6. ✅ Orphan source rows ([2]-[5], [15], [17]) → strukturálně cleaned in final evidence table

## Cost Estimate

- Discovery (Haiku): ~$0.05
- Reading (Sonnet): ~$0.30
- Synthesis (lead Opus): ~$0.40
- Verification: ~$0.20
- Final brief: ~$0.30
- **Estimated total:** ~$1.25

## Knowledge Graph Status

Auto-ingest pending (next step). Will populate:
- Entity pages: Shahnovsky&Dror2026, Plan-MCTS, AgentRewardBench, WebGraphEval, TRACE, WebArena Verified, Bilenko2026, ToT, LATS, Koh2024, AgentOccam
- Source summary: arxiv-2603.12710 with cross-links
- Concept-graph updates: trajectory-evaluation, planning-taxonomy, web-agent-architecture nodes
- Learnings candidates: "linear well-tuned > naive tree search on WebArena", "Recovery Rate as orchestration metric", "plan-space search granularity matters"
