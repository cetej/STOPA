---
name: LlamaFirewall
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [agent-defense-frameworks]
tags: [security, prompt-injection, guardrails]
---

# LlamaFirewall

> Meta PurpleLlama projekt — open-source guardrail systém pro LLM agenty s vrstvená architekturou (PromptGuard 2 + CodeShield + AlignmentCheck). Pip instalovatelný, aktivně vyvíjen.

## Key Facts

- PromptGuard 2: BERT classifier (22M/86M params), latence 19–92 ms, AUC 0.98, Recall@1%FPR 97.5% (ref: sources/agent-defense-frameworks.md)
- CodeShield: Semgrep + regex, ~70 ms, 96% precision / 79% recall (CyberSecEval3) — nezávislý na LLM
- AlignmentCheck: LLM CoT auditor, 860–1490 ms, vyžaduje Together API + Llama 4 Maverick
- Kombinace PG+AC: ASR 1.75% z baseline — >90% redukce
- GitHub Issue #147 (open): false positive tuning při kombinaci scannerů

## Relevance to STOPA

PromptGuard 2 + CodeShield jsou okamžitě integrovatelné do STOPA PostToolUse hooku — latence je přijatelná, API je synchronní, nezávislé na Llama. AlignmentCheck vhodný pro selektivní async audit (ne každý tool call). ADOPT verdikt pro PG+CS.

## Mentioned In

- [AI Agent Defense Frameworks Research](../sources/agent-defense-frameworks.md)
