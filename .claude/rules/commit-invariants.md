---
globs: ".claude/skills/{self-evolve,autoloop,autoresearch,autoharness}/SKILL.md,.claude/commands/{self-evolve,autoloop,autoresearch,autoharness}.md"
---

# Commit Invariants for Iterative Skills

Ref: Autogenesis Protocol (arXiv:2604.15034), §3.2.2 Commit operator κ.

The Commit operator κ accepts a candidate state ONLY when the score improves AND all safety invariants hold. This rule defines the mandatory invariants. If any fails, the candidate MUST be rolled back — even if the score improved.

## Mandatory invariants (checked on EVERY commit)

### I1. No description regression
- Skill `description:` field MUST still start with `Use when`
- If the edit removed or replaced `Use when...` → **ROLLBACK**
- Why: critical for routing (core-invariants #3)

### I2. Size bounded
- Memory files MUST be < 500 lines (core-invariants #5) — hard limit
- SKILL.md files: growth per single evolution iteration MUST be ≤ +15% of pre-edit line count
  - Example: 600-line skill → next iteration may add at most 90 lines (→ 690)
  - Rationale: prevents "evolution bloat" while allowing gradual growth. Skills grow naturally as they absorb patterns.
  - Absolute ceiling: 1200 lines — above this, split into references/ sub-files before further evolution
- Overflow → **ROLLBACK** (evolution is not a license to bloat)

### I3. No secret leak
- No new matches for `sk-`, `API_KEY=`, `SECRET`, `TOKEN=`, bearer tokens in the diff
- Env var references (`os.environ["X"]`) are OK; literal values are not
- Match → **ROLLBACK** (core-invariants #4)

### I4. No syntax regression
- For Python files: `python -c "import ast; ast.parse(open('<file>').read())"` must pass
- For JSON files: `python -m json.tool <file>` must pass
- For Markdown: YAML frontmatter must parse (if present)
- Parse error → **ROLLBACK**

### I5. No test regression (when tests exist)
- Any test that passed BEFORE the edit must still pass AFTER
- New failures introduced by the edit → **ROLLBACK**
- Does not apply when no tests exist for the changed code

### I6. No circular reference in learnings
- If edit adds `supersedes:` or `related:` fields: target files must exist
- Dangling reference → **ROLLBACK**

### I10. No LLM config modification during iterative evolution
- Iterative skills (`/self-evolve`, `/autoloop`, `/autoresearch`, `/autoharness`) MUST NOT modify the target skill's LLM configuration fields during the κ Commit step
- Forbidden fields in YAML frontmatter (top-level OR inside `handoffs[]`):
  - `model:` (haiku | sonnet | opus)
  - `effort:` (low | high | auto)
  - `maxTurns:`
  - `temperature:` and `reasoning_effort:` (if present — Claude SDK doesn't currently expose these in skill frontmatter, but the prohibition holds for any future config field that controls model behavior)
- Detection: `git diff HEAD~1 -- <skill.md>` matching `^[+-](model|effort|maxTurns|temperature|reasoning_effort):` in the YAML frontmatter region
- Match → **ROLLBACK**
- Why: AHE evolve_prompt.md L229-241 — "LLM config changes consistently cause broad, hard-to-diagnose regressions." Switching haiku↔sonnet↔opus shifts behavior across the entire skill body in ways pass_rate can mask short-term but degrade weeks later. Same applies to `effort:` and `maxTurns:` — they reshape the agent's reasoning depth, not just one capability.
- LLM config is an **operator decision**, not an optimization target. Changes land via human review (PR), not iterative loops.
- Exception: user-initiated `--bump-model <new>` flag passed to the iterative skill, which writes the change with `decision: operator-override` in the change_ledger entry. No such flag exists yet — until implemented, this invariant has no exception.

## Recommended invariants (check when relevant)

### I7. Frontmatter preserved
- YAML frontmatter keys present before edit must still be present after (unless explicit removal was the intent)

### I8. Anti-Rationalization Defense preserved
- Skills with this section: row count MUST NOT decrease (can grow, never shrink)
- Shrinking → **ROLLBACK** (evolution should add defenses, not remove them)

### I9. Verification Checklist preserved
- Same rule as I8 for `Verification Checklist` heading

### I10. No LLM config drift during iterative skill evolution
- Iterative skills (`/self-evolve`, `/autoloop`, `/autoresearch`) MUST NOT modify these fields in skill YAML frontmatter:
  - `model:` (haiku/sonnet/opus)
  - `temperature:`
  - `reasoning_effort:`
  - `max_tokens:`
- These are operator-level decisions, not improvement targets
- Detection in diff → **ROLLBACK**
- Why: LLM config changes cause broad regressions that mask the effect of every other harness change. Per AHE (arXiv:2604.25850): "LLM config changes consistently cause broad, hard-to-diagnose regressions."
- Manual operator changes outside `/self-evolve` runs are allowed (this invariant applies only to iterative skill evolution flows)

## Mechanism

- Run invariants AFTER score evaluation (ε), BEFORE commit (κ)
- Invariant failure takes precedence over score improvement — never commit unsafe even if scoreful
- Log the failed invariant to trace (TSV column `invariant_violation`)
- After rollback: count as "discarded" in optstate change_ledger
- 3 consecutive invariant violations in same skill → STOP, escalate to user

## Adding new invariants

When failure post-mortems reveal a class of regression, add an invariant here rather than adding ad-hoc checks in the skill. Central rule → all iterative skills benefit.

## Why not put these in code?

For now, invariants are checked by the skill's Critic gate (human-in-the-agent). Future: `tools/check-invariants.py` called by a PostToolUse hook on Edit. Keeping as rule first allows iteration without code complexity.
