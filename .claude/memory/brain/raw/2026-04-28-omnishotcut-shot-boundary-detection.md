---
title: OmniShotCut: Detekce hranic záběrů pomocí transformerů
url: http://arxiv.org/abs/2604.24762v1
date: 2026-04-28
concepts: ["Shot Boundary Detection", "Vision Transformer", "Relační predikce", "Syntetická generace přechodů", "Strukturovaná anotace videa"]
entities: ["Boyang Wang", "Guangyi Xu", "Zhipeng Tang", "Jiahui Zhang", "Zezhou Cheng"]
source: brain-ingest-local
---

# OmniShotCut: Detekce hranic záběrů pomocí transformerů

**URL**: http://arxiv.org/abs/2604.24762v1

## Key Idea

Nová metoda pro automatickou detekci přechodů mezi záběry ve videu pomocí transformer architektury založené na shot-query přístupu, která modeluje vztahy mezi záběry a dokáže detekovat i subtilní diskontinuity.

## Claims

- Existující metody SBD produkují neinterpretovatelné hranice přechodů a přehlížejí subtilní diskontinuity
- OmniShotCut formuluje SBD jako strukturovanou relační predikci, společně odhadující rozsahy záběrů s intra-shot a inter-shot vztahy
- Plně syntetický pipeline pro generaci přechodů umožňuje vyhnout se nepřesnému ručnímu labelování
- OmniShotCutBench představuje moderní benchmark pro holistické a diagnostické vyhodnocení

## Relevance for STOPA

Detekce hranic záběrů je klíčová pro segmentaci a pochopení struktury videa, což je relevantní pro orchestraci multimodálních agentů při práci s video obsahem a časovou synchronizací.
