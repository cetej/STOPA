---
date: 2026-03-23
type: best_practice
severity: medium
component: orchestration
tags: [gsd, wave-execution, deviation-rules, verification]
summary: "GSD wave execution: batch independent tasks, verify after each wave, deviation rules for agent coordination."
source: external_research
---

## Problém
Multi-agent task execution needs structured coordination patterns.

## Root Cause
Without wave-based execution and deviation rules, agents drift or duplicate work.

## Reseni
Wave execution: topological sort subtasks -> wave number -> parallel execution. Prefer vertical slices over horizontal layers. Deviation rules: sub-agents fix bugs inline (max 3 attempts), STOP on architectural change. Pre-existing bugs: log only. Analysis-paralysis guard: 5+ read-only ops without Write/Edit = stuck. Goal-backward verification: L1 Exists -> L2 Substantive -> L3 Wired -> L4 Flows.

## Prevence
NOT adopted from GSD: XML task format, lifecycle workflow, artifact system, requirements traceability IDs — too heavyweight for STOPA.
