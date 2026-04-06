---
date: 2026-03-24
type: best_practice
severity: high
component: orchestration
tags: [agent-identity, memory-hygiene, scheduled-maintenance, budget, browser]
summary: "OpenClaw $12K burn postmortem: 5 agent degradation patterns — identity collapse, memory bloat, budget blindness, browser loops, session amnesia."
source: external_research
uses: 1
confidence: 0.8
verify_check: "manual"
---

## Problém

OpenClaw postmortem ($12,229 API burn za 30 dní) odhalil 5 vzorů degradace autonomních agentů:
1. Browser Relay (live Chrome) nespolehlivý v produkci — stovky zombie tabů, random failures
2. Agent identity bloat — jeden agent s mnoha rolemi tiše degraduje kvalitu
3. Memory/session bloat — dead sessions a nestrukturovaná paměť žerou tokeny
4. Žádná viditelnost = stuck agenti burning budget bez povšimnutí
5. Ad-hoc prompty místo Skills = re-discovery overhead při každém cron runu

## Root Cause

Absence maintenance discipline. Autonomní agenti negenerují odpady viditelně — degradace je postupná a těžko pozorovatelná, dokud kvalita nespadne nebo nepřijde účet.

## Řešení

- **Playwright > live Chrome** — stabilní, cron-friendly (STOPA už má v /browse)
- **1 agent = 1 role** — dedikovaný SOUL.md/SKILL.md (STOPA spawn template má Goal+Role)
- **Scheduled memory maintenance** — nightly/weekly cleanup místo manuálního /scribe maintenance
- **Explicit skill reference v cron** — vždy říct "použij skill X", agent ho nenajde sám
- **Circuit breakers** — loop detection, budget limits (STOPA už má)

## Prevence

- Zavést scheduled task pro memory maintenance (weekly)
- V /harness a scheduled tasks vždy explicitně referencovat skill name
- Při scaling na 3+ agentů zajistit visibility (TaskList, mission control)
