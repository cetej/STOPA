---
title: RecursiveMAS: Rekurzivní multi-agentní systémy s latentní komunikací
url: http://arxiv.org/abs/2604.25917v1
date: 2026-04-29
concepts: ["rekurzivní multi-agentní systémy", "latentní prostorová komunikace", "RecursiveLink modul", "inner-outer loop learning", "gradient-based credit assignment", "heterogenní agentní kolaborace"]
entities: ["Xiyuan Yang", "James Zou", "Markus J. Buehler", "Jingrui He"]
source: brain-ingest-local
---

# RecursiveMAS: Rekurzivní multi-agentní systémy s latentní komunikací

**URL**: http://arxiv.org/abs/2604.25917v1

## Key Idea

RecursiveMAS rozšiřuje princip rekurzivního škálování z jednotlivých modelů na multi-agentní systémy, kde agenti spolupracují v rekurzivní smyčce skrze sdílený latentní prostor místo textové komunikace, což vede k rychlejšímu a efektivnějšímu řešení komplexních úloh.

## Claims

- RecursiveMAS dosahuje průměrného zlepšení přesnosti o 8,3% oproti pokročilým single/multi-agent a rekurzivním baselinům
- Systém poskytuje 1,2×-2,4× zrychlení inference a 34,6%-75,6% redukci spotřeby tokenů
- RecursiveMAS je výpočetně efektivnější než standardní textové multi-agentní systémy a udržuje stabilní gradienty během rekurzivního tréninku
- Framework byl úspěšně testován na 9 benchmarcích pokrývajících matematiku, vědu, medicínu, vyhledávání a generování kódu

## Relevance for STOPA

RecursiveMAS představuje nový přístup k orchestraci multi-agentních systémů s rekurzivní komunikací v latentním prostoru, což může inspirovat STOPA k efektivnějším formám koordinace a sdílení informací mezi agenty s nižší latencí než textová komunikace.
