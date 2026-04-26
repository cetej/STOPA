---
title: Temporální taskifikace v kontinuálním učení: zdroj nestability vyhodnocování
url: http://arxiv.org/abs/2604.21930v1
date: 2026-04-26
concepts: ["streaming continual learning", "temporal taskification", "boundary-profile sensitivity", "catastrophic forgetting", "plasticity-stability profiling"]
entities: ["Nicolae Filat", "Ahmed Hussain", "Konstantinos Kalogiannis", "Elena Burceanu", "CESNET-Timeseries24"]
source: brain-ingest-local
---

# Temporální taskifikace v kontinuálním učení: zdroj nestability vyhodnocování

**URL**: http://arxiv.org/abs/2604.21930v1

## Key Idea

Způsob, jakým se kontinuální datový proud rozdělí na časové úlohy (taskifikace), významně ovlivňuje výsledky benchmarků kontinuálního učení, přičemž různá validní rozdělení stejného streamu vedou k odlišným závěrům o výkonnosti modelů.

## Claims

- Temporální rozdělení datového streamu na úlohy není neutrální preprocessing, ale strukturální komponenta vyhodnocování
- Různá validní rozdělení stejného streamu mohou indukovat různé CL režimy a vést k odlišným benchmarkovým závěrům
- Kratší taskifikace vyvolávají hlučnější vzorce distribuce, větší strukturální vzdálenosti a vyšší citlivost na perturbace hranic
- Změna pouze taskifikace (při fixním streamu, modelu a tréninkovém rozpočtu) významně mění forecasting error, zapomínání a backward transfer

## Relevance for STOPA

Pro orchestraci STOPA je klíčové pochopení, jak rozdělení kontinuálního streamu dat ovlivňuje adaptaci a učení systému. Výsledky ukazují nutnost explicitně řídit temporální segmentaci dat jako první-řadovou evaluační proměnnou při orchestraci distribuovaných kontinuálních procesů.
