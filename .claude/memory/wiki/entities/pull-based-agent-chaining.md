---
name: Pull-based Agent Chaining
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mbif-cpr-research]
tags: [orchestration, multi-agent]
---

# Pull-based Agent Chaining

> Coordination pattern where agents never call other agents directly — instead, an agent writes `### Suggested next agent` in its output, and the dispatcher (not the agent) decides whether to follow the suggestion.

## Key Facts

- Implemented in My-Brain-Is-Full-Crew (ref: sources/mbif-cpr-research.md)
- Anti-recursion rules: max depth 3, no agent twice in one chain, no circular patterns (ref: sources/mbif-cpr-research.md)
- Each sub-agent receives explicit call chain context: "Call chain so far: [scribe, architect]. You are step 3 of max 3." (ref: sources/mbif-cpr-research.md)
- Dispatcher has full control; agent has no authority to invoke peers (ref: sources/mbif-cpr-research.md)

## Relevance to STOPA

Complements STOPA's circuit breakers (3× same agent = STOP). Explicit call chain injection is directly adoptable in /orchestrate's agent prompt template. Prevents runaway chaining without centralizing all logic in the orchestrator.

## Mentioned In

- [MBIF vs CPR Research](../sources/mbif-cpr-research.md)
