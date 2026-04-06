---
date: 2026-04-06
type: anti_pattern
severity: high
component: skill
tags: [research, orchestration, deepresearch]
summary: "Researcher sub-agent s 30+ tool calls běží hodiny. Omezit na max 15 volání, široký scope rozdělit na víc menších agentů."
source: user_correction
uses: 0
harmful_uses: 0
confidence: 0.9
verify_check: manual
successful_uses: 0
---

## Problém

Deepresearch landscape agent dostal příliš široký scope (6+ metod k prozkoumání) a provedl 34 tool volání za ~4 hodiny. Uživatel byl pryč 1-2 hodiny a process stále běžel.

**Why:** Každý WebSearch + WebFetch pár trvá 30-120s. 34 volání = kumulativně hodiny, plus rate limiting a pomalé stránky.

**How to apply:**
- Max 15 tool volání per researcher agent
- Pokud scope vyžaduje víc: rozděl na 2-3 menší agenty (každý 8-12 volání)
- Pro landscape/survey: dej agentovi prioritizovaný seznam — "top 3 nejdůležitější, zbytek jen pokud zbývá budget"
- Vždy komunikuj uživateli odhadovanou dobu běhu při spuštění agentů
