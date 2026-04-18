---
date: 2026-04-18
type: anti_pattern
severity: high
component: orchestration
tags: [monitoring, panic-detector, calm-steering, task-types, circuit-breaker]
summary: Parallel monitoring (calm-steering, panic-detector) helps on loop-prone/open-ended tasks but is NEUTRAL or NEGATIVE on structured tasks. Don't apply monitoring universally — gate by task-type to avoid hurting deterministic pipelines.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.6
maturity: draft
verify_check: "manual"
skill_scope: [orchestrate, harness]
related: [2026-04-08-heartbeat-mid-run-steering.md]
---

## Monitoring is Task-Type Dependent

Cognitive Companion paper (arXiv:2604.13759) tested parallel monitoring across task types. Result:
- **Helpful**: loop-prone and open-ended tasks (52-62% repetition reduction)
- **Neutral or NEGATIVE**: structured tasks

**Why**: Structured tasks have deterministic execution paths. An interrupt that says "slow down, are you looping?" on a harness pipeline step disrupts legitimate progress. The monitor can't distinguish "stuck in loop" from "correctly iterating through a loop."

**STOPA implication**: Current panic-detector.py fires based on edit→fail pattern — it doesn't know whether the task is open-ended (fix ambiguous bug) or structured (run harness, apply ruff autofix). On structured tasks, rapid edits after failure are often correct behavior (retry, continue with next file, etc.) — calm-steering yellow/red there is noise.

**How to apply**: Add task-type tag to orchestrate Phase 0 output (`task_type: structured | open-ended | loop-prone`). panic-detector.py reads tag and gates intervention: structured tasks get only `:red` on true escalation (≥5 rapid failures), skip `:yellow` entirely.

**Caveat**: Paper is a feasibility study (authors' own framing), not definitive. Treat task-type gating as experimental — measure via outcomes/ before committing to hard cutoffs.
