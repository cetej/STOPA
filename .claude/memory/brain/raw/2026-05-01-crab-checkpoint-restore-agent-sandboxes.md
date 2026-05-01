---
title: Crab: Checkpoint/Restore runtime pro AI agenty s 87% redukcí trafficu
url: http://arxiv.org/abs/2604.28138v1
date: 2026-05-01
concepts: ["checkpoint/restore", "agent sandboxing", "eBPF monitoring", "semantics-aware recovery", "OS-level state tracking", "fault tolerance"]
entities: ["Tianyuan Wu", "Chaokun Chang", "Lunxi Cao", "Wei Gao", "Wei Wang"]
source: brain-ingest-local
---

# Crab: Checkpoint/Restore runtime pro AI agenty s 87% redukcí trafficu

**URL**: http://arxiv.org/abs/2604.28138v1

## Key Idea

Crab je runtime pro sandboxované AI agenty, který inteligentně rozhoduje o checkpointech na základě skutečných OS efektů jednotlivých akcí agenta pomocí eBPF monitoringu. Dosahuje 100% korektní recovery při 87% nižším checkpointovém trafficu.

## Claims

- Přes 75% akcí AI agentů neprodukuje žádný stav relevantní pro recovery
- Crab zvyšuje úspěšnost recovery z 8% (pouze chat history) na 100%
- Crab redukuje checkpoint traffic až o 87% oproti per-turn checkpointingu
- Overhead Crab runtime je pouze 1.9% oproti běhu bez fault tolerance

## Relevance for STOPA

Přímo relevantní pro STOPA orchestraci AI agentů - řeší fault tolerance a state management při paralelním běhu více agent sandboxů. eBPF-based monitoring je architektonicky kompatibilní s host-level orchestrací.
