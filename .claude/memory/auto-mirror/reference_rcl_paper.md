---
name: RCL Paper — Reflective Context Learning
description: arXiv:2604.03189 — 7 optimization primitives for context-space learning (reflect-mutate loop), 3+4 STOPA gaps, full integration plan in docs/RCL_INTEGRATION.md
type: reference
---

**Paper:** Vassilyev et al., "Reflective Context Learning: Studying the Optimization Primitives of Context Space", arXiv:2604.03189, 2026. MIT license.
**Repo:** https://github.com/nvassilyev/RCL
**Integration plan:** `docs/RCL_INTEGRATION.md`

## Core Idea

Formalizes reflect-mutate loop for optimizing agent context (playbooks/skills). Playbook = structured instruction set with per-entry helpful/harmful counters (analog of SKILL.md + learnings). Tested on AppWorld, BrowseComp+, RewardBench2.

## 7 Optimization Primitives

1. **Failure Replay** — ReplayBuffer: re-execute failed tasks, graduate after 5 passes, evict after 3 post-reflection fails
2. **Grouped Rollouts** — K rollouts per task for variance reduction
3. **Mini-batching** — reflect on N failure traces per iteration
4. **Dual-trace Credit Assignment** — baseline + PP (Perturbation Probes: XML self-report tags) → contrastive reflector signal
5. **Optimizer State** — OptimizationStateManager: rolling JSON with change_ledger, strategies, velocity, updated by LLM in background
6. **Auxiliary Losses** — enriched reflector: failure_type (ACTIONABLE_GAP/EXECUTION_VARIANCE/INTRACTABLE), root_cause, coverage_gaps
7. **Batched Reflection** — all signal traces in single LLM call

## Architecture (from repo)

- `Playbook` = list of `PlaybookEntry{content, section, entry_id, helpful_count, harmful_count}` → rendered as markdown in system prompt
- `Reflector` → analyzes failed traces → per-entry assessments (helpful/harmful/neutral) + analysis
- `Mutator` → 0-3 operations (ADD/UPDATE/DELETE) per iteration, conservative philosophy
- `ReplayBuffer` → sampling with under-seen priority, graduation/eviction lifecycle
- `OptimizationStateManager` → rolling JSON state: health, change_ledger, hypotheses, interference_patterns, velocity
- Model allocation: cheap agent + strong optimizer (validates STOPA tier system)
- Entry design: EXPLICIT > IMPLICIT, PROCEDURAL > DECLARATIVE, DEFENSIVE > OPTIMISTIC

## STOPA Integration — 3 Primary Gaps

1. **Dual-trace credit assignment** → `memory/outcomes/` with learnings_applied + credit field → `outcome-credit.py` hook closes retrieval loop
2. **Per-skill optimizer state** → `memory/optstate/<skill>.json` with change_ledger, strategies_that_work/fail, velocity
3. **Systematic failure replay** → activate failures/ pipeline (auto-write via hook) + self-evolve replay buffer from outcomes/

## 4 Structural Gaps (from audit)

4. failures/ directory empty — feedback loop unexercised
5. Trace data 7-day TTL — no durable archive
6. Learnings uses counters at 0-1 — retrieval loop not closed
7. No cross-run mutation ledger

## Implementation: 3 phases in docs/RCL_INTEGRATION.md

**Phase 1** (highest ROI): outcomes/ + credit loop → closes retrieval-use-feedback loop
**Phase 2**: optstate/ + failure pipeline → per-skill momentum + automatic failure records
**Phase 3**: replay buffer + lightweight PP → full RCL-level optimization
