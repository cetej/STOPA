---
title: HERMES++: Unifikovaný model autonomního řízení pro 3D scénu
url: http://arxiv.org/abs/2604.28196v1
date: 2026-05-01
concepts: ["driving world model", "3D scene understanding", "future geometry prediction", "LLM reasoning", "BEV representation", "point cloud prediction", "autonomous driving"]
entities: ["Xin Zhou", "Dingkang Liang", "Xiwu Chen", "Hengshuang Zhao", "Xiang Bai"]
source: brain-ingest-local
---

# HERMES++: Unifikovaný model autonomního řízení pro 3D scénu

**URL**: http://arxiv.org/abs/2604.28196v1

## Key Idea

HERMES++ kombinuje porozumění 3D scénám a predikci budoucí geometrie do jednoho modelu autonomního řízení. Využívá LLM pro sémantické uvažování společně s predikcí fyzikální evoluce prostředí.

## Claims

- HERMES++ integruje 3D porozumění scénám a predikci budoucí geometrie v rámci jediného frameworku
- Model překonává specializované přístupy v obou úlohách: predikci point cloudů i 3D porozumění scénám
- Používá BEV reprezentaci pro konsolidaci multi-view prostorové informace kompatibilní s LLM
- Joint Geometric Optimization strategie kombinuje explicitní geometrická omezení s implicitní latentní regularizací

## Relevance for STOPA

Ukazuje směr unifikace různých AI schopností (LLM reasoning + fyzikální predikce) v jednom modelu, což je relevantní pro orchestraci heterogenních AI komponent v autonomních systémech.
