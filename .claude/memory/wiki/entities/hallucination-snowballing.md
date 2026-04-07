---
name: Hallucination Snowballing
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [agent-memory-problems]
tags: [memory, failure-mode, fmp]
---

# Hallucination Snowballing

> Zhang et al. 2023 (arXiv:2305.13534) — mechanismus kde LLM po commitmentu k chybné odpovědi generuje další falešná tvrzení na její podporu místo korekce. Commitment bias v kontextu přebíjí sebekorekci.

## Key Facts

- ChatGPT identifikoval 67% vlastních chyb v izolaci, GPT-4 87% — ale oba je v kontextu propagovali dál (ref: sources/agent-memory-problems.md)
- Mechanismus: jakmile agent "commitne" k odpovědi, downstream generace ji konzistentně podporuje
- Žádný velký memory systém netrackuje epistemickou spolehlivost při zápisu

## Relevance to STOPA

Vysvětluje proč STOPA `harmful_uses:` counter a Reflexion verbální nota jsou klíčové. Agent může "vědět" že jeho learning je špatný — ale v kontextu ho dál aplikuje. Obrana: explicitní confidence decay a `supersedes:` chain při opravě chybného learningu.

## Mentioned In

- [Agent Memory Problems Research](../sources/agent-memory-problems.md)
