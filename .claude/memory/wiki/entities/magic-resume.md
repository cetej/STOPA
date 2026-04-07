---
name: Magic Resume
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [magic-resume-research]
tags: [web]
---
# Magic Resume

> Open-source CV editor (4.5K stars) na TanStack Start + Zustand + Tiptap — produkt je menší klon Reactive-Resume, ale obsahuje přenositelné architektonické vzory.

## Key Facts

- Repo: https://github.com/JOYCEQL/magic-resume, Live: https://magicv.art
- Stack: TanStack Start + React 18 + Zustand + Tiptap 3
- Template Registry Pattern: `registry.ts` — přidání šablony = 1 objekt, 0 jiných změn (ref: sources/magic-resume-research.md)
- PDF Export: server-side Puppeteer + client-side html2pdf.js fallback; před exportem: strip animací, transform→zoom konverze, base64 images
- Three-Panel Workbench: side panel | edit panel | live preview, vše resizable přes `react-resizable-panels`
- Slabiny: 0 testů, dvě UI knihovny (Shadcn + HeroUI), SSR disabled

## Relevance to STOPA

Template Registry Pattern adoptovatelný v KARTOGRAF (map styles), GRAFIK (layers), NG-ROBOT (article templates). Three-Panel Workbench pro KARTOGRAF a MONITOR. PDF Export Pipeline pro KARTOGRAF.

## Mentioned In

- [Magic Resume — Rozbor a doporučení](../sources/magic-resume-research.md)
