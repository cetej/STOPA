---
title: Charakterizace streamovací složitosti CSP pomocí ne-redundance
url: http://arxiv.org/abs/2604.21922v1
date: 2026-04-26
concepts: ["Constraint Satisfaction Problems (CSP)", "streamovací algoritmy", "ne-redundance", "paměťová složitost", "jednoprůchodové zpracování"]
entities: ["Amatya Sharma", "Santhoshini Velusamy", "Vu (TCS 2024)", "Chou, Golovnev, Sudan, Velusamy (JACM 2024)", "Bessiere, Carbonnel, Katsirelos (AAAI 2020)"]
source: brain-ingest-local
---

# Charakterizace streamovací složitosti CSP pomocí ne-redundance

**URL**: http://arxiv.org/abs/2604.21922v1

## Key Idea

Článek kompletně charakterizuje paměťovou složitost jednoprůchodového streamování pro rozhodování splnitelnosti problémů omezujících podmínek (CSP) pomocí strukturálního parametru ne-redundance.

## Claims

- Jednoprůchodová streamovací složitost CSP(Γ) je charakterizována až na logaritmický faktor pomocí ne-redundance NRD_n(Γ)
- Pro k-SAT existuje optimální dolní mez paměťové složitosti Ω(n^k)
- Pro obecné CSP existuje dolní mez Ω(n) paměťové složitosti
- Ne-redundance je maximální počet omezení nad n proměnnými tak, že každé omezení C je ne-redundantní (existuje ohodnocení splňující všechna omezení kromě C)

## Relevance for STOPA

Výsledky o paměťově efektivním streamovacím zpracování složitých omezujících podmínek jsou relevantní pro optimalizaci orchestrace distribuovaných systémů, kde je třeba zpracovávat a vyhodnocovat omezení v reálném čase s minimálními paměťovými nároky.
