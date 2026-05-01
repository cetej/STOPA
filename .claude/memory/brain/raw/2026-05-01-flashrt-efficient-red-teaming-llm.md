---
title: FlashRT: Efektivní red-teaming pro prompt injection a korupci znalostí v LLM
url: http://arxiv.org/abs/2604.28157v1
date: 2026-05-01
concepts: ["red-teaming", "prompt injection", "knowledge corruption", "long-context LLM", "optimalizační útoky", "bezpečnost AI"]
entities: ["Yanting Wang", "Chenlong Yin", "Ying Chen", "Jinyuan Jia", "Gemini-3.1-Pro", "Qwen-3.5", "nanoGCG", "TAP", "AutoDAN"]
source: brain-ingest-local
---

# FlashRT: Efektivní red-teaming pro prompt injection a korupci znalostí v LLM

**URL**: http://arxiv.org/abs/2604.28157v1

## Key Idea

FlashRT je framework pro optimalizační útoky na long-context LLM (prompt injection, knowledge corruption), který dosahuje 2-7× rychlejšího běhu a 2-4× nižší spotřeby paměti oproti existujícím metodám.

## Claims

- FlashRT dosahuje 2-7× zrychlení při red-teaming útocích na long-context LLM (např. z 1 hodiny na <10 minut)
- FlashRT snižuje spotřebu GPU paměti 2-4× (např. z 264.1 GB na 65.7 GB při 32K token kontextu)
- FlashRT lze aplikovat na black-box optimalizační metody jako TAP a AutoDAN

## Relevance for STOPA

Pro STOPA orchestraci je klíčové zajistit bezpečnost při práci s dlouhými kontexty a externími zdroji dat. FlashRT umožňuje efektivní testování odolnosti LLM vůči prompt injection a knowledge corruption útokům.
