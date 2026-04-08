---
name: autoharness
variant: compact
description: Condensed autoharness for repeat invocations within session. Use full SKILL.md for first invocation.
---

# AutoHarness — Compact (Session Re-invocation)

Observe failures → synthesize Python validator → iterate until 100% pass rate.

## Three Types

| Type | How | When |
|------|-----|------|
| action-filter | Generate set of legal outputs, skill picks | Output is one of N known-good options |
| action-verifier | Skill proposes, code validates + returns feedback | Most common (default) |
| policy | Deterministic code replaces LLM entirely | Simple transforms |

## Pipeline

1. **Failure Collection** → learnings (grep component/tags), git history (fix/revert commits), troubleshooting docs, eval failures. Min 3 failures required. Classify: SYNTAX/SCHEMA/LOGIC/DEPENDENCY/FORMAT/CONSTRAINT.
2. **Generate validator.py** → stdlib-only Python. No try-except. One check per failure. Explicit feedback on failure.
3. **Refinement loop** (max 5 iterations) → test against all failures, score pass_rate. Haiku refines. Confound isolation: change logic OR thresholds, never both.
4. **Novel data validation** → Haiku generates 3-5 new test inputs. >80% accuracy → PASS.
5. **Adversarial escalation** (if escalate:true) → Sonnet red-team tries to bypass. Max 2 rounds.
6. **Integration** → Hook (PostToolUse), standalone script, or inline in skill.

## Critical Rules

- No try-except in validators — errors must surface
- No LLM calls — pure Python, zero inference cost
- No external deps — stdlib only
- Circuit breaker: pass_rate <0.8 after max iterations → STOP with analysis
- Min 3 failures before generating anything
