---
title: HERMES++: Unifikovaný model pro 3D porozumění a generování scén při autonomním řízení
url: http://arxiv.org/abs/2604.28196v1
date: 2026-05-01
concepts: ["driving world models", "3D scene understanding", "LLM reasoning", "BEV representation", "geometric prediction", "autonomous driving"]
entities: ["Xin Zhou", "Dingkang Liang", "Xiwu Chen", "Feiyang Tan", "Dingyuan Zhang", "Hengshuang Zhao", "Xiang Bai"]
source: brain-ingest-local
---

# HERMES++: Unifikovaný model pro 3D porozumění a generování scén při autonomním řízení

**URL**: http://arxiv.org/abs/2604.28196v1

## Key Idea

HERMES++ integruje 3D porozumění scénám a predikci budoucí geometrie do jediného frameworku, spojující silné stránky LLM pro reasoning s predikcí fyzikální evoluce prostředí pro autonomní řízení.

## Claims

- Stávající přístupy k driving world models se zaměřují převážně na generování budoucích scén, ale opomíjejí komplexní 3D porozumění scénám
- HERMES++ dosahuje silného výkonu a překonává specializované přístupy jak v predikci budoucích point cloudů, tak v úlohách 3D porozumění scénám
- Model využívá BEV reprezentaci pro konsolidaci multi-view prostorových informací do struktury kompatibilní s LLM a zavádí Current-to-Future Link pro propojení sémantického kontextu s geometrickou evolucí

## Relevance for STOPA

Demonstrovat unifikovaný přístup k propojení různých typů reasoning (sémantické vs. geometrické) může inspirovat STOPA orchestraci při koordinaci mezi různými AI agenty specializujícími se na odlišné aspekty komplexních úloh.
