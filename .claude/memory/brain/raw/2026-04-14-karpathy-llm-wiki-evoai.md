---
title: "Why Karpathy's LLM Wiki Is the Future of Personal Knowledge — EvoAI Labs"
source: https://evoailabs.medium.com/why-andrej-karpathys-llm-wiki-is-the-future-of-personal-knowledge-7ac398383772
date: 2026-04-14
type: article
tags: [karpathy, llm-wiki, second-brain, compounding, rag-critique]
concepts: [llm-wiki, second-brain, zettelkasten]
---

## Main Thesis

LLM-maintained wikis = paradigm shift od pasivní informační retrieval k aktivním, self-maintaining systémům které kumulativně compoundují znalosti.

## Klíčová kritika RAG

"There is no accumulation." — RAG při opakovaných podobných dotazech dělá identickou práci bez budování persistent insights nebo connections.

## Proč manuální wiki selhávají

Zettelkasten, Obsidian atd.: maintenance burden roste rychleji než value. "Bookkeeping burden—updating cross-references, tagging, and noting contradictions—grows much faster than the value."

## Jak LLM Wiki řeší obojí

Automatizovaná vrstva mezi raw sources a uživatelem. LLM "pre-compiles" sources — čte, extrahuje koncepty, permanentně tká interlinked markdown wiki.

## Tři vrstvy (author's framing)

1. Raw, immutable sources (PDFs, articles, transcripts)
2. LLM-maintained markdown wiki (summaries + concept pages)
3. Configuration schema (struktura a formatting rules)

## Tři compounding operace

1. **Ingest** — nové dokumenty → automatic summary + aktualizace 10-15 related concept pages + backlinks
2. **Query** — LLM naviguje wiki strukturu → ukládá discovered connections jako nové pages
3. **Lint** — broken links, contradictions, orphaned content

## Posun paradigmatu

AI: search engine → "tireless librarian and system maintainer".
Systém se skutečně vyvíjí — každý ingest přidává trvalou hodnotu.
