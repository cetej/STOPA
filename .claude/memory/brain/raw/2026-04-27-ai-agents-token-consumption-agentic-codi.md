---
title: Jak AI agenti utrácejí tokeny při programovacích úlohách
url: http://arxiv.org/abs/2604.22750v1
date: 2026-04-27
concepts: ["spotřeba tokenů", "AI agenti", "agentic coding", "token efficiency", "cost prediction", "SWE-bench"]
entities: ["Longju Bai", "Jiaxin Pei", "Rada Mihalcea", "Erik Brynjolfsson", "Alex Pentland", "GPT-5", "Claude-Sonnet-4.5", "Kimi-K2"]
source: brain-ingest-local
---

# Jak AI agenti utrácejí tokeny při programovacích úlohách

**URL**: http://arxiv.org/abs/2604.22750v1

## Key Idea

První systematická studie spotřeby tokenů u AI agentů v kódovacích úlohách ukazuje, že agenti spotřebují 1000× více tokenů než běžné LLM úlohy, spotřeba je vysoce variabilní a modely neumí přesně předpovědět své vlastní náklady.

## Claims

- Agentic úlohy spotřebují 1000× více tokenů než běžné code reasoning a code chat úlohy
- Spotřeba tokenů na stejné úloze se může lišit až 30×, přičemž vyšší spotřeba neznamená vyšší úspěšnost
- Kimi-K2 a Claude-Sonnet-4.5 v průměru spotřebují o 1,5 milionu tokenů více než GPT-5
- Hodnocení obtížnosti úlohy experty jen slabě koreluje se skutečnými náklady na tokeny
- Frontier modely neumí přesně předpovědět svou vlastní spotřebu tokenů (korelace max 0.39) a systematicky ji podceňují

## Relevance for STOPA

Pro STOPA orchestraci je klíčové pochopit ekonomiku AI agentů - spotřeba tokenů je vysoce variabilní a obtížně predikovatelná, což vyžaduje monitorování a optimalizaci nákladů při orchestraci dlouhotrvajících agentic úloh.
