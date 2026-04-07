---
title: "Magic Resume — Rozbor a doporučení"
slug: magic-resume-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 8
claims_extracted: 4
---
# Magic Resume — Rozbor a doporučení

> **TL;DR**: Magic Resume (4.5K stars) je open-source CV editor na TanStack Start + Zustand + Tiptap. Samotný produkt je menší klon Reactive-Resume, ale obsahuje přenositelné architektonické vzory: Template Registry Pattern, Three-Panel Workbench UX a PDF Export Pipeline s CSS strippingem.

## Key Claims

1. Template Registry Pattern (jeden objekt v registry.ts = nová šablona) implementuje Open-Closed princip — přidání šablony nevyžaduje změnu žádného jiného souboru — `[verified]`
2. Zustand partialize + custom merge umožňuje rekonstruovat derived state při rehydrataci bez ukládání computed hodnot — `[verified]`
3. PDF export vyžaduje před Puppeteer renderingem: strip animací, konverzi transform→zoom, inline base64 images — jinak Puppeteer špatně počítá pagination — `[verified]`
4. Reactive-Resume (36K stars, podobný stack) je de facto standard v open-source resume builder prostoru — Magic Resume je menší klon s méně features — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Magic Resume | tool | new |
| Reactive-Resume | tool | new |
| TanStack Start | tool | new |
| Zustand | tool | new |
| Tiptap | tool | new |
| Template Registry Pattern | concept | new |
| Three-Panel Workbench | concept | new |
| react-resizable-panels | tool | new |

## Relations

- Magic Resume `built-on` TanStack Start
- Magic Resume `uses` Zustand
- Magic Resume `uses` Tiptap
- Magic Resume `clone-of` Reactive-Resume
- Template Registry Pattern `implements` Open-Closed Principle
- Three-Panel Workbench `uses` react-resizable-panels
