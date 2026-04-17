---
date: 2026-04-07
type: best_practice
severity: medium
component: general
tags: [ui-architecture, media, generation, pattern, dynamic-controls]
summary: "Model metadata jako single source of truth pro dynamické UI: jeden JSON soubor definuje inputy/limity/typy controls pro 200+ modelů, UI se generuje automaticky. Eliminuje O(N) komponent per model → O(1) generický formulář. Aplikovatelné na GRAFIK layery/efekty."
source: external_research
uses: 1
harmful_uses: 0
confidence: 0.85
successful_uses: 0
verify_check: "manual"
---

## Situace

Open-Higgsfield-AI (Next.js 14, 200+ AI modelů) řeší problém: jak vytvořit UI pro desítky modelů s různými parametry bez duplicitního kódu?

## Řešení: Model Metadata Pattern

1. **Jeden metadata soubor** (`models.js`, 261 KB) definuje pro každý model:
   - `inputs`: schéma parametrů (`type`, `enum`, `default`, `min`, `max`, `step`)
   - `imageField`: jak serializovat obrázky do API (`images_list` vs `image_url`)
   - `maxImages`: limit referenčních obrázků
   - `hasPrompt`, `showAr`, `showQualityBtn`: conditional UI flags

2. **Generický formulář** čte metadata aktuálního modelu → renderuje odpovídající controls
3. **Kaskádový update**: `selectModel(id)` → `getAspectRatiosForModel(id)` → update controls

## Prompt Composition (Cinema Studio)

Funkce `buildNanoBananaPrompt()` skládá prompt z vizuálních parametrů:
- Uživatel vybere kameru, objektiv, clonu (ScrollColumn picker se snap-to-center)
- Systém: `"shot on [camera], [lens] at [focal]mm, aperture [aperture], cinematic lighting"`
- Odděluje doménovou znalost od uživatelského vstupu

## Aplikace na STOPA projekty

- **GRAFIK**: layery a efekty jako metadata → dynamické property panely
- **`/nano`, `/klip`**: model switching bez duplicitního kódu, prompt composition z vizuálních parametrů
- **`/prompt-evolve`**: prompt je composable z fragmentů, ne monolitický string
