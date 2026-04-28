---
name: WebArena Verified
type: tool
first_seen: 2026-04-26
last_updated: 2026-04-26
sources: [ai-planning-framework-web-agents]
tags: [benchmark, evaluation, web-agents]
---

# WebArena Verified

> El hattami et al. (NeurIPS 2025 SEA, ServiceNow/Mila) — audit a oprava všech 812 WebArena tasks: type-aware comparators místo substring matching, structured JSON status, Hard subset.

## Key Facts

- Audit 812 WebArena tasks: nalezeny "underspecified goals and brittle checkers" (ref: sources/ai-planning-framework-web-agents.md)
- Type-aware comparators redukují false negatives o ~11% oproti substring matching (ref: sources/ai-planning-framework-web-agents.md)
- WebArena Verified Hard subset: 137 tasks, -83% eval cost oproti plnému benchmarku (ref: sources/ai-planning-framework-web-agents.md)
- Structured JSON schema s explicit status codes pro deterministické skórování (ref: sources/ai-planning-framework-web-agents.md)
- Template-level macro averages + 95% CIs (místo per-task micro averages) (ref: sources/ai-planning-framework-web-agents.md)

## Relevance to STOPA

Argument pro použití Hard subset (137 tasks, -83% cost) pro rychlé iterace při evaluaci web agentů. Brittle substring matching = anti-pattern pro STOPA eval hooks.

## Mentioned In

- [AI Planning Framework for LLM-Based Web Agents Research Brief](../sources/ai-planning-framework-web-agents.md)
