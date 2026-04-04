---
generated: 2026-04-04
cluster: orchestration-multi-agent
sources: 7
last_updated: 2026-04-04
---

# Multi-Agent Orchestration

> **TL;DR**: Centralized orchestration beats decentralized (1.36x vs 0.88x speedup). Serial tasks below 40% parallelizability waste 5.83x tokens. AI agents degrade iteratively — checkpoints and quality gates are mandatory.

## Overview

Research on distributed LLM agent systems (arXiv:2603.12229) proves that centralized coordination consistently outperforms decentralized approaches. For tasks with low parallelizability (p < 0.4), multi-agent systems cost 5.83x tokens for only 1.13x speedup — an Amdahl gate and ROI cost gate were added to the orchestrate skill to prevent this waste (ref: 2026-04-02-distributed-systems-amdahl-gate.md).

Dynamic agent graph orchestration (BiGMAS) demonstrates that task-specific graph topologies outperform fixed structures: a GraphDesigner analyzes the task and generates appropriate topology (3 nodes for simple, 9 for complex), with agents coordinating via centralized shared workspace (ref: 2026-03-29-bigmas-directed-graph-orchestration.md). This aligns with Society of Thought findings (Kim et al. 2026) that RL optimization spontaneously generates multi-agent debate in reasoning models — heterogeneous perspectives improve performance, and shared state (STOPA's checkpoint) is necessary to prevent temporal misalignment (ref: 2026-03-30-society-of-thought-orchestration.md).

Iterative agent work suffers from structural erosion: SlopCodeBench shows AI agents produce 2.2x more redundant code than humans and no agent completes long sequences without degradation (ref: 2026-03-29-slopcodebench-iterative-degradation.md). AutoAgent patterns address this with anti-overfitting guards ("if this eval case disappeared, would the change still be worthwhile?") and parallel candidate evaluation via sandboxes — though STOPA remains sequential until CC gets native parallel execution (ref: 2026-04-03-autoagent-overfitting-guard.md, 2026-04-03-autoagent-parallel-candidates.md). The Claudini autoresearch loop succeeds when starting from existing implementations with dense quantitative feedback (ref: 2026-03-29-claudini-autoresearch-loop.md).

## Key Rules

1. **Centralized > decentralized**: use a coordinator, not peer-to-peer agents (ref: 2026-04-02-distributed-systems-amdahl-gate.md)
2. **Amdahl gate**: skip multi-agent for tasks with p < 0.4 parallelizability (ref: 2026-04-02-distributed-systems-amdahl-gate.md)
3. **Anti-overfitting guard**: ask "would this change be worthwhile without this eval case?" (ref: 2026-04-03-autoagent-overfitting-guard.md)
4. **Checkpoints between iterations**: agents degrade without quality gates (ref: 2026-03-29-slopcodebench-iterative-degradation.md)
5. **Heterogeneous critic perspectives**: different system prompts for critic agents (ref: 2026-03-30-society-of-thought-orchestration.md)
6. **Start from existing code**: autoresearch works best with existing implementations (ref: 2026-03-29-claudini-autoresearch-loop.md)

## Patterns

### Do
- Scale graph complexity with task demands (ref: 2026-03-29-bigmas-directed-graph-orchestration.md)
- Use explicit refactor phases between iterations (ref: 2026-03-29-slopcodebench-iterative-degradation.md)
- Evaluate multiple candidates when possible, even sequentially (ref: 2026-04-03-autoagent-parallel-candidates.md)

### Don't
- Parallelize serial-dominant tasks (p < 0.4) — 5.83x cost for 1.13x speedup (ref: 2026-04-02-distributed-systems-amdahl-gate.md)
- Trust iterative agent output without checkpoints (ref: 2026-03-29-slopcodebench-iterative-degradation.md)
- Accept improvements that only work on specific eval cases (ref: 2026-04-03-autoagent-overfitting-guard.md)

## Open Questions

- GAP: No data on optimal graph topology for STOPA's specific task types

## Related Articles

- See also: [orchestration-resilience](orchestration-resilience.md) — error handling and verification
- See also: [skill-evaluation](skill-evaluation.md) — adversarial debate patterns

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-03-autoagent-overfitting-guard](../learnings/2026-04-03-autoagent-overfitting-guard.md) | 2026-04-03 | high | Anti-overfitting guard from AutoAgent |
| [2026-04-03-autoagent-parallel-candidates](../learnings/2026-04-03-autoagent-parallel-candidates.md) | 2026-04-03 | medium | Parallel candidates — STOPA limitation |
| [2026-04-02-distributed-systems-amdahl-gate](../learnings/2026-04-02-distributed-systems-amdahl-gate.md) | 2026-04-02 | high | Centralized wins, Amdahl gate added |
| [2026-03-30-society-of-thought-orchestration](../learnings/2026-03-30-society-of-thought-orchestration.md) | 2026-03-30 | high | RL spontaneously creates multi-agent debate |
| [2026-03-29-bigmas-directed-graph-orchestration](../learnings/2026-03-29-bigmas-directed-graph-orchestration.md) | 2026-03-29 | medium | Dynamic graph topology scales with task |
| [2026-03-29-claudini-autoresearch-loop](../learnings/2026-03-29-claudini-autoresearch-loop.md) | 2026-03-29 | high | Autoresearch succeeds from existing code |
| [2026-03-29-slopcodebench-iterative-degradation](../learnings/2026-03-29-slopcodebench-iterative-degradation.md) | 2026-03-29 | high | 2.2x redundancy, iterative degradation |
