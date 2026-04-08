---
name: Heartbeat-Triggered Intervention
type: concept
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [coral-autonomous-multi-agent-evolution]
tags: [orchestration, multi-agent, monitoring, reflection]
---

# Heartbeat-Triggered Intervention

> An orchestration pattern where a manager process periodically interrupts running agents with targeted prompts (reflection, skill consolidation, direction change) without terminating the agent session.

## Key Facts

- Manager sends heartbeat prompts to interrupt agents with actions: reflection, skill consolidation, or task reorientation (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Agents continue running after intervention — heartbeat is non-destructive injection, not a restart (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Enables orchestrator-level steering of long-running autonomous agents mid-execution (ref: sources/coral-autonomous-multi-agent-evolution.md)
- Distinct from critic: critic evaluates output quality; heartbeat steers direction/reflection without output evaluation (ref: sources/coral-autonomous-multi-agent-evolution.md)

## Relevance to STOPA

STOPA's current critic runs as a post-step check; heartbeat-triggered intervention would enable mid-run course correction in `farm` tier and `self-evolve` without full agent restart — maps to `calm-steering` pattern already in behavioral genome.

## Mentioned In

- [CORAL: Autonomous Multi-Agent Evolution for Open-Ended Discovery](../sources/coral-autonomous-multi-agent-evolution.md)
