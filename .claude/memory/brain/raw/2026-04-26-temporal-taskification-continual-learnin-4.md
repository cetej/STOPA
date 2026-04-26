---
title: Temporální taskifikace v kontinuálním učení: zdroj nestability evaluace
url: http://arxiv.org/abs/2604.21930v1
date: 2026-04-26
concepts: ["Streaming Continual Learning", "temporální taskifikace", "plasticity and stability profiles", "Boundary-Profile Sensitivity", "catastrophic forgetting", "Experience Replay", "Elastic Weight Consolidation"]
entities: ["Nicolae Filat", "Ahmed Hussain", "Konstantinos Kalogiannis", "Elena Burceanu", "CESNET-Timeseries24"]
source: brain-ingest-local
---

# Temporální taskifikace v kontinuálním učení: zdroj nestability evaluace

**URL**: http://arxiv.org/abs/2604.21930v1

## Key Idea

Způsob rozdělení datového streamu na diskrétní úlohy (temporální taskifikace) v kontinuálním učení není neutrální předprocesing, ale strukturální složka evaluace, která může zásadně ovlivnit závěry benchmarků a výkon modelů.

## Claims

- Různá validní rozdělení stejného datového streamu mohou indukovat odlišné režimy kontinuálního učení a vést k rozdílným závěrům benchmarků
- Při experimentech s predikcí síťového provozu způsobily rozdíly v taskifikaci (9, 30 a 44denní úseky) podstatné změny v chybě predikce, zapomínání a zpětném transferu při zachování stejných dat, modelu a trénovacího rozpočtu
- Kratší taskifikace vyvolávají šumivější distribuční vzory, větší strukturální vzdálenosti a vyšší Boundary-Profile Sensitivity, což indikuje větší citlivost na perturbace hranic úloh

## Relevance for STOPA

Pro STOPA orchestraci je klíčové pochopení, že způsob segmentace streamovaných dat do úloh může zásadně ovlivnit výkon kontinuálního učení. Při orchestraci AI modelů nad časovými řadami je třeba taskifikaci považovat za evaluační proměnnou první třídy, nikoliv jen technickou záležitost.
