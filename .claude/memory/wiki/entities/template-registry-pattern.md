---
name: Template Registry Pattern
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [magic-resume-research]
tags: [planning, code-quality]
---
# Template Registry Pattern

> Architektonický vzor: každá šablona je jeden objekt v centrálním `registry.ts` — přidání šablony = 1 soubor, 0 jiných změn. Implementuje Open-Closed princip.

## Key Facts

- Každý záznam obsahuje: typed config objekt (colorScheme, spacing, sections) + React komponenta
- Přidání nové šablony: jeden objekt v registry, žádné jiné změny
- Type-safe: config validován TypeScriptem při kompilaci
- Open-Closed princip: rozšiřitelné bez modifikace existujícího kódu (ref: sources/magic-resume-research.md)
- Implementace: `registry.ts` v magic-resume / Reactive-Resume

## Relevance to STOPA

Přenositelné do KARTOGRAF (registry map stylů), GRAFIK (registry vrstev), NG-ROBOT (registry šablon článků). STOPA skills mají podobný pattern, ale bez typed config objektů.

## Mentioned In

- [Magic Resume — Rozbor a doporučení](../sources/magic-resume-research.md)
