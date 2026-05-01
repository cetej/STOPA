---
title: GenWildSplat: Generalizovatelná 3D rekonstrukce z řídkých neomezených snímků
url: http://arxiv.org/abs/2604.28193v1
date: 2026-05-01
concepts: ["sparse-view 3D rekonstrukce", "3D Gaussian Splatting", "feed-forward inference", "curriculum learning", "appearance adaptation", "canonical space", "generalizace bez optimalizace"]
entities: ["Vinayak Gupta", "Chih-Hao Lin", "Shenlong Wang", "Anand Bhattad", "Jia-Bin Huang", "PhotoTourism", "MegaScenes"]
source: brain-ingest-local
---

# GenWildSplat: Generalizovatelná 3D rekonstrukce z řídkých neomezených snímků

**URL**: http://arxiv.org/abs/2604.28193v1

## Key Idea

GenWildSplat je feed-forward framework pro 3D rekonstrukci outdoor scén z řídkých, nepolohovaných internetových fotek bez nutnosti optimalizace pro každou scénu. Využívá naučené geometrické priory, adaptér pro osvětlení a sémantickou segmentaci pro zvládání přechodných objektů.

## Claims

- GenWildSplat nepotřebuje per-scene optimalizaci na rozdíl od existujících metod
- Dosahuje state-of-the-art výsledků ve feed-forward renderingu na PhotoTourism a MegaScenes benchmarku
- Framework zvládá různé podmínky osvětlení a přechodné okluze pomocí appearance adapteru a sémantické segmentace
- Umožňuje real-time inferenci bez test-time optimalizace

## Relevance for STOPA

GenWildSplat ukazuje pokrok v generalizovatelné 3D rekonstrukci bez náročné optimalizace. Pro STOPA orchestraci je relevantní jako příklad efektivního využití naučených priorů místo výpočetně náročného per-instance tuningu – analogie pro orchestraci agentů s předtrénovanými schopnostmi.
