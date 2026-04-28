---
title: Analýza spotřeby tokenů u AI agentů v programátorských úlohách
url: http://arxiv.org/abs/2604.22750v1
date: 2026-04-27
concepts: ["spotřeba tokenů", "AI agenti", "agentické programování", "SWE-bench", "nákladová efektivita LLM", "predikce nákladů"]
entities: ["Longju Bai", "Jiaxin Pei", "Erik Brynjolfsson", "Alex Pentland", "GPT-5", "Claude-Sonnet-4.5", "Kimi-K2"]
source: brain-ingest-local
---

# Analýza spotřeby tokenů u AI agentů v programátorských úlohách

**URL**: http://arxiv.org/abs/2604.22750v1

## Key Idea

První systematická studie spotřeby tokenů AI agenty při řešení programátorských úloh odhaluje, že agentické úlohy spotřebují 1000× více tokenů než běžné programování, spotřeba je vysoce variabilní (až 30× rozdíl), a modely nedokážou přesně predikovat vlastní náklady.

## Claims

- Agentické programátorské úlohy spotřebují 1000× více tokenů než běžné code reasoning a code chat, přičemž náklady táhnou hlavně vstupní tokeny
- Spotřeba tokenů na stejné úloze se může lišit až 30×, vyšší spotřeba neznamená vyšší přesnost - přesnost často vrcholí při středních nákladech
- Modely se výrazně liší v efektivitě: Kimi-K2 a Claude-Sonnet-4.5 průměrně spotřebují o 1,5M tokenů více než GPT-5
- Obtížnost úlohy hodnocená experty jen slabě koreluje se skutečnými tokenovými náklady
- Frontier modely nedokážou přesně predikovat vlastní spotřebu tokenů (korelace max 0.39) a systematicky ji podceňují

## Relevance for STOPA

Pro STOPA orchestraci je klíčové pochopení ekonomiky AI agentů - nepředvídatelná spotřeba tokenů a neschopnost modelů predikovat vlastní náklady vyžaduje robustní cost monitoring a budget management při orchestraci komplexních agentických workflow.
