---
name: COORDINATOR_MODE
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [claw-code-architecture]
tags: [orchestration, security, multi-agent]
---

# COORDINATOR_MODE

> Architektonický vzor z Claw Code / Claude Code kde koordinátor má přístup pouze k [Agent, SendMessage, TaskStop] — fyzicky nemůže číst/psát soubory ani spouštět shell.

## Key Facts

- Povolené tools: Agent, SendMessage, TaskStop — nic jiného (ref: sources/claw-code-architecture.md)
- System prompt obsahuje: "Do not rubber-stamp weak work"
- 4 fáze práce: Research → Synthesis → Implementation → Verification
- Nutí delegaci — odstraňuje antipattern kde orchestrátor dělá práci sám

## Relevance to STOPA

Přímá inspirace pro /orchestrate skill refaktoring. STOPA orchestrátor aktuálně má přístup ke všem tools — COORDINATOR_MODE vzor by odstranil antipattern "orchestrátor dělá práci místo delegace". Implementace: `allowed-tools: [Agent, Read, Grep, Glob, TodoWrite]` v SKILL.md frontmatter.

## Mentioned In

- [Claw Code — Architektonická analýza pro STOPA](../sources/claw-code-architecture.md)
