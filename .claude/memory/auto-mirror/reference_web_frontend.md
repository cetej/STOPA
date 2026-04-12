---
name: reference_web_frontend
description: Foundational web/frontend libraries and concepts worth using when building web UIs and frontends
type: reference
---

Referenční knihovna zajímavých frontend technologií a konceptů pro budoucí webové projekty.

## Text Layout

### Pretext
- **Repo:** github.com/chenglou/pretext
- **Install:** `npm install @chenglou/pretext`
- **Verze:** 0.0.3 (vydáno 2026-03-29)
- **Autor:** Cheng Lou (@_chenglou — React core team alumnus, nyní Midjourney)
- **Citát autora:** *"Text layout & measurement was the last & biggest bottleneck for unlocking much more interesting UIs, especially in the age of AI. With this solved, no longer do we have to choose between the flashiness of a GL landing page, vs the practicality of a blog article."*

#### Co dělá
Pure TypeScript text measurement a layout **bez DOM reflow**. Dva fáze:
- `prepare(text, font)` — analýza + měření přes canvas `measureText` (~19ms/500 textů, one-time)
- `layout(prepared, maxWidth, lineHeight)` — čistá aritmetika na cachovaných datech (~0.09ms/500 textů, hot path)

460× rychlejší než interleaved DOM measurements.

#### API (zjednodušeno)
```typescript
// Use-case 1: výška textu bez DOM
prepare(text, font, opts?) → PreparedText
layout(prepared, maxWidth, lineHeight) → { height, lineCount }

// Use-case 2: přesný layout po řádcích
prepareWithSegments(text, font, opts?) → PreparedTextWithSegments
layoutWithLines(prepared, maxWidth, lineHeight) → { lines: LayoutLine[], height, lineCount }
layoutNextLine(prepared, cursor, maxWidth) → LayoutLine | null  // text obtékající překážky
walkLineRanges(prepared, maxWidth, onLine) → number             // geometry-only pass
```

#### Demos (živé)
- **Masonry** — stovky tisíc textových boxů, různé výšky, 120fps bez DOM, `chenglou.me/pretext/masonry/`
- **Bubbles** — shrinkwrapped chat bubliny, `chenglou.me/pretext/bubbles/`
- **Dynamic Layout** — responzivní magazínový layout s obtékáním obrázků, `chenglou.me/pretext/dynamic-layout`
- **Variable ASCII** — variable font ASCII art, `chenglou.me/pretext/variable-typographic-ascii`

#### Technická implementace
- Segmentace přes `Intl.Segmenter` (respektuje locale — CJK, Arab, Thai...)
- Bidi support (RTL text) — `segLevels: Int8Array` pro custom rendering
- Emoji korekce (Chrome/Firefox nafukují emoji width na macOS <24px — auto-detekce)
- Engine profiles per browser (Chrome vs Safari lineFitEpsilon, prefix width preference)
- 7,680/7,680 testů passing across Chrome/Safari/Firefox

#### Kdy použít
- **Map labeling** (KARTOGRAF) — přesné umístění bez reflow, WebGL-ready via OffscreenCanvas
- **Hustý dashboard** (MONITOR) — news feed, tabulky bez janku
- **Chat UI** (Záchvěv web) — shrinkwrapped bubliny
- **Jakýkoli web** kde text layout je bottleneck nebo potřebuješ přesnou kontrolu nad layoutem

#### Omezení
- `system-ui` font nespolehlivý na macOS (canvas vs DOM různé optical variants)
- Žádná automatická dělení slov (jen soft hyphens `\u00AD`)
- Zatím jen browser (OffscreenCanvas nebo DOM canvas) — SSR plánováno
