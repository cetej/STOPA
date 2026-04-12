---
name: HERA Paper — Experience as Infrastructure
description: Virginia Tech multi-agent RAG with failure-driven learning (+38.69% SOTA), 3 mechanisms for STOPA integration
type: reference
---

**Paper:** arXiv:2604.00901v2 (Li & Ramakrishnan, Virginia Tech)
**Full analysis:** `docs/HERA_INTEGRATION.md`

## Three Core Mechanisms

1. **Experience Library** — (query_type, insight, utility) tuples ranked by empirical success rate. Consolidation: ADD/MERGE/PRUNE/KEEP. Maps to STOPA learnings/ but with utility tracking.

2. **Role-aware Prompt Evolution (RoPE)** — identify failing agent → generate prompt variants along 3 axes (efficiency, thoroughness, risk_sensitivity) → replay full trajectory → extract operational rules + behavioral principles. Ablation: removal causes up to -30%. Strongest single component.

3. **Topology Evolution** — agent graphs spontaneously reorganize (4 phases: initial → exploration → refinement → optimization). Redundant agents pruned, compact high-performance networks emerge. Nobody designed these structures — they emerged from failure.

## Key Numbers

- +38.69% average over SOTA across 6 RAG benchmarks
- MusiQue F1: +32% (hardest multi-hop)
- HoVer accuracy: +64.95% (OOD fact verification)
- Token usage DECLINES over time (system gets cheaper as it gets smarter)
- Synergy: Experience Library + RoPE > sum of parts (non-additive)

## STOPA Integration Plan

6-phase implementation in `docs/HERA_INTEGRATION.md`:
- Phase 1: Failure classification + trajectory storage
- Phase 2: Agent fault attribution
- Phase 3: Experience Library upgrade (utility scoring)
- Phase 4: RoPE-lite (mental replay, not full — cost-aware)
- Phase 5: Topology evolution tracking
- Phase 6: GRPO-lite (optional, very expensive)

**Key design decision:** Mental replay instead of full trajectory replay (10x cheaper, sufficient for skill-level improvement). Full replay only for 3+ repeated same-class failures.

## Limitations (from paper)

- No symbolic reasoning (fails on set operations)
- Property disambiguation weakness
- Backbone-dependent (Qwen >> Llama)
- PRUNE may lose edge-case insights
- Benchmarked only on RAG, not code tasks
