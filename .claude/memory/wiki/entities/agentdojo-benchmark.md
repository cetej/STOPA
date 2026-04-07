---
name: AgentDojo benchmark
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [agent-defense-frameworks]
tags: [security, benchmarks, prompt-injection]
---

# AgentDojo benchmark

> Standardní benchmark pro hodnocení LLM agent bezpečnosti (prompt injection, task alignment) — obsahuje Travel, Workspace, Banking, Slack domény.

## Key Facts

- Baseline ASR (Attack Success Rate): 47.69% bez obrany (ref: sources/agent-defense-frameworks.md)
- LlamaFirewall PromptGuard 2: redukce ASR o 57% na AgentDojo
- CaMeL: 77% task success s provable security (baseline 84%)
- TaskShield: ASR 2.07% na GPT-4o — nejlepší výsledek na benchmarku
- Kombinace LlamaFirewall PG+AC: ASR 1.75%

## Relevance to STOPA

Referenční benchmark pro porovnání efektivity security mechanismů. STOPA PostToolUse hook s LlamaFirewall by měl být testován na AgentDojo-style scénářích pro kalibraci false positive rate.

## Mentioned In

- [AI Agent Defense Frameworks Research](../sources/agent-defense-frameworks.md)
