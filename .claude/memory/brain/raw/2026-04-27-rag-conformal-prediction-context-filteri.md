---
title: RAG s konfirmální predikcí: statisticky garantované filtrování kontextu
url: https://arxiv.org/abs/2511.17908
date: 2026-04-27
concepts: ["Retrieval-Augmented Generation (RAG)", "Konfirmální predikce", "Context engineering", "Coverage-controlled filtering", "Faktická přesnost LLM"]
entities: ["Debashish Chakraborty", "Eugene Yang", "Daniel Khashabi", "Dawn Lawrie", "Kevin Duh", "ECIR 2026"]
source: brain-ingest-local
---

# RAG s konfirmální predikcí: statisticky garantované filtrování kontextu

**URL**: https://arxiv.org/abs/2511.17908

## Key Idea

Článek navrhuje použití konfirmální predikce pro principiální filtrování kontextu v RAG systémech, které poskytuje statistické záruky na zachování relevantních důkazů při redukci šumu a délky kontextu o 2-3×.

## Claims

- Konfirmální filtrování konzistentně dosahuje cílového pokrytí a zajišťuje zachování specifikované frakce relevantních úryvků
- Redukuje zachovaný kontext 2-3× oproti nefiltrovanému retrievalu při zachování faktické přesnosti
- Přístup je model-agnostický a poskytuje statisticky principiální způsob kontextového inženýrství pro RAG
- Faktická přesnost měřená ARGUE F1 se zlepšuje při přísném filtrování a zůstává stabilní při mírném pokrytí na datasetu NeuCLIR

## Relevance for STOPA

Pro STOPA orchestraci je relevantní statisticky garantovaný přístup k filtrování a redukci kontextu v RAG systémech, který umožňuje optimalizovat délku a kvalitu vstupů pro LLM při zachování faktické přesnosti odpovědí.
