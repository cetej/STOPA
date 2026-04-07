---
name: Three-Panel Workbench
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [magic-resume-research]
tags: [web, planning]
---
# Three-Panel Workbench

> UX pattern: Side panel (navigace) | Edit panel (formuláře/editace) | Preview (live render) — všechny panely nezávisle resizable, obousměrný klik navigace mezi panely.

## Key Facts

- Implementace přes `react-resizable-panels` (6KB, stabilní, well-maintained)
- Obousměrný klik: klik v preview → zvýrazní editor, klik v editoru → scroll preview
- Framer Motion `Reorder.Item` s `dragListener={false}` + GripVertical handle pro DnD bez accidental drags (ref: sources/magic-resume-research.md)
- Aplikace: Magic Resume (templates | sections | preview)

## Relevance to STOPA

Adoptovatelný v KARTOGRAF (layers panel | properties | map preview), GRAFIK (layers | editor | canvas), MONITOR (sources | config | dashboard).

## Mentioned In

- [Magic Resume — Rozbor a doporučení](../sources/magic-resume-research.md)
