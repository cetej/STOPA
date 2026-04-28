---
title: Analýza a predikce spotřeby tokenů u AI agentů při kódovacích úlohách
url: http://arxiv.org/abs/2604.22750v1
date: 2026-04-27
concepts: ["spotřeba tokenů", "AI agenti", "token efficiency", "agentic coding", "predikce nákladů", "SWE-bench", "LLM ekonomika"]
entities: ["Longju Bai", "Jiaxin Pei", "Rada Mihalcea", "Erik Brynjolfsson", "Alex Pentland", "GPT-5", "Claude-Sonnet-4.5", "Kimi-K2"]
source: brain-ingest-local
---

# Analýza a predikce spotřeby tokenů u AI agentů při kódovacích úlohách

**URL**: http://arxiv.org/abs/2604.22750v1

## Key Idea

První systematická studie spotřeby tokenů AI agenty při kódování odhaluje, že agentické úlohy spotřebují 1000× více tokenů než běžné kódování, náklady jsou velmi variabilní (až 30× rozdíl na stejné úloze) a modely nedokáží přesně predikovat vlastní spotřebu tokenů.

## Claims

- Agentické úlohy spotřebují 1000× více tokenů než code reasoning a code chat, přičemž vstupní tokeny tvoří hlavní náklad.
- Spotřeba tokenů je velmi variabilní: běhy na stejné úloze se mohou lišit až 30×, vyšší spotřeba tokenů neznamená vyšší přesnost.
- Kimi-K2 a Claude-Sonnet-4.5 v průměru spotřebují o 1,5 milionu tokenů více než GPT-5 na stejných úlohách.
- Obtížnost úlohy hodnocená lidskými experty jen slabě koreluje se skutečnou spotřebou tokenů.
- Frontier modely nedokáží přesně predikovat vlastní spotřebu tokenů (korelace max 0.39) a systematicky podceňují reálné náklady.

## Relevance for STOPA

Pro STOPA orchestraci je klíčové pochopit ekonomiku AI agentů a vzory spotřeby tokenů při komplexních úlohách, zejména pro optimalizaci nákladů a predikci zdrojů při dlouhodobém spouštění autonomních pracovních toků.
