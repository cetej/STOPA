---
title: ATRS: Adaptivní přerozdělování trajektorií pro paralelní optimalizaci
url: http://arxiv.org/abs/2604.22715v1
date: 2026-04-27
concepts: ["paralelní optimalizace trajektorií", "ADMM (Alternating Direction Method of Multipliers)", "deep reinforcement learning", "multi-agent shared policy", "motion planning", "adaptivní rozdělování segmentů"]
entities: ["Jiajun Yu", "Guodong Liu", "Li Wang", "Pengxiang Zhou", "Wentao Liu", "Yin He", "Chao Xu", "Fei Gao", "Yanjun Cao", "IEEE Robotics and Automation Letters"]
source: brain-ingest-local
---

# ATRS: Adaptivní přerozdělování trajektorií pro paralelní optimalizaci

**URL**: http://arxiv.org/abs/2604.22715v1

## Key Idea

Framework ATRS využívá sdílenou neuronovou síť řízenou hlubokým reinforcement learningem k dynamickému přerozdělování segmentů trajektorie během paralelní ADMM optimalizace, čímž řeší stagnaci v silně omezených oblastech a zrychluje konvergenci.

## Claims

- ATRS redukuje počet iterací až o 26,0 % a výpočetní čas až o 19,1 % oproti fixním strukturám ADMM
- Framework dosahuje zero-shot generalizace do neznámých prostředí díky využití vnitřních stavů solveru místo geometrických rysů prostředí
- Systém umožňuje real-time onboard přeplánování s cyklem 35 ms bez degradace při přechodu ze simulace do reálného světa

## Relevance for STOPA

ATRS představuje adaptivní optimalizační framework s neuronovou politikou, který by mohl inspirovat orchestraci paralelních agentů v STOPA – zejména dynamické přerozdělování úkolů mezi agenty a učení se z interních stavů systému místo fixních pravidel.
