---
name: Model Metadata Dynamic UI
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [open-higgsfield-ai-patterns]
tags: [ui-architecture, media, generation, pattern]
---

# Model Metadata Dynamic UI

> Vzor kde jeden metadata soubor definuje všechny parametry modelu (inputy, limity, typy controls) a UI se z něj generuje automaticky — žádné hardcoded formuláře per model.

## Key Facts

- Open-Higgsfield-AI: `models.js` (261 KB) obsahuje 200+ modelů, každý s `inputs` schématem (`type`, `enum`, `default`, `min`, `max`, `step`)
- UI controls se renderují podmíněně přes `showX` booleany odvozené z aktuálního modelu
- Kaskádový update: výběr modelu → `getAspectRatiosForModel(id)` → update controls → re-render
- `imageField` v metadata řídí serializaci do API (single image vs array) bez větvení kódu
- Vzor eliminuje O(N) komponent per model → O(1) generický formulář + O(N) metadata (ref: sources/open-higgsfield-ai-patterns.md)

## Relevance to STOPA

Přímo aplikovatelné na **GRAFIK** (layerový editor): efekty a transformace jako metadata → dynamické UI panely. Také relevantní pro `/nano` a `/klip` — model switching bez duplicitního kódu.

## Mentioned In

- [Open-Higgsfield-AI Patterns](../sources/open-higgsfield-ai-patterns.md)
