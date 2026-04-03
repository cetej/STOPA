# Session Completion Contract (standard + deep tier)

**Skip for light and farm tiers.** Light tasks are fast enough that contract overhead isn't worth it. Farm tasks have mechanical verification built in.

Agents suffer from **context anxiety** — as context grows, they become increasingly desperate to end the session, declaring "done" prematurely or implementing A' instead of A (@systematicls). The completion contract is an independent audit that prevents premature session closure.

## Contract Definition (written in Phase 3, enforced in Phase 5)

During Phase 3 (Decomposition), the orchestrator MUST write a machine-checkable contract to `state.md` under the plan:

```markdown
### Completion Contract

| # | Assertion | Check Method | Status |
|---|-----------|-------------|--------|
| CC1 | <what must be true> | <how to verify — command, grep, test> | pending |
| CC2 | <what must be true> | <how to verify> | pending |
| CC3 | <what must be true> | <how to verify> | pending |
```

## Rules for contract assertions

- Derived from success criteria + acceptance criteria (not new requirements)
- Must be independently verifiable (a command you can run, a grep you can check)
- 3-7 assertions total — cover the most critical outcomes, not every subtask
- At least 1 assertion must test integration (not just individual subtask completion)
- Example: "CC1: `ruff check src/ --select E` returns 0 violations" (not "code is clean")
- Example: "CC2: `grep -r 'old_function_name' src/` returns 0 matches" (not "refactoring is complete")
- Example: "CC3: `python -c 'from app.auth import validate_token; print(validate_token.__doc__)'` runs without error"

## Contract Enforcement (Phase 5)

After all acceptance criteria pass, spawn an independent agent to audit the contract:

```
Agent(model: "haiku", prompt: "
  You are an independent contract auditor. Your ONLY job is to verify
  whether the completion contract is satisfied.

  Completion Contract:
  <paste contract table>

  For each assertion:
  1. Run the check method exactly as written
  2. Record: PASS (check succeeded) or FAIL (check failed, with output)
  3. Do NOT interpret, explain, or soften failures — just report

  Output a table:
  | # | Assertion | Result | Evidence |
  |---|-----------|--------|----------|

  Final: ALL_PASS or BLOCKED (list failing assertions)
")
```

## If contract audit returns BLOCKED

1. The session CANNOT be declared complete
2. List the failing assertions to the orchestrator
3. Orchestrator must fix the specific failures (re-dispatch to Phase 4 for affected subtasks)
4. Re-run contract audit after fixes
5. Max 2 contract audit rounds — if still failing after 2nd round, escalate to user

## If contract audit returns ALL_PASS

- Proceed to critic and Phase 6 normally
- Record in state.md: "Contract: ALL_PASS (N/N assertions verified)"

**Cost:** 1 × Haiku agent per audit round. Cheap insurance against premature completion claims.
