---
title: DV-World: Benchmark pro agenty datové vizualizace v reálném světě
url: http://arxiv.org/abs/2604.25914v1
date: 2026-04-29
concepts: ["benchmark pro AI agenty", "datová vizualizace", "tabulkové procesory", "cross-platform evoluce", "proaktivní alignment záměrů", "hybridní evaluace", "MLLM-as-a-Judge"]
entities: ["Jinxiang Meng", "Shaoping Huang", "Fangyu Lei", "arXiv"]
source: brain-ingest-local
---

# DV-World: Benchmark pro agenty datové vizualizace v reálném světě

**URL**: http://arxiv.org/abs/2604.25914v1

## Key Idea

DV-World je nový benchmark s 260 úlohami pro evaluaci AI agentů v datové vizualizaci napříč reálnými scénáři: práce v tabulkových procesorech, evoluce vizualizací a interakce s uživateli s nejasými požadavky.

## Claims

- Současné benchmarky trpí sandbox izolací, zaměřením pouze na tvorbu v jednom jazyce a předpokladem perfektních instrukcí
- DV-World obsahuje 260 úloh pokrývajících 3 domény: DV-Sheet (nativní manipulace s tabulkami), DV-Evolution (adaptace vizualizací) a DV-Interact (alignment s nejasými požadavky)
- State-of-the-art modely dosahují méně než 50% celkového výkonu na DV-World
- Hybridní evaluace kombinuje Table-value Alignment pro číselnou přesnost a MLLM-as-a-Judge pro sémantické hodnocení

## Relevance for STOPA

Benchmark ukazuje limity současných LLM v komplexních multi-krokových pracovních postupech s reálnými nástroji (tabulkové procesory, cross-platform konverze), což je relevantní pro design STOPA orchestrace vyžadující robustní práci s datovými nástroji a adaptaci na nejasné požadavky.
