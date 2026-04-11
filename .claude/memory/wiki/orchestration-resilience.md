---
generated: 2026-04-04
cluster: orchestration-resilience
sources: 11
last_updated: 2026-04-11
---

# Orchestration Resilience & Verification

> **TL;DR**: Classify errors before counting fix attempts (infra → stop, transient → 1 retry, logic → 3-fix escalation). Verification is the bottleneck, not code generation. Fixed failures become permanent test cases — the bar rises additively.

## Overview

The 3-fix escalation rule is a cornerstone of STOPA resilience, but raw counting fails when infrastructure errors (ENOENT, OOM) are mixed with logic bugs. GSD2 error classification introduces a mandatory triage step: infrastructure errors get immediate stop (no retries), transient errors (429, timeout) get one retry with 5s pause, and only logic errors follow normal 3-fix escalation (ref: 2026-04-01-gsd2-error-classification.md).

A critical anti-pattern emerged from the NG-ROBOT Wave 3 audit: changes to shared interfaces (API envelope, response format) were verified only by running pytest, missing 70 broken JS consumer calls. Any audit or refactor touching shared interfaces MUST verify ALL consumers, not just the changed layer (ref: 2026-04-02-audit-must-verify-consumers.md).

The regression gate pattern (NeoSigma auto-harness) extends verification forward: every fixed failure cluster becomes a permanent test case in an accumulating regression suite. With the gate, every improvement is additive — the bar rises from 0.56 to 0.78 TAU3. Without the gate, optimizing in a loop is structurally inevitable (ref: 2026-04-05-regression-gate-pattern.md).

The self-improving harness closes feedback loops with 6 upgrades: auto-scribe writes learnings automatically from session traces, trace-bridge unifies trace formats, graduation-check auto-detects promotable learnings, impact-tracker measures learning effectiveness via critic scores, strategy persistence enables warm-start across sessions, and auto-handoff chains enforce skill transitions on PIVOT/PLATEAU signals (ref: 2026-04-05-self-improving-harness.md).

The broader insight is that code generation is no longer the bottleneck — verification and testing are. Proportional effort should be allocated to proving correctness (ref: 2026-04-03-testing-bottleneck.md). GSD wave execution patterns provide structured coordination for multi-agent task execution: topological sort → wave number → parallel execution, with deviation rules (sub-agents fix inline max 3 attempts, STOP on architectural change), analysis-paralysis guard (5+ read-only ops without Write/Edit = stuck), and goal-backward verification L1→L4 (ref: 2026-03-23-gsd-patterns.md).

LLM judges (including GPT-5) prioritize structural formatting over factual correctness (r=0.65 overall on PaperOrchestra). The `/eval` and `/critic` skills must combine LLM structural scoring with grep/search verification for factual claims — never rely on LLM scoring alone for concrete assertions (ref: 2026-04-08-llm-judge-factuality-weak.md). The **Verification Shift** meta-pattern unifies this: use LLM for structure, tools for facts, cascade-order checking (verify L1 before L3), and regression gates — a four-layer protocol for every /critic and /verify run (ref: 2026-04-11-verification-shift-meta-pattern.md). The SMART gate ("Is this answerable from loaded context?") eliminates ~20% of unnecessary tool calls (ref: 2026-04-03-smart-tool-overuse.md). Modern Claude models handle multi-step reasoning natively, so harness scaffolding should be simplified — but determinism must be preserved for critical paths (ref: 2026-03-26-harness-simplification.md).

## Key Rules

1. **Classify errors before counting**: infra=stop, transient=1 retry, logic=3-fix (ref: 2026-04-01-gsd2-error-classification.md)
2. **Verify ALL consumers**: cross-cutting changes must test every consumer layer (ref: 2026-04-02-audit-must-verify-consumers.md)
3. **Regression gate on fixed failures**: every resolved cluster becomes a permanent test case (ref: 2026-04-05-regression-gate-pattern.md)
4. **Close feedback loops**: auto-scribe + trace-bridge + graduation-check as minimum harness (ref: 2026-04-05-self-improving-harness.md)
5. **Verification > generation**: allocate proportional effort to proving correctness (ref: 2026-04-03-testing-bottleneck.md)
6. **SMART gate before tool calls**: check if answer is in loaded context first (ref: 2026-04-03-smart-tool-overuse.md)
7. **Simplify scaffolding, keep determinism**: trust model capability but verify critical paths (ref: 2026-03-26-harness-simplification.md)
8. **Wave execution for multi-agent tasks**: topological sort subtasks into waves, prefer vertical slices over horizontal layers (ref: 2026-03-23-gsd-patterns.md)
9. **LLM judge + tools for verification**: LLM scores structure; grep/search verifies facts (ref: 2026-04-08-llm-judge-factuality-weak.md)
10. **Four-layer verification protocol**: L1 syntax → L2 semantic+cross-check → L3 downstream → L4 regression (ref: 2026-04-11-verification-shift-meta-pattern.md)

## Patterns

### Do
- Run consumer-side tests after any API/interface change (ref: 2026-04-02-audit-must-verify-consumers.md)
- Cluster failures by root cause (not symptom) before proposing fix (ref: 2026-04-05-regression-gate-pattern.md)
- Two-step gate: regression suite PASS + overall score must not drop (ref: 2026-04-05-regression-gate-pattern.md)
- Ask "Is this answerable from loaded context?" before spawning agents (ref: 2026-04-03-smart-tool-overuse.md)

### Don't
- Count infrastructure errors toward 3-fix limit (ref: 2026-04-01-gsd2-error-classification.md)
- Verify only the changed layer in cross-cutting changes (ref: 2026-04-02-audit-must-verify-consumers.md)
- Accept improvements without running regression suite from prior iterations (ref: 2026-04-05-regression-gate-pattern.md)

## Open Questions

- Budget calibration baseline established: 7 historical tasks analyzed, measurement protocol defined using ccusage + session tagging. No actual vs estimated comparison data yet — protocol needs execution (ref: 2026-04-07-budget-calibration-baseline.md).
- WARNING: `harness-simplification.md` advocates simplifying scaffolding, while deterministic harnesses are emphasized for critical pipelines. Resolution: simplify advisory scaffolding but keep deterministic harnesses for critical pipelines.

## Related Articles

- See also: [orchestration-multi-agent](orchestration-multi-agent.md) — multi-agent coordination
- See also: [pipeline-engineering](pipeline-engineering.md) — deterministic harness patterns

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-05-regression-gate-pattern](../learnings/2026-04-05-regression-gate-pattern.md) | 2026-04-05 | high | Fixed failures become permanent test cases — bar rises additively |
| [2026-04-05-self-improving-harness](../learnings/2026-04-05-self-improving-harness.md) | 2026-04-05 | high | 6 feedback loop upgrades closing harness gaps |
| [2026-04-07-budget-calibration-baseline](../learnings/2026-04-07-budget-calibration-baseline.md) | 2026-04-07 | medium | Budget calibration baseline: 7 tasks analyzed, protocol defined |
| [2026-04-03-smart-tool-overuse](../learnings/2026-04-03-smart-tool-overuse.md) | 2026-04-03 | medium | SMART gate eliminates 20% unnecessary calls |
| [2026-04-03-testing-bottleneck](../learnings/2026-04-03-testing-bottleneck.md) | 2026-04-03 | medium | Verification is the new bottleneck |
| [2026-04-02-audit-must-verify-consumers](../learnings/2026-04-02-audit-must-verify-consumers.md) | 2026-04-02 | critical | Must verify ALL consumers on interface changes |
| [2026-04-01-gsd2-error-classification](../learnings/2026-04-01-gsd2-error-classification.md) | 2026-04-01 | high | Error classification before fix counting |
| [2026-03-26-harness-simplification](../learnings/2026-03-26-harness-simplification.md) | 2026-03-26 | high | Simplify scaffolding, trust model capability |
| [2026-03-23-gsd-patterns](../learnings/2026-03-23-gsd-patterns.md) | 2026-03-23 | medium | Wave execution, deviation rules, goal-backward L1-L4 verification |
| [2026-04-08-llm-judge-factuality-weak](../learnings/2026-04-08-llm-judge-factuality-weak.md) | 2026-04-08 | high | LLM judges score structure, not facts — combine with grep/search |
| [2026-04-11-verification-shift-meta-pattern](../learnings/2026-04-11-verification-shift-meta-pattern.md) | 2026-04-11 | high | Verification Shift: 4-layer protocol (syntax/semantic/downstream/regression) |
