---
title: LoHo-Manip: Dlouhodobá robotická manipulace pomocí VLA plánování
url: http://arxiv.org/abs/2604.21924v1
date: 2026-04-26
concepts: ["Vision-Language-Action (VLA) politiky", "Dlouhodobé plánování úkolů", "Trace-conditioned execution", "Receding-horizon management", "Vizuální trajektorie jako prompt", "Implicitní zpětná vazba a přeplánování", "Modulární task management"]
entities: ["Isabella Liu", "An-Chieh Cheng", "Xiaolong Wang", "Sifei Liu", "NVIDIA", "UC San Diego"]
source: brain-ingest-local
---

# LoHo-Manip: Dlouhodobá robotická manipulace pomocí VLA plánování

**URL**: http://arxiv.org/abs/2604.21924v1

## Key Idea

Framework LoHo-Manip řeší dlouhodobé robotické úkoly kombinací vision-language-action politik s dedikovaným plánovacím modelem, který predikuje vizuální trajektorie a sekvence podúkolů pro robustní vykonávání komplexních instrukcí.

## Claims

- VLA politiky selhávají u dlouhodobých úkolů kvůli kumulativním chybám a potřebě multi-krokového uvažování
- Oddělení task managera od exekutora umožňuje škálování krátkých VLA politik na dlouhé horizonty
- Vizuální trajektorie (2D keypoint traces) jako prompt výrazně zlepšují lokální kontrolu a navigaci
- Predikce zbývajícího plánu v každém kroku vytváří implicitní closed-loop systém s automatickým přeplánováním
- Přístup dosahuje silných výsledků v simulaci i na reálném robotickém rameni Franka
- Systém vykazuje robustnost vůči chybám a lepší generalizaci na out-of-distribution scénáře

## Relevance for STOPA

Framework demonstruje modulární přístup k řízení komplexních úkolů s dekompozicí na plánování a exekuci, což je analogické STOPA orchestraci. Kombinace jazykové paměti (subtask sekvence) a vizuálních promptů (traces) ukazuje efektivní způsob, jak propojit high-level plánování s low-level prováděním agentů.
