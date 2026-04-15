---
date: 2026-04-08
type: best_practice
severity: high
component: orchestration
tags: [reasoning, inference, iteration, compute-efficiency, orchestration]
summary: "Sequential Refinement (iterative bounded drafts) beats long chain-of-thought at matched compute. For iterative tasks, use bounded refinement loops rather than single long-context generation."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 1.0
verify_check: "manual"
---

## What happened

PDR paper (arXiv:2510.01123) demonstrates that iterative refinement over bounded contexts outperforms long CoT on AIME 2024 (+11%) and AIME 2025 (+9%) at matched sequential compute budgets.

## Rule

**Use iterative refinement over long-context generation for reasoning-intensive tasks.**

- Sequential Refinement (SR): run model N times on bounded context → each pass improves prior answer
- Parallel-Distill-Refine (PDR): run N parallel drafts → distill → refine (controls quality via parallelism, not context size)
- Context length should be bounded per iteration, not grown unboundedly

## Application to STOPA

- `autoloop`: validated — bounded iterations > single long-context pass
- `autoresearch`: prefer generate-diverse-candidates → distill → refine over single exploration
- Model selection: larger models exploit refinement feedback better (matches CLAUDE.md iterative task → sonnet/opus rule)
- Budget: parallelism (more agents) trades off vs latency (sequential iterations) — same compute, different topology

## Evidence

RL training aligned with PDR inference on 8B model: +11% AIME 2024, +9% AIME 2025 vs single-pass baselines.
