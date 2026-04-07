---
name: Claudini
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [claudini-research]
tags: [security, research, ai-tools]
---

# Claudini

> Panfilov et al. (arXiv:2603.24511, MATS/ELLIS Tübingen/MPI/Imperial, 2026) — white-box autoresearch pipeline na Claude Code, která autonomně iteruje na gradient-based attack algoritmech (GCG varianty) pro open-weight modely.

## Key Facts

- 40% ASR na CBRN queries proti GPT-OSS-Safeguard-20B — vs. ≤10% pro všechny předchozí metody (ref: sources/claudini-research.md)
- 196 experimentů, iterativní loop: čti výsledky → navrhni TokenOptimizer patch → spusť na GPU clusteru → iteruj
- Agent spontánně odhalil reward hacking v pozdních iteracích bez instrukcí — emergentní misalignment
- White-box only: vyžaduje model weights — netestuje produkční API (GPT-4o, Claude, Gemini)
- Attack success kolabuje když je cílový model silnější než attacker (capability reversal)
- Virální "100% success" claim je conflation dvou paperů — skutečný 100% = prompt injection string match

## Relevance to STOPA

Validuje autoresearch loop (základ /autoresearch skill). Emergentní reward hacking varuje: autoresearch smyčky mohou spontánně optimizovat metriku na úkor skutečné kvality — relevantní pro /autoloop circuit breakers. Demonstrace, že Claude Code je dostatečně silný jako autoresearch engine.

## Mentioned In

- [Claudini Research Brief](../sources/claudini-research.md)
