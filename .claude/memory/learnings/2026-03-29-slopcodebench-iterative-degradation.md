---
date: 2026-03-29
type: anti_pattern
severity: high
component: orchestration
tags: [code-quality, orchestration, multi-session, iterative, agent-degradation]
summary: "AI coding agents produkují kód 2.2× více redundantní než lidský a trpí strukturální erozí při iterativním vývoji. Žádný agent nedokončí dlouhou sekvenci bez degradace. Mitigation: checkpointy + explicitní refactor fáze + quality gates mezi iteracemi."
uses: 0
harmful_uses: 0
verify_check: "manual"
source: "arXiv:2603.24755 — SlopCodeBench (Orlanski et al.)"
---

# Iterative Agent Code Degradation (SlopCodeBench)

## Co se děje

Při iterativním vývoji (agent rozšiřuje vlastní kód pod měnícími se požadavky) nastávají dva jevy:

1. **Verbosity drift** — kód se stává 2.2× redundantnějším než ekvivalentní lidský kód
2. **Structural erosion** — komplexita se koncentruje do "god functions/classes", architektura se zhoršuje

Žádný testovaný agent nedokončil plnou sekvenci (20 problémů, 93 checkpointů) bez selhání.

## Proč se to děje

- Agent "patch-uje" existující kód místo refaktorování
- Každá iterace přidává vrstvu, neodstraňuje tech debt
- Context o celé architektuře se ztrácí při dlouhých sekvencích
- Pass-rate benchmarky to nezachytí — kód "funguje" ale degraduje

## Mitigation pro STOPA orchestrate

1. **Explicitní refactor fáze**: Každé 3-5 iterací přidat dedikovaný "refactor checkpoint" — agent přečte celý modul a zjednodušuje
2. **Quality gates**: Po každé iteraci zkontrolovat délku kódu (verbosity flag pokud > 1.5× baseline)
3. **Architecture anchoring**: Na začátku session přečíst celý cílový soubor a zapsat architectural invariants do kontextu
4. **Diff-first review**: Místo "přidej feature X" říkat "přidej feature X, přičemž celkový kód nesmí vzrůst o více než Y řádků"

## Aplikace na ZÁCHVĚV UI

- app.py je 854 řádků — před dalšími bloky přečíst celý soubor
- Bloky 4-9 implementovat s vědomím, že každý blok přidá ~100 řádků
- Po blocích 4-5 a 6-7 přidat mini-refactor fázi
