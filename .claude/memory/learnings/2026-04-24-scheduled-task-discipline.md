---
date: 2026-04-24
type: anti_pattern
severity: high
component: orchestration
tags: [scheduled-tasks, autonomy, whitelist, execution-discipline, cross-project]
summary: "Scheduled/autonomous agenti opakovaně porušují dva pilíře disciplíny: (1) rozšiřují explicitní whitelisty o 'podobné' patterny (daily-rebalancer: 4× correction), (2) reportují 'should change X' místo skutečné exekuce (evolve-skills: 5 frustration + 2 correction). Pravidlo: v scheduled módu MATCH EXAKTNĚ whitelist a APLIKUJ změny — nikdy ne suggest-only."
source: user_correction
maturity: draft
confidence: 0.9
uses: 0
successful_uses: 0
harmful_uses: 0
verify_check: "manual"
skill_scope: [scheduled-tasks]
---

## Problém

Dva druhy selhání autonomních scheduled agentů (mimo hlavní CC session):

### Selhání 1: Expanze whitelistu

`daily-rebalancer` má explicitní whitelist 3 cest pro auto-commit:
- `.claude/memory/*.md` (hook-generated state)
- `.claude/memory/*.jsonl`
- `.claude/hooks/*-state.json`

Agent opakovaně přidal **další** cesty (source code, configs) s odůvodněním "vypadá to podobně hook-generated". User corrected 4× (2026-04-20 → 2026-04-24):

> **NEVER** auto-add other patterns — only the three above

### Selhání 2: Describe-only mode

`auto-evolve-skills` volá `scripts/evolve-skills.py`. Agent v promptu dostal "analyze session evidence and decide whether the skill file needs improvement". Místo toho, aby změny **aplikoval**, produkoval zprávy "measure this, change that". 5 frustration signálů + 2 corrections:

> You NEVER do the work yourself
> Don't "suggest" — just do it

## Root Cause

Autonomní scheduled kontext **není interaktivní session** — uživatel nemůže potvrdit. Agent tedy musí být:
1. **Striktnější** v dodržování pravidel (žádná "heuristická" expanze whitelistu)
2. **Agresívnější** v exekuci (pokud je v promptu "aplikuj", aplikuj — nenabízej)

Interaktivní Autonomy feedback říká "ptej se jen u destruktivních akcí". V scheduled módu se ale **nemůže** ptát. Default shift: v scheduled = aplikuj vše co není explicitně destruktivní (git reset, rm -rf, force push).

## Pravidla

### Pro scheduled-task SKILL.md autory
1. **Whitelist ≠ heuristika.** Pokud je v SKILL uvedeno "only these 3 patterns", agent nesmí přidat čtvrtý — i když je "hook-generated".
2. **Explicitní exekuční mandát.** SKILL musí říkat `APPLY changes, don't propose` pro modifikační kroky. Slova "suggest/propose/recommend" ve scheduled SKILL = anti-pattern.
3. **Fallback při nejistotě:** nikdy "asi by se hodilo přidat X" → raději **silent skip** s logem.

### Pro STOPA runtime
- `/improve` + scheduled sweep se nesmí přidávat do whitelistů jiných scheduled tasks bez explicitního povolení.
- Správa scheduled tasks mimo STOPA (`~/.claude/scheduled-tasks/`) je cross-project — oprava musí jít přímo do toho SKILL.md, ne do STOPA rules.

## Aplikace

Když edituješ scheduled-task SKILL.md:
- Hledej slova "suggest", "propose", "recommend", "consider" v krocích, které mění stav → nahraď imperativem ("apply", "commit", "write").
- Hledej whitelisty → zkontroluj že jsou uzavřené (nic jako "…and similar patterns").
- Přidej závěr: "If uncertain, skip silently and log — never expand scope."

## Evidence

- `corrections.jsonl` entries: 2026-04-20T10:20, 2026-04-21T12:09, 2026-04-22T10:50, 2026-04-24T08:19 (daily-rebalancer)
- `corrections.jsonl` entries: 2026-04-19T03:29, 2026-04-19T03:30, 2026-04-20T04:52, 2026-04-20T04:52, 2026-04-23T04:03, 2026-04-23T05:49 (evolve-skills frustration/corrections)
- Feedback memory: `feedback_autonomy.md`

## Related

- `feedback_autonomy.md` — user wants max autonomy + "just do it"
- `2026-04-08-descriptive-over-narrative-generative.md` — describe-vs-execute tension
