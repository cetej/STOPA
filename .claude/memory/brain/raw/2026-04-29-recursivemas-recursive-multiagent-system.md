---
title: RecursiveMAS: Rekurzivní multi-agentní systémy pro škálovatelnou kolaboraci
url: http://arxiv.org/abs/2604.25917v1
date: 2026-04-29
concepts: ["rekurzivní multi-agentní systémy", "latentní prostor komunikace", "inner-outer loop učení", "gradient-based credit assignment", "RecursiveLink modul"]
entities: ["Xiyuan Yang", "James Zou", "Markus J. Buehler", "Jingrui He"]
source: brain-ingest-local
---

# RecursiveMAS: Rekurzivní multi-agentní systémy pro škálovatelnou kolaboraci

**URL**: http://arxiv.org/abs/2604.25917v1

## Key Idea

RecursiveMAS rozšiřuje princip rekurzivních jazykových modelů na multi-agentní systémy, umožňuje iterativní kolaboraci agentů v latentním prostoru namísto textové komunikace, dosahuje 8,3% zlepšení přesnosti a 1,2-2,4× rychlejší inference.

## Claims

- RecursiveMAS dosahuje průměrného zlepšení přesnosti o 8,3% oproti pokročilým single/multi-agent a rekurzivním baseline systémům
- Systém poskytuje 1,2-2,4× rychlejší end-to-end inferenci a 34,6%-75,6% redukci využití tokenů
- RecursiveMAS je efektivnější než standardní textové MAS systémy a udržuje stabilní gradienty během rekurzivního tréninku
- Framework byl testován napříč 9 benchmarky zahrnujícími matematiku, vědu, medicínu, vyhledávání a generování kódu

## Relevance for STOPA

RecursiveMAS představuje pokročilou architekturu pro orchestraci multi-agentních systémů s důrazem na efektivní latentní komunikaci namísto textové, což je relevantní pro optimalizaci výkonu a nákladů v STOPA orchestraci.
