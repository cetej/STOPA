---
generated: 2026-04-04
cluster: pipeline-engineering
sources: 7
last_updated: 2026-04-30
---

# Pipeline Engineering

> **TL;DR**: Sonnet 4.6 with thinking:disabled aggressively summarizes (40% output loss); use PATCH format or thinking:adaptive+effort:medium. Batch scripts for 30+ file edits.

## Overview

Pipeline engineering bridges the gap between skill-based best-effort processing and deterministic, repeatable execution. The most impactful recent finding: Sonnet 4.6 with `thinking:disabled` aggressively summarizes long text (~40% of output), while `thinking:adaptive` leaks chain-of-thought and XML tool markup into output. Low effort exacerbates both problems. The fix is either effort:medium + adaptive, or switching to PATCH/diff format instead of full text reproduction. Stripping `<antml*>/<thinking>` tags is a recommended safety net (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md).

When bulk mechanical changes touch 30+ files, the Read/Edit tool loop creates approval fatigue — batch Python scripts with --dry-run mode are the practical solution (ref: 2026-03-25-batch-edit-pattern.md). For any repeatable multi-step process requiring >90% reliability, use deterministic Python harnesses: fixed phases (Python controls order), programmatic validation after each step, template output. Skills are best-effort (~90%), harnesses are deterministic (99.9%), prompt tweaking caps at ~95% (ref: 2026-03-23-harness-engineering.md). For long-reasoning deep-tier tasks at >64k context, TriAttention (arXiv:2604.04921) provides 10.7× KV cache compression and 2.5× throughput by using pre-RoPE vector space for importance scoring instead of unstable post-RoPE attention scores. Watch model release notes for "fast weights" or "TTT support" signals (ref: 2026-04-09-triattention-pre-rope-kv-compression.md).

Three independent sources converge on a multi-session project harness pattern: Anthropic's Claude Code internal practices, OpenAI Codex (1M LOC, 3 engineers), and Princeton SWE-agent (+64% from interface design alone). Convergent patterns: `feature-list.json` as JSON ground truth (models resist editing JSON casually — the rigidity is the feature), `progress.md` + git commits for context-boundary survival, `init.sh` + smoke test for session-start reliability, and `docs/` as a progressive-disclosure system of record. STOPA adopted this via `/project-init --harness` and `/build-project` per-feature loop, with `scripts/passes-rate.py` measuring global completion rate. **Do NOT convert `feature-list.json` to YAML** — JSON rigidity prevents "I'll just tweak this done" edits. Per-feature sequential loop (not parallel batch): isolates which commit broke passes:bool and collapses rework costs (ref: 2026-04-19-harness-engineering-adoption.md).

## Key Rules

1. **Multi-session harness: JSON ground truth + progress.md + init.sh**: these three together prevent context-boundary confusion and "declare victory too early" (ref: 2026-04-19-harness-engineering-adoption.md)
2. **Sequential per-feature loop, not parallel batch**: isolates passes:bool regression to a single commit (ref: 2026-04-19-harness-engineering-adoption.md)
3. **Sonnet 4.6 thinking:disabled summarizes**: use adaptive+medium or PATCH format (ref: 2026-04-01-sonnet46-thinking-effort-breaking-change.md)
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



### 2026-04-28: Genus-consensus fallback for translation pipelines

Translation pipelines (PREKLAD) hallucinated Czech names for newly-discovered species absent from termdb ("tarantule" for *Ceratogyrus attonitifer*, "bull elephant" mistranslated). Phase 1 had no genus-level fallback - when a species lookup missed, the model invented a name rather than escalating uncertainty. Fix: `NormalizedTermDB.lookup_genus_consensus()` extracts a shared CZ genus from at least 3 termdb siblings of the same Latin genus and supplies the formulation "novy druh <CZ_genus> (*Latin*)" as a pre-fetch hint into Phase 1. Pattern generalizes: pipeline miss-handlers should escalate to one-step-up taxonomic/structural fallback before falling back to model improvisation. (ref: 2026-04-28-genus-consensus-cross-project.md)

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-01-sonnet46-thinking-effort-breaking-change](../learnings/2026-04-01-sonnet46-thinking-effort-breaking-change.md) | 2026-04-01 | critical | Thinking/effort breaking change in Sonnet 4.6 |
| [2026-03-25-batch-edit-pattern](../learnings/2026-03-25-batch-edit-pattern.md) | 2026-03-25 | high | Batch scripts for bulk file edits |
| [2026-03-23-harness-engineering](../learnings/2026-03-23-harness-engineering.md) | 2026-03-23 | high | Deterministic harnesses: Python phases + validation > skill best-effort |
| [2026-04-09-triattention-pre-rope-kv-compression](../learnings/2026-04-09-triattention-pre-rope-kv-compression.md) | 2026-04-09 | medium | TriAttention: 10.7× KV cache, 2.5× throughput for long-reasoning |
| [2026-04-14-openmontage-production-governance](../learnings/2026-04-14-openmontage-production-governance.md) | 2026-04-14 | high | OpenMontage: 7D scoring, delivery promises, slideshow risk |
| [2026-04-19-harness-engineering-adoption](../learnings/2026-04-19-harness-engineering-adoption.md) | 2026-04-19 | high | Multi-session harness: feature-list.json + progress.md + init.sh validated by Anthropic+OpenAI+SWE-agent |
| [2026-04-28-genus-consensus-cross-project](../learnings/2026-04-28-genus-consensus-cross-project.md) | 2026-04-28 | high | Genus-consensus fallback prevents species-name hallucination - generalizes to any taxonomic miss-handler |
