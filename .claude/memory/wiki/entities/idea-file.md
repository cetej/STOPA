---
name: Idea File
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [idea-file-research]
tags: [documentation, planning, orchestration, memory]
---

# Idea File

> Markdown dokument popisující záměr (co postavit a proč), nikoli implementaci (jak). Agent si přečte záměr a postaví implementaci sám. Pojmenování od Andreje Karpathyho, 4. dubna 2026.

## Key Facts

- Definice: "sdílíme záměr v Markdownu, ne kód" — `llm-wiki.md` gist je první publikovaný idea file (ref: sources/idea-file-research.md)
- Předchůdci: autoresearch `program.md` (2026-03-06), AGENTS.md (2025-08), SKILL.md (2025-12) — všechny jsou instantiace téhož principu (ref: sources/idea-file-research.md)
- Karpathy explicitně: "you don't 'use it' directly, it's just a recipe/idea — give it to your agent" (ref: sources/idea-file-research.md)
- AWS Kiro implementuje 3-file spec format s event-driven hooks jako praktická varianta (ref: sources/idea-file-research.md)
- GitHub spec-kit: 4 spec soubory jako executable artifacts (ref: sources/idea-file-research.md)
- Kritika (Böckeler/martinfowler.com): agenti specifikace ignorují nebo over-interpretují; historická paralela s Model-Driven Development (ref: sources/idea-file-research.md)

## Relevance to STOPA

SKILL.md je STOPA implementace idea file principu — context engineering artifact popisující záměr a podmínky použití. CLAUDE.md je master idea file pro celý orchestrační systém. Tento koncept validuje STOPA architekturu jako "intent-first, not implementation-first".

## Mentioned In

- [Idea File Research](../sources/idea-file-research.md)
