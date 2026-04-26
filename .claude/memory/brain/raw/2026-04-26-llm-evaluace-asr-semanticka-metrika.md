---
title: Hodnocení automatického rozpoznávání řeči pomocí generativních LLM
url: http://arxiv.org/abs/2604.21928v1
date: 2026-04-26
concepts: ["Automatické rozpoznávání řeči (ASR)", "Hodnocení kvality transkripce", "Generativní velké jazykové modely", "Sémantické metriky vs. WER", "Embeddingové reprezentace"]
entities: ["Thibault Bañeras-Roux", "HATS dataset", "Word Error Rate (WER)"]
source: brain-ingest-local
---

# Hodnocení automatického rozpoznávání řeči pomocí generativních LLM

**URL**: http://arxiv.org/abs/2604.21928v1

## Key Idea

Článek zkoumá použití velkých jazykových modelů (LLM) pro hodnocení kvality automatického rozpoznávání řeči jako sémantickou alternativu k tradičnímu WER, která lépe koreluje s lidským vnímáním.

## Claims

- Nejlepší LLM dosahují 92-94% shody s lidskými anotátory při výběru nejlepší hypotézy, oproti 63% u WER
- Embeddingové reprezentace z decoder-based LLM vykazují srovnatelný výkon s encoder modely
- LLM nabízejí směr k interpretovatelným a sémantickým evaluacím ASR systémů

## Relevance for STOPA

Pro STOPA orchestraci je klíčové zajistit kvalitu ASR výstupů v multimodálních systémech. Použití LLM pro sémantické hodnocení může zlepšit validaci řečových vstupů a jejich transformaci před dalším zpracováním v orchestračním workflow.
