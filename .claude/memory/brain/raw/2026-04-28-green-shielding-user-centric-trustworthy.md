---
title: Green Shielding: Uživatelsky zaměřený přístup k důvěryhodné AI
url: http://arxiv.org/abs/2604.24700v1
date: 2026-04-28
concepts: ["Green Shielding", "uživatelsky zaměřené testování AI", "CUE kritéria (Context, Utility, Elicitation)", "robustnost vůči běžným perturbacím", "lékařská diagnostika s LLM", "Pareto trade-offy v kvalitě výstupů"]
entities: ["Aaron J. Li", "Bin Yu", "HealthCareMagic-Diagnosis (HCM-Dx)"]
source: brain-ingest-local
---

# Green Shielding: Uživatelsky zaměřený přístup k důvěryhodné AI

**URL**: http://arxiv.org/abs/2604.24700v1

## Key Idea

Green Shielding je metodologie pro testování robustnosti AI modelů vůči běžným (ne-adversariálním) variacím v uživatelských dotazech. V lékařské diagnostice ukazuje, že drobné změny ve formulaci dotazu systematicky ovlivňují kvalitu odpovědí LLM podle klinicky relevantních dimenzí.

## Claims

- Existující red-teaming neřeší citlivost LLM na běžné, ne-adversariální variace v uživatelských dotazech
- Neutralizace dotazů (odstranění uživatelských faktorů při zachování klinického obsahu) zvyšuje věrohodnost a stručnost diferenciálních diagnóz, ale snižuje pokrytí kritických stavů
- Různé způsoby formulace dotazů vedou k systematickým posunům v klinicky relevantních vlastnostech výstupů LLM
- CUE kritéria (autentický kontext, reálná utilita, realistické variace) umožňují validní hodnocení AI v high-stakes doménách

## Relevance for STOPA

Ukazuje, že orchestrace AI by měla respektovat citlivost modelů na formulaci promptů. Pro STOPA je relevantní při návrhu rozhraní – i malé změny v tom, jak je dotaz předán agentovi, mohou systematicky měnit kvalitu odpovědi podél více dimenzí současně (přesnost vs. bezpečnost).
