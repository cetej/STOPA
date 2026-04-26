---
title: Dlouhohorizontová manipulace pomocí VLA plánování se stopami
url: http://arxiv.org/abs/2604.21924v1
date: 2026-04-26
concepts: ["Vision-Language-Action (VLA) politiky", "Dlouhohorizontová robotická manipulace", "Vizuální stopy jako trajektoriové prompty", "Rekurzivní plánování s progress-aware pamětí", "Implicitní uzavřená smyčka pro recovery"]
entities: ["Isabella Liu", "An-Chieh Cheng", "Xiaolong Wang", "Sifei Liu", "NVIDIA", "UC San Diego"]
source: brain-ingest-local
---

# Dlouhohorizontová manipulace pomocí VLA plánování se stopami

**URL**: http://arxiv.org/abs/2604.21924v1

## Key Idea

LoHo-Manip je modulární framework, který rozšiřuje krátkohorizontové VLA (vision-language-action) politiky na dlouhohorizontové úlohy pomocí dedikovaného task-management VLM, který předpovídá vizuální stopy (2D trajektorie klíčových bodů) pro navádění robota.

## Claims

- Decoupling task managera od executoru umožňuje efektivní škálování na dlouhohorizontové úlohy bez potřeby velkých vizuálních bufferů historie
- Předpovídání zbývajícího plánu v každém kroku vytváří implicitní uzavřenou smyčku, která umožňuje automatické pokračování a přeplánování bez ručně navržené recovery logiky
- Vizuální stopy (2D trajektorie klíčových bodů) poskytují kompaktní a efektivní způsob komunikace prostorových záměrů mezi managerem a executorem
- Framework dosahuje výrazného zlepšení v úspěšnosti dlouhohorizontových úloh, robustnosti a generalizaci na out-of-distribution scénáře v simulaci i na reálném robotu Franka

## Relevance for STOPA

Demonstruje modulární přístup k orchestraci složitých úloh s oddělením high-level plánování (task manager) od low-level exekuce (VLA executor), což je analogické k orchestraci AI agentů v STOPA. Vizuální stopy jako kompaktní komunikační mechanismus mohou inspirovat efektivní způsoby předávání kontextu mezi agenty.
