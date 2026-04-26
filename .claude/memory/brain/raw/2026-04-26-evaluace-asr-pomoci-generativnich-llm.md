---
title: Hodnocení ASR pomocí generativních velkých jazykových modelů
url: http://arxiv.org/abs/2604.21928v1
date: 2026-04-26
concepts: ["automatické rozpoznávání řeči", "hodnocení ASR", "generativní LLM", "sémantické metriky", "Word Error Rate", "embeddingy", "kvalitativní klasifikace chyb"]
entities: ["Thibault Bañeras-Roux", "Shashi Kumar", "Driss Khalil", "Sergio Burdisso", "Petr Motlicek", "HATS dataset"]
source: brain-ingest-local
---

# Hodnocení ASR pomocí generativních velkých jazykových modelů

**URL**: http://arxiv.org/abs/2604.21928v1

## Key Idea

Článek zkoumá použití velkých jazykových modelů (LLM) pro hodnocení automatického rozpoznávání řeči (ASR) a ukazuje, že LLM dosahují 92-94% shody s lidskými anotátory při výběru nejlepší hypotézy, což výrazně převyšuje tradiční metriku WER (63%).

## Claims

- Nejlepší LLM dosahují 92-94% shody s lidskými anotátory při výběru hypotézy ASR, ve srovnání s pouhými 63% pro WER
- Embeddingy z decoder-based LLM vykazují výkon srovnatelný s encoder modely při sémantickém hodnocení
- LLM nabízejí slibný směr pro interpretovatelné a sémantické hodnocení ASR, které lépe koresponduje s lidským vnímáním než tradiční WER

## Relevance for STOPA

Pro STOPA orchestraci je relevantní využití LLM pro sémantické hodnocení výstupů řečových systémů, což umožňuje lepší validaci a výběr mezi alternativními hypotézami v rámci multimodálních AI agentů.
