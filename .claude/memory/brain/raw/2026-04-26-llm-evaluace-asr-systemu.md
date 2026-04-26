---
title: Evaluace ASR systémů pomocí generativních velkých jazykových modelů
url: http://arxiv.org/abs/2604.21928v1
date: 2026-04-26
concepts: ["automatické rozpoznávání řeči (ASR)", "generativní jazykové modely", "sémantické metriky", "Word Error Rate (WER)", "embeddingy", "hodnocení kvality transkripce"]
entities: ["Thibault Bañeras-Roux", "Shashi Kumar", "Driss Khalil", "Sergio Burdisso", "Petr Motlicek", "HATS dataset"]
source: brain-ingest-local
---

# Evaluace ASR systémů pomocí generativních velkých jazykových modelů

**URL**: http://arxiv.org/abs/2604.21928v1

## Key Idea

Studie zkoumá využití velkých jazykových modelů (LLM) pro hodnocení automatického rozpoznávání řeči (ASR), přičemž ukazuje, že LLM dosahují 92-94% shody s lidskými anotátory při výběru nejlepší hypotézy, což výrazně převyšuje tradiční metriku WER (63%).

## Claims

- Nejlepší LLM dosahují 92-94% shody s lidskými anotátory při výběru lepší hypotézy ASR, zatímco WER pouze 63%
- Embeddingy z decoder-based LLM vykazují srovnatelný výkon s encoder modely pro měření sémantické vzdálenosti
- LLM nabízejí směr k interpretovatelné a sémanticky orientované evaluaci ASR, která lépe koreluje s lidským vnímáním než tradiční WER

## Relevance for STOPA

Pro STOPA orchestraci nabízí pokročilé metody evaluace kvality ASR komponent v ML pipeline, umožňující sémantické hodnocení transkripčních výstupů a lepší alignment s lidským vnímáním kvality.
