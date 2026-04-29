---
title: RecursiveMAS: Rekurzivní multi-agentní systémy pro efektivnější spolupráci
url: http://arxiv.org/abs/2604.25917v1
date: 2026-04-29
concepts: ["rekurzivní multi-agentní systémy", "latentní prostor pro spolupráci agentů", "RecursiveLink modul", "inner-outer loop učení", "gradient-based credit assignment"]
entities: ["Xiyuan Yang", "James Zou", "Markus J. Buehler", "Cornell University"]
source: brain-ingest-local
---

# RecursiveMAS: Rekurzivní multi-agentní systémy pro efektivnější spolupráci

**URL**: http://arxiv.org/abs/2604.25917v1

## Key Idea

RecursiveMAS rozšiřuje princip rekurzivních výpočtů z jednotlivých modelů na celé multi-agentní systémy, kde agenti spolupracují v iterativních smyčkách přes latentní stavy namísto textové komunikace, což vede k vyšší efektivitě a přesnosti.

## Claims

- RecursiveMAS dosahuje průměrného zlepšení přesnosti o 8,3% oproti pokročilým baseline metodám
- Framework poskytuje 1,2×-2,4× zrychlení inference a snížení použití tokenů o 34,6%-75,6%
- RecursiveMAS je efektivnější než standardní textové MAS a udržuje stabilní gradienty během rekurzivního tréninku
- Systém úspěšně funguje pod 4 reprezentativními vzory spolupráce agentů napříč 9 benchmarky

## Relevance for STOPA

RecursiveMAS představuje nový přístup k orchestraci multi-agentních systémů využívající latentní prostor místo textové komunikace, což by mohlo inspirovat efektivnější architektury pro STOPA orchestraci s nižší latencí a spotřebou zdrojů.
