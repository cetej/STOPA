---
name: Call Chain Tracking
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mbif-cpr-implementation-plan]
tags: [orchestration, memory, agent-coordination]
---

# Call Chain Tracking

> Mechanismus pro předávání kontextu o předchozích agentech každému nově spawnovanému sub-agentu — eliminuje duplicitní práci a umožňuje pozičně-vědomou koordinaci.

## Key Facts

- Původ v My-Brain-Is-Full-Crew: dispatcher předá každému agentovi "Call chain so far: [scribe, architect]. You are step 3 of max 3." (ref: sources/mbif-cpr-implementation-plan.md)
- STOPA adaptace: EXECUTION CONTEXT blok s chain, position, prior outputs (1-řádkový summary per agent), remaining budget (ref: sources/mbif-cpr-implementation-plan.md)
- "Prior outputs" místo jen jmen — dává víc kontextu za minimální token cost (ref: sources/mbif-cpr-implementation-plan.md)
- Anti-recursion: max depth závisí na tieru (light=1, standard=4, deep=8) (ref: sources/mbif-cpr-implementation-plan.md)
- Effort implementace: Low — edit 1 sekce v orchestrate SKILL.md Phase 4 (Execute) (ref: sources/mbif-cpr-implementation-plan.md)

## Relevance to STOPA

P1 priorita pro orchestrate SKILL.md. Agent chain context injection řeší problém kdy agent-3 neví co udělal agent-1. Aditivní změna, nízké riziko.

## Mentioned In

- [MBIF/CPR Implementation Plan](../sources/mbif-cpr-implementation-plan.md)
