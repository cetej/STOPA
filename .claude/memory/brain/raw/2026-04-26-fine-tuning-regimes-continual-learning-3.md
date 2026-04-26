---
title: Režimy doladění definují odlišné problémy kontinuálního učení
url: http://arxiv.org/abs/2604.21927v1
date: 2026-04-26
concepts: ["continual learning", "fine-tuning režimy", "catastrophic forgetting", "task incremental learning", "trénovatelná hloubka", "projikovaná optimalizace"]
entities: ["Paul-Tiberiu Iordache", "Elena Burceanu"]
source: brain-ingest-local
---

# Režimy doladění definují odlišné problémy kontinuálního učení

**URL**: http://arxiv.org/abs/2604.21927v1

## Key Idea

Režim fine-tuningu (tj. která část parametrů modelu se trénuje) zásadně mění charakter problému kontinuálního učení. Srovnávání metod CL není invariantní vůči volbě trénovatelné hloubky modelu.

## Claims

- Změna trénovatelné hloubky modelu mění efektivní aktualizační signál pro učení nových úloh i zachování znalostí.
- Relativní pořadí výkonnosti metod kontinuálního učení (EWC, LwF, SI, GEM) se nemění konzistentně napříč různými režimy fine-tuningu.
- Hlubší adaptační režimy jsou spojeny s většími magnitudami aktualizací parametrů, vyšším zapomínáním a silnějším vztahem mezi těmito faktory.
- Srovnávací závěry v kontinuálním učení silně závisí na zvoleném režimu fine-tuningu, což vyžaduje režimově-specifické evaluační protokoly.

## Relevance for STOPA

Pro STOPA orchestraci je klíčové porozumění tomu, jak různé strategie adaptace modelů (částečný vs. plný fine-tuning) ovlivňují jejich schopnost učit se nové úlohy bez ztráty předchozích znalostí. Tato práce ukazuje, že volba trénovatelných parametrů není jen technický detail, ale zásadně mění chování systému.
