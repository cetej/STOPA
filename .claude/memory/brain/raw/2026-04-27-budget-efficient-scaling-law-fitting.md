---
title: Efektivní fitování škálovacích zákonů pomocí aktivního výběru experimentů
url: http://arxiv.org/abs/2604.22753v1
date: 2026-04-27
concepts: ["scaling laws", "sequential experimental design", "budget-aware training", "active learning", "extrapolation accuracy", "pilot experiments"]
entities: ["Sijie Li", "Shanda Li", "Haowei Lin", "Weiwei Sun", "Ameet Talwalkar", "Yiming Yang"]
source: brain-ingest-local
---

# Efektivní fitování škálovacích zákonů pomocí aktivního výběru experimentů

**URL**: http://arxiv.org/abs/2604.22753v1

## Key Idea

Metoda pro fitování škálovacích zákonů (scaling laws) v ML, která sekvenčně vybírá pilotní experimenty tak, aby se dosáhlo přesné extrapolace při použití pouze ~10 % celkového trénovacího rozpočtu, namísto nákladného spouštění všech možných kombinací.

## Claims

- Fitování škálovacích zákonů může stát miliony dolarů a již není rutinním preprocessing krokem
- Navržená metoda dosahuje výkonu srovnatelného s fitováním na celé sadě experimentů při použití pouze ~10 % rozpočtu
- Uncertainty-aware sekvenční alokace rozpočtu konzistentně překonává klasické design-based baselines napříč různorodými benchmarky

## Relevance for STOPA

Pro STOPA orchestraci je relevantní optimalizace výpočetních zdrojů při škálování AI modelů a inteligentní alokace rozpočtu na experimenty, což může významně snížit náklady na plánování velkých tréninkových běhů.
