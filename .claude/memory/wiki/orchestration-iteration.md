---
generated: 2026-04-12
cluster: orchestration-iteration
sources: 13
last_updated: 2026-04-14
---

# Iterative Optimization Patterns

> **TL;DR**: Iterative refinement (autoloop, autoresearch, self-evolve) follows a "paradox" — early iterations are unreliable predictors of final quality, overfitting to eval metrics is the primary failure mode, and evolutionary approaches (EGGROLL) outperform gradient-based optimization for prompt tuning.

## Overview

STOPA's iterative skills (autoloop, autoresearch, self-evolve) share common optimization patterns distilled from research and practice. The iteration paradox reveals that performance at iterations 1-3 poorly predicts final outcome — patience through initial noise is essential (ref: 2026-04-11-iteration-paradox-meta-pattern.md). The primary risk is overfitting: agents optimize for the metric rather than the underlying goal, requiring explicit overfitting guards (ref: 2026-04-03-autoagent-overfitting-guard.md).

EGGROLL-style evolutionary optimization (low-rank ES with GRPO scoring) outperforms manual prompt engineering for prompt tuning tasks (ref: 2026-04-10-eggroll-evolutionary-optimization.md). The Claudini pattern shows that removing the human bottleneck from research loops (auto-hypothesis, auto-experiment, auto-analysis) dramatically increases throughput (ref: 2026-04-08-auto-research-removes-human-bottleneck.md).

## Key Rules

1. **Don't judge early iterations**: Performance at iter 1-3 is unreliable — commit to at least 5 iterations before evaluating (ref: 2026-04-08-early-iteration-performance-unreliable.md)
2. **Guard against overfitting**: Hold out test cases from the optimization loop — never optimize on full eval set (ref: 2026-04-03-autoagent-overfitting-guard.md)
3. **Regression gates**: After each improvement, verify previous gains are preserved (ref: 2026-04-05-regression-gate-pattern.md)
4. **Parallel candidates**: Run 2-3 candidates per iteration, not sequential (ref: 2026-04-03-autoagent-parallel-candidates.md)
5. **Direction-magnitude decoupling**: Separate "what to change" from "how much to change" (ref: 2026-04-08-direction-magnitude-decoupling-optimization.md)

## Patterns

### Do
- Use evolutionary approaches (population-based) for prompt optimization (ref: 2026-04-10-eggroll-evolutionary-optimization.md)
- Share successful strategies across runs via optstate JSON (ref: 2026-04-05-self-improving-harness.md)
- Remove human from loop where possible — auto-research beats guided research (ref: 2026-04-08-auto-research-removes-human-bottleneck.md)

### Don't
- Don't stop at first improvement — explore alternatives even when score rises (ref: 2026-04-11-iteration-paradox-meta-pattern.md)
- Don't self-sharpen on own outputs without external validation (ref: 2026-04-06-osft-self-sharpening.md)
- Don't use Claudini loop without explicit termination criteria (ref: 2026-03-29-claudini-autoresearch-loop.md)

## Related Articles

- See also: [orchestration-multi-agent](orchestration-multi-agent.md)
- See also: [skill-evaluation](skill-evaluation.md)

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
| [2026-04-12-fresh-session-self-report-verification](../learnings/2026-04-12-fresh-session-self-report-verification.md) | 2026-04-12 | medium | Verify agent self-reports from fresh session |
| [2026-04-12-sycophancy-not-hallucination](../learnings/2026-04-12-sycophancy-not-hallucination.md) | 2026-04-12 | high | Sycophancy distinct from hallucination |
