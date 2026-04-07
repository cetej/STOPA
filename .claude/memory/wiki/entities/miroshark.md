---
name: MiroShark
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [miroshark-research]
tags: [orchestration, multi-agent, research, osint]
---

# MiroShark

> Anglický fork MiroFish (Shanda Group) — open-source swarm intelligence engine: dokument → Neo4j knowledge graph → stovky AI agentů s unikátními osobnostmi → paralelní simulace Twitter + Reddit + Polymarket. AGPL-3.0.

## Key Facts

- 427 stars, 68 forks, 15 dní od vzniku (2026-03-20) — rychlý growth (ref: sources/miroshark-research.md)
- 5 fází: Graph Build → Agent Setup → Simulace (OASIS/CAMEL-AI) → Report (ReACT agent) → Interakce
- 5 vrstev kontextu per agent: grafy atributy, vztahy, sémantické vyhledávání, související uzly, LLM web research
- Smart Model routing: Ollama pro bulk simulační kola, cloud/Claude pro reporty a ontologii
- Belief state per agent: stance (-1 to +1), confidence (0-1), trust per agent (0-1)
- Žádné published benchmarky prediktivní přesnosti — "SimCity for prediction"
- AGPL-3.0 — virální licence, omezuje komerční použití

## Relevance to STOPA

Knowledge graph → persona generation pipeline je zajímavý vzor pro Záchvěv (narrative simulation layer). Belief state pattern (stance/confidence/trust) je adoptovatelný nezávisle. Smart Model routing odpovídá STOPA budget tier designu. Sliding-window round memory relevantní pro /autoloop.

## Mentioned In

- [MiroShark Research Report](../sources/miroshark-research.md)
