---
date: 2026-04-06
type: architecture
severity: medium
component: orchestration
tags: [research, self-improvement, model-training, temperature-decoupling]
summary: "OSFT (Online SFT) achieves RL-comparable reasoning improvement by self-sharpening — model finetunes on own outputs with decoupled temperatures (sampling sharp, training soft). No reward model needed, 8x cheaper than GRPO. Key insight: latent knowledge unlocking, not new learning."
source: external_research
confidence: 0.7
uses: 0
harmful_uses: 0
impact_score: 0.0
verify_check: "manual"
---

# OSFT — Online SFT for LLM Reasoning (arXiv:2510.18814)

## Core Mechanism
- Model generates response at temperature tau_s (sharp, e.g. 0.6)
- Finetunes on own response at temperature tau_t (soft, e.g. 1.0)
- Gradient: proportional to J_theta[p_tau_t - p_tau_s] — amplifies existing peaks
- Critical: tau_s < tau_t required; coupled temperatures = zero gradient (score-function identity)

## Key Results (Qwen2.5-Math-7B)
- OSFT Pass@1: 73.8% vs GRPO 67.9% (OSFT wins)
- GRPO wins at Pass@8+ (better diversity)
- 1 rollout/prompt vs 8 for GRPO (8x compute savings)
- No reward model needed

## Implications for STOPA
1. **Self-evolve skill**: validates self-improvement without external reward — model can improve own skills by iterating on own outputs
2. **Temperature analogy**: using different model tiers for generation vs validation = structural temperature decoupling
3. **Base quality matters**: OSFT weak on Llama3.1-8B, strong on Qwen-Math — parallels STOPA tier system (stronger model for iterative tasks)
4. **Pass@1 vs diversity tradeoff**: self-sharpening reduces diversity — council/multi-agent needed for exploration
5. **Latent knowledge**: structured self-feedback unlocks existing capabilities — same principle as learnings retrieval system

## Limitations
- Only verifiable tasks (math, code) — open-ended unclear
- No convergence guarantees
- Base model quality is prerequisite
