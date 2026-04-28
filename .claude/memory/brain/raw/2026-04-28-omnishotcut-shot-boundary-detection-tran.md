---
title: OmniShotCut: Detekce hranice záběrů pomocí transformeru a syntetických dat
url: http://arxiv.org/abs/2604.24762v1
date: 2026-04-28
concepts: ["Shot Boundary Detection", "video transformer", "relační predikce", "syntetická trénovací data", "intra-shot a inter-shot relace"]
entities: ["Boyang Wang", "Guangyi Xu", "Zhipeng Tang", "Jiahui Zhang", "Zezhou Cheng"]
source: brain-ingest-local
---

# OmniShotCut: Detekce hranice záběrů pomocí transformeru a syntetických dat

**URL**: http://arxiv.org/abs/2604.24762v1

## Key Idea

Nová metoda detekce hranic záběrů ve videu (SBD) založená na transformeru s dotazy na záběry, která formuluje problém jako strukturovanou relační predikci a využívá plně syntetickou pipeline pro vytváření anotací přechodů s přesnými hranicemi.

## Claims

- Existující SBD metody produkují neinterpretovatelné hranice na přechodech a přehlížejí jemné diskontinuity
- OmniShotCut formuluje SBD jako strukturovanou relační predikci, která společně odhaduje rozsahy záběrů s intra-shot a inter-shot relacemi
- Plně syntetická pipeline přechodů automaticky reprodukuje hlavní rodiny přechodů s přesnými hranicemi a parametrizovanými variantami

## Relevance for STOPA

Metoda strukturované relační predikce a využití syntetických dat pro přesné anotace by mohla inspirovat orchestraci multimodálních AI workflow, kde je třeba detekovat a analyzovat přechody a relace mezi částmi komplexních vstupů.
