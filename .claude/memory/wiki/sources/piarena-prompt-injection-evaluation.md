---
title: "PIArena: A Platform for Prompt Injection Evaluation"
slug: piarena-prompt-injection-evaluation
source_type: paper
url: "https://arxiv.org/abs/2604.08499"
date_ingested: 2026-04-11
date_published: "2026-04 (ACL 2026)"
entities_extracted: 5
claims_extracted: 6
---

# PIArena: A Platform for Prompt Injection Evaluation

> **TL;DR**: Unified prompt injection platform (ACL 2026, arXiv:2604.08499). Strategy-based adaptive attack defeats all 9 defenses at 86% ASR. Task-alignment attacks are fundamentally unsolvable by instruction-level detection (44-82% ASR, all defenses fail). Claude Sonnet 4.5 is most robust closed-source model (31% ASR). No defense achieves high utility AND low ASR simultaneously.

## Key Claims

1. Strategy-based adaptive attack (10 strategies + feedback refinement) achieves 86% ASR vs PISanitizer (best prevention) — `verified`
2. Task-alignment attacks defeat all 9 defenses: 44-82% ASR in knowledge corruption scenarios — `verified`
3. Claude Sonnet 4.5 is most robust closed-source model: 31% ASR vs direct attack (GPT-5 = 70%, Gemini 3 Pro = 83%) — `verified`
4. Robustness training ineffective: GPT-4o-mini robustness-trained achieves 76% ASR — `verified`
5. No defense achieves high utility AND low ASR simultaneously (PISanitizer: 99% utility/86% ASR; SecAlign++: 45% utility/21% ASR) — `argued`
6. Instruction-level detection fundamentally insufficient for task-alignment; content-level verification is the only mitigation — `argued`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [PIArena](../entities/piarena.md) | paper | new |
| [task-alignment attack](../entities/task-alignment-attack.md) | concept | new |
| [strategy-based adaptive attack](../entities/strategy-based-adaptive-attack.md) | concept | new |
| [defense-utility tradeoff](../entities/defense-utility-tradeoff.md) | concept | new |
| [content-level verification](../entities/content-level-verification.md) | concept | new |

## Relations

- strategy-based adaptive attack `defeats` PISanitizer — 86% ASR vs 11% for static direct attack
- task-alignment attack `defeats` prompt-injection defense — fundamental limit, all 9 defenses fail
- content-level verification `extends` prompt-injection defense — only viable mitigation for task-alignment
- defense-utility tradeoff `affects` SecAlign++ — 21% ASR but only 45% utility

## Cross-References

- Related learnings: [2026-04-05-agent-defense-frameworks](../learnings/2026-04-05-agent-defense-frameworks.md) — PromptGuard is one of the 9 PIArena defenses; adaptive attacks defeat it despite AUC 0.98 on static patterns
- Related wiki articles: [general-security-environment](../general-security-environment.md) — defense frameworks, PromptGuard ADOPT recommendation
- Contradictions: none — PromptGuard's 1.75% ASR in existing learning is for static attack types; PIArena adaptive results (86%) use different methodology
