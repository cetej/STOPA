---
title: "Vertikální škálování STOPA orchestrace — Technická zpráva"
slug: vertical-scaling-report
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 7
claims_extracted: 5
---
# Vertikální škálování STOPA orchestrace — Technická zpráva

> **TL;DR**: Technická zpráva dokumentuje 3-fázový plán vertikálního škálování STOPA: Fáze A (3-level scout output, aktuálně), Fáze B (/telescope skill, za 2 týdny), Fáze C (plná integrace, za 6 týdnů). Break-even: 1 z 8 úkolů s cross-level problémem.

## Key Claims

1. HCAG (arXiv:2603.20299) prokazuje, že flat RAG selhává na komplexních kódových bázích — hierarchická abstrakce je matematicky cost-optimální vs. flat přístup — `[verified]`
2. HexMachina prokazuje, že 3-agent core je optimum — víc agentů neznamená lepší výsledek — fázová separace (discovery→improvement) je kritická — `[verified]`
3. Token overhead vertikálního škálování je zvládnutelný: Fáze A +0%, B +10-20%, C +25-40%; SkillReducer umožňuje 48-75% úsporu přes hierarchickou kompresi — `[argued]`
4. HTN+LLM (arXiv:2511.18165): čistě LLM hierarchické plánování má 1% syntaktickou validitu — hybridní enforcement je nutný — `[verified]`
5. Break-even: pokud alespoň 1 z 8 úkolů má cross-level problém, vertikální škálování se finančně vyplatí ($1.55 úspora per incident) — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| HCAG (arXiv:2603.20299) | paper | existing (hcag.md) |
| HexMachina | tool/paper | existing (hexmachina.md) |
| HMAS Taxonomy (arXiv:2508.12683) | paper | existing (hmas-taxonomy.md) |
| SkillReducer | concept | existing (skillreducer.md) |
| /telescope skill | concept | new |
| 3-Level Scout | concept | new |
| HTN+LLM (arXiv:2511.18165) | paper | new |

## Relations

- /telescope skill `extends` scout
- 3-Level Scout `produces` makro+mezo+mikro context
- HCAG `validates` vertical scaling approach
- HexMachina `validates` 3-agent optimum
- HTN+LLM `validates` need-for-hybrid-enforcement
