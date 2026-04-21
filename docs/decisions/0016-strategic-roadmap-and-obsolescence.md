---
date: 2026-04-21
status: RESEARCH
component: general
tags: [strategy, roadmap, competitive-analysis, obsolescence]
---

# 0016 — Strategic Roadmap: Goals, Means, Competition, Obsolescence

## Context

Uživatel otevřel strategickou linku (2026-04-21) pro meta-agent systém STOPA a navazující projekty. Čtyři body, které je třeba systematicky rozpracovat:

1. **Schvalovací tření** — permission prompts pro hook-generated file writes brzdí autonomii. Cíl: "Jarvis-like" meta-agent systém se minimálním user-in-the-loop tření. → taktický, řeší se samostatně (todo queue).
2. **Cíle rozvoje** — definovat vektory růstu pro STOPA i všechny target projekty (NG-ROBOT, ADOBE-AUTOMAT, ZACHVEV, POLYBOT, MONITOR, GRAFIK, KARTOGRAF, DANE, BONANZA, ADVISORS). Predict / adapt / anticipate.
3. **Prostředky a benchmark** — nejen definovat cíle, ale i prostředky, průběžně testovat. Najít konkurenční meta-agent projekty (letta, mem0, ByteRover, Semaclaw, Karpathy LLM wiki, MemGPT, Sakana AI scientists, process-reward-agents). Srovnat, inspirovat se.
4. **Životnost / obsolescence** — kdy bude takový systém překonán rozvojem AI, a čím. Jak dlouho dává smysl investovat do současné architektury.

## Decision

Rozpracovat jako **strukturovaný proces, ne jedno sezení**:

**Fáze A — taktická úleva (teď)**
- Fix permission friction (bod 1). Samostatný todo/workflow.

**Fáze B — competitive mapping (další krok po A)**
- `/deepresearch` na meta-agent ekosystém. Kandidáti již identifikovaní v brain/wiki: byterover, corpus2skill, externalization, knowledge-compounding, process-reward-agents, semaclaw, persistent-identity, missing-knowledge-layer.
- Doplnit o letta, mem0, MemGPT, Sakana, Karpathy LLM wiki detail.
- Výstup: srovnávací tabulka (capability × projekt × zralost × overlap se STOPA).

**Fáze C — strategic council (po B)**
- `/council` session (4–5 perspektiv: architect, product, skeptik, futurolog, operations).
- Vstupy: B výstup + současný stav STOPA + 10 target projektů.
- Výstup: per-projekt vektory růstu + success criteria + explicitní obsolescence triggers.

**Fáze D — obsolescence estimate (po C)**
- Scenario analýza: jaký AI pokrok by STOPA overtakoval? (modely s native memory, OS-level agents, hosted meta-agent platformy).
- Horizon: Q3 2026, Q1 2027, H2 2027.
- Triggers pro pivot/sunset každé komponenty.

**Fáze E — continuous testing (průběžně)**
- Měřitelné KPI pro každý vektor růstu.
- Kvartální revize tohoto ADR (trigger: každý quarter nebo major AI release).

## Alternatives Considered

- **Jedno brainstorming sezení teď** — odmítnuto: bez mapy konkurence by se generovaly nápady ve vakuu. User sám v bodu 3 požaduje "hledat konkurenční projekty".
- **Automatizovat vše okamžitě** — odmítnuto: bez jasných success criteria (fáze C) by se automatizace točila v kruhu.
- **Pouze fix permissions a odložit zbytek** — odmítnuto: user explicitně požádal "poznamenej, ať se neztratí".

## Consequences

- **Průběžná priorita**: autonomie (Jarvis-like UX) je explicitně deklarovaný dlouhodobý cíl — každé design rozhodnutí by se mu mělo měřit.
- **Research backlog**: fáze B triggeruje `/deepresearch` minimálně 1× na meta-agent ekosystém, pravděpodobně víc iterací.
- **Follow-ups**:
  - [ ] Fáze A — permission fix (v tomto todo)
  - [ ] Fáze B — deepresearch competitive landscape
  - [ ] Fáze C — council session
  - [ ] Fáze D — obsolescence scenarios
  - [ ] Fáze E — KPI tracking setup
- **Revize**: kvartálně, nebo při major AI release (GPT-5, Claude 5, Gemini 3.5, OS-level agents launch).
