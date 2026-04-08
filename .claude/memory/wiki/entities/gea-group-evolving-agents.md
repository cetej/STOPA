---
name: GEA (Group-Evolving Agents)
type: paper
first_seen: 2026-04-08
last_updated: 2026-04-08
sources: [group-evolving-agents-gea]
tags: [orchestration, multi-agent, self-improvement, evolution]
---

# GEA (Group-Evolving Agents)

> Weng et al. 2026 (arXiv:2602.04837) — framework pro skupinovou evoluci agentů přes sdílení zkušeností; dosahuje 71.0% na SWE-bench Verified, překonává izolovanou self-evolution o +14pp.

## Key Facts

- Skupina agentů jako základní evoluční jednotka — místo izolované stromové evoluce každý agent přistupuje k agregovaným trasám všech groupmates (code patches, execution logs, failure outcomes) (ref: sources/group-evolving-agents-gea.md)
- SWE-bench Verified: 71.0% vs 56.7% (self-evolving baseline), 88.3% vs 68.3% (Polyglot benchmark) (ref: sources/group-evolving-agents-gea.md)
- Matched human-designed frameworks (71.8% SWE-bench, 52.0% Polyglot) bez human guidance (ref: sources/group-evolving-agents-gea.md)
- Integruje nástroje ze ~dvojnásobku ancestor agentů: 17 vs 9 (izolovaná evoluce) (ref: sources/group-evolving-agents-gea.md)
- Bug repair: 1.4 iterace vs 5 u nezávislé evoluce (ref: sources/group-evolving-agents-gea.md)
- Tři fáze evoluce: reflection → evolution (patch generation) → acting (evaluation) (ref: sources/group-evolving-agents-gea.md)
- Přenositelnost: evoluované patche cílí na workflows/tools, ne model-specific prompty → funguje přes GPT i Claude rodiny (ref: sources/group-evolving-agents-gea.md)

## Relevance to STOPA

Přímá validace multi-agent přístupu v STOPA. Klíčové pro `/self-evolve` a `/orchestrate`: sdílení zkušeností mezi souběžnými agenty (aktuálně chybí) by mohlo eliminovat "mrtvé" evoluční větve a urychlit konvergenci. Performance-Novelty selektor je přímý kandidát pro UCB1 v ASI-Evolve integraci.

## Mentioned In

- [GEA: Group-Evolving Agents](../sources/group-evolving-agents-gea.md)
