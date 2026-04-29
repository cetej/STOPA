---
title: Pythia: Optimalizace servingu LLM pro multi-agentní architektury
url: http://arxiv.org/abs/2604.25899v1
date: 2026-04-29
concepts: ["multi-agentní architektury", "LLM serving", "optimalizace cache", "workflow sémantika", "prediktabilita agentů", "resource contention", "queuing delays"]
entities: ["Shan Yu", "Junyi Shu", "Harry Xu", "Xuanzhe Liu", "Xin Jin"]
source: brain-ingest-local
---

# Pythia: Optimalizace servingu LLM pro multi-agentní architektury

**URL**: http://arxiv.org/abs/2604.25899v1

## Key Idea

Pythia je serving systém pro LLM, který využívá sémantickou prediktabilitu multi-agentních workflow k optimalizaci výkonu pomocí zachycení struktury agentních úloh, čímž dosahuje vyšší propustnosti a nižší latence oproti současným řešením.

## Claims

- Současné LLM serving systémy neefektivně zpracovávají agentní workloady, protože je behandlují jako generický traffic
- Analýza produkčních dat odhalila nízkou hit rate prefix cache, vážnou resource contention z long-context requestů a významné queuing delays
- Pythia zachycuje workflow sémantiku přes jednoduché rozhraní a využívá ji k optimalizaci, což výrazně zlepšuje throughput a job completion time

## Relevance for STOPA

Přímo relevantní pro STOPA orchestraci - ukazuje jak využít strukturu multi-agentních workflow k optimalizaci resource managementu a schedulingu, což jsou klíčové aspekty orchestrace agentních systémů.
