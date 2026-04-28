---
title: World-R1: 3D konzistence v generování videa pomocí reinforcement learning
url: http://arxiv.org/abs/2604.24764v1
date: 2026-04-28
concepts: ["text-to-video generation", "3D konzistence", "reinforcement learning", "Flow-GRPO optimalizace", "world simulation", "video foundation models"]
entities: ["Weijie Wang", "Xiaoxuan He", "Bohan Zhuang", "Microsoft"]
source: brain-ingest-local
---

# World-R1: 3D konzistence v generování videa pomocí reinforcement learning

**URL**: http://arxiv.org/abs/2604.24764v1

## Key Idea

Framework pro zlepšení 3D konzistence v AI generovaných videích pomocí reinforcement learning s feedbackem z 3D modelů, bez nutnosti měnit architekturu základního modelu.

## Claims

- Existující video foundation modely trpí geometrickými nekonzistencemi navzdory dobré vizuální kvalitě
- World-R1 využívá reinforcement learning s feedbackem z pre-trénovaných 3D modelů k vynucení strukturální koherence
- Přístup významně zlepšuje 3D konzistenci při zachování původní vizuální kvality základního modelu
- Metoda nevyžaduje změny architektury a je škálovatelná

## Relevance for STOPA

Ukazuje, jak využít reinforcement learning s feedbackem z externích modelů k vylepšení výstupů foundation modelů – paradigma aplikovatelné na orchestraci a alignment multi-model systémů.
