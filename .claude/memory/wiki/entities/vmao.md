---
name: VMAO (inter-phase completeness verifier)
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoalpha-stopa-research]
tags: [orchestration, verification, multi-agent]
---

# VMAO (inter-phase completeness verifier)

> arXiv:2603.11445 (2026) — framework přidávající completeness verifier MEZI orchestrační fáze (ne jen na konci). Quality jump 3.1 → 4.2 při přidání inter-phase verifikace.

## Key Facts

- Quality 3.1 → 4.2 při přidání completeness verifier MEZI fáze (ref: sources/egoalpha-stopa-research.md)
- Verifikace jen na konci pipeline nestačí — chyby z early fází se zesilují
- Lightweight check: "jsou všechny subtasky pokryté? chybí nějaký artifact?"
- Komplementární k STOPA circuit breakers (ty zastavují smyčky, VMAO ověřuje úplnost)

## Relevance to STOPA

Identifikovaná mezera v STOPA: orchestrate verifikuje pouze na konci, ne mezi plan→build a build→verify. Doporučení: přidat lightweight completeness check do Phase 3 wave checkpoint v orchestrate/SKILL.md.

## Mentioned In

- [EgoAlpha Prompt Techniques vs. STOPA](../sources/egoalpha-stopa-research.md)
