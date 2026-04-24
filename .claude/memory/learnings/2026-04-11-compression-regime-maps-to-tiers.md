---
date: 2026-04-11
type: best_practice
severity: medium
component: orchestration
tags: [multi-agent, context-sharing, budget-tiers, compression, orchestration]
summary: "Optimal context compression varies systematically by task type: long/broad → light compression (preserve coverage, 49% savings), hard/focused → aggressive compression (strip noise, +3pp accuracy), simple → moderate. Maps directly to STOPA budget tiers."
source: external_research
maturity: draft
uses: 4
harmful_uses: 0
successful_uses: 0
confidence: 1.00
verify_check: "manual"
related: [2026-04-11-task-guided-context-beats-raw-sharing.md, 2026-04-10-rlm-architectural-principles.md, 2026-04-12-small-model-compression-threshold.md]
skill_scope: [orchestrate]
---

# Compression Regime Maps to STOPA Budget Tiers

## Finding

Latent Briefing discovered systematic relationship between task characteristics and optimal compression level:

| Task Type | Optimal Threshold | Compression | Why |
|-----------|------------------|-------------|-----|
| Long docs (32k-100k) | Light (t=-1.0) | 18% removed | Dispersed info — coverage matters |
| Hard questions | Aggressive (t=2.0) | 79% removed | Strip speculative noise |
| Short/easy | Moderate (t=1.0) | 68% removed | Remove redundancy only |

## Mapping to STOPA Tiers

| STOPA Tier | Task Character | Context Strategy |
|-----------|---------------|-----------------|
| `light` | Simple fix, short context | Minimal context: just subtask + relevant file refs |
| `standard` | Multi-file, moderate | Scout report + subtask — strip orchestrator reasoning |
| `deep` | Cross-cutting, broad | Preserve broad context (scout map, prior results, dependencies) |
| `farm` | Bulk mechanical | Extremely focused: just pattern + file list (maximum compression) |

The `deep` tier generates longest orchestrator trajectories but should use LIGHTEST context filtering (broad coverage needed). Counter-intuitively, `farm` tier (simplest tasks) benefits from most aggressive filtering (just the pattern).

**Why:** One-size context strategy wastes tokens on easy tasks and starves workers on hard tasks. The regime analysis shows this isn't a smooth spectrum — there are qualitatively different optima.
**How to apply:** In orchestrate Phase 4 (agent prompt construction), match context strategy to tier. light/farm: minimal context (max compression). standard: moderate. deep: preserve breadth.
