---
title: Skill-RAG: Chytrější vyhledávání pouze když je potřeba
url: https://x.com/omarsar0/status/2046249336162632155
date: 2026-04-26
concepts: ["RAG (Retrieval-Augmented Generation)", "failure-state detection", "hidden-state probing", "adaptivní vyhledávání", "multi-step reasoning", "skill-based routing"]
entities: ["Skill-RAG", "HotpotQA", "Natural Questions", "TriviaQA", "DAIR.AI Academy"]
source: brain-ingest-local
---

# Skill-RAG: Chytrější vyhledávání pouze když je potřeba

**URL**: https://x.com/omarsar0/status/2046249336162632155

## Key Idea

Skill-RAG je nový přístup k RAG systémům, který dokáže detekovat, kdy jazykový model potřebuje pomoc s informacemi, a teprve pak provádí cílené vyhledávání. Místo neefektivního vyhledávání při každém dotazu používá analýzu skrytých stavů modelu k rozpoznání blížící se znalostní mezery.

## Claims

- Většina RAG systémů plýtvá zdroji tím, že vyhledává při každém dotazu, i když model již zná odpověď
- Skill-RAG používá analýzu skrytých stavů k detekci okamžiku, kdy LLM selhává v znalostech, a teprve pak aktivuje specializovanou vyhledávací strategii
- Při testování na HotpotQA, Natural Questions a TriviaQA dosáhl Skill-RAG lepších výsledků než standardní RAG systémy jak v efektivitě, tak v přesnosti
- RAG se vyvíjí od monolitického pipeline k sadě dovedností, mezi kterými agent vybírá podle potřeby

## Relevance for STOPA

Pro STOPA orchestraci je klíčová schopnost rozhodnout, kdy skutečně potřebujeme externí zdroje a jaký typ vyhledávání použít. Skill-RAG ukazuje cestu k adaptivní orchestraci, kde se komponenty aktivují až při detekci skutečné potřeby, což je zásadní pro efektivní multi-step reasoning.
