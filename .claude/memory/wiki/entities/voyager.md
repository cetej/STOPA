---
name: Voyager (skill library)
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoalpha-stopa-research]
tags: [skill-design, memory, orchestration]
---

# Voyager (skill library)

> Wang et al. 2023 (arXiv:2305.16291) — lifelong learning agent v Minecraftu s auto-generováním, verifikací a ukládáním skills do skill library. První formální validace skill accumulation vzoru.

## Key Facts

- Lifelong skill accumulation: auto-generate, verify, store — iterativní rozšiřování skill library (ref: sources/egoalpha-stopa-research.md)
- STOPA skills/ + learnings/ + graduation pipeline jsou nejbližší produkční implementací Voyager vzoru
- Skills se generují z požadavků, verifikují exekucí, ukládají do library pro reuse

## Relevance to STOPA

Akademická validace STOPA skill accumulation designu. STOPA /skill-generator + /evolve + graduation pipeline odpovídá Voyager skill library. Voyager jako precedent pro confidence-based graduation (`uses >= 10` AND `confidence >= 0.8`).

## Mentioned In

- [EgoAlpha Prompt Techniques vs. STOPA](../sources/egoalpha-stopa-research.md)
