---
name: Letta sleep-time compute
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [idea-file-research]
tags: [memory, orchestration]
---

# Letta sleep-time compute

> Background memory consolidation spouštěná v idle periods — asynchronní syntéza atomických paměťových záznamů do strukturovaných znalostí bez blokování aktivní session.

## Key Facts

- Letta (MemGPT team): sleep-time compute jako alternativa k real-time memory update (ref: sources/idea-file-research.md)
- Implementuje fázi 2 (Consolidate) 3-fázového memory lifecycle: idle trigger → background consolidation → structured knowledge update (ref: sources/idea-file-research.md)
- Kontrastuje s EverMemOS Reflect fází — consolidation vs. cross-temporal pattern detection jsou odlišné operace (ref: sources/idea-file-research.md)

## Relevance to STOPA

Inspirace pro STOPA `/sweep` skill upgrade — spouštět konsolidaci jako sleep-time operaci mimo hlavní session. Aktuálně STOPA `/compile` je on-demand; sleep-time varianta by umožnila background knowledge compilation.

## Mentioned In

- [Idea File Research](../sources/idea-file-research.md)
