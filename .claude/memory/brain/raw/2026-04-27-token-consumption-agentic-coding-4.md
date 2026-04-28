---
title: Analýza a predikce spotřeby tokenů u AI agentů v kódovacích úlohách
url: http://arxiv.org/abs/2604.22750v1
date: 2026-04-27
concepts: ["spotřeba tokenů", "AI agenti", "ekonomika LLM", "kódovací úlohy", "predikce nákladů", "token efficiency", "SWE-bench"]
entities: ["Longju Bai", "Jiaxin Pei", "Rada Mihalcea", "Erik Brynjolfsson", "Alex Pentland", "GPT-5", "Claude-Sonnet-4.5", "Kimi-K2"]
source: brain-ingest-local
---

# Analýza a predikce spotřeby tokenů u AI agentů v kódovacích úlohách

**URL**: http://arxiv.org/abs/2604.22750v1

## Key Idea

První systematická studie spotřeby tokenů u AI agentů při kódování ukazuje, že agentní úlohy jsou 1000x dražší než běžné kódování, spotřeba je vysoce variabilní (až 30x rozdíl) a modely neumí přesně predikovat své vlastní náklady.

## Claims

- Agentní kódovací úlohy spotřebují 1000x více tokenů než běžné kódování, přičemž vstupní tokeny tvoří většinu nákladů
- Spotřeba tokenů na stejné úloze se může lišit až 30x a vyšší spotřeba nekoreluje s vyšší přesností
- Modely jako Kimi-K2 a Claude-Sonnet-4.5 spotřebují v průměru o 1,5 milionu tokenů více než GPT-5 na stejných úlohách
- Lidmi hodnocená obtížnost úlohy slabě koreluje se skutečnými náklady na tokeny
- Frontier modely neumí přesně predikovat vlastní spotřebu tokenů (korelace max 0.39) a systematicky podceňují skutečné náklady

## Relevance for STOPA

Klíčové pro ekonomiku STOPA orchestrace – ukazuje, že agentní workflow jsou extrémně nákladné a nepředvídatelné, což vyžaduje sofistikované nástroje pro monitoring a predikci nákladů před spuštěním agentů.
