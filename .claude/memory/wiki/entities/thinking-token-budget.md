---
name: Thinking Token Budget
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [single-agent-vs-multi-agent-thinking-budget]
tags: [orchestration, evaluation, compute-budget]
---

# Thinking Token Budget

> Metodologie pro fair srovnání SAS vs MAS: měří pouze intermediate reasoning tokeny (thinking tokens), nezapočítává prompty, kontext, nebo finální odpovědi.

## Key Facts

- Standardní benchmarky MAS zaměňují "lepší výkon" s "více compute" — multi-agent systémy přirozeně spotřebují více tokenů (N agentů × k tokenů), zatímco single-agent je omezeno na k tokenů
- Spravedlivé srovnání: SAS obdrží stejný thinking budget jako celý MAS (součet myšlení všech agentů)
- Testovaný rozsah: 100–10 000 thinking tokenů; plateau nastává kolem 1 000–2 000 tokenů
- Implementační úskalí: Gemini 2.5 API-based token accounting je nespolehlivé — je potřeba proxy měření
- Tran & Kiela (arXiv:2604.02460): SAS pod rovným budgetem konzistentně dosahuje SAS ≥ MAS (ref: sources/single-agent-vs-multi-agent-thinking-budget.md)

## Relevance to STOPA

Při porovnávání efektivity STOPA orchestration tierů je třeba měřit **celkové thinking tokeny** (součet přes všechny agenty), ne jen model calls — bez tohoto controllingu mohou být výsledky zavádějící.

## Mentioned In

- [Single-Agent LLMs vs Multi-Agent Systems Under Equal Thinking Token Budgets](../sources/single-agent-vs-multi-agent-thinking-budget.md)
