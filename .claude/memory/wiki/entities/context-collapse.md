---
name: Context Collapse
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [ace-agentic-context-engineering]
tags: [memory, context-management, failure-mode]
---

# Context Collapse

> Selhání kde systém při aktualizaci kontextu radikálně ztratí informaci — konkrétně měřeno v Dynamic Cheatsheet: 18 282 → 122 tokenů v jednom kroku, accuracy klesla z 66.7% na 57.1% (pod no-adaptation baseline 63.7%).

## Key Facts

- Empiricky změřeno v Dynamic Cheatsheet na AppWorld benchmark (ref: sources/ace-agentic-context-engineering.md)
- Způsobuje pokles accuracy pod baseline — horší než žádná adaptace
- ACE prevence: append-only ADD, nikdy nepřepisovat existující entries
- Riziko nastává při "context rewrite" přístupu — přepsání = ztráta akumulované znalosti

## Relevance to STOPA

STOPA memory systém používá append-only vzor (nové learnings = nové soubory, ne přepis). `critical-patterns.md` je hand-curated — nesmí být přepsán automaticky. Varování: /compact skill musí zachovat strukturu, ne jen zkrátit.

## Mentioned In

- [ACE — Agentic Context Engineering](../sources/ace-agentic-context-engineering.md)
