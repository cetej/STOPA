---
title: LoHo-Manip: Dlouhodobá robotická manipulace pomocí VLA plánování
url: http://arxiv.org/abs/2604.21924v1
date: 2026-04-26
concepts: ["Vision-Language-Action (VLA) politiky", "Dlouhodobé plánování úloh", "Vizuální stopy (visual trace)", "Progresivní plánování s pamětí", "Modularní robotická architektura", "Closed-loop replánování"]
entities: ["Isabella Liu", "An-Chieh Cheng", "Xiaolong Wang", "NVIDIA", "UC San Diego"]
source: brain-ingest-local
---

# LoHo-Manip: Dlouhodobá robotická manipulace pomocí VLA plánování

**URL**: http://arxiv.org/abs/2604.21924v1

## Key Idea

Framework pro dlouhodobé robotické manipulace kombinující vision-language-action (VLA) politiky s manažerem úloh, který využívá vizuální stopy a progresivní plánování pro rozklad složitých úloh na posloupnost jednodušších kroků.

## Claims

- LoHo-Manip dosahuje výrazně vyšší úspěšnosti v dlouhodobých manipulačních úlohách než běžné VLA politiky.
- Systém využívá vizuální stopy (2D trajektorie klíčových bodů) pro vedení exekučního modelu místo ukládání vizuální historie.
- Manažer úloh predikuje zbývající plán s explicitním rozdělením hotovo/zbývá, což umožňuje automatické pokračování při selhání bez ručně kódované recovery logiky.
- Framework prokazuje silnou robustnost a out-of-distribution generalizaci na reálném robotovi Franka i v simulacích.

## Relevance for STOPA

Relevantní pro STOPA orchestraci díky modularitě - oddělení plánování od exekuce, progresivní dekomponování komplexních úloh a closed-loop adaptaci podobné adaptivní orchestraci workflow s možností zotavení z chyb.
