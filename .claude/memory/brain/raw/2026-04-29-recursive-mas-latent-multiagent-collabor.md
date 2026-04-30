---
title: RecursiveMAS: Rekurzivní multi-agentní systémy pro škálování spolupráce
url: http://arxiv.org/abs/2604.25917v1
date: 2026-04-29
concepts: ["rekurzivní multi-agentní systémy", "latentní prostor výpočtu", "RecursiveLink modul", "inner-outer loop learning", "gradientní optimalizace celého systému", "škálování spolupráce agentů"]
entities: ["Xiyuan Yang", "James Zou", "Markus J. Buehler", "MIT", "Stanford University"]
source: brain-ingest-local
---

# RecursiveMAS: Rekurzivní multi-agentní systémy pro škálování spolupráce

**URL**: http://arxiv.org/abs/2604.25917v1

## Key Idea

RecursiveMAS rozšiřuje princip rekurzivního škálování jazykových modelů na multi-agentní systémy tím, že celý systém chápe jako jednotný rekurzivní výpočet v latentním prostoru, umožňující efektivnější spolupráci agentů s menší spotřebou tokenů.

## Claims

- RecursiveMAS dosahuje průměrného zlepšení přesnosti o 8.3% oproti pokročilým single/multi-agent baseline řešením
- Framework poskytuje 1.2×-2.4× zrychlení inference a snížení spotřeby tokenů o 34.6%-75.6%
- RecursiveMAS je výpočetně efektivnější než standardní textové multi-agentní systémy a udržuje stabilní gradienty během rekurzivního tréningu
- Systém byl úspěšně testován na 9 benchmarcích zahrnujících matematiku, vědu, medicínu, vyhledávání a generování kódu

## Relevance for STOPA

RecursiveMAS ukazuje nový přístup k orchestraci agentů přes latentní prostor místo textové komunikace, což může výrazně zefektivnit STOPA orchestraci komplexních multi-agentních workflow s menší spotřebou tokenů a rychlejší inference.
