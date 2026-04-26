---
title: ErrorProbe: Samozdokonalující diagnostika chyb v multi-agentních systémech
url: https://arxiv.org/abs/2604.17658
date: 2026-04-26
concepts: ["multi-agentní systémy", "diagnostika chyb", "LLM", "sémantická atribuce selhání", "episodická paměť", "zpětné trasování", "autonomous debugging"]
entities: ["Jiazheng Li", "Emine Yilmaz", "Bei Chen", "Dieu-Thu Le", "ACL 2026"]
source: brain-ingest-local
---

# ErrorProbe: Samozdokonalující diagnostika chyb v multi-agentních systémech

**URL**: https://arxiv.org/abs/2604.17658

## Key Idea

ErrorProbe je framework pro automatickou diagnostiku selhání v LLM-based multi-agentních systémech, který identifikuje problematické agenty a kroky bez potřeby manuální anotace, využívá třístavový pipeline s detekci anomálií, zpětným trasováním a ověřováním hypotéz pomocí specializovaného týmu agentů.

## Claims

- ErrorProbe významně překonává baseline řešení zejména v lokalizaci chyb na úrovni jednotlivých kroků
- Framework udržuje verifikovanou episodickou paměť, která se aktualizuje pouze při potvrzení chybových vzorů spustitelným důkazem
- Verifikovaná paměť umožňuje robustní cross-domain transfer bez potřeby přetrénování
- Existující diagnostické přístupy spoléhající na expertní anotaci nebo 'LLM-as-a-judge' nedokážou efektivně identifikovat rozhodující chybové kroky v dlouhých kontextech

## Relevance for STOPA

Pro STOPA orchestraci je klíčová schopnost automaticky diagnostikovat selhání v komplexních multi-agentních workflow a identifikovat konkrétní problematické kroky a agenty, což je nezbytné pro spolehlivý provoz a kontinuální zlepšování orchestrovaných systémů.
