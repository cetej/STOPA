---
name: Zep
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [agent-memory-problems]
tags: [memory, knowledge-graph, temporal]
---

# Zep

> Rasmussen et al. 2025 (arXiv:2501.13956) — graph-based memory pro LLM agenty s bi-temporálním modelem: každá hrana knowledge grafu má t_valid a t_invalid.

## Key Facts

- Bi-temporální model: t_valid/t_invalid per edge — nová informace invaliduje staré hrany (ref: sources/agent-memory-problems.md)
- 94.8% vs MemGPT 93.4% na DMR benchmarku
- Jediný systém s principiálním řešením temporal staleness přes graph edge invalidation
- Produkční nasazení dostupné

## Relevance to STOPA

STOPA `supersedes:` chains v learnings jsou analogií Zep edge invalidation — starší learning se přeskočí při retrieval. Zep bi-temporal vzor je silnější: každý fakt má explicitní platnost od-do. Potenciální upgrade pro STOPA learnings: přidat `valid_until:` field.

## Mentioned In

- [Agent Memory Problems Research](../sources/agent-memory-problems.md)
