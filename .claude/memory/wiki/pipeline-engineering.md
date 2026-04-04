---
generated: 2026-04-04
cluster: pipeline-engineering
sources: 3
last_updated: 2026-04-04
---

# Pipeline Engineering

> **TL;DR**: Sonnet 4.6 with thinking:disabled aggressively summarizes (40% output loss); use PATCH format or thinking:adaptive+effort:medium. Deterministic Python harnesses for >90% reliability. Batch scripts for 30+ file edits.

## Overview

Pipeline engineering bridges the gap between skill-based best-effort processing and deterministic, repeatable execution. The most impactful recent finding: Sonnet 4.6 with `thinking:disabled` aggressively summarizes long text (~40% of output), while `thinking:adaptive` leaks chain-of-thought and XML tool markup into output. Low effort exacerbates both problems. The fix is either effort:medium + adaptive, or switching to PATCH/diff format instead of full text reproduction. Stripping `<antml*>/<thinking>` tags is a recommended safety net (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md).

For processes requiring >90% reliability, deterministic Python harnesses (scripts controlling execution order and validation) are structurally superior to prompt-based skills which cap at ~95% even with extensive tuning (ref: harness-engineering.md). When bulk mechanical changes touch 30+ files, the Read/Edit tool loop creates approval fatigue — batch Python scripts with --dry-run mode are the practical solution (ref: 2026-03-25-batch-edit-pattern.md).

## Key Rules

1. **Sonnet 4.6 thinking:disabled summarizes**: use adaptive+medium or PATCH format (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
2. **Strip thinking tags as safety net**: `<antml*>` and `<thinking>` can leak (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
3. **Harness > skill for >90% reliability**: Python controls order + validation (ref: harness-engineering.md)
4. **Batch scripts for 30+ files**: --dry-run mode, avoids approval fatigue (ref: 2026-03-25-batch-edit-pattern.md)

## Patterns

### Do
- Use PATCH/diff format for text reproduction pipelines (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
- Write deterministic Python harnesses for critical repeatable processes (ref: harness-engineering.md)
- Add --dry-run to batch edit scripts (ref: 2026-03-25-batch-edit-pattern.md)

### Don't
- Use thinking:disabled for text-heavy pipelines (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
- Use effort:low for anything requiring faithful reproduction (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
- Edit 30+ files individually via Read/Edit loop (ref: 2026-03-25-batch-edit-pattern.md)

## Open Questions

- WARNING: `harness-simplification.md` (orchestration cluster) advocates simplifying harnesses while this cluster emphasizes their necessity. Resolution: simplify scaffolding for advisory/reasoning tasks, keep deterministic harnesses for data pipelines and critical processes.

## Related Articles

- See also: [orchestration-resilience](orchestration-resilience.md) — error classification and verification patterns
- See also: [general-security-environment](general-security-environment.md) — API and model behavior

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-01-sonnet46-thinking-effort-breaking-change](../learnings/2026-04-01-sonnet46-thinking-effort-breaking-change.md) | 2026-04-01 | critical | Thinking/effort breaking change in Sonnet 4.6 |
| [harness-engineering](../learnings/harness-engineering.md) | 2026-03-23 | high | Deterministic harnesses for >90% reliability |
| [2026-03-25-batch-edit-pattern](../learnings/2026-03-25-batch-edit-pattern.md) | 2026-03-25 | high | Batch scripts for bulk file edits |
