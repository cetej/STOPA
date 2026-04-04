---
generated: 2026-04-04
cluster: orchestration-resilience
sources: 6
last_updated: 2026-04-04
---

# Orchestration Resilience & Verification

> **TL;DR**: Classify errors before counting fix attempts (infra → stop, transient → 1 retry, logic → 3-fix escalation). Verification is the bottleneck, not code generation. Cross-cutting changes must verify ALL consumers.

## Overview

The 3-fix escalation rule is a cornerstone of STOPA resilience, but raw counting fails when infrastructure errors (ENOENT, OOM) are mixed with logic bugs. GSD2 error classification introduces a mandatory triage step: infrastructure errors get immediate stop (no retries), transient errors (429, timeout) get one retry with 5s pause, and only logic errors follow normal 3-fix escalation (ref: 2026-04-01-gsd2-error-classification.md).

A critical anti-pattern emerged from the NG-ROBOT Wave 3 audit: changes to shared interfaces (API envelope, response format) were verified only by running pytest, missing 70 broken JS consumer calls. Any audit or refactor touching shared interfaces MUST verify ALL consumers, not just the changed layer (ref: 2026-04-02-audit-must-verify-consumers.md).

The broader insight is that code generation is no longer the bottleneck — verification and testing are. Proportional effort should be allocated to proving correctness (ref: 2026-04-03-testing-bottleneck.md). The SMART gate ("Is this answerable from loaded context?") eliminates ~20% of unnecessary tool calls, especially in light tier orchestration (ref: 2026-04-03-smart-tool-overuse.md). Modern Claude models handle multi-step reasoning natively, so harness scaffolding should be simplified — but determinism must be preserved for critical paths (ref: 2026-03-26-harness-simplification.md). GSD wave execution provides the mechanical framework: batch independent tasks, verify after each wave (ref: gsd-patterns.md).

## Key Rules

1. **Classify errors before counting**: infra=stop, transient=1 retry, logic=3-fix (ref: 2026-04-01-gsd2-error-classification.md)
2. **Verify ALL consumers**: cross-cutting changes must test every consumer layer (ref: 2026-04-02-audit-must-verify-consumers.md)
3. **Verification > generation**: allocate proportional effort to proving correctness (ref: 2026-04-03-testing-bottleneck.md)
4. **SMART gate before tool calls**: check if answer is in loaded context first (ref: 2026-04-03-smart-tool-overuse.md)
5. **Simplify scaffolding, keep determinism**: trust model capability but verify critical paths (ref: 2026-03-26-harness-simplification.md)
6. **Wave execution with verification**: batch → verify → next batch (ref: gsd-patterns.md)

## Patterns

### Do
- Run consumer-side tests after any API/interface change (ref: 2026-04-02-audit-must-verify-consumers.md)
- Ask "Is this answerable from loaded context?" before spawning agents (ref: 2026-04-03-smart-tool-overuse.md)
- Immediately stop on infrastructure errors — retrying wastes budget (ref: 2026-04-01-gsd2-error-classification.md)

### Don't
- Count infrastructure errors toward 3-fix limit (ref: 2026-04-01-gsd2-error-classification.md)
- Verify only the changed layer in cross-cutting changes (ref: 2026-04-02-audit-must-verify-consumers.md)
- Over-scaffold when the model handles reasoning natively (ref: 2026-03-26-harness-simplification.md)

## Open Questions

- WARNING: `harness-simplification.md` advocates simplifying scaffolding, while `harness-engineering.md` (in pipeline cluster) emphasizes deterministic Python harnesses for >90% reliability. Resolution: simplify advisory scaffolding but keep deterministic harnesses for critical pipelines.

## Related Articles

- See also: [orchestration-multi-agent](orchestration-multi-agent.md) — multi-agent coordination
- See also: [pipeline-engineering](pipeline-engineering.md) — deterministic harness patterns

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-03-smart-tool-overuse](../learnings/2026-04-03-smart-tool-overuse.md) | 2026-04-03 | medium | SMART gate eliminates 20% unnecessary calls |
| [2026-04-03-testing-bottleneck](../learnings/2026-04-03-testing-bottleneck.md) | 2026-04-03 | medium | Verification is the new bottleneck |
| [2026-04-02-audit-must-verify-consumers](../learnings/2026-04-02-audit-must-verify-consumers.md) | 2026-04-02 | critical | Must verify ALL consumers on interface changes |
| [2026-04-01-gsd2-error-classification](../learnings/2026-04-01-gsd2-error-classification.md) | 2026-04-01 | high | Error classification before fix counting |
| [2026-03-26-harness-simplification](../learnings/2026-03-26-harness-simplification.md) | 2026-03-26 | high | Simplify scaffolding, trust model capability |
| [gsd-patterns](../learnings/gsd-patterns.md) | 2026-03-23 | medium | GSD wave execution pattern |
