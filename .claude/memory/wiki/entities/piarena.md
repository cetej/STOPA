---
name: PIArena
type: paper
first_seen: 2026-04-11
last_updated: 2026-04-11
sources: [piarena-prompt-injection-evaluation]
tags: [security, prompt-injection, evaluation, benchmark]
---

# PIArena

> Unified evaluation platform for prompt injection attacks and defenses (ACL 2026).

## Key Facts

- Platform covering 9 defenses (4 prevention, 5 detection), 13 datasets, 1700 samples (ref: sources/piarena-prompt-injection-evaluation.md)
- Paper: arXiv:2604.08499, Geng, Yin, Wang, Chen, Jia (Virginia Tech + Penn State), ACL 2026 (ref: sources/piarena-prompt-injection-evaluation.md)
- Code: github.com/sleeepeer/PIArena — extensible plug-and-play attack/defense API (ref: sources/piarena-prompt-injection-evaluation.md)
- Introduced strategy-based adaptive attack achieving 86% ASR vs best prevention defense (ref: sources/piarena-prompt-injection-evaluation.md)
- Identified task-alignment as fundamental unsolved problem for all 9 evaluated defenses (ref: sources/piarena-prompt-injection-evaluation.md)
- Four modules: Benchmark (standardized format), Attack (plug-and-play), Defense (unified output), Evaluator (utility + ASR) (ref: sources/piarena-prompt-injection-evaluation.md)

## Relevance to STOPA

Provides the most comprehensive prompt injection benchmark to date. Task-alignment findings directly challenge STOPA's instruction-level defense assumptions — content-level verification gap identified in `/security-review`.

## Mentioned In

- [PIArena: Prompt Injection Evaluation Platform](../sources/piarena-prompt-injection-evaluation.md)
