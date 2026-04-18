---
name: Reasoning Degradation
type: concept
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [cognitive-companion-parallel-monitoring]
tags: [failure-mode, monitoring, multi-step-tasks, orchestration]
---

# Reasoning Degradation

> Failure mode in multi-step LLM agent tasks: looping (same action repeated), drift (objective lost), stuck states (no progress). Distinct from single-step hallucination.

## Key Facts

- Prevalence: up to 30% failure rate on hard multi-step tasks attributable to degradation (not capability limits) (ref: sources/cognitive-companion-parallel-monitoring.md)
- Three observable sub-patterns: looping, drift, stuck — each has distinct behavioral signatures
- Detection methods: LLM-as-judge (inspect outputs, 10-15% overhead), LLM-based Companion (parallel, ~11% overhead, 52-62% reduction), Probe-based (hidden states, zero overhead)
- Task-type factor: degradation is concentrated on loop-prone/open-ended tasks; structured tasks exhibit it less
- Scale factor: small models (1B-1.5B) don't benefit from monitoring — possibly degradation isn't the main failure mode at that scale (capability is)

## Relevance to STOPA

Directly informs STOPA's circuit breakers (3-fix escalation) and panic-detector hook. The 30% baseline failure rate justifies the intervention cost. Task-type dependency argues for conditional monitoring: don't inject calm-steering on harness/structured tasks. STOPA's existing "edit→fail rapid patching" pattern in panic-detector.py targets the "stuck" sub-pattern specifically.

## Mentioned In

- [Cognitive Companion: Parallel Monitoring](../sources/cognitive-companion-parallel-monitoring.md)
