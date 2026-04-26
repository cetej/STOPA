---
title: Temporální taskifikace v průběžném učení: zdroj nestability evaluace
url: http://arxiv.org/abs/2604.21930v1
date: 2026-04-26
concepts: ["Streaming Continual Learning", "temporální taskifikace", "plasticity a stability profily", "Boundary-Profile Sensitivity", "Experience Replay", "Elastic Weight Consolidation"]
entities: ["Nicolae Filat", "Ahmed Hussain", "Konstantinos Kalogiannis", "Elena Burceanu", "CESNET-Timeseries24"]
source: brain-ingest-local
---

# Temporální taskifikace v průběžném učení: zdroj nestability evaluace

**URL**: http://arxiv.org/abs/2604.21930v1

## Key Idea

Způsob rozdělení kontinuálního datového proudu na časové úseky (taskifikace) zásadně ovlivňuje výsledky evaluace modelů průběžného učení, i při zachování stejných dat a metod. Různé časové hranice vedou k odlišným režimům učení a závěrům o výkonnosti.

## Claims

- Temporální taskifikace není neutrální předzpracování, ale strukturální komponenta evaluace průběžného učení
- Rozdílné rozdělení stejného datového proudu může indukovat různé režimy průběžného učení a vést k odlišným benchmarkovým závěrům
- Kratší taskifikace indukují hlučnější distribuční vzory, větší strukturální vzdálenosti a vyšší citlivost na perturbace hranic
- Závěry benchmarků v streaming CL závisí nejen na algoritmu a datech, ale i na způsobu taskifikace

## Relevance for STOPA

Pro STOPA orchestraci agentů je zásadní, že způsob segmentace kontinuálních procesů a datových toků může fundamentálně měnit výkon a chování učících se komponent. Temporální dělení úloh je kritickou designovou volbou ovlivňující adaptabilitu systému.
