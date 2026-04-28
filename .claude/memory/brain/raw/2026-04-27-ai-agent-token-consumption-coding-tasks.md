---
title: Jak AI agenti utrácejí tokeny při řešení programovacích úloh
url: http://arxiv.org/abs/2604.22750v1
date: 2026-04-27
concepts: ["Token consumption", "AI agenti", "SWE-bench", "Ekonomika LLM", "Predikce nákladů", "Efektivita modelů"]
entities: ["Longju Bai", "Jiaxin Pei", "Rada Mihalcea", "Erik Brynjolfsson", "Alex Pentland", "GPT-5", "Claude-Sonnet-4.5", "Kimi-K2"]
source: brain-ingest-local
---

# Jak AI agenti utrácejí tokeny při řešení programovacích úloh

**URL**: http://arxiv.org/abs/2604.22750v1

## Key Idea

První systematická studie spotřeby tokenů u AI agentů při programovacích úlohách ukazuje, že agentické úlohy spotřebují 1000x více tokenů než běžné kódování, spotřeba je vysoce variabilní (až 30x rozdíl při stejné úloze) a modely neumí přesně predikovat své vlastní náklady.

## Claims

- Agentické programovací úlohy spotřebují 1000x více tokenů než běžné code reasoning a code chat, hlavně kvůli vstupním tokenům
- Spotřeba tokenů je vysoce nestabilní – stejná úloha může vyžadovat až 30x rozdíl v tokenech, přičemž vyšší spotřeba nezaručuje lepší přesnost
- Modely se výrazně liší v efektivitě: Kimi-K2 a Claude-Sonnet-4.5 spotřebují v průměru o 1,5 milionu tokenů více než GPT-5
- Lidské hodnocení složitosti úlohy pouze slabě koreluje s reálnými náklady na tokeny
- Moderní modely neumí přesně predikovat vlastní spotřebu tokenů (korelace max. 0,39) a systematicky podceňují skutečné náklady

## Relevance for STOPA

Pro STOPA orchestraci je klíčové pochopit náklady a efektivitu agentů při složitých úlohách. Studie ukazuje vysokou variabilitu a nepředvídatelnost nákladů, což je kritické pro plánování a optimalizaci agentických workflow.
