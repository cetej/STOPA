---
title: ParaManager: Malý model jako orchestrátor agentů a nástrojů
url: https://arxiv.org/abs/2604.17009
date: 2026-04-27
concepts: ["multi-agent orchestration", "agent-as-tool paradigm", "parallel subtask decomposition", "protocol normalization", "reinforcement learning pro orchestraci", "lightweight orchestrator"]
entities: ["Wenzhen Yuan", "Wanli Ouyang", "Lei Bai"]
source: brain-ingest-local
---

# ParaManager: Malý model jako orchestrátor agentů a nástrojů

**URL**: https://arxiv.org/abs/2604.17009

## Key Idea

Výzkum představuje Agent-as-Tool paradigma, kde malý model (ParaManager) orchestruje jak agenty, tak nástroje jako jednotný action space, umožňující paralelní dekompozici úkolů a asynchronní exekuci s použitím SFT a RL tréninku.

## Claims

- Unifikace agentů a nástrojů do standardizovaného action space s normalizovanými protokoly snižuje komplexitu systému a zvyšuje rozšiřitelnost
- ParaManager dosahuje silné výkonnosti napříč benchmarky a robustní generalizaci na neviděné model pooly
- Dvoustupňový trénink (SFT s recovery mechanismy + RL) optimalizuje úspěšnost úkolů, protokolovou compliance, diverzitu a efektivitu

## Relevance for STOPA

Přímo relevantní pro STOPA orchestraci - představuje lightweight přístup k orchestraci heterogenních agentů a nástrojů přes unifikované rozhraní, s důrazem na paralelizaci a stavově-aware dekompozici úkolů.
