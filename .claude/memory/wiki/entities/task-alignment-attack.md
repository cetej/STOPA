---
name: task-alignment attack
type: concept
first_seen: 2026-04-11
last_updated: 2026-04-11
sources: [piarena-prompt-injection-evaluation]
tags: [security, prompt-injection, attack, defense-gap]
---

# Task-Alignment Attack

> A prompt injection scenario where the injected task semantically aligns with the legitimate target task, making instruction-level detection ineffective.

## Key Facts

- In RAG/QA: both target (answer from context) and injection (insert false info) use context — indistinguishable at instruction level (ref: sources/piarena-prompt-injection-evaluation.md)
- All 9 tested defenses fail: 44-82% ASR despite being active in knowledge corruption scenarios (ref: sources/piarena-prompt-injection-evaluation.md)
- Utility degrades from 91% baseline to 43-50% when defenses attempt to block task-aligned attacks (ref: sources/piarena-prompt-injection-evaluation.md)
- Content-level verification (fact-checking, grounding checks) is the only viable mitigation (ref: sources/piarena-prompt-injection-evaluation.md)
- Represents a qualitatively different threat class from explicit instruction injection (ref: sources/piarena-prompt-injection-evaluation.md)

## Relevance to STOPA

STOPA's current defense (system prompt: external content = untrusted, user confirmation) handles explicit injection but NOT task-alignment. Orchestrator agents doing RAG or summarization remain vulnerable to disinformation that bypasses instruction checks.

## Mentioned In

- [PIArena: Prompt Injection Evaluation Platform](../sources/piarena-prompt-injection-evaluation.md)
