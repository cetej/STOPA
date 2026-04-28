---
title: DiffuSAM: Difuzní adaptace SAM2 pro medicínskou segmentaci bez promptů
url: http://arxiv.org/abs/2604.24719v1
date: 2026-04-28
concepts: ["Segment Anything Model (SAM2)", "difuzní modely", "medicínská segmentace obrazu", "few-shot learning", "source-free domain adaptation", "prompt-free segmentation"]
entities: ["Tal Grossman", "Noa Cahan", "Lev Ayzenberg", "Hayit Greenspan"]
source: brain-ingest-local
---

# DiffuSAM: Difuzní adaptace SAM2 pro medicínskou segmentaci bez promptů

**URL**: http://arxiv.org/abs/2604.24719v1

## Key Idea

DiffuSAM je difuzní adaptace SAM2, která umožňuje automatickou segmentaci medicínských snímků (CT, MRI) bez nutnosti uživatelských promptů, využívá lehkou difuzní prior pro generování embeddings kompatibilních s SAM2.

## Claims

- SAM a SAM2 dosahují silné výkonnosti při zero-shot segmentaci s prompty, ale jejich trénink na přírodních obrázcích omezuje přenos na medicínská data
- DiffuSAM syntetizuje embeddingy kompatibilní se SAM2 pomocí lehké difuzní prior z frozen SAM2 image features, eliminuje nutnost uživatelských promptů
- Difuzní prior je kondicionovaná na dříve segmentovaných řezech, což zajišťuje prostorovou konzistenci napříč volumy
- DiffuSAM dosahuje konkurenceschopné výkonnosti na BTCV a CHAOS datasetech pro CT a MRI v režimech SF-UDA a Few-Shot s efektivním tréninkem a inferencí

## Relevance for STOPA

Ukazuje pokročilou adaptaci foundation modelů (SAM2) pomocí difuzních technik pro specifické domény bez nutnosti promptů – relevantní pro orchestraci AI nástrojů v kontextech vyžadujících automatizaci a transfer learning.
