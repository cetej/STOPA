---
name: Cognitive Companion
type: concept
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [cognitive-companion-parallel-monitoring]
tags: [monitoring, resilience, orchestration, reasoning-degradation]
---

# Cognitive Companion

> Lightweight parallel monitoring architecture that runs alongside an LLM agent to detect reasoning degradation (loops, drift, stuck states) and trigger recovery.

## Key Facts

- Two implementations: LLM-based (~11% overhead, 52-62% repetition reduction on loop-prone tasks) and Probe-based (zero overhead, layer-28 hidden states, AUROC 0.840) (ref: sources/cognitive-companion-parallel-monitoring.md)
- Target failure mode: up to 30% failure rate on hard multi-step tasks attributable to loops/drift/stuck states (ref: sources/cognitive-companion-parallel-monitoring.md)
- Task-type dependency: effective on loop-prone/open-ended tasks; neutral to NEGATIVE on structured tasks — monitoring isn't universally helpful (ref: sources/cognitive-companion-parallel-monitoring.md)
- Scale boundary: no improvement on 1B-1.5B parameter models — companion patterns require model capacity to leverage the interrupt (ref: sources/cognitive-companion-parallel-monitoring.md)
- Feasibility study, not definitive validation — authors' own framing

## Relevance to STOPA

STOPA already has panic-detector hook + calm-steering protocol (edit→fail pattern matching with colored intervention messages). Cognitive Companion validates the architecture and adds empirical evidence: ~52-62% loop reduction is achievable, BUT monitoring should be task-type-aware. Structured tasks (e.g., harness execution) may be HURT by calm-steering interrupts. Future: gate panic-detector by task-type tag from orchestrator.

## Mentioned In

- [Cognitive Companion: Parallel Monitoring](../sources/cognitive-companion-parallel-monitoring.md)
