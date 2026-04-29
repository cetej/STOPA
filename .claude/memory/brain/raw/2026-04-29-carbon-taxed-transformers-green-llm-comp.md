---
title: Carbon-Taxed Transformers: Komprese LLM pro udržitelné AI
url: http://arxiv.org/abs/2604.25903v1
date: 2026-04-29
concepts: ["komprese LLM", "udržitelné AI", "carbon pricing", "model compression pipeline", "software engineering tasks", "inference optimization", "environmentální náklady AI"]
entities: ["Ajmain Inqiad Alam", "Palash Roy", "Chanchal K. Roy", "Banani Roy", "Kevin A. Schneider", "ACM Software Engineering"]
source: brain-ingest-local
---

# Carbon-Taxed Transformers: Komprese LLM pro udržitelné AI

**URL**: http://arxiv.org/abs/2604.25903v1

## Key Idea

Článek představuje CTT pipeline, systematickou metodu komprese velkých jazykových modelů inspirovanou ekonomickou uhlíkovou daní, která snižuje paměťovou náročnost až o 49x, čas inference až o 10x a emise CO2 až o 81% při zachování ~98% přesnosti.

## Claims

- CTT dosahuje až 49x redukce paměti a až 10x zrychlení inference při zachování vysoké přesnosti
- Metoda snižuje CO2 emise až o 81% oproti nekomprimovaným modelům
- Pipeline funguje napříč různými architekturami (encoder-only, encoder-decoder, decoder-only) a SE úlohami
- Ablační studie potvrzují důležitost pořadí kroků v pipeline i individuálních komponent

## Relevance for STOPA

Pro STOPA orchestraci je CTT relevantní jako metodologie efektivního deploymentu LLM v produkčním prostředí, kde jsou výpočetní zdroje a energetická náročnost kritickými faktory při škálování AI agentů.
