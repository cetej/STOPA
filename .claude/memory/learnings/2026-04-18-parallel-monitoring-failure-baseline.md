---
date: 2026-04-18
type: architecture
severity: medium
component: orchestration
tags: [monitoring, circuit-breaker, failure-rates, benchmark]
summary: "Empirical baseline for parallel monitoring — LLM agents fail up to 30% on hard multi-step tasks via reasoning degradation (loops/drift/stuck). Parallel monitor achieves 52-62% repetition reduction at ~11% overhead. Justifies STOPA's panic-detector investment."
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.95
maturity: draft
verify_check: "manual"
skill_scope: [orchestrate]
---

## Parallel Monitoring Empirical Baseline

Cognitive Companion (arXiv:2604.13759) provides numbers STOPA previously lacked:

**Baseline failure rate**: up to 30% on hard multi-step tasks attributable to reasoning degradation — distinct from capability failures. This is the addressable surface for circuit breakers and panic-detector.

**Monitoring effectiveness**:
- LLM-based Companion: 52-62% repetition reduction on loop-prone tasks, ~11% inference overhead
- Probe-based Companion (hidden states, layer 28): zero overhead, AUROC 0.840, mean effect +0.471
- LLM-as-judge baseline: 10-15% overhead per step (worse trade-off than parallel)

**STOPA position**: panic-detector.py is a cheap pattern-match monitor (near-zero overhead, no LLM call). It's closer to probe-based in cost profile but much simpler — trades AUROC for trivial implementation. The 52-62% reduction is the upper bound STOPA should aspire to; current panic-detector effectiveness is unmeasured.

**How to apply**: Add outcome tracking — when panic-detector fires, record whether subsequent session showed reduced edit→fail cycles. Without measurement we can't know if the hook helps or just adds noise. Target: 30%+ reduction in post-red edit→fail cycles vs. pre-hook baseline.

**Caveat**: Paper is feasibility study. Treat numbers as order-of-magnitude, not precise targets.
