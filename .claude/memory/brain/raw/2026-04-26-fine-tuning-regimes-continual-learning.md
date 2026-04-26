---
title: Režimy dolaďování definují odlišné problémy kontinuálního učení
url: http://arxiv.org/abs/2604.21927v1
date: 2026-04-26
concepts: ["Kontinuální učení (continual learning)", "Fine-tuning režimy", "Zapomínání v neuronových sítích", "Projikovaná optimalizace", "Task-incremental learning"]
entities: ["Paul-Tiberiu Iordache", "Elena Burceanu"]
source: brain-ingest-local
---

# Režimy dolaďování definují odlišné problémy kontinuálního učení

**URL**: http://arxiv.org/abs/2604.21927v1

## Key Idea

Výběr trainovatelných parametrů (fine-tuning režim) zásadně mění problémy kontinuálního učení. Srovnání metod není invariantní napříč různými režimy dolaďování, což vyžaduje nové evaluační protokoly.

## Claims

- Režim dolaďování (definovaný podprostorem trainovatelných parametrů) je klíčová evaluační proměnná v kontinuálním učení
- Relativní pořadí metod kontinuálního učení (EWC, LwF, SI, GEM) se nemění konzistentně napříč různými režimy trainovatelných hloubek
- Hlubší adaptační režimy jsou spojeny s většími aktualizacemi parametrů, vyšším zapomínáním a silnější závislostí mezi nimi
- Srovnávací závěry v kontinuálním učení silně závisí na zvoleném režimu dolaďování

## Relevance for STOPA

Pro STOPA orchestraci je klíčové, že výběr trainovatelných parametrů při adaptaci modelů není neutrální volba, ale zásadně ovlivňuje schopnost systému učit se nové úlohy při zachování předchozích znalostí. Tento poznatek je kritický pro dlouhodobé nasazení adaptivních AI systémů.
