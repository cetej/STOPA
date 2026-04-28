---
title: Analýza spotřeby tokenů u AI agentů v programátorských úlohách
url: http://arxiv.org/abs/2604.22750v1
date: 2026-04-27
concepts: ["token consumption", "AI agents", "agentic coding", "cost prediction", "SWE-bench", "token efficiency", "LLM economics"]
entities: ["Longju Bai", "University of Michigan", "MIT", "GPT-5", "Claude-Sonnet-4.5", "Kimi-K2"]
source: brain-ingest-local
---

# Analýza spotřeby tokenů u AI agentů v programátorských úlohách

**URL**: http://arxiv.org/abs/2604.22750v1

## Key Idea

První systematická studie spotřeby tokenů u AI agentů při programování ukazuje, že agentní úlohy spotřebují 1000× více tokenů než běžné programování, spotřeba je vysoce variabilní (až 30× rozdíl) a modely nedokážou přesně predikovat vlastní náklady.

## Claims

- Agentní programátorské úlohy spotřebují 1000× více tokenů než standardní code reasoning a code chat
- Spotřeba tokenů na stejné úloze může kolísat až 30×, vyšší spotřeba neznamená vyšší úspěšnost
- Kimi-K2 a Claude-Sonnet-4.5 průměrně spotřebují o 1,5 milionu tokenů více než GPT-5 na stejných úlohách
- Lidmi hodnocená obtížnost úlohy slabě koreluje se skutečnou spotřebou tokenů
- Modely systematicky podceňují vlastní spotřebu tokenů s korelací pouze do 0.39

## Relevance for STOPA

Zásadní pro plánování nákladů STOPA orchestrace - ukazuje nepředvídatelnost spotřeby tokenů u agentních workflow a potřebu monitoringu nákladů v reálném čase při orchestraci AI agentů.
