---
name: FActScore
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoalpha-stopa-research]
tags: [verification, testing, research]
---

# FActScore

> Min et al. 2023 (arXiv:2305.14251) — evaluační framework dekomponující komplexní claimy na atomické části a ověřující každou nezávisle. Odhaluje chyby skryté v holistickém review.

## Key Facts

- Atomic decomposition odhalí chyby, které holistic review přehlédne (ref: sources/egoalpha-stopa-research.md)
- Každý atomický claim ověřen nezávisle — precizní lokalizace faktických chyb
- Aplikovatelné na STOPA /verify skill: nová fáze před main verification

## Relevance to STOPA

Identifikovaná mezera v STOPA /verify: dělá holistický check místo atomické dekompozice. Doporučení: přidat fázi "rozlož output na atomické claimy, ověř každý nezávisle" před main verification step.

## Mentioned In

- [EgoAlpha Prompt Techniques vs. STOPA](../sources/egoalpha-stopa-research.md)
