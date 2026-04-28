---
title: World-R1: Posílení 3D konzistence v text-to-video generování pomocí RL
url: http://arxiv.org/abs/2604.24764v1
date: 2026-04-28
concepts: ["text-to-video generování", "reinforcement learning", "3D konzistence", "Flow-GRPO", "geometrická koherence", "world simulation", "foundation modely"]
entities: ["Microsoft", "Weijie Wang", "Bohan Zhuang"]
source: brain-ingest-local
---

# World-R1: Posílení 3D konzistence v text-to-video generování pomocí RL

**URL**: http://arxiv.org/abs/2604.24764v1

## Key Idea

World-R1 je framework využívající reinforcement learning (konkrétně Flow-GRPO) k zlepšení 3D geometrické konzistence ve video generování, bez nutnosti měnit architekturu modelu. Využívá feedback z předtrénovaných 3D modelů k vynucení strukturální koherence.

## Claims

- Existující video modely často trpí geometrickými nekonzistencemi a klasické metody injektace 3D priorů jsou výpočetně náročné
- World-R1 pomocí Flow-GRPO optimalizuje model s feedbackem z 3D foundation modelů a VLM bez změny architektury
- Periodická oddělená tréninková strategie balancuje rigidní geometrickou konzistenci s dynamickou fluiditou scény
- Framework výrazně zvyšuje 3D konzistenci při zachování původní vizuální kvality foundation modelu

## Relevance for STOPA

World-R1 demonstruje použití reinforcement learningu pro alignování generativních modelů s komplexními omezeními (3D geometrie). Tento přístup může být relevantní pro orchestraci AI agentů v STOPA, kde je třeba alignovat chování podle složitých pravidel bez přetrénování celých modelů.
