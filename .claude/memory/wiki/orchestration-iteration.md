---
generated: 2026-04-12
cluster: orchestration-iteration
sources: 16
last_updated: 2026-04-17
---

# Iterative Optimization Patterns

> **TL;DR**: Iterative refinement (autoloop, autoresearch, self-evolve) follows a "paradox" — early iterations are unreliable predictors of final quality, overfitting to eval metrics is the primary failure mode, and evolutionary approaches (EGGROLL) outperform gradient-based optimization for prompt tuning. Four 2026-04 additions sharpen the toolkit: **Best-of-N parallel candidates** replace linear try-fail-try sequences; **Parcae exponential decay** predicts iteration ceiling after 3-4 samples; **PRM step-verification** kills failing pipelines mid-flight instead of running to completion.

## Overview

STOPA's iterative skills (autoloop, autoresearch, self-evolve) share common optimization patterns distilled from research and practice. The iteration paradox reveals that performance at iterations 1-3 poorly predicts final outcome — patience through initial noise is essential (ref: 2026-04-11-iteration-paradox-meta-pattern.md). The primary risk is overfitting: agents optimize for the metric rather than the underlying goal, requiring explicit overfitting guards (ref: 2026-04-03-autoagent-overfitting-guard.md).

EGGROLL-style evolutionary optimization (low-rank ES with GRPO scoring) outperforms manual prompt engineering for prompt tuning tasks (ref: 2026-04-10-eggroll-evolutionary-optimization.md). The Claudini pattern shows that removing the human bottleneck from research loops (auto-hypothesis, auto-experiment, auto-analysis) dramatically increases throughput (ref: 2026-04-08-auto-research-removes-human-bottleneck.md).

### Three 2026-04 Sharpening Patterns

**Best-of-N with PRM scoring** (arXiv:2501.09686, ref: 2026-04-15-best-of-n-parallel-candidates.md) replaces linear iteration with parallel candidate generation: fork N=2-3 independent approaches, score each with a lightweight critic, expand the best. Explorational breadth beats depth-first retry — iterating on the best starting point converges faster than patching the first.

**Parcae exponential decay** (arXiv:2604.12946, ref: 2026-04-15-parcae-exponential-decay-stopping.md) models iterative compute as `L(T) = L∞ + Z·exp(-z·T)`. After 3-4 iterations the model fits with 0.85-1.3% prediction error — the predicted floor `L∞` tells you whether remaining iterations can possibly reach target, enabling early termination before burning compute. Plateau-detection ("3 iterations without improvement") is a lagging signal; fitted decay is leading.

**PRM step-verification** (ref: 2026-04-15-prm-step-verification-orchestrate.md) adds a haiku-level check after each subtask ("did this step satisfy the plan?") instead of running the full pipeline and critiquing at the end. Step-level rewards (Process Reward Models) dramatically outperform Outcome Reward Models for multi-step reasoning — identifies WHERE failure occurred, kills pipeline early on FAIL. Cost: ~200 tokens/subtask; ROI: skipped compute when step 2 of 6 fails.

## Key Rules

1. **Don't judge early iterations**: Performance at iter 1-3 is unreliable — commit to at least 5 iterations before evaluating (ref: 2026-04-08-early-iteration-performance-unreliable.md)
2. **Guard against overfitting**: Hold out test cases from the optimization loop — never optimize on full eval set (ref: 2026-04-03-autoagent-overfitting-guard.md)
3. **Regression gates**: After each improvement, verify previous gains are preserved (ref: 2026-04-05-regression-gate-pattern.md)
4. **Parallel candidates over linear iteration**: Fork N=2-3 candidates, score lightweight, expand best — not try-A-then-B (ref: 2026-04-15-best-of-n-parallel-candidates.md, 2026-04-03-autoagent-parallel-candidates.md)
5. **Direction-magnitude decoupling**: Separate "what to change" from "how much to change" (ref: 2026-04-08-direction-magnitude-decoupling-optimization.md)
6. **Fit exponential decay after 4+ iterations**: `L(T) = L∞ + Z·exp(-z·T)`; if `L∞ < target`, STOP — remaining iterations can't reach target (ref: 2026-04-15-parcae-exponential-decay-stopping.md)
7. **Training depth caps inference depth**: If skill self-evolved with max 5 iterations, deploying with 15 won't help — propagate `recommended_max_iterations` into optstate (ref: 2026-04-15-parcae-exponential-decay-stopping.md)
8. **Variable depth per-item in farm tier**: Classify item complexity before distribution — simple fix=1 iter, complex=3 — uniform effort wastes budget (ref: 2026-04-15-parcae-exponential-decay-stopping.md)
9. **PRM step-checks over ORM end-critic**: After each subtask, haiku verifies step satisfied plan — FAIL kills pipeline early (ref: 2026-04-15-prm-step-verification-orchestrate.md)

## Patterns

### Do
- Use evolutionary approaches (population-based) for prompt optimization (ref: 2026-04-10-eggroll-evolutionary-optimization.md)
- Share successful strategies across runs via optstate JSON (ref: 2026-04-05-self-improving-harness.md)
- Remove human from loop where possible — auto-research beats guided research (ref: 2026-04-08-auto-research-removes-human-bottleneck.md)
- Fork 2-3 parallel agent candidates for deep-tier orchestrate approaches (ref: 2026-04-15-best-of-n-parallel-candidates.md)
- Fit exponential decay to score trajectory for early-termination (ref: 2026-04-15-parcae-exponential-decay-stopping.md)
- Insert haiku step-checks after each orchestrate subtask (ref: 2026-04-15-prm-step-verification-orchestrate.md)

### Don't
- Don't stop at first improvement — explore alternatives even when score rises (ref: 2026-04-11-iteration-paradox-meta-pattern.md)
- Don't self-sharpen on own outputs without external validation (ref: 2026-04-06-osft-self-sharpening.md)
- Don't use Claudini loop without explicit termination criteria (ref: 2026-03-29-claudini-autoresearch-loop.md)
- Don't run Best-of-N with N>3 on Claude API — cost grows linearly with little benefit (ref: 2026-04-15-best-of-n-parallel-candidates.md)
- Don't apply Best-of-N to light tier — single-pass suffices; task must be decomposable into independent branches (ref: 2026-04-15-best-of-n-parallel-candidates.md)
- Don't rely on plateau-detection alone — it's a lagging signal vs fitted decay (ref: 2026-04-15-parcae-exponential-decay-stopping.md)

## Open Questions

- GAP: No empirical data yet on Best-of-N × PRM-scoring combined cost in STOPA — needs pilot run on deep-tier orchestrate task
- GAP: Parcae `L∞` fit requires `scripts/loop-state.py decay-predict`; current status unknown (implementation exists per related learnings but not confirmed active)

## Related Articles

- See also: [orchestration-multi-agent](orchestration-multi-agent.md) — parallel agent coordination
- See also: [skill-evaluation](skill-evaluation.md) — critic patterns, reward models

## Source Learnings

| File | Date | Severity | Uses | Summary |
|------|------|----------|------|---------|
| iteration-paradox-meta-pattern | 2026-04-11 | high | 1 | Meta-pattern: early iters unreliable |
| eggroll-evolutionary-optimization | 2026-04-10 | high | 1 | Low-rank ES + GRPO scoring |
| auto-research-removes-human-bottleneck | 2026-04-08 | high | 1 | Autonomous research loops |
| autoagent-overfitting-guard | 2026-04-03 | high | 1 | Hold-out sets prevent metric gaming |
| regression-gate-pattern | 2026-04-05 | high | 1 | Verify previous gains preserved |
| direction-magnitude-decoupling | 2026-04-08 | medium | 1 | Separate direction from magnitude |
| early-iteration-performance-unreliable | 2026-04-08 | high | 1 | Don't judge early iterations |
| self-improving-harness | 2026-04-05 | high | 0 | Cross-run strategy persistence |
| osft-self-sharpening | 2026-04-06 | medium | 0 | Self-training risks without external data |
| autoagent-parallel-candidates | 2026-04-03 | medium | 0 | Run multiple candidates per iteration |
| claudini-autoresearch-loop | 2026-03-29 | high | 0 | Autonomous research pipeline |
| [2026-04-12-fresh-session-self-report-verification](../learnings/2026-04-12-fresh-session-self-report-verification.md) | 2026-04-12 | medium | — | Verify agent self-reports from fresh session |
| [2026-04-12-sycophancy-not-hallucination](../learnings/2026-04-12-sycophancy-not-hallucination.md) | 2026-04-12 | high | — | Sycophancy distinct from hallucination |
| [2026-04-15-best-of-n-parallel-candidates](../learnings/2026-04-15-best-of-n-parallel-candidates.md) | 2026-04-15 | medium | 3 | Best-of-N: fork 2-3 parallel, score, expand best — not linear retry |
| [2026-04-15-parcae-exponential-decay-stopping](../learnings/2026-04-15-parcae-exponential-decay-stopping.md) | 2026-04-15 | high | 2 | `L(T)=L∞+Z·exp(-z·T)` fits after 4 iters; training depth caps inference |
| [2026-04-15-prm-step-verification-orchestrate](../learnings/2026-04-15-prm-step-verification-orchestrate.md) | 2026-04-15 | high | 3 | PRM step-check after each subtask — early-kill on FAIL; ~200 tok/step |
