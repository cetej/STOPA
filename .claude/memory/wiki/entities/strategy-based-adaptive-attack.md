---
name: strategy-based adaptive attack
type: concept
first_seen: 2026-04-11
last_updated: 2026-04-11
sources: [piarena-prompt-injection-evaluation]
tags: [security, prompt-injection, attack, adaptive]
---

# Strategy-Based Adaptive Attack

> A two-phase prompt injection attack using 10 rewriting strategies and feedback-driven refinement to adaptively defeat defenses.

## Key Facts

- Phase 1 — Candidate Generation: Attacker LLM rewrites injection into 10 strategies (Author's Note, System Update, etc.), generating N candidates per strategy (ref: sources/piarena-prompt-injection-evaluation.md)
- Phase 2 — Refinement: failed attempts trigger one of three paths: Stealth (detected → increase stealth), Imperativeness (ignored → increase urgency), General (analyze failure → adapt) (ref: sources/piarena-prompt-injection-evaluation.md)
- 99% ASR without defense; 86% ASR vs PISanitizer (best prevention); 2-8× higher ASR than static attacks (ref: sources/piarena-prompt-injection-evaluation.md)
- Defeats PromptGuard (one of the 9 evaluated defenses) despite its 97.5% Recall@1%FPR on static patterns (ref: sources/piarena-prompt-injection-evaluation.md)

## Relevance to STOPA

STOPA's content-sanitizer.py (regex + PromptGuard) uses static detection patterns — strategy-based adaptive attacks specifically exploit feedback to circumvent static rules. Static defenses need adaptive complement or behavioral constraints.

## Mentioned In

- [PIArena: Prompt Injection Evaluation Platform](../sources/piarena-prompt-injection-evaluation.md)
