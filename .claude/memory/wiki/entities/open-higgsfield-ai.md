---
name: Open Higgsfield AI
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [open-higgsfield-ai-patterns]
tags: [media, generation, open-source, next-js]
---

# Open Higgsfield AI

> Open-source klon Higgsfield AI — Next.js 14 monorepo s 4 generativními studii (Image, Video, Lip Sync, Cinema), 200+ modelů přes Muapi.ai gateway.

## Key Facts

- Stack: Next.js 14 (App Router), React 18, Tailwind CSS v3, npm workspaces monorepo, Electron desktop
- 4 studia: Image (50+ T2I, 55+ I2I), Video (40+ T2V, 60+ I2V), Lip Sync (9 modelů), Cinema (virtuální kamera)
- Architektura: lokální stav per studio, sdílená logika v `packages/studio`, model metadata jako single source of truth
- Electron wrapper: < 50 řádků, `webSecurity: false` pro API calls z `file://`, statický Next.js export
- Licence: MIT (ref: sources/open-higgsfield-ai-patterns.md)

## Relevance to STOPA

Referenční implementace pro GRAFIK (image editor) a budoucí video editor — monorepo struktura, model metadata pattern, prompt composition, Cinema Studio UI vzory.

## Mentioned In

- [Open-Higgsfield-AI Patterns](../sources/open-higgsfield-ai-patterns.md)
