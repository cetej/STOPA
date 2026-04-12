---
name: reference_memory_systems_research
description: Deep research on AI agent memory systems — what makes memory useful, retrieval quality, consolidation/dreams, empirical results (MemoryOS, A-MEM, Mem0, MemMachine, ACT-R, OpenClaw)
type: reference
---

Comprehensive research (2026-04-11, 12 sources, 40+ discovery) on AI agent memory systems.

**Key findings:**

1. **Retrieval >> Storage**: MemMachine ablation shows +9.4% from retrieval optimization vs +0.8% from ingestion improvements. Invest in hybrid-retrieve.py, not more YAML fields.

2. **Three-signal fusion** (ACT-R): effective retrieval = recency/frequency + semantic relevance + importance. Keyword search captures zero signals. STOPA partially implements via time-weighted relevance + impact_score + hybrid-retrieve.

3. **Reflection is load-bearing**: Reflexion 91% vs 80% HumanEval. Generative Agents degenerate in 48h without reflection. Dreams/offline consolidation is not optional.

4. **Quality >> Quantity**: Curated memory beats add-all. Fine-tuned evaluator (300 examples) dramatically outperforms vanilla LLM judge for admission. History-based deletion (low utility) > periodic cleanup.

5. **Hierarchical pre-filtering**: ByteRover 5-tier tree resolves most queries at sub-100ms without embedding calls. STOPA's flat grep misses this.

6. **OpenClaw dream cycle**: collect (7d logs) → consolidate (dedup, link) → evaluate (score, forgetting curves). Smart Skip saves 90% tokens on idle days.

7. **A-MEM backward-updating**: New memories trigger context updates on old related memories. STOPA has `related:` and `supersedes:` but no automatic backward-updating.

**STOPA gaps identified**: (1) no offline dream consolidation, (2) no backward-updating, (3) no structural pre-filtering, (4) no utility-based archival, (5) no downstream impact measurement.

**Action taken**: Created `/dreams` skill + scheduled task (daily 4:47 AM) for LLM-powered cross-session consolidation.

Full brief: `outputs/memory-systems-research.md`
Sources: arxiv 2603.07670, 2506.06326, 2502.12110, 2504.19413, 2604.04853, 2505.16067, 2604.01599 + OpenClaw docs + LangChain LangMem
