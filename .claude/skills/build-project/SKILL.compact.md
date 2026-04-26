---
name: build-project
variant: compact
description: Condensed build-project for repeat invocations within session. Use full SKILL.md for first invocation.
---

# Build Project — Compact (Session Re-invocation)

You build complete projects from natural language requirements via the harness pattern: `feature-list.json` as ground truth, per-feature end-to-end verification, `progress.md` for multi-session continuity.

## Harness Invariants (must hold at completion)

1. `docs/feature-list.json` exists; every feature has `passes: true`
2. Each `passes: true` set ONLY after end-to-end verification (not unit tests alone)
3. `docs/progress.md` has a session log entry per build session
4. Git history: one commit per feature (or coherent batch)
5. `./init.sh` runs cleanly from fresh checkout + passes smoke test

If any invariant fails → project is partially built, NOT done.

## Pipeline (compressed)

| Phase | Action | Gate |
|-------|--------|------|
| 1 Requirements | Parse → 5-30 features with id/category/description/steps/passes:false | HUMAN GATE before proceed |
| 2 Research | If domain unfamiliar: `/deepresearch <domain>` | — |
| 3 Scaffold | `/project-init --harness` (creates feature-list.json) | — |
| 4 Per-feature | Implement ONE feature; mark `passes:true` only after E2E verify | one feature at a time |
| 5 Integration | Wire features; full smoke test | smoke must pass |
| 6 Close | Update progress.md; git commit; register in projects.json | — |

## Per-feature loop (Phase 4 core)

```
For each feature in feature-list.json (passes: false):
  1. Read feature.steps (E2E verifiable, not unit)
  2. Decompose into subtasks via /orchestrate (or direct if light tier)
  3. Implement
  4. Run E2E verification — execute each feature.step
  5. If ALL steps pass → set passes: true; commit; update progress.md
  6. If ANY step fails → keep passes: false; log; continue or escalate
```

## Circuit Breakers

- Feature E2E fails 3× → STOP, escalate to user
- 5 features in row fail → STOP, fundamental issue with spec
- Smoke test fails after integration → STOP, do not declare done
- Budget exceeds 80% before half features done → re-spec or descope

## Critical Rules

- Never set `passes: true` without E2E verification (NOT unit tests alone)
- Always commit per feature (or coherent batch) — keeps git history aligned with feature-list
- Update `docs/progress.md` at end of EVERY session (multi-session continuity)
- Verify `./init.sh` runs cleanly before declaring project complete
- Register completed project in `~/.claude/memory/projects.json`

## When to load full SKILL.md

- First invocation of /build-project in this session
- Specialized scaffold needed (non-standard /project-init flags)
- Cross-feature coordination (features sharing state)
- Multi-session resumption with stale checkpoint

For these: invoke with `--full` flag.
