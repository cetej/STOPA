---
title: World-R1: Zlepšení 3D konzistence v generování videa pomocí RL
url: http://arxiv.org/abs/2604.24764v1
date: 2026-04-28
concepts: ["text-to-video generování", "reinforcement learning pro video syntézu", "3D geometrická konzistence", "Flow-GRPO optimalizace", "video foundation modely", "world simulation"]
entities: ["Weijie Wang", "Microsoft", "Bohan Zhuang"]
source: brain-ingest-local
---

# World-R1: Zlepšení 3D konzistence v generování videa pomocí RL

**URL**: http://arxiv.org/abs/2604.24764v1

## Key Idea

World-R1 je framework využívající reinforcement learning k vylepšení text-to-video modelů o 3D geometrickou konzistenci bez změny architektury, pouze pomocí zpětné vazby z předtrénovaných 3D modelů.

## Claims

- Existující video foundation modely trpí geometrickou nekonzistencí navzdory impresivní vizuální syntéze
- World-R1 dosahuje významného zlepšení 3D konzistence bez změny základní architektury modelu pomocí RL
- Periodická oddělená tréninková strategie umožňuje vyvážit rigidní geometrickou konzistenci s dynamikou scény
- Framework používá zpětnou vazbu z předtrénovaných 3D modelů a vision-language modelů k prosazení strukturální koherence

## Relevance for STOPA

Ukazuje pokročilé použití RL pro alignment videa s fyzikálními/geometrickými omezeními, což je relevantní pro orchestraci multi-modálních AI systémů vyžadujících konzistenci napříč modalitami.
