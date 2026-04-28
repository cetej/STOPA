---
title: Analýza spotřeby tokenů u AI agentů v programovacích úlohách
url: http://arxiv.org/abs/2604.22750v1
date: 2026-04-27
concepts: ["spotřeba tokenů", "AI agenti", "agentic coding", "náklady LLM", "token efficiency", "predikce nákladů"]
entities: ["SWE-bench Verified", "GPT-5", "Claude-Sonnet-4.5", "Kimi-K2"]
source: brain-ingest-local
---

# Analýza spotřeby tokenů u AI agentů v programovacích úlohách

**URL**: http://arxiv.org/abs/2604.22750v1

## Key Idea

První systematická studie spotřeby tokenů u AI agentů při řešení programovacích úloh, která odhaluje 1000x vyšší spotřebu než u běžného kódování, vysokou variabilitu a neschopnost modelů předpovídat vlastní náklady.

## Claims

- Agentic úlohy spotřebovávají 1000x více tokenů než běžné kódování, přičemž vstupní tokeny tvoří většinu nákladů
- Spotřeba tokenů je vysoce variabilní - běhy stejné úlohy se mohou lišit až 30x v celkovém počtu tokenů
- Frontier modely selhávají při předpovídání vlastní spotřeby tokenů (korelace pouze do 0.39) a systematicky podceňují skutečné náklady
- Kimi-K2 a Claude-Sonnet-4.5 spotřebovávají v průměru o 1.5 milionu tokenů více než GPT-5
- Lidské hodnocení obtížnosti úlohy má jen slabou korelaci se skutečnými náklady na tokeny

## Relevance for STOPA

Kritická studie pro ekonomiku AI agentů - odhaluje obrovské náklady agentic úloh a nutnost optimalizace spotřeby tokenů při orchestraci agentů. Relevantní pro cost monitoring a resource management v STOPA.
