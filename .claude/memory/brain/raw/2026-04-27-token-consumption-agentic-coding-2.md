---
title: Analýza spotřeby tokenů u AI agentů v kódovacích úlohách
url: http://arxiv.org/abs/2604.22750v1
date: 2026-04-27
concepts: ["spotřeba tokenů", "AI agenti", "agentic coding", "ekonomika LLM", "token efficiency", "predikce nákladů"]
entities: ["SWE-bench Verified", "GPT-5", "Claude-Sonnet-4.5", "Kimi-K2"]
source: brain-ingest-local
---

# Analýza spotřeby tokenů u AI agentů v kódovacích úlohách

**URL**: http://arxiv.org/abs/2604.22750v1

## Key Idea

První systematická studie spotřeby tokenů u AI agentů při programování ukazuje, že agentní úlohy spotřebují 1000x více tokenů než běžné kódování, s vysokou variabilitou (až 30x rozdíl na stejné úloze) a že modely nedokáží přesně predikovat vlastní náklady.

## Claims

- Agentní úlohy spotřebují 1000x více tokenů než code reasoning a code chat, s dominancí vstupních tokenů
- Spotřeba tokenů je vysoce variabilní: stejná úloha může mít až 30x rozdíl v nákladech, vyšší spotřeba neznačí vyšší přesnost
- Modely se liší v token efficiency: Kimi-K2 a Claude-Sonnet-4.5 spotřebují průměrně o 1,5M+ tokenů více než GPT-5
- Lidské hodnocení obtížnosti úlohy jen slabě koreluje se skutečnými náklady na tokeny
- Frontier modely systematicky podceňují vlastní spotřebu tokenů (korelace nejvýše 0.39)

## Relevance for STOPA

Klíčové pro pochopení ekonomiky nasazení AI agentů v produkčních orchestracích - ukazuje nepředvídatelnost nákladů a nutnost monitoringu spotřeby tokenů při řízení agentních workflow.
