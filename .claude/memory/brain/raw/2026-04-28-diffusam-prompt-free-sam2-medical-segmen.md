---
title: DiffuSAM: Difuzní adaptace SAM2 pro medicínskou segmentaci bez promptů
url: http://arxiv.org/abs/2604.24719v1
date: 2026-04-28
concepts: ["Segment Anything Model (SAM2)", "Diffusion models", "Source-Free Unsupervised Domain Adaptation", "Few-shot learning", "Prompt-free segmentation", "Medical image segmentation", "3D volumetric consistency"]
entities: ["Tal Grossman", "Noa Cahan", "Lev Ayzenberg", "Hayit Greenspan", "BTCV dataset", "CHAOS dataset"]
source: brain-ingest-local
---

# DiffuSAM: Difuzní adaptace SAM2 pro medicínskou segmentaci bez promptů

**URL**: http://arxiv.org/abs/2604.24719v1

## Key Idea

DiffuSAM je difuzní adaptace SAM2, která umožňuje přesnou segmentaci medicínských snímků bez nutnosti uživatelských promptů pomocí lehkého difuzního modelu generujícího embeddingy kompatibilní se SAM2.

## Claims

- DiffuSAM eliminuje potřebu uživatelských promptů pro SAM2 v medicínské segmentaci pomocí difuzního modelu generujícího masky
- Model dosahuje konkurenceschopných výsledků na BTCV a CHAOS datasetech v režimech Source-Free UDA a Few-Shot při efektivním trénování
- Difuzní prior je podmíněn předchozími segmentovanými řezy, což zajišťuje prostorovou konzistenci napříč 3D objemy
- Framework syntetizuje embeddingy kompatibilní se SAM2 z zmrazených SAM2 obrazových příznaků pomocí lehkého difuzního modelu

## Relevance for STOPA

Demonstrace adaptace velkých foundational modelů (SAM2) pro specifické domény bez fine-tuningu celého modelu, pomocí lehkých difuzních adaptérů – přístup relevantní pro efektivní orchestraci AI modelů v produkčních scénářích.
