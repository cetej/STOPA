---
date: 2026-04-15
type: architecture
severity: medium
component: general
tags: [self-improvement, training, distillation, repair-loop]
summary: "SD-ZERO: self-revision turns binary rewards into dense token-level supervision. Model plays dual roles (generator + reviser). Reviser concentrates corrections on error tokens (self-localization). Phase 1 trains revision ability, Phase 2 distills reviser knowledge back into generator. +10.5% on Qwen3-4B, -50% response length. Directly applicable to repair loops and critic patterns."
source: external_research
confidence: 0.6
maturity: draft
uses: 0
successful_uses: 0
harmful_uses: 0
skill_scope: [autoloop, autoresearch, self-evolve, critic]
---

## SD-ZERO: Self-Distillation Zero (arXiv:2604.12002)

Princeton/Toronto/CMU — Yinghui He, Kaur, Bhaskar, et al.

### Core mechanism
1. **Self-Revision Training (SRT)**: Model learns to revise own incorrect responses. Prompt: "Wait, this is not correct, let me start over." Only successful revisions retained.
2. **Self-Distillation**: Reviser provides token-level KL divergence supervision to generator. Concentrates on error tokens (self-localization).

### Key results
- SRT alone: +7.8% (Qwen3-4B)
- SD-ZERO combined: +10.5%
- Response length: -50% in Phase 2
- Beats RFT, GRPO, SDFT under matched budget

### Applicable patterns for STOPA
1. **Self-revision before critic**: Agent revises own output with "check this" prompt BEFORE spawning expensive critic agent. Cheaper, faster, catches obvious errors.
2. **Error localization**: Don't rewrite everything — identify WHERE the error is. Critic feedback should point to specific lines/tokens, not global "this is wrong."
3. **Binary → dense signal**: Our outcome system has pass/fail. Self-revision ON failures produces richer learning than just recording the failure.
4. **Length reduction via distillation**: Iterative self-revision naturally produces shorter, focused outputs — relevant for token budget.

### Limitations
- Only works for verifiable domains (math, code, structured outputs)
- Doesn't extend well to "thinking models" with long exploratory CoT
- Requires multiple training iterations (not single-pass)
