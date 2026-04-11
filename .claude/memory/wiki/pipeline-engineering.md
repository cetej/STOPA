---
generated: 2026-04-04
cluster: pipeline-engineering
sources: 4
last_updated: 2026-04-11
---

# Pipeline Engineering

> **TL;DR**: Sonnet 4.6 with thinking:disabled aggressively summarizes (40% output loss); use PATCH format or thinking:adaptive+effort:medium. Batch scripts for 30+ file edits.

## Overview

Pipeline engineering bridges the gap between skill-based best-effort processing and deterministic, repeatable execution. The most impactful recent finding: Sonnet 4.6 with `thinking:disabled` aggressively summarizes long text (~40% of output), while `thinking:adaptive` leaks chain-of-thought and XML tool markup into output. Low effort exacerbates both problems. The fix is either effort:medium + adaptive, or switching to PATCH/diff format instead of full text reproduction. Stripping `<antml*>/<thinking>` tags is a recommended safety net (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md).

When bulk mechanical changes touch 30+ files, the Read/Edit tool loop creates approval fatigue — batch Python scripts with --dry-run mode are the practical solution (ref: 2026-03-25-batch-edit-pattern.md). For any repeatable multi-step process requiring >90% reliability, use deterministic Python harnesses: fixed phases (Python controls order), programmatic validation after each step, template output. Skills are best-effort (~90%), harnesses are deterministic (99.9%), prompt tweaking caps at ~95% (ref: 2026-03-23-harness-engineering.md). For long-reasoning deep-tier tasks at >64k context, TriAttention (arXiv:2604.04921) provides 10.7× KV cache compression and 2.5× throughput by using pre-RoPE vector space for importance scoring instead of unstable post-RoPE attention scores. Watch model release notes for "fast weights" or "TTT support" signals (ref: 2026-04-09-triattention-pre-rope-kv-compression.md).

## Key Rules

1. **Sonnet 4.6 thinking:disabled summarizes**: use adaptive+medium or PATCH format (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
2. **Strip thinking tags as safety net**: `<antml*>` and `<thinking>` can leak (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
3. **Batch scripts for 30+ files**: --dry-run mode, avoids approval fatigue (ref: 2026-03-25-batch-edit-pattern.md)
4. **Harness > skill for >90% reliability**: Python-controlled phases, programmatic validation, template output (ref: 2026-03-23-harness-engineering.md)
5. **TriAttention for long-reasoning**: 10.7× KV compression at >64k context via pre-RoPE scoring (ref: 2026-04-09-triattention-pre-rope-kv-compression.md)

## Patterns

### Do
- Use PATCH/diff format for text reproduction pipelines (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
- Add --dry-run to batch edit scripts (ref: 2026-03-25-batch-edit-pattern.md)
- Use Python harness pattern for multi-step processes needing deterministic reliability (ref: 2026-03-23-harness-engineering.md)

### Don't
- Use thinking:disabled for text-heavy pipelines (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
- Use effort:low for anything requiring faithful reproduction (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
- Edit 30+ files individually via Read/Edit loop (ref: 2026-03-25-batch-edit-pattern.md)

## Open Questions

- WARNING: `harness-simplification.md` (orchestration cluster) advocates simplifying harnesses while deterministic execution is emphasized here. Resolution: simplify scaffolding for advisory/reasoning tasks, keep deterministic harnesses for data pipelines and critical processes.

## Related Articles

- See also: [orchestration-resilience](orchestration-resilience.md) — error classification and verification patterns
- See also: [general-security-environment](general-security-environment.md) — API and model behavior

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-01-sonnet46-thinking-effort-breaking-change](../learnings/2026-04-01-sonnet46-thinking-effort-breaking-change.md) | 2026-04-01 | critical | Thinking/effort breaking change in Sonnet 4.6 |
| [2026-03-25-batch-edit-pattern](../learnings/2026-03-25-batch-edit-pattern.md) | 2026-03-25 | high | Batch scripts for bulk file edits |
| [2026-03-23-harness-engineering](../learnings/2026-03-23-harness-engineering.md) | 2026-03-23 | high | Deterministic harnesses: Python phases + validation > skill best-effort |
| [2026-04-09-triattention-pre-rope-kv-compression](../learnings/2026-04-09-triattention-pre-rope-kv-compression.md) | 2026-04-09 | medium | TriAttention: 10.7× KV cache, 2.5× throughput for long-reasoning |
