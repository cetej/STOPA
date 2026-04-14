---
title: "Karpathy LLM Knowledge Base / Second Brain — CoderSera"
source: https://ghost.codersera.com/blog/karpathy-llm-knowledge-base-second-brain/
date: 2026-04-14
type: article
tags: [karpathy, llm-wiki, second-brain, architecture]
concepts: [llm-wiki, second-brain, compiler-analogy]
---

## Summary

Analýza Karpathyho posunu od používání LLM pro generování kódu k "knowledge manipulation" — budování self-maintaining osobní wiki.

## Tříložková architektura (přesnější popis)

| Složka | Role | Pravidla |
|--------|------|---------|
| **raw/** | Append-only repository zdrojů | PDF, články, poznámky, screenshoty → markdown. LLM pouze čte. |
| **wiki/** | LLM output — strukturované wiki | Interlinked markdown articles + index soubor |
| **outputs/** | Persistentní výstupy dotazů | Auditovatelné syntetizované reporty |

## Compilation Step (přesnější)

Při příchodu nových zdrojů do `raw/`:
1. LLM identifikuje nové koncepty
2. Vytváří nebo aktualizuje wiki articles
3. Generuje backlinky
4. Refreshuje index
5. Kontroluje duplicity a kontradikce v celém indexu

## Linting Pass

Periodický health check:
- Inconsistencies
- Chybějící articles pro referencované koncepty
- Content gaps

## Schema-Driven Execution

`CLAUDE.md` definuje ingestion rules, formatting conventions, operational procedures. Posun: člověk přechází z "content writer" na "precise instruction crafter".

## Proč není RAG

Místo vektorového fragmentování dokumentů → full contextual summaries. LLM čte kompaktní index + kompletní articles při query time. Žádné similarity searches přes embeddings.

## Limity

- Škáluje na "few hundred articles" (pak omezují context windows)
- Token cost roste s scale
- Accuracy závisí na source comprehension LLM
- Žádný real-time retrieval pro multi-user concurrent access
- Human oversight nutný pro fact-checking
