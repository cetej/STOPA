# Failure Outcome Protocol — Mandatory Exit Discipline

All iterative skills (autoloop, autoresearch, self-evolve, deepresearch) and execution agents (KODER) MUST write an outcome file at every exit point — including failure paths. Without this, the failure pipeline (`failure-recorder.py` → `failures/F###`) goes silent and `learn-from-failure`, HERA replay validation, and draft→validated graduation have no input.

Smoke test 2026-04-27 confirmed the hooks work end-to-end when fed a synthetic outcome:failure file. Audit found `.claude/memory/failures/` empty because skills only write outcomes on the success path. This protocol fixes that.

## When to write outcome: failure | partial

Write outcome BEFORE returning to user when ANY of these occur:

- Circuit breaker fires (3 consecutive reverts/crashes/discards/invariant violations)
- Plateau exit without sufficient improvement (no progress for N rounds, budget left)
- Budget exhausted before convergence
- Infrastructure error (ENOENT, EACCES, OOM, missing dep, git/lock contention, eval command not found)
- Eval/verify command timeout (5× baseline)
- Precondition check fails during Phase 0 setup
- 3-fix limit exceeded (KODER agent)
- User-requested abort mid-loop
- ANY unhandled exception during a Phase

The default success-path "Outcome Record" handles outcome:success. Failure paths must mirror it — same template, just `outcome: failure | partial` and a canonical `exit_reason`.

## Canonical exit_reason values

Must match `class_map` in [.claude/hooks/failure-recorder.py:170-177](../hooks/failure-recorder.py):

| exit_reason | When to use | failure_class (auto) |
|---|---|---|
| `crash_loop` | 3+ consecutive crashes, reverts, or invariant violations | logic |
| `stuck` | Logic dead-end; no valid path forward (e.g., 3-fix limit, BLOCKED) | logic |
| `plateau` | Improvement stalled; ceiling reached but budget left | logic |
| `budget_exceeded` | Iteration count or token budget hit before goal | resource |
| `timeout` | Single eval/verify exceeded 5× baseline time | timeout |
| `infra_error` | ENOENT, EACCES, OOM, missing dep, git failure, eval-not-found, scope_exceeded | resource |

Success outcomes may use any descriptive value (`convergence`, `solved`, `max_score`, `completed`) — only `outcome: failure | partial` flows through `class_map`. Default fallback for unknown values is `logic`, which loses resource/timeout signal.

## Outcome write template

Path: `.claude/memory/outcomes/<YYYY-MM-DD>-<skill>-<outcome>-<slug>.md`

```yaml
---
skill: <skill-name>
run_id: <skill>-<slug>-<timestamp>
date: <YYYY-MM-DD>
task: "<best-available task description>"
outcome: failure | partial
score_start: <baseline if measured, else "n/a">
score_end: <best-so-far if measured, else "n/a">
iterations: <count completed, 0 if Phase 0 abort>
kept: <count if measured>
discarded: <count if measured>
exit_reason: <canonical value from table above>
---

## Trajectory Summary

1. <step|iter> N: <one-line description of what happened>
...
(Max 15 entries. If failure happened in Phase 0/setup: write "Setup phase only — no iterations executed".)

## What Failed

- <root cause or signal>
- <symptom that triggered exit>

## Learnings Applied

- file: <learning-filename.md> | credit: harmful | evidence: <why this misled>
- file: <other.md> | credit: neutral | evidence: <consulted but not decisive>
... (every learning consulted; mark `harmful` if it led to the wrong direction; `neutral` if read but not load-bearing)
```

## Mechanism — why outcome write must precede user message

1. `failure-recorder.py` is a PostToolUse hook on Write to `.claude/memory/outcomes/`. It reads `outcome:` and `exit_reason:` from frontmatter, creates `failures/F###-<slug>.md` automatically.
2. `outcome-credit.py` reads `## Learnings Applied` and bumps `harmful_uses` / `successful_uses` / confidence on each referenced learning.
3. If skill returns to user without writing outcome → both hooks have nothing to act on → pipeline silent.
4. After 2+ same-class failures, `failure-recorder.py` recommends `/learn-from-failure <skill>`. This needs records to fire.

## Don't skip this — even on Phase 0 aborts

Even if the loop never started (eval command broken, git dirty, target missing), write the outcome with `iterations: 0` and `score_start/end: n/a`. Phase 0 failures classify as `infra_error` and are diagnostic — they reveal precondition gaps that block users.

After writing, mention in the user message: "Outcome recorded as failure (exit_reason: X) in `<filename>`."

## Anti-patterns

| Rationalization | Why wrong | Do instead |
|---|---|---|
| "The loop crashed before iteration 1, no outcome to write" | Phase 0 failures ARE outcomes — they reveal infra gaps | Write outcome with iterations:0, exit_reason:infra_error |
| "User aborted, that's not a real failure" | User abort still wastes budget — record it as partial with exit_reason:stuck | Write outcome:partial, exit_reason:stuck |
| "I'll just tell the user what went wrong" | Verbal report doesn't trigger hooks. failures/ stays empty. | Write outcome FIRST, then user message can reference it |
| "Failure outcome with iterations:0 looks bad in metrics" | Honest failures > silent dormancy. Metrics measure what's recorded. | Write the outcome. Pipeline relies on truth, not vanity. |
