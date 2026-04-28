---
title: World-R1: Posílení 3D konzistence v generování videa pomocí RL
url: http://arxiv.org/abs/2604.24764v1
date: 2026-04-28
concepts: ["text-to-video generování", "reinforcement learning", "3D geometrická konzistence", "video foundation modely", "Flow-GRPO", "world simulation"]
entities: ["Weijie Wang", "Microsoft", "Bohan Zhuang"]
source: brain-ingest-local
---

# World-R1: Posílení 3D konzistence v generování videa pomocí RL

**URL**: http://arxiv.org/abs/2604.24764v1

## Key Idea

Framework využívající reinforcement learning k prosazení 3D geometrické konzistence ve video foundation modelech bez změny architektury, pomocí zpětné vazby z 3D modelů.

## Claims

- Existující video foundation modely často trpí geometrickými nekonzistencemi navzdory kvalitní vizuální syntéze.
- World-R1 využívá Flow-GRPO k optimalizaci s feedbackem z předtrénovaných 3D a vision-language modelů bez změny architektury.
- Periodická oddělená tréninková strategie vyvažuje rigidní geometrickou konzistenci s dynamickou plynulostí scén.
- Přístup významně zvyšuje 3D konzistenci při zachování původní vizuální kvality foundation modelu.

## Relevance for STOPA

Relevantní pro orchestraci multimodálních modelů v STOPA - ukazuje, jak lze kombinovat výstupy různých foundation modelů (3D, VLM) pro zlepšení konzistence bez přetrénování základních modelů.
