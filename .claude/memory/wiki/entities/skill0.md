---
name: SKILL0 (progressive skill withdrawal)
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [egoalpha-stopa-research]
tags: [skill-design, orchestration, cost-optimization, context-engineering]
---

# SKILL0 (progressive skill withdrawal)

> arXiv:2604.02268 (2026) — progressive skill withdrawal: plná verze skillu při první invokaci, kondenzovaná verze při opakovaných voláních. +9.7% ALFWorld při redukci z 5-7K na 0.5K tokenů.

## Key Facts

- +9.7% ALFWorld s 0.5K vs. 5-7K tokenů — méně tokenů = lepší výkon (ref: sources/egoalpha-stopa-research.md)
- Validuje STOPA SKILL.compact.md a `effort: auto` v frontmatter
- Dynamic Curriculum: 1. invokace = plný SKILL.md, opakované invokace = SKILL.compact.md
- On-policy helpfulness scoring — navrhováno jako next step pro STOPA
- Compact variant zachovává circuit breakery a hard stops, odstraňuje step-by-step workflow

## Relevance to STOPA

Přímá akademická validace STOPA SKILL.compact.md designu. Potvrzuje, že `effort: auto` je správný přístup. Navrhovaný next step: přidat on-policy helpfulness scoring do compact variants.

## Mentioned In

- [EgoAlpha Prompt Techniques vs. STOPA](../sources/egoalpha-stopa-research.md)
