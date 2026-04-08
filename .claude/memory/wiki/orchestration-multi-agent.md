---
generated: 2026-04-04
cluster: orchestration-multi-agent
sources: 13
last_updated: 2026-04-08
---

# Multi-Agent Orchestration

> **TL;DR**: Centralized orchestration beats decentralized (1.36x vs 0.88x speedup). At equal thinking-token budgets, single-agent systems match or beat multi-agent — MAS advantage comes from unconstrained compute, not architecture. Self-organizing +8% on exploratory; hierarchical wins on structured. PDDL I/O contracts cut failures 3x. Repo-level instruction files (AGENTS.md) reduce agent runtime by 28.64%.

## Overview

Research on distributed LLM agent systems (arXiv:2603.12229) proves that centralized coordination consistently outperforms decentralized approaches. For tasks with low parallelizability (p < 0.4), multi-agent systems cost 5.83x tokens for only 1.13x speedup — an Amdahl gate and ROI cost gate were added to the orchestrate skill to prevent this waste (ref: 2026-04-02-distributed-systems-amdahl-gate.md).

Dynamic agent graph orchestration (BiGMAS) demonstrates that task-specific graph topologies outperform fixed structures: a GraphDesigner analyzes the task and generates appropriate topology (3 nodes for simple, 9 for complex), with agents coordinating via centralized shared workspace (ref: 2026-03-29-bigmas-directed-graph-orchestration.md). This aligns with Society of Thought findings (Kim et al. 2026) that RL optimization spontaneously generates multi-agent debate in reasoning models — heterogeneous perspectives improve performance, and shared state (STOPA's checkpoint) is necessary to prevent temporal misalignment (ref: 2026-03-30-society-of-thought-orchestration.md).

A/B testing confirmed that self-organizing agents (given only a mission, no prescribed roles) outperform hierarchical assignment by +8% on exploratory tasks (audit, research, scouting), while hierarchical assignment wins on structured output tasks like ranking and scoring. Orchestrate should detect task style and adjust prescription level accordingly (ref: 2026-04-06-self-organizing-agents-ab-test.md).

Neuro-symbolic orchestration patterns from PDDL research (arXiv:2602.19260) show that explicit operator interfaces — `input-contract`, `preconditions`, `effects` per skill — enable plan chain validation BEFORE agent execution, eliminating downstream failures from incompatible handoffs. Combined with `done_when` completion criteria and mid-execution replanning, these patterns outperform end-to-end VLA approaches 3x (ref: 2026-04-07-nsm-neuro-symbolic-orchestration.md).

A key compute-budget finding (DPI research, arXiv 2026) shows that at equal thinking-token budgets, single-agent systems achieve equal or better performance than multi-agent ones. MAS advantage comes from unconstrained compute scaling, not architectural superiority. The remaining justifications for MAS are parallelization, specialization, and fault isolation (ref: 2026-04-07-sas-beats-mas-equal-compute.md).

MoM/TARo-inspired upgrades brought four improvements to orchestrate: scout quality gate (upstream-first verification), role-specific critic weights, per-subtask adaptive model routing, and haiku-first difficulty estimation (ref: 2026-04-07-mom-taro-orchestration-upgrades.md). Empirical validation from agent benchmarks confirmed that repo-level instruction files (AGENTS.md / CLAUDE.md / skills) reduce agent runtime by 28.64% and output token consumption by 16.58% while maintaining task completion — validating STOPA's design philosophy (ref: 2026-04-07-agents-md-efficiency-validated.md).

OpenFang (Rust Agent OS) contributes three reference patterns: sandbox isolation via runtime metering in tool-gate.py, Merkle audit trail for OSINT outputs, and daemon-based scheduling without a running session (ref: 2026-04-05-openfang-architecture-patterns.md).

Iterative agent work suffers from structural erosion: SlopCodeBench shows AI agents produce 2.2x more redundant code than humans and no agent completes long sequences without degradation (ref: 2026-03-29-slopcodebench-iterative-degradation.md). AutoAgent patterns address this with anti-overfitting guards (ref: 2026-04-03-autoagent-overfitting-guard.md).

## Key Rules

1. **Centralized > decentralized**: use a coordinator, not peer-to-peer agents (ref: 2026-04-02-distributed-systems-amdahl-gate.md)
2. **Amdahl gate**: skip multi-agent for tasks with p < 0.4 parallelizability (ref: 2026-04-02-distributed-systems-amdahl-gate.md)
3. **Self-org for exploration, hierarchical for structured output**: detect task style in Phase 1 (ref: 2026-04-06-self-organizing-agents-ab-test.md)
4. **Validate plan chain BEFORE launch**: effects(step N) must satisfy preconditions(step N+1) (ref: 2026-04-07-nsm-neuro-symbolic-orchestration.md)
5. **done_when per subtask**: machine-verifiable completion criteria, not "I think I'm done" (ref: 2026-04-07-nsm-neuro-symbolic-orchestration.md)
6. **Anti-overfitting guard**: ask "would this change be worthwhile without this eval case?" (ref: 2026-04-03-autoagent-overfitting-guard.md)
7. **Checkpoints between iterations**: agents degrade without quality gates (ref: 2026-03-29-slopcodebench-iterative-degradation.md)
8. **Daemon scheduling for headless**: Python daemon + claude-code-sdk-python for session-independent scheduling (ref: 2026-04-05-openfang-architecture-patterns.md)
9. **SAS ≥ MAS at equal compute**: only use MAS when parallelization, specialization, or fault isolation justify overhead (ref: 2026-04-07-sas-beats-mas-equal-compute.md)
10. **AGENTS.md saves 28.64% runtime**: maintain quality instruction files at repo level (ref: 2026-04-07-agents-md-efficiency-validated.md)
11. **Upstream-first scout gate**: verify source quality before processing (ref: 2026-04-07-mom-taro-orchestration-upgrades.md)

## Patterns

### Do
- Scale graph complexity with task demands (ref: 2026-03-29-bigmas-directed-graph-orchestration.md)
- Use explicit refactor phases between iterations (ref: 2026-03-29-slopcodebench-iterative-degradation.md)
- Tag tool outputs as `[UNTRUSTED]` when from external sources; block use in privileged tools (ref: 2026-04-05-openfang-architecture-patterns.md)
- Define `input-contract` and `output-contract` on all Tier 1 skills (ref: 2026-04-07-nsm-neuro-symbolic-orchestration.md)

### Don't
- Parallelize serial-dominant tasks (p < 0.4) — 5.83x cost for 1.13x speedup (ref: 2026-04-02-distributed-systems-amdahl-gate.md)
- Prescribe roles on exploratory tasks — self-org discovers what hierarchical misses (ref: 2026-04-06-self-organizing-agents-ab-test.md)
- Launch agent chain without verifying output contracts match downstream input contracts (ref: 2026-04-07-nsm-neuro-symbolic-orchestration.md)

## Open Questions

- GAP: No data on optimal graph topology for STOPA's specific task types
- Daemon scheduling (OpenFang pattern 3) flagged high priority but not yet implemented

## Related Articles

- See also: [orchestration-resilience](orchestration-resilience.md) — error handling and verification
- See also: [skill-evaluation](skill-evaluation.md) — adversarial debate patterns

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-07-nsm-neuro-symbolic-orchestration](../learnings/2026-04-07-nsm-neuro-symbolic-orchestration.md) | 2026-04-07 | high | PDDL patterns: I/O contracts, done-when, replanning — 3x over VLA |
| [2026-04-06-self-organizing-agents-ab-test](../learnings/2026-04-06-self-organizing-agents-ab-test.md) | 2026-04-06 | high | Self-org +8% exploratory; hierarchical better for structured output |
| [2026-04-05-openfang-architecture-patterns](../learnings/2026-04-05-openfang-architecture-patterns.md) | 2026-04-05 | medium | Rust Agent OS: sandbox, Merkle audit, daemon scheduling |
| [2026-04-03-autoagent-overfitting-guard](../learnings/2026-04-03-autoagent-overfitting-guard.md) | 2026-04-03 | high | Anti-overfitting guard from AutoAgent |
| [2026-04-03-autoagent-parallel-candidates](../learnings/2026-04-03-autoagent-parallel-candidates.md) | 2026-04-03 | medium | Parallel candidates — STOPA limitation |
| [2026-04-02-distributed-systems-amdahl-gate](../learnings/2026-04-02-distributed-systems-amdahl-gate.md) | 2026-04-02 | high | Centralized wins, Amdahl gate added |
| [2026-03-30-society-of-thought-orchestration](../learnings/2026-03-30-society-of-thought-orchestration.md) | 2026-03-30 | high | RL spontaneously creates multi-agent debate |
| [2026-03-29-bigmas-directed-graph-orchestration](../learnings/2026-03-29-bigmas-directed-graph-orchestration.md) | 2026-03-29 | medium | Dynamic graph topology scales with task |
| [2026-03-29-claudini-autoresearch-loop](../learnings/2026-03-29-claudini-autoresearch-loop.md) | 2026-03-29 | high | Autoresearch succeeds from existing code |
| [2026-04-07-sas-beats-mas-equal-compute](../learnings/2026-04-07-sas-beats-mas-equal-compute.md) | 2026-04-07 | high | SAS ≥ MAS at equal thinking-token budget |
| [2026-04-07-mom-taro-orchestration-upgrades](../learnings/2026-04-07-mom-taro-orchestration-upgrades.md) | 2026-04-07 | high | Scout gate, role-specific critic, adaptive routing |
| [2026-04-07-agents-md-efficiency-validated](../learnings/2026-04-07-agents-md-efficiency-validated.md) | 2026-04-07 | high | AGENTS.md reduces runtime 28.64%, output tokens 16.58% |
| [2026-03-29-slopcodebench-iterative-degradation](../learnings/2026-03-29-slopcodebench-iterative-degradation.md) | 2026-03-29 | high | 2.2x redundancy, iterative degradation |
