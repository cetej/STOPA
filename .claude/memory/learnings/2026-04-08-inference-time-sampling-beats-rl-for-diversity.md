---
date: 2026-04-08
type: best_practice
severity: medium
component: orchestration
tags: [inference-time, sampling, model-selection, autoloop, autoresearch, diversity]
summary: "For iterative exploration tasks (autoloop, autoresearch), high-temperature sampling > RL-tuned models. RL post-training causes diversity collapse — repeated runs produce near-identical outputs. Base/lightly-tuned models with sampling preserve the exploration space."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.85
verify_check: "manual"
related: []
---

## Detail

arXiv:2510.14901 (Harvard): Sampling from p^α (MCMC power distributions) nearly matches GRPO RL training on MATH500 (74.8% vs 78.5%) and beats it on HumanEval (57.3% vs 53.7%) — **without any training**. Key finding: RL post-training causes **diversity collapse** — Pass@k diversity drops because the model narrows to a high-reward region.

## Application to STOPA

When designing iterative skills that generate multiple candidate solutions:
- Prefer higher temperature over greedy decoding
- Do NOT use RL-tuned specialized models (e.g., math-specific) when diversity of approaches matters
- Best-of-N with diverse samples > single high-confidence greedy output for reasoning tasks
- Budget implication: quality diversity costs ~9× tokens vs greedy — factor into tier selection

Skills affected: `/autoloop`, `/autoresearch`, `/self-evolve` (candidate generation phase)
