---
title: UAE: Sladění dense retrieverů s užitečností LLM pomocí destilace
url: http://arxiv.org/abs/2604.22722v1
date: 2026-04-27
concepts: ["Dense retrieval", "Utility-aligned embeddings", "Distribution matching", "Utility-Modulated InfoNCE", "RAG (Retrieval-Augmented Generation)", "Perplexity-based utility", "Bi-encoder"]
entities: ["Rajinder Sandhu", "Di Mu", "Cheng Chang", "Md Shahriar Tasjid", "Himanshu Rai", "Maksims Volkovs", "Ga Wu", "QASPER", "BGE-Base"]
source: brain-ingest-local
---

# UAE: Sladění dense retrieverů s užitečností LLM pomocí destilace

**URL**: http://arxiv.org/abs/2604.22722v1

## Key Idea

Metoda Utility-Aligned Embeddings (UAE) trénuje bi-encoder tak, aby napodoboval distribuci užitečnosti odvozenou z perplexity LLM, čímž kombinuje výhody sémantického vyhledávání a LLM re-rankingu bez nutnosti inference LLM za běhu.

## Claims

- UAE zlepšuje Recall@1 o 30,59% a MAP o 30,16% oproti baseline BGE-Base na QASPER benchmarku
- UAE je více než 180× rychlejší než efektivní metody LLM re-rankingu při zachování konkurenční výkonnosti
- Token F1 se zlepšil o 17,3% oproti sémantickému baseline
- Sladění retrievalu s generativní užitečností poskytuje spolehlivé kontexty ve velkém měřítku

## Relevance for STOPA

UAE přímo adresuje výzvu efektivního retrievalu v RAG systémech – klíčové pro STOPA orchestraci, kde je třeba rychle a přesně vyhledávat relevantní kontexty pro LLM bez nákladné inference za běhu.
