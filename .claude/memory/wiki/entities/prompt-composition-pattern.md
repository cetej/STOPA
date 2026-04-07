---
name: Prompt Composition Pattern
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [open-higgsfield-ai-patterns]
tags: [ui-architecture, media, generation, prompt-engineering, pattern]
---

# Prompt Composition Pattern

> Funkce překládá vizuální/technické parametry (kamera, objektiv, clona, ohnisko) do textového promptu pro generativní model — uživatel nastavuje parametry vizuálně, systém skládá prompt.

## Key Facts

- Open-Higgsfield-AI Cinema Studio: `buildNanoBananaPrompt()` skládá `"shot on a [camera], using a [lens] at [focal]mm, aperture [aperture], shallow depth of field, cinematic lighting, 8K resolution"`
- ScrollColumn picker: snap-to-center scroll s opacity/scale animací pro výběr parametrů — fyzické ovládání místo textového vstupu
- Vzor odděluje doménovou znalost (jaké prompt fragmenty fungují) od uživatelského vstupu (vizuální výběr)
- Analogie s CSS-in-JS: deklarativní parametry → imperativní výstup (ref: sources/open-higgsfield-ai-patterns.md)

## Relevance to STOPA

Aplikovatelné na GRAFIK (style/efekt parametry → prompt pro Qwen-Image-Layered), `/nano` (vizuální parametry místo raw prompt), `/klip` (kamera nastavení pro video generaci). Validuje směr `/prompt-evolve` — prompt je composable, ne monolitický string.

## Mentioned In

- [Open-Higgsfield-AI Patterns](../sources/open-higgsfield-ai-patterns.md)
