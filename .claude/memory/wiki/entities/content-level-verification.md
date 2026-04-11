---
name: content-level verification
type: concept
first_seen: 2026-04-11
last_updated: 2026-04-11
sources: [piarena-prompt-injection-evaluation]
tags: [security, prompt-injection, defense, verification]
---

# Content-Level Verification

> A defense approach that checks the truthfulness/grounding of generated content rather than detecting injected instructions — the only viable mitigation for task-alignment attacks.

## Key Facts

- Required when injection semantically aligns with target task — instruction detection cannot distinguish legitimate from malicious (ref: sources/piarena-prompt-injection-evaluation.md)
- Contrast with instruction-level detection (PromptGuard, PIGuard): detects presence of injected commands, not content quality (ref: sources/piarena-prompt-injection-evaluation.md)
- Examples: RAG grounding checks (does answer match source?), fact-verification against known ground truth (ref: sources/piarena-prompt-injection-evaluation.md)
- Not yet implemented in any of the 9 PIArena defenses — identified as open research problem (ref: sources/piarena-prompt-injection-evaluation.md)

## Relevance to STOPA

Gap in STOPA's current defense architecture. `/security-review` and `/verify` skills could add content-level checks for RAG/summarization pipelines — e.g., verify agent output is grounded in source documents rather than injected disinformation.

## Mentioned In

- [PIArena: Prompt Injection Evaluation Platform](../sources/piarena-prompt-injection-evaluation.md)
