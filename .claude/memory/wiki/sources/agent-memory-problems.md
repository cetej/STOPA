---
title: "Uncontrolled Memory Growth & False Memory Propagation in LLM Agents"
slug: agent-memory-problems
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 10
claims_extracted: 5
---

# Uncontrolled Memory Growth & False Memory Propagation in LLM Agents

> **TL;DR**: Dva systémová selhání paměti agentů: UMG (nekontrolovaný růst) a FMP (propagace falešných vzpomínek). Klíčový nález: LLM identifikuje 67–87% vlastních chyb v izolaci, ale v kontextu je stejně propaguje — commitment bias přebije sebekorekci. Nejsilnější obrana: write-time admission control (A-MAC) odmítne špatnou paměť před zápisem.

## Key Claims

1. LLM identifikuje 67–87% vlastních chyb v izolaci, ale v kontextu je propaguje dál — commitment bias přebíjí sebekorekci — `[verified]`
2. MemoryGraft: 9% otrávených záznamů z 110 → 47.9% všech retrieval výsledků, poisoning přetrvává neomezeně — `[verified]`
3. MINJA (NeurIPS 2025): >95% injection success rate přes normální user queries bez přímého přístupu k memory banku — `[verified]`
4. A-MAC write-time admission: F1 0.583 na LoCoMo, 31% snížení latence — write-gate efektivnější než retroaktivní oprava — `[verified]`
5. Nejlepší LLM detektor kontradikcí: Claude-3 Sonnet + CoT = 0.71 accuracy — detekce kontradikcí je intrinsicky těžká — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| A-MAC | paper | new |
| MemGPT | paper | new |
| AgeMem | paper | new |
| MemoryGraft | paper | new |
| MINJA | paper | new |
| Zep (bi-temporal KG) | tool | new |
| Hallucination Snowballing | concept | new |
| UMG (Uncontrolled Memory Growth) | concept | new |
| FMP (False Memory Propagation) | concept | new |
| A-MEM | paper | new |

## Relations

- A-MAC `prevents` FMP via write-time admission control (5-factor scoring)
- MemGPT `manages` UMG via 3-tier OS-inspired paging
- MemoryGraft `exploits` absence of confidence tracking in retrieval
- MINJA `injects` false memories via normal user queries
- Zep `solves` temporal staleness via bi-temporal edge invalidation
