---
date: 2026-04-07
type: architecture
severity: high
component: orchestration
tags: [adaptive-routing, role-specific-critic, upstream-first, weak-to-strong, parallel-rollouts]
summary: "Implemented 4 MoM/TARo-inspired upgrades: scout quality gate (upstream-first), role-specific critic weights, per-subtask adaptive model routing, haiku-first difficulty estimation."
source: external_research
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.00
verify_check: "Grep('Scout Quality Gate', path='.claude/commands/orchestrate.md') → 1+ matches"
related: [2026-04-06-self-organizing-agents-ab-test.md]
---

## What Changed

4 proposals from MoM (arXiv:2510.20176) and TARo (arXiv:2603.18411) implemented in orchestrate.md and critic.md:

1. **Scout Quality Gate** (orchestrate Phase 2): Validates scout output completeness before planning. Light tier: file coverage only. Standard+: + dependency map + test discovery. Deep: + risk signals. Model upgrade rule: scout runs one tier higher than workers.

2. **Role-Specific Critic Weights** (critic Phase 4): New weight profiles per agent role (scout/planner, worker/builder, verifier/reviewer, researcher). Scout evaluated on coverage/completeness, worker on correctness, verifier on safety, researcher on evidence grounding. Activated via `--role` flag or auto-inferred.

3. **Per-Subtask Adaptive Model Routing** (orchestrate Phase 4): Heuristic router selects haiku/sonnet/opus per subtask based on complexity signals. Single-file edit → haiku, multi-file logic → sonnet, cross-cutting/security → opus. Failed subtask → upgrade +1 tier.

4. **Haiku-First Difficulty Estimation** (orchestrate Phase 4): For ambiguous subtasks, run through haiku first. If critic ≥ 3.5 → keep haiku result. If fail → route to sonnet/opus with haiku context. Expected 40-60% cost savings on routine tasks.

## Supporting Research

- RouteLLM (arXiv:2406.18665): 2x cost reduction, cross-model transfer
- RTR (arXiv:2505.19435): Joint model+strategy routing, 40-60% savings
- Self-Certainty BoN (arXiv:2502.18581): ~80% cheaper than reward models
- GDPO (arXiv:2601.05242): Decoupled per-dimension reward normalization
- Process Reward Models (arXiv:2502.10325): Step-level per-role scoring

## Not Yet Implemented (Phase 2)

- P3: Best-of-N parallel rollouts for deep-tier subtasks
- P6: Heterogeneous rollout teams (mix models within wave)
- Data-driven router training from budget.md traces
- Per-role PRM evaluators (Phase 2 of role-specific critic)
