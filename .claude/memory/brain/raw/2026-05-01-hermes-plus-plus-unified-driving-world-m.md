---
title: HERMES++: Unifikovaný model světa pro autonomní řízení
url: http://arxiv.org/abs/2604.28196v1
date: 2026-05-01
concepts: ["autonomní řízení", "world model", "3D scene understanding", "BEV reprezentace", "LLM integrace", "geometrická predikce", "point cloud prediction"]
entities: ["Xin Zhou", "Dingkang Liang", "Xiwu Chen", "Hengshuang Zhao", "Xiang Bai", "ICCV 2025"]
source: brain-ingest-local
---

# HERMES++: Unifikovaný model světa pro autonomní řízení

**URL**: http://arxiv.org/abs/2604.28196v1

## Key Idea

HERMES++ kombinuje porozumění 3D scénám a predikci budoucí geometrie v jednom modelu pro autonomní řízení, integrující schopnosti velkých jazykových modelů s fyzikální simulací pomocí BEV reprezentace a geometrických optimalizací.

## Claims

- HERMES++ překonává specializované přístupy jak v predikci budoucích point cloudů, tak v úlohách porozumění 3D scénám
- Model integruje LLM pro reasoning s geometrickou predikcí pomocí BEV reprezentace kompatibilní s LLM
- Joint Geometric Optimization strategie sjednocuje explicitní geometrická omezení s implicitní latentní regularizací

## Relevance for STOPA

Ukazuje architekturu pro sjednocení heterogenních AI schopností (LLM reasoning + geometrická predikce) v jednom systému, což je relevantní pro orchestraci různých AI komponent v STOPA při řešení komplexních úloh vyžadujících více modů inference.
