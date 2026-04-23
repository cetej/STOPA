---
date: 2026-04-23
type: best_practice
severity: medium
component: orchestration
tags: [verification, orchestration-validation, field-study, external-evidence]
summary: "UCSD + Cornell field study (Huang et al., arXiv:2512.14012, N=13 observed + N=99 surveyed experienced devs): delegují max 2.1 kroků agentovi PŘED validací. Všech 13 observed kontrolovalo design (vlastní plán nebo revize agent-generated plánu). Validates STOPA orchestrate (budget tiers + critic per 2 rounds) + behavioral-genome § Verification."
source: external_research
uses: 0
harmful_uses: 0
successful_uses: 0
confidence: 0.8
maturity: draft
verify_check: "manual"
related: []
---

## Context

Mixed-methods field study (Aug-Oct 2025), UCSD + Cornell, Huang et al. ([arXiv:2512.14012](https://arxiv.org/abs/2512.14012)):
- N=13 observed session + N=99 surveyed experienced devs
- **Klíčové číslo:** 2.1 kroků průměrně = tolik dev zadá agentovi PŘED validací
- Všech 13 observed participantů kontrolovalo design (vlastní plán, nebo revize agent-generated plánu)
- Agenti vnímáni pozitivně, ale JEN jako productivity boost, ne autonomní implementátoři
- Retence agency = deliberate quality-driven strategie, ne luddite resistance

## Relevance pro STOPA

Externí empirická validace existujícího designu:
- **orchestrate budget tiers** (light 0-1 agents, standard 2-4, deep 5-8) + **critic gate každé 2 rounds** = alignment s 2.1 steps finding
- **rules/core-invariants.md #6** ("Verify before claiming done") — bod validován externí studií
- **behavioral-genome.md § Verification + Code Editing Discipline** — citable evidence

## Action

Knowledge-only (no code change). Až při příštím edit `behavioral-genome.md § Verification` přidat citation:
> *"Externí validace: Huang et al. (arXiv:2512.14012, N=13+99 experienced devs) ukazují průměr 2.1 kroků delegace před validací — STOPA budget tiers + critic gates jsou v souladu."*

## Rationale

Mixed-methods study N=112 (field + survey) na experienced devs = solid evidence. Číslo 2.1 je konkrétní benchmark který by STOPA měl respektovat při budget tier tuning. Hodnota = citable reference, ne nová mechanika.
