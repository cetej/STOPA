---
title: TSN-Affinity: Kontinuální offline RL pomocí podobnostně řízené reuse parametrů
url: http://arxiv.org/abs/2604.25898v1
date: 2026-04-29
concepts: ["continual offline reinforcement learning", "catastrophic forgetting", "task-specific parameterization", "similarity-driven routing", "architectural continual learning", "TinySubNetworks", "Decision Transformer"]
entities: ["Dominik Żurek", "Kamil Faber", "Marcin Pietron", "Paweł Gajewski", "Roberto Corizzo"]
source: brain-ingest-local
---

# TSN-Affinity: Kontinuální offline RL pomocí podobnostně řízené reuse parametrů

**URL**: http://arxiv.org/abs/2604.25898v1

## Key Idea

Nová metoda pro kontinuální offline reinforcement learning, která používá architekturu TinySubNetworks a Decision Transformer s routing strategií založenou na podobnosti akcí a latentních reprezentací, bez potřeby replay bufferů.

## Claims

- TSN-Affinity dosahuje silné retence znalostí pomocí řídkých SubNetworks bez potřeby replay bufferů
- Routing založený na podobnosti akcí a latentních reprezentací zlepšuje multi-task výkon
- Architektury založené na podobnostně řízené reuse jsou životaschopnou alternativou k replay-based strategiím v CORL
- Metoda byla úspěšně evaluována na Atari hrách i simulacích robotické manipulace s Franka Emika Panda (diskrétní i spojité řízení)

## Relevance for STOPA

Kontinuální učení bez zapomínání je klíčové pro dlouhodobou orchestraci AI agentů. Podobnostně řízená reuse parametrů by mohla inspirovat efektivnější způsoby sdílení znalostí mezi agenty v STOPA ekosystému.
