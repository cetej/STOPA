---
name: defense-utility tradeoff
type: concept
first_seen: 2026-04-11
last_updated: 2026-04-11
sources: [piarena-prompt-injection-evaluation]
tags: [security, prompt-injection, defense, tradeoff]
---

# Defense-Utility Tradeoff

> The fundamental tension between injection defense strength and task utility preservation — no current defense achieves both simultaneously.

## Key Facts

- PISanitizer: 99% utility, 86% ASR vs adaptive attack (high utility, low security) (ref: sources/piarena-prompt-injection-evaluation.md)
- SecAlign++: 45-84% utility, 21% ASR (strong security, destroys utility) (ref: sources/piarena-prompt-injection-evaluation.md)
- PIGuard: 72% utility, 79% ASR (best balance, but still weak on security) (ref: sources/piarena-prompt-injection-evaluation.md)
- No tested defense escapes the tradeoff — it is a fundamental property, not an implementation gap (ref: sources/piarena-prompt-injection-evaluation.md)
- Robustness training (GPT-4o-mini) worsens both: 76% ASR AND likely lower utility than unmodified model (ref: sources/piarena-prompt-injection-evaluation.md)

## Relevance to STOPA

Informs hook configuration: STOPA should not expect a single defense layer to solve both utility and security. Layered architecture (regex + PromptGuard + user confirmation) is validated — each layer sacrifices some utility for security incrementally.

## Mentioned In

- [PIArena: Prompt Injection Evaluation Platform](../sources/piarena-prompt-injection-evaluation.md)
