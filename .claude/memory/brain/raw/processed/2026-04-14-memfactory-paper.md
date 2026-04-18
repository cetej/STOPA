---
title: "MemFactory: Unified Agent Memory Framework"
source: https://arxiv.org/abs/2603.29493
date: 2026-04-14
type: academic-paper
tags: [memory, agent, rl, grpo, unified-framework]
concepts: [memfactory, agent-memory-taxonomy, active-metacognitive-curation]
---

## Summary

MemFactory je unifikovaný framework pro trénink a evaluaci memory-driven agent pipeline. Řeší fragmentaci existujících implementací — každý přístup měl vlastní infrastrukturu, nešlo je kombinovat ani porovnávat.

## Architektura

**Tři základní paměťové operace** (plug-and-play modulárně):
- **Extraction** — co z interakce uložit
- **Updating** — jak aktualizovat existující záznamy
- **Retrieval** — jak hledat relevantní paměti

"Lego-like" atomic components → custom agent construction.

## Klíčová technika: GRPO

Nativně integruje Group Relative Policy Optimization (GRPO) pro fine-tuning interních memory management politik pomocí multi-dimensionálních environmental rewards.

## Podporované paradigmata (out-of-the-box)

- Memory-R1
- RMM (Reinforced Memory Management)
- MemAgent

## Výsledky

Relative gains **až 14.8%** na evaluačních setech vs base models. Validováno na open-source MemAgent architektuře.

## Klíčová myšlenka

Jako LLaMA-Factory pro LLM fine-tuning → MemFactory pro agent memory fine-tuning. Standardizovaná, rozšiřitelná infrastruktura snižuje bariéru vstupu.

## Code

https://github.com/MemTensor/MemFactory

## Relevance pro 2BRAIN / STOPA

- Ukazuje že memory ops (extract/update/retrieve) jsou fundamentální primitiva — koreluje s 2BRAIN ingest/query/lint cyklem
- GRPO reward shaping = cesta k eventually self-improving memory systems
- Modular design = inspirace pro STOPA skill decomposition
