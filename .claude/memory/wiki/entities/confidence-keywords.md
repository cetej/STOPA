---
name: Confidence Keywords
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mbif-cpr-implementation-plan]
tags: [memory, session, retrieval]
---

# Confidence Keywords

> Dedikované klíčová slova v session logách / intermediate JSON artefaktech pro grep-based retrieval — rychlejší a přesnější než full-text search.

## Key Facts

- Původ v CPR systému: `Confidence keywords` pole v Quick Reference sekci session logu (ref: sources/mbif-cpr-implementation-plan.md)
- STOPA adaptace: `keywords` pole v intermediate JSON (3-8 slov: project names, technical terms, action verbs, framework names, ticket IDs) (ref: sources/mbif-cpr-implementation-plan.md)
- Extrakce Haiku sub-agentem při tvorbě summary — zero extra cost (rozšíří existující Haiku prompt) (ref: sources/mbif-cpr-implementation-plan.md)
- Přidávají se do checkpoint.md YAML frontmatter: `keywords: ["auth", "JWT", "migration"]` (ref: sources/mbif-cpr-implementation-plan.md)
- Rozšíření scratchpad.md: nový sloupec Keywords v tabulce (ref: sources/mbif-cpr-implementation-plan.md)
- Search pattern: `grep -l '"keywords".*auth' .claude/memory/intermediate/*.json` (ref: sources/mbif-cpr-implementation-plan.md)

## Relevance to STOPA

P2 priorita. Zlepší searchability intermediate artefaktů. Aditivní — nic se neruší. Logicky navazuje po implementaci truncation boundary.

## Mentioned In

- [MBIF/CPR Implementation Plan](../sources/mbif-cpr-implementation-plan.md)
