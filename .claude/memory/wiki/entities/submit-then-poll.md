---
name: Submit-Then-Poll Pattern
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [open-higgsfield-ai-patterns]
tags: [async, api-pattern, media, generation]
---

# Submit-Then-Poll Pattern

> Async generační vzor: odešli request → obdrž requestId → polluj status každých N sekund → vrať výsledek při completed/failed.

## Key Facts

- Open-Higgsfield-AI: `pollForResult(requestId, key, maxAttempts=900, interval=2000)` — 2s interval, max 30 min pro video, 2 min pro obrázky
- Status stavy: `pending` → `processing` → `completed`/`succeeded`/`failed`
- Univerzální pattern nezávislý na backendu (Muapi.ai, fal.ai, Replicate, RunPod — všechny ho používají)
- Konfigurovatelné timeouty per task type, ne globální (ref: sources/open-higgsfield-ai-patterns.md)

## Relevance to STOPA

STOPA `/nano` a `/klip` již tento vzor implementují přes fal.ai. Vzor je validovaný — pokud se přidá nový backend, stačí adaptovat requestId format a status mapping.

## Mentioned In

- [Open-Higgsfield-AI Patterns](../sources/open-higgsfield-ai-patterns.md)
