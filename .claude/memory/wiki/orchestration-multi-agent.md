---
generated: 2026-04-04
cluster: orchestration-multi-agent
sources: 23
last_updated: 2026-04-11
---

# Multi-Agent Orchestration

> **TL;DR**: Centralized orchestration beats decentralized (1.36x vs 0.88x speedup). At equal thinking-token budgets, single-agent systems match or beat multi-agent — MAS advantage comes from unconstrained compute, not architecture. Self-organizing +8% on exploratory; hierarchical wins on structured. PDDL I/O contracts cut failures 3x. Repo-level instruction files (AGENTS.md) reduce agent runtime by 28.64%. CORAL: shared public dir + heartbeat steering > checkpoint handoff for parallel agents.

## Overview

Research on distributed LLM agent systems (arXiv:2603.12229) proves that centralized coordination consistently outperforms decentralized approaches. For tasks with low parallelizability (p < 0.4), multi-agent systems cost 5.83x tokens for only 1.13x speedup — an Amdahl gate and ROI cost gate were added to the orchestrate skill to prevent this waste (ref: 2026-04-02-distributed-systems-amdahl-gate.md).

Dynamic agent graph orchestration (BiGMAS) demonstrates that task-specific graph topologies outperform fixed structures: a GraphDesigner analyzes the task and generates appropriate topology (3 nodes for simple, 9 for complex), with agents coordinating via centralized shared workspace (ref: 2026-03-29-bigmas-directed-graph-orchestration.md). A/B testing confirmed that self-organizing agents (given only a mission, no prescribed roles) outperform hierarchical assignment by +8% on exploratory tasks, while hierarchical assignment wins on structured output tasks (ref: 2026-04-06-self-organizing-agents-ab-test.md).

A key compute-budget finding shows that at equal thinking-token budgets, single-agent systems achieve equal or better performance than multi-agent ones. MAS advantage comes from unconstrained compute scaling, not architectural superiority — remaining justifications for MAS are parallelization, specialization, and fault isolation (ref: 2026-04-07-sas-beats-mas-equal-compute.md).

CORAL (arXiv:2604.01658) introduces two critical patterns for farm-tier parallel execution. First, **shared public state**: each agent gets its own git worktree branch (filesystem isolation), with a single `.coral/public/` symlinked directory readable/writable by all agents. This eliminates checkpoint-based handoff polling — symlink reads are filesystem-level, zero sync overhead. Knowledge reuse, not parallelism itself, is the primary driver of multi-agent performance gains (ref: 2026-04-08-shared-public-state-agent-coordination.md). Second, **heartbeat mid-run steering**: the orchestrator sends periodic prompt-injections (reflection, skill consolidation, direction change) into running agents without restarting them. Unlike the critic (which evaluates post-step output), heartbeat changes direction mid-iteration — enabling the orchestrator to abort unproductive exploration branches before the full iteration completes (ref: 2026-04-08-heartbeat-mid-run-steering.md).

GEA (arXiv:2602.04837) extends this with **group experience sharing**: agents share full evolutionary trajectories (code patches, execution logs, failure outcomes) with all group members, not just their own history. This achieves 71.0% vs 56.7% on SWE-bench Verified, 2x toolset diversity, and reduces bug-repair iterations from 5 to 1.4. STOPA's findings ledger in farm tier is a static analog — dynamic sharing during execution is the remaining gap (ref: 2026-04-08-group-experience-sharing-beats-isolated-evolution.md).

For iterative skills generating multiple candidate solutions, **sampling diversity beats RL fine-tuning**: high-temperature sampling from base models nearly matches GRPO RL on MATH500 (74.8% vs 78.5%) and exceeds it on HumanEval (57.3% vs 53.7%) — without training. RL post-training causes diversity collapse (Pass@k narrows to high-reward region). Budget note: diverse sampling costs ~9x tokens vs greedy — factor into tier selection (ref: 2026-04-08-inference-time-sampling-beats-rl-for-diversity.md).

The **human bottleneck** in iterative optimization is eliminated when verification is cheap: define objective + metric + boundaries, let agents iterate autonomously overnight. Auto-research found untuned hyperparameters that 20 years of manual tuning missed (ref: 2026-04-08-auto-research-removes-human-bottleneck.md). Sequential Refinement (PDR, arXiv:2510.01123) validates bounded refinement loops over single long-context passes: +11% AIME 2024, +9% AIME 2025. Use generate-diverse-candidates → distill → refine over single exploration in autoloop/autoresearch (ref: 2026-04-08-iterative-refinement-beats-long-cot.md).

Front-loading reasoning structure at mid-training yields 9× gains vs adding it at call-time (Meta RAM blog). **curriculum-hints** in SKILL.md is the closest STOPA analog — reasoning structure present before the task, not appended after failure (ref: 2026-04-08-reasoning-midtraining-beats-posttraining.md). EGGROLL (Oxford/MILA) formalizes three evolution principles: rank-1 perturbation suffices when population is adequate, population z-score normalization stabilizes selection, and three sigma regimes (linearize/critical/diverge) govern mutation optimality (ref: 2026-04-10-eggroll-evolutionary-optimization.md).

RLM architectural validation (arXiv:2512.24601) confirmed three STOPA patterns: budget propagation to sub-agents (soft-cap + 20% reserve), metadata-first scout (file count/risk signals without reading files), and recursion depth guard at max-depth 1 (ref: 2026-04-10-rlm-architectural-principles.md). The **Iteration Paradox** meta-pattern consolidates contradictory advice: iterate with bounded context, maintain diversity, don't trust early winners, estimate asymptote ceiling after 5+ iterations, apply regression gate, and manage sigma (mutation strength) with small edits early and larger exploration late (ref: 2026-04-11-iteration-paradox-meta-pattern.md).

Neuro-symbolic patterns from PDDL research show explicit operator interfaces — `input-contract`, `preconditions`, `effects` — enable plan chain validation before agent execution, eliminating downstream failures from incompatible handoffs (ref: 2026-04-07-nsm-neuro-symbolic-orchestration.md). Empirical validation confirmed repo-level instruction files reduce agent runtime by 28.64% and output tokens by 16.58% (ref: 2026-04-07-agents-md-efficiency-validated.md).

## Key Rules

1. **Centralized > decentralized**: use a coordinator, not peer-to-peer agents (ref: 2026-04-02-distributed-systems-amdahl-gate.md)
2. **Amdahl gate**: skip multi-agent for tasks with p < 0.4 parallelizability (ref: 2026-04-02-distributed-systems-amdahl-gate.md)
3. **Self-org for exploration, hierarchical for structured output**: detect task style in Phase 1 (ref: 2026-04-06-self-organizing-agents-ab-test.md)
4. **Validate plan chain BEFORE launch**: effects(step N) must satisfy preconditions(step N+1) (ref: 2026-04-07-nsm-neuro-symbolic-orchestration.md)
5. **AGENTS.md saves 28.64% runtime**: maintain quality instruction files at repo level (ref: 2026-04-07-agents-md-efficiency-validated.md)
6. **SAS ≥ MAS at equal compute**: only use MAS when parallelization, specialization, or fault isolation justify overhead (ref: 2026-04-07-sas-beats-mas-equal-compute.md)
7. **Shared dir > checkpoint handoff for parallel farm agents**: use `.claude/shared/agent-N.md` slots, not checkpoint polling (ref: 2026-04-08-shared-public-state-agent-coordination.md)
8. **Heartbeat ≠ critic**: heartbeat changes direction mid-run; critic evaluates post-step output (ref: 2026-04-08-heartbeat-mid-run-steering.md)
9. **Group experience sharing for farm tier**: agents must read ALL group member traces, not just own history (ref: 2026-04-08-group-experience-sharing-beats-isolated-evolution.md)
10. **High-temperature sampling for exploration**: RL-tuned models collapse diversity — use base model + high temp for autoloop/autoresearch candidate generation (ref: 2026-04-08-inference-time-sampling-beats-rl-for-diversity.md)
11. **Anti-overfitting guard**: ask "would this change be worthwhile without this eval case?" (ref: 2026-04-03-autoagent-overfitting-guard.md)
12. **Autoresearch requires objective metric**: confirm cheap verify exists before launching — else use /orchestrate (ref: 2026-04-08-auto-research-removes-human-bottleneck.md)
13. **Bounded refinement over long-context**: iterative loop with N bounded passes > single long-context generation (ref: 2026-04-08-iterative-refinement-beats-long-cot.md)
14. **Don't trust first 2-3 iterations**: approach winning early may lose at scale — give each 5+ iterations before judging, estimate sigmoid ceiling (ref: 2026-04-11-iteration-paradox-meta-pattern.md)
15. **Budget propagation to sub-agents**: soft-cap with 20% reserve, min viable $0.03 (ref: 2026-04-10-rlm-architectural-principles.md)

## Patterns

### Do
- Scale graph complexity with task demands (ref: 2026-03-29-bigmas-directed-graph-orchestration.md)
- Use explicit refactor phases between iterations (ref: 2026-03-29-slopcodebench-iterative-degradation.md)
- Tag tool outputs as `[UNTRUSTED]` when from external sources (ref: 2026-04-05-openfang-architecture-patterns.md)
- Define `input-contract` and `output-contract` on all Tier 1 skills (ref: 2026-04-07-nsm-neuro-symbolic-orchestration.md)
- In farm tier: inject heartbeat reflection prompts after N iterations without improvement (ref: 2026-04-08-heartbeat-mid-run-steering.md)
- In farm tier: write intermediate results to shared slot files for cross-agent knowledge reuse (ref: 2026-04-08-shared-public-state-agent-coordination.md)

### Don't
- Parallelize serial-dominant tasks (p < 0.4) — 5.83x cost for 1.13x speedup (ref: 2026-04-02-distributed-systems-amdahl-gate.md)
- Prescribe roles on exploratory tasks — self-org discovers what hierarchical misses (ref: 2026-04-06-self-organizing-agents-ab-test.md)
- Launch agent chain without verifying output contracts match downstream input contracts (ref: 2026-04-07-nsm-neuro-symbolic-orchestration.md)
- Use RL-tuned specialized models for diversity-requiring tasks — prefer base model + temperature (ref: 2026-04-08-inference-time-sampling-beats-rl-for-diversity.md)
- Pass raw orchestrator trajectory to workers — speculative reasoning is noise that degrades worker accuracy; send task-relevant facts only (ref: 2026-04-11-speculative-reasoning-degrades-workers.md)
- Use same context strategy for all tiers — deep needs broad coverage, light/farm need maximal compression (ref: 2026-04-11-compression-regime-maps-to-tiers.md)

## STOPA as Program.md

Karpathy's "program.md" framing (ref: sources/karpathy-nopriors-autoagent-loopy-era.md) — a research organization described entirely as markdown files (roles, workflows, policies) — maps directly to STOPA. The SKILL.md files, hooks.json, CLAUDE.md rules, and memory architecture together form the "program.md" for this orchestration system. Different configurations of these files produce different research velocities and quality outcomes.

This enables meta-optimization: running auto-research on STOPA itself (via `/self-evolve --mode system`) to find better orchestration configurations. The contest idea — same hardware, different program.mds, leaderboard of improvement rate — is the direction for system-level self-evolution.

Key implications:
- **Skills = roles**: each SKILL.md defines a specialized agent role within the org
- **Rules = policies**: `.claude/rules/*.md` files encode org-wide constraints
- **Memory = institutional knowledge**: learnings, wiki, decisions form the org's accumulated expertise
- **Evolve = meta-optimization**: `/evolve` and `/self-evolve` run optimization over the org configuration itself

See also: [program-md-research-org](entities/program-md-research-org.md) entity page.

## Open Questions

- GAP: No STOPA implementation of GEA-style dynamic group experience sharing during farm tier execution (currently findings ledger is static, written after completion)
- GAP: No data on optimal graph topology for STOPA's specific task types
- GAP: Daemon scheduling (OpenFang pattern 3) flagged high priority but not yet implemented

## Related Articles

- See also: [orchestration-resilience](orchestration-resilience.md) — error handling and verification
- See also: [general-security-environment](general-security-environment.md) — agent trust and deception
- See also: [skill-evaluation](skill-evaluation.md) — adversarial debate patterns

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-08-shared-public-state-agent-coordination](../learnings/2026-04-08-shared-public-state-agent-coordination.md) | 2026-04-08 | medium | CORAL: shared public dir, zero sync overhead, knowledge reuse > parallelism |
| [2026-04-08-heartbeat-mid-run-steering](../learnings/2026-04-08-heartbeat-mid-run-steering.md) | 2026-04-08 | medium | Heartbeat mid-run steering distinct from post-step critic |
| [2026-04-08-group-experience-sharing-beats-isolated-evolution](../learnings/2026-04-08-group-experience-sharing-beats-isolated-evolution.md) | 2026-04-08 | high | GEA: group experience sharing 71% vs 56.7%, 1.4 vs 5 iterations |
| [2026-04-08-inference-time-sampling-beats-rl-for-diversity](../learnings/2026-04-08-inference-time-sampling-beats-rl-for-diversity.md) | 2026-04-08 | medium | High-temp sampling > RL-tuned for diversity in iterative skills |
| [2026-04-07-nsm-neuro-symbolic-orchestration](../learnings/2026-04-07-nsm-neuro-symbolic-orchestration.md) | 2026-04-07 | high | PDDL patterns: I/O contracts, done-when, replanning — 3x over VLA |
| [2026-04-07-sas-beats-mas-equal-compute](../learnings/2026-04-07-sas-beats-mas-equal-compute.md) | 2026-04-07 | high | SAS ≥ MAS at equal thinking-token budget |
| [2026-04-07-mom-taro-orchestration-upgrades](../learnings/2026-04-07-mom-taro-orchestration-upgrades.md) | 2026-04-07 | high | Scout gate, role-specific critic, adaptive routing |
| [2026-04-07-agents-md-efficiency-validated](../learnings/2026-04-07-agents-md-efficiency-validated.md) | 2026-04-07 | high | AGENTS.md reduces runtime 28.64%, output tokens 16.58% |
| [2026-04-06-self-organizing-agents-ab-test](../learnings/2026-04-06-self-organizing-agents-ab-test.md) | 2026-04-06 | high | Self-org +8% exploratory; hierarchical better for structured output |
| [2026-04-05-openfang-architecture-patterns](../learnings/2026-04-05-openfang-architecture-patterns.md) | 2026-04-05 | medium | Rust Agent OS: sandbox, Merkle audit, daemon scheduling |
| [2026-04-03-autoagent-overfitting-guard](../learnings/2026-04-03-autoagent-overfitting-guard.md) | 2026-04-03 | high | Anti-overfitting guard from AutoAgent |
| [2026-04-03-autoagent-parallel-candidates](../learnings/2026-04-03-autoagent-parallel-candidates.md) | 2026-04-03 | medium | Parallel candidates — STOPA limitation |
| [2026-04-02-distributed-systems-amdahl-gate](../learnings/2026-04-02-distributed-systems-amdahl-gate.md) | 2026-04-02 | high | Centralized wins, Amdahl gate added |
| [2026-03-30-society-of-thought-orchestration](../learnings/2026-03-30-society-of-thought-orchestration.md) | 2026-03-30 | high | RL spontaneously creates multi-agent debate |
| [2026-03-29-bigmas-directed-graph-orchestration](../learnings/2026-03-29-bigmas-directed-graph-orchestration.md) | 2026-03-29 | medium | Dynamic graph topology scales with task |
| [2026-03-29-claudini-autoresearch-loop](../learnings/2026-03-29-claudini-autoresearch-loop.md) | 2026-03-29 | high | Autoresearch succeeds from existing code |
| [2026-03-29-slopcodebench-iterative-degradation](../learnings/2026-03-29-slopcodebench-iterative-degradation.md) | 2026-03-29 | high | 2.2x redundancy, iterative degradation |
| [2026-04-08-auto-research-removes-human-bottleneck](../learnings/2026-04-08-auto-research-removes-human-bottleneck.md) | 2026-04-08 | high | Human is always bottleneck — remove self when verify is cheap |
| [2026-04-08-iterative-refinement-beats-long-cot](../learnings/2026-04-08-iterative-refinement-beats-long-cot.md) | 2026-04-08 | high | PDR: bounded refinement loops beat single long-context pass (+11% AIME) |
| [2026-04-08-reasoning-midtraining-beats-posttraining](../learnings/2026-04-08-reasoning-midtraining-beats-posttraining.md) | 2026-04-08 | high | Front-loading reasoning structure yields 9× gains; validates curriculum-hints |
| [2026-04-10-eggroll-evolutionary-optimization](../learnings/2026-04-10-eggroll-evolutionary-optimization.md) | 2026-04-10 | high | EGGROLL: rank-1 perturbation, population z-score scoring, sigma regimes |
| [2026-04-10-rlm-architectural-principles](../learnings/2026-04-10-rlm-architectural-principles.md) | 2026-04-10 | high | RLM validates: budget propagation, metadata-first scout, depth guard |
| [2026-04-11-iteration-paradox-meta-pattern](../learnings/2026-04-11-iteration-paradox-meta-pattern.md) | 2026-04-11 | high | Iteration Paradox: bounded context + diversity + ceiling estimation protocol |
