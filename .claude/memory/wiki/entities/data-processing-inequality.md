---
name: Data Processing Inequality
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [single-agent-vs-multi-agent-thinking-budget]
tags: [orchestration, information-theory, multi-agent]
---

# Data Processing Inequality

> Informačně-teoretický princip: každý mezičlánek v datovém řetězci nemůže zvýšit množství informace — může ji jen zachovat nebo ztratit.

## Key Facts

- Formálně: pro Markov chain X → Y → Z platí I(X;Z) ≤ I(X;Y) — agent zpracovávající filtrovanou zprávu nemá víc informace než agent s přístupem k plnému kontextu
- Tran & Kiela (arXiv:2604.02460) ji aplikují na MAS: každý agent-handoff je datový mezičlánek → MAS nevyhnutelně ztrácí informaci oproti SAS
- Výjimka: když single-agent context utilization selže (korupce, délka, šum) — pak MAS Debate může kompenzovat, protože dekompozice eliminuje "interference patterns" v přímém zpracování
- Praktická implikace: MAS je architektonicky podřazené SAS za rovných podmínek; superiority claim musí vždy kontrolovat compute budget (ref: sources/single-agent-vs-multi-agent-thinking-budget.md)

## Relevance to STOPA

STOPA multi-agent orchestration je zdůvodněno **paralelizací a specializací**, ne reasoning superiority — DPI potvrzuje, že multi-agent přínos je operační (souběžná práce, role separation), ne kognitivní.

## Mentioned In

- [Single-Agent LLMs vs Multi-Agent Systems Under Equal Thinking Token Budgets](../sources/single-agent-vs-multi-agent-thinking-budget.md)
