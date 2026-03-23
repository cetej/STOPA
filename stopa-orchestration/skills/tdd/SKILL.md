---
name: tdd
description: Use when implementing any feature or bugfix where tests exist or should exist. Trigger on 'tdd', 'test first', 'red green refactor', 'write test', 'napiš test'. Do NOT use for exploratory code, prototypes, one-off scripts, or projects without test infrastructure. Do NOT use when user just wants to run existing tests (use Bash directly).
argument-hint: [feature or bug to implement with TDD — e.g. 'add validation to Phase 7 captions', 'fix photo_offset indexing']
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Edit, Write, Agent
model: sonnet
effort: medium
maxTurns: 25
---

# TDD — Test-Driven Development

You implement features and fixes using strict RED-GREEN-REFACTOR discipline. You write the test first, watch it fail, then write minimal code to pass.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If you didn't watch the test fail, you don't know if it tests the right thing.

## Process

### Step 1: Understand the target

Parse ARGUMENTS to determine what to implement:
- Feature request → identify the behavior to test
- Bug report → identify the failing condition to reproduce
- Read CLAUDE.md for test framework, project conventions, run commands

Find existing tests:
```
Glob: **/test*/**  **/tests/**  **/*_test.*  **/*test_*.*  **/*.spec.*
```

Identify test framework (pytest, jest, vitest, unittest, etc.) and patterns used.

### Step 2: RED — Write a failing test

Write ONE minimal test that describes the desired behavior:
- Test the public interface, not internals
- Name it clearly: `test_<what>_<condition>_<expected>`
- Use arrange-act-assert structure
- Include edge case if the behavior involves boundaries

Run the test. It MUST fail. If it passes:
- Your test doesn't test what you think → rewrite
- Feature already exists → verify and report to user

Show the failure output to prove it tests the right thing.

### Step 3: GREEN — Write minimal code to pass

Write the SIMPLEST code that makes the test pass:
- No optimization
- No "while I'm here" improvements
- No handling of cases the test doesn't cover
- Hardcoded values are OK if they pass the test (refactor later)

Run the test. It MUST pass now. If it doesn't:
- Fix the implementation, not the test
- If stuck after 3 attempts → report to user, don't thrash

Run ALL tests (not just the new one) to check for regressions.

### Step 4: REFACTOR — Clean up with green tests

Now improve the code while keeping tests green:
- Remove duplication
- Improve names
- Extract helpers if pattern repeats 3+×
- Simplify logic

After each refactor step, run tests to confirm green.

### Step 5: Next cycle or done

If more behavior is needed:
- Return to Step 2 with the next test
- Each cycle should be small: 1 test → 1 behavior

If feature is complete:
- Run full test suite
- Report summary

## Output Format

After each RED-GREEN-REFACTOR cycle, report:

```
## TDD Cycle [N]
**RED**: [test name] — tests [what behavior]
**Failure**: [actual failure message — proof it tests the right thing]
**GREEN**: [what code was written to pass]
**REFACTOR**: [what was improved, or "no refactoring needed"]
**Tests**: [X passed, Y total, 0 regressions]
```

Final report:

```
## TDD Summary
**Feature**: [what was implemented]
**Cycles**: [N RED-GREEN-REFACTOR cycles]
**Tests added**: [count]
**Test coverage**: [which behaviors are covered]
**Regressions**: [none, or list]
```

## Anti-Rationalization Defense

| Rationalization | Reality | Do Instead |
|----------------|---------|------------|
| "I'll write tests after the code works" | You won't know what the test proves | Write test first, always |
| "This is too simple to need a test" | Simple code breaks in integration | Test it anyway — it's fast |
| "Let me write all tests first, then implement" | Batch mode loses RED feedback | One test at a time |
| "Test passes, I can skip refactor" | Tech debt accumulates per cycle | At least evaluate, then skip consciously |
| "I need to refactor before I can test" | Refactoring without tests is dangerous | Write characterization test first |
| "The test framework isn't set up" | Setup IS the first task | Set up framework, then TDD |

## Rules

- NEVER write production code before a failing test
- NEVER modify a test to make it pass (fix the code instead)
- ONE test per cycle — don't batch
- Run ALL tests after GREEN, not just the new one
- If no test framework exists, set one up first (ask user for preference)
- Report in Czech if user's request is in Czech
