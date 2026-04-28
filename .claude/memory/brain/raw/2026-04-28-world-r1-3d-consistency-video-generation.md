---
title: World-R1: Posílení 3D konzistence v text-to-video modelech pomocí RL
url: http://arxiv.org/abs/2604.24764v1
date: 2026-04-28
concepts: ["text-to-video generování", "3D konzistence", "posilované učení (RL)", "Flow-GRPO", "world simulation", "video foundation models", "geometrická koherence"]
entities: ["Microsoft", "Weijie Wang", "Bohan Zhuang"]
source: brain-ingest-local
---

# World-R1: Posílení 3D konzistence v text-to-video modelech pomocí RL

**URL**: http://arxiv.org/abs/2604.24764v1

## Key Idea

World-R1 je framework využívající posilované učení (Flow-GRPO) k vylepšení 3D konzistence ve video generování bez změny architektury modelu, přičemž využívá feedback od předtrénovaných 3D modelů.

## Claims

- Existující video foundation modely trpí geometrickými nekonzistencemi navzdory kvalitní vizuální syntéze
- World-R1 zlepšuje 3D konzistenci pomocí RL bez změny architektury modelu, což umožňuje lepší škálovatelnost než metody s architektonickými úpravami
- Periodická oddělená tréninková strategie vyvažuje rigidní geometrickou konzistenci s dynamickou fluiditou scény

## Relevance for STOPA

Ukazuje aplikaci pokročilého RL (Flow-GRPO) pro vylepšení foundation modelů pomocí externí zpětné vazby, což je relevantní pro orchestraci evaluace a zlepšování AI modelů v STOPA systémech.
