---
title: LaST-R1: Adaptivní fyzikální uvažování pro robotické manipulace
url: http://arxiv.org/abs/2604.28192v1
date: 2026-05-01
concepts: ["Vision-Language-Action modely", "latentní Chain-of-Thought", "Latent-to-Action Policy Optimization (LAPO)", "reinforcement learning pro robotiku", "adaptivní horizont uvažování", "fyzikální modelování světa"]
entities: ["Hao Chen", "Jiaming Liu", "Zhonghao Yan", "Pheng-Ann Heng", "LIBERO benchmark"]
source: brain-ingest-local
---

# LaST-R1: Adaptivní fyzikální uvažování pro robotické manipulace

**URL**: http://arxiv.org/abs/2604.28192v1

## Key Idea

LaST-R1 je framework pro Vision-Language-Action modely, který kombinuje latentní Chain-of-Thought uvažování nad fyzikální dynamikou s reinforcement learningem (LAPO algoritmus) pro optimalizaci jak procesu uvažování, tak samotných akcí robota.

## Claims

- LaST-R1 dosahuje 99,8% úspěšnosti na LIBERO benchmarku pouze s one-shot supervised warm-up
- LAPO post-training přináší až 44% zlepšení oproti počáteční politice v reálném světě
- Framework umožňuje dynamicky přizpůsobovat horizont uvažování podle složitosti prostředí
- Metoda funguje jak pro single-arm, tak dual-arm robotické nastavení

## Relevance for STOPA

LaST-R1 ukazuje architekturu pro integraci latentního uvažování s akcemi agentů, což je relevantní pro orchestraci autonomních systémů, kde je potřeba propojit plánování založené na porozumění fyzikálnímu světu s konkrétními výkonnými akcemi.
