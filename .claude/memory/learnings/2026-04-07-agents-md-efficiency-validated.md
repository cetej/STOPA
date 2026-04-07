---
date: 2026-04-07
type: best_practice
severity: high
component: orchestration
tags: [skill, memory, orchestration, documentation]
summary: Repo-level instrukční soubory (AGENTS.md / CLAUDE.md / skills) snižují runtime AI agenta o 28.64% a spotřebu output tokenů o 16.58% při zachování task completion. Empirická validace STOPA design philosophy.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.7
verify_check: "Glob('CLAUDE.md') → 1+ matches"
---

## AGENTS.md Effect on AI Coding Agent Efficiency

**Studie**: "On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents" (arXiv:2601.20404)
**Prezentováno**: JAWs workshop, ICSE 2026, April 12-18, Rio de Janeiro
**Dataset**: 10 repozitářů, 124 PR (Codex + Claude Code)

### Klíčové výsledky

| Metrika | Změna | Signifikance |
|---------|-------|--------------|
| Median runtime | -28.64% | Statisticky signifikantní |
| Output tokens | -16.58% | Statisticky signifikantní |
| Task completion | beze změny | Žádná ztráta kvality |

### Jak to funguje

Repo-level instrukční soubory dávají agentovi kontext o:
- Architektonická rozhodnutí a konvence
- Zakázané operace a anti-patterny
- Stack a dependency informace
- Test strategie a validační příkazy

Agent nepotřebuje explorovat → méně tool calls → nižší runtime a tokeny.

### Dopad na STOPA

STOPA CLAUDE.md, skills/, a .claude/rules/ soubory jsou přesně tento pattern.
Studie empiricky validuje, že:
1. CLAUDE.md v target projektech = přímý ROI (runtime + tokeny + bezpečnost)
2. Onboarding checklisty pro target projekty MUSÍ zahrnovat CLAUDE.md setup
3. Skills s preconditions/effects YAML jsou správný směr

### Aplikace

- Při sync do target projektů: ověř, že CLAUDE.md existuje a je aktuální
- Při `/orchestrate`: připomeň, že dobré CLAUDE.md snižuje agent runtime
- Při `/project-init`: CLAUDE.md je povinný artefakt, ne optional

**Why**: Empirická data z 124 PR study, nejde o teorii ale o měření.
**How to apply**: Udržuj CLAUDE.md v každém target projektu aktuální — je to přímý performance lever.
