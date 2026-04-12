---
name: reference_distributed_systems_paper
description: "arXiv:2603.12229 — LLM Teams as Distributed Systems: Amdahl's law for agent teams, centralized vs decentralized topology benchmarks, cost-performance tradeoffs"
type: reference
---

**Paper:** "Language Model Teams as Distributed Systems" (arXiv:2603.12229)
**Authors:** Mieczkowski, Collins, Sucholutsky, Vélez, Griffiths (Princeton/Cambridge)
**Date:** 2026-03-12

Key findings integrated into STOPA /orchestrate skill:
- Centralized orchestrator is decisively better (1.36× vs 0.88× median speedup)
- Amdahl's formula with 0.75 empirical discount predicts real-world agent team speedup
- p < 0.4 → never multi-agent (5.83× cost for 1.13× speedup)
- File ownership manifests prevent the #1 consistency failure (concurrent writes)
- Diminishing returns after 4 agents; Claude Sonnet 4.6 scales best

**How to apply:** When designing or modifying multi-agent workflows, reference this paper's quantitative bounds. The parallelizability estimate (p = independent/total subtasks) is the key decision variable.
