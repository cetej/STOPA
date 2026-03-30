---
date: 2026-03-26
type: architecture
severity: high
component: memory
tags: [autodream, dream, memory-consolidation, coexistence, cc-native]
summary: "AutoDream (/dream) coexists with STOPA memory: dream=janitor (cleanup), scribe=architect (structured writes). Protect YAML frontmatter."
source: auto_pattern
---

# AutoDream (`/dream`) — koexistence s STOPA memory systémem

## Zjištění

CC v2.1.81+ má nativní AutoDream: background subagent se 4 fázemi (Orient, Gather Signal, Consolidate, Prune+Index). Trigger: 24h + 5 sessions. Feature flag: `tengu_onyx_plover`.

## Rizika pro STOPA

1. Dream může smazat archive soubory (považuje za stale) → STOPA pravidlo "nikdy nemazat historii"
2. Dream nemá YAML frontmatter support → může zničit grep-first retrieval strukturu v learnings/
3. Dream dělá nepravdivé sumarizace bez ověření (issue #38493)
4. Žádný log změn → nemožné auditovat co dream udělal

## Ochranná opatření (implementováno 2026-03-26)

- HTML komentář na začátku MEMORY.md instruující dream: nemazat learnings/, archive soubory, zachovat YAML frontmatter
- Rozhodnutí zaznamenáno v decisions.md

## Eskalační plán

Pokud dream rozbíjí STOPA formát → `"autoDreamEnabled": false` v settings.json.
Future: FileChanged hook na `.claude/memory/` pro post-dream validaci.
