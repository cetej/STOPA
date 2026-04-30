---
title: RecursiveMAS: Rekurzivní Multi-agentní systémy pro efektivnější kolaboraci
url: http://arxiv.org/abs/2604.25917v1
date: 2026-04-29
concepts: ["rekurzivní výpočet", "multi-agentní systémy", "latentní stavy", "gradient-based optimization", "agent collaboration", "RecursiveLink modul", "inner-outer loop learning"]
entities: ["Xiyuan Yang", "James Zou", "Markus J. Buehler", "Cornell University"]
source: brain-ingest-local
---

# RecursiveMAS: Rekurzivní Multi-agentní systémy pro efektivnější kolaboraci

**URL**: http://arxiv.org/abs/2604.25917v1

## Key Idea

RecursiveMAS rozšiřuje princip rekurzivního škálování z jednotlivých jazykových modelů na multi-agentní systémy, kde heterogenní agenti spolupracují v rekurzivní smyčce přes latentní stavy. Umožňuje optimalizaci celého systému pomocí gradientů a dosahuje 8.3% vyšší přesnosti při 1.2-2.4× rychlejší inferenci.

## Claims

- RecursiveMAS dosahuje průměrného zlepšení přesnosti o 8.3% oproti pokročilým single/multi-agentním a rekurzivním baseline modelům
- Framework zajišťuje 1.2×-2.4× zrychlení end-to-end inference a 34.6%-75.6% redukci použití tokenů
- RecursiveMAS je efektivnější než standardní textové multi-agentní systémy a udržuje stabilní gradienty během rekurzivního tréninku
- Framework byl vyhodnocen na 9 benchmarcích pokrývajících matematiku, vědu, medicínu, vyhledávání a generování kódu

## Relevance for STOPA

RecursiveMAS představuje pokročilý framework pro orchestraci heterogenních AI agentů s využitím rekurzivních latentních stavů místo textové komunikace, což je přímo relevantní pro efektivní koordinaci agentů v STOPA systému a optimalizaci celého workflow pomocí sdílených gradientů.
