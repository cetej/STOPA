---
title: Časová taskifikace v kontinuálním učení: Zdroj nestability vyhodnocování
url: http://arxiv.org/abs/2604.21930v1
date: 2026-04-26
concepts: ["Streaming Continual Learning", "Temporal Taskification", "Boundary-Profile Sensitivity (BPS)", "Plasticity and Stability Profiles", "Catastrophic Forgetting"]
entities: ["Nicolae Filat", "Ahmed Hussain", "Konstantinos Kalogiannis", "Elena Burceanu", "CESNET-Timeseries24"]
source: brain-ingest-local
---

# Časová taskifikace v kontinuálním učení: Zdroj nestability vyhodnocování

**URL**: http://arxiv.org/abs/2604.21930v1

## Key Idea

Způsob, jakým je kontinuální datový proud rozdělen na diskrétní úlohy (taskifikace), významně ovlivňuje výsledky benchmarků a závěry o výkonnosti metod kontinuálního učení, což ukazuje, že taskifikace není neutrální preprocessingový krok, ale strukturální komponenta evaluace.

## Claims

- Různé časové rozdělení stejného datového proudu mohou vyvolat různé režimy kontinuálního učení a tedy odlišné benchmarkové závěry
- Experimentální srovnání čtyř metod (continual finetuning, Experience Replay, EWC, LwF) s 9, 30 a 44denními úlohami ukázalo podstatné změny v chybovosti predikce, zapomínání a backward transferu pouze v důsledku změny taskifikace
- Kratší taskifikace indukují hlučnější vzory na úrovni distribuce, větší strukturální vzdálenosti a vyšší Boundary-Profile Sensitivity, což indikuje větší citlivost na perturbace hranic

## Relevance for STOPA

Pro STOPA orchestraci je klíčové, jak jsou dlouhodobé datové proudy segmentovány do učebních úloh. Tento výzkum ukazuje, že časové rozdělení dat významně ovlivňuje schopnost systému adaptovat se bez zapomínání, což je kritické pro kontinuální učení AI agentů v produkčním prostředí.
