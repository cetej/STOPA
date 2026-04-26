---
title: Long-Horizon Manipulation via Trace-Conditioned VLA Planning
url: http://arxiv.org/abs/2604.21924v1
date: 2026-04-26
concepts: ["Vision-Language-Action (VLA) politiky", "Vizuální stopy jako 2D trajektorie", "Receding-horizon plánování", "Progress-aware task decomposition", "Trace-conditioned execution", "Modulární architektura manager-executor"]
entities: ["Isabella Liu", "An-Chieh Cheng", "Xiaolong Wang", "Sifei Liu", "NVIDIA", "UC San Diego"]
source: brain-ingest-local
---

# Long-Horizon Manipulation via Trace-Conditioned VLA Planning

**URL**: http://arxiv.org/abs/2604.21924v1

## Key Idea

Framework LoHo-Manip pro dlouhodobé robotické manipulace kombinuje manažerský VLM model s exekučním VLA, přičemž používá vizuální stopy (2D trajektorie klíčových bodů) jako kompaktní prostorovou paměť pro návod robota.

## Claims

- Dlouhodobé manipulační úlohy jsou pro současné VLA politiky náročné kvůli vícekrokovosti a kumulativním chybám při exekuci.
- LoHo-Manip rozděluje rozhodování na manažerský VLM (predikce zbývajícího plánu) a exekuční VLA (lokální řízení podle vizuální stopy).
- Vizuální stopy jako 2D klíčové body poskytují kompaktní prostorovou paměť a umožňují automatické opakování a přeplánování bez explicitní recovery logiky.
- Predikce zbývajícího plánu v každém kroku vytváří implicitní zpětnou vazbu, kdy neúspěšné kroky přetrvávají v dalších výstupech.
- Experimentální výsledky v simulaci i na reálném robotovi Franka ukazují zlepšení v úspěšnosti dlouhodobých úloh a robustnosti vůči změnám prostředí.

## Relevance for STOPA

Koncept vizuálních stop jako kompaktní prostorové paměti a modulární architektura manager-executor jsou relevantní pro STOPA orchestraci multi-agentních systémů, kde podobné přístupy mohou sloužit k decomposici složitých úloh a koordinaci agentů.
