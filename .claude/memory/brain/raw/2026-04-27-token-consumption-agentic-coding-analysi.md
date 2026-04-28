---
title: Analýza a predikce spotřeby tokenů u AI agentů v programovacích úlohách
url: http://arxiv.org/abs/2604.22750v1
date: 2026-04-27
concepts: ["token consumption", "AI agents", "agentic coding", "cost prediction", "SWE-bench", "computational efficiency", "LLM economics"]
entities: ["Longju Bai", "Xingyao Wang", "Rada Mihalcea", "Erik Brynjolfsson", "Alex Pentland", "GPT-5", "Claude-Sonnet-4.5", "Kimi-K2"]
source: brain-ingest-local
---

# Analýza a predikce spotřeby tokenů u AI agentů v programovacích úlohách

**URL**: http://arxiv.org/abs/2604.22750v1

## Key Idea

První systematická studie spotřeby tokenů u AI agentů řešících kódovací úlohy, která ukazuje že agentní úlohy jsou 1000x dražší než běžný chat, spotřeba je vysoce variabilní a modely nedokáží přesně předpovídat vlastní náklady.

## Claims

- Agentní kódovací úlohy spotřebují 1000x více tokenů než běžný code chat, přičemž většinu tvoří vstupní tokeny
- Spotřeba tokenů na stejné úloze se může lišit až 30x a vyšší spotřeba neznamená vyšší úspěšnost - přesnost často klesá při vysokých nákladech
- Kimi-K2 a Claude-Sonnet-4.5 v průměru spotřebují o 1.5M tokenů více než GPT-5 na stejných úlohách
- Lidské hodnocení složitosti úloh slabě koreluje s reálnou spotřebou tokenů agentů
- Frontier modely nedokáží přesně předpovídat vlastní spotřebu tokenů (korelace pouze do 0.39) a systematicky podceňují reálné náklady

## Relevance for STOPA

Pro STOPA orchestraci je klíčové pochopení nákladových vzorců AI agentů při složitých úlohách - umožňuje optimalizaci výběru modelů, predikci nákladů a efektivnější workflow design při nasazování agentních systémů.
