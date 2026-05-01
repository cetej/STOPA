---
title: Latent Adversarial Detection: Detekce multi-turn útoků na LLM pomocí aktivací
url: http://arxiv.org/abs/2604.28129v1
date: 2026-05-01
concepts: ["prompt injection", "multi-turn attacks", "LLM activations", "adversarial restlessness", "residual stream", "trajectory features", "activation-level detection"]
entities: ["Prashant Kulkarni", "LMSYS-Chat-1M", "SafeDialBench"]
source: brain-ingest-local
---

# Latent Adversarial Detection: Detekce multi-turn útoků na LLM pomocí aktivací

**URL**: http://arxiv.org/abs/2604.28129v1

## Key Idea

Výzkum ukazuje, že multi-turn prompt injection útoky zanechávají měřitelnou stopu v aktivacích LLM – každá fáze útoku (budování důvěry, pivotování, eskalace) posouvá aktivace, což vytváří charakteristický signál nazvaný 'adversarial restlessness', který umožňuje detekci s 93,8% přesností.

## Claims

- Multi-turn útoky zanechávají aktivační stopu v residual stream modelu – celková délka trajektorie přesahuje běžné konverzace
- Pět skalárních trajectory features zvyšuje detekci z 76,2% na 93,8% na syntetických datech
- Detekční sondy jsou model-specifické a nepřenášejí se mezi architekturami (testováno na modelech 24B-70B)
- Tří-fázové turn-level labely (benign/pivoting/adversarial) jsou nezbytné – binární labely produkují 50-59% false positives
- Kombinované tří-zdrojové trénování dosahuje 89,4% detekce při 2,4% false positive rate

## Relevance for STOPA

Pro STOPA orchestraci je klíčové chápat, jak detekovat adversariální chování v multi-turn interakcích s LLM. Tento přístup založený na aktivacích by mohl doplnit text-level obrany při orchestraci agentů, kteří vedou delší konverzace.
