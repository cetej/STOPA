---
title: Hodnocení ASR pomocí generativních velkých jazykových modelů
url: http://arxiv.org/abs/2604.21928v1
date: 2026-04-26
concepts: ["Automatické rozpoznávání řeči (ASR)", "Hodnocení sémantické podobnosti", "Generativní embeddingy", "Word Error Rate (WER)", "Lidská percepce"]
entities: ["Thibault Bañeras-Roux", "Petr Motlicek", "HATS dataset"]
source: brain-ingest-local
---

# Hodnocení ASR pomocí generativních velkých jazykových modelů

**URL**: http://arxiv.org/abs/2604.21928v1

## Key Idea

Článek zkoumá využití velkých jazykových modelů (LLM) pro hodnocení automatického rozpoznávání řeči (ASR), přičemž ukazuje, že LLM dosahují 92-94% shody s lidskými anotátory při výběru nejlepší hypotézy, oproti pouhým 63% u tradiční metriky WER.

## Claims

- Nejlepší LLM dosahují 92-94% shody s lidskými anotátory při výběru správné hypotézy, zatímco WER dosahuje pouze 63%
- Embeddingy z decoder-based LLM vykazují srovnatelný výkon s encoder modely při měření sémantické vzdálenosti
- LLM nabízejí slibný směr pro interpretovatelné a sémantické hodnocení ASR systémů

## Relevance for STOPA

Pro STOPA orchestraci je klíčové měřit kvalitu ASR komponent nejen technicky, ale i sémanticky. Použití LLM pro hodnocení umožňuje lépe vyhodnotit, zda orchestrace správně porozuměla vstupním příkazům a může automaticky detekovat významové chyby.
