---
title: "MiroShark — Open-Source Swarm Intelligence Engine"
slug: miroshark-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 6
claims_extracted: 4
---

# MiroShark — Open-Source Swarm Intelligence Engine

> **TL;DR**: MiroShark (github.com/aaronjmars/MiroShark) je anglický fork MiroFish (Shanda Group). Dokument → Neo4j knowledge graf → stovky AI agentů s unikátními osobnostmi → paralelní simulace Twitter + Reddit + Polymarket. Výstup: analytická zpráva o šíření narativů. Relevantní vzory pro STOPA: knowledge graph → persona generation pipeline, belief state tracking (stance/confidence/trust), smart model routing (levný model pro bulk, drahý pro analýzu).

## Key Claims

1. Knowledge graph → persona generation pipeline: z každé entity Neo4j grafu se generuje agent s 5 vrstvami kontextu — `[asserted]`
2. Market-Media Bridge: sentiment ze sociálních sítí → trader prompty, market ceny → social media prompty — elegantní cross-domain pattern — `[asserted]`
3. Sliding-window round memory s background LLM kompakcí starých kol — relevantní pro autoloop — `[asserted]`
4. Žádné published benchmarky pro prediktivní přesnost — systém generuje přesvědčivé narativy, ale nezaručuje přesné predikce — `[asserted]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| MiroShark | tool | new |
| OASIS (CAMEL-AI simulation engine) | tool | new |
| Neo4j (knowledge graph) | tool | existing (check) |
| MiroFish | tool | new |
| Belief state tracking (stance/confidence/trust) | concept | new |
| Market-Media Bridge | concept | new |

## Relations

- `MiroShark` `forks from` `MiroFish`
- `MiroShark` `uses` `OASIS (CAMEL-AI simulation engine)`
- `MiroShark` `stores entities in` `Neo4j (knowledge graph)`
- `OASIS (CAMEL-AI simulation engine)` `implements` `Belief state tracking`
- `Market-Media Bridge` `connects` `Social simulation` `to` `Prediction markets`
