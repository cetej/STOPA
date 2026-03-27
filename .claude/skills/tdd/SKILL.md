---
name: tdd
description: Use when implementing features via test-driven development cycle. Trigger on 'TDD', 'test first', 'red-green-refactor'. Do NOT use when tests already exist and pass.
argument-hint: <feature description> [--framework pytest|jest|vitest]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
effort: high
maxTurns: 25
disallowedTools: Agent
---

# TDD — Red-Green-Refactor Enforcer

You implement features using strict test-driven development. You NEVER write implementation before the test. You NEVER skip the refactor step.

## Shared Memory

1. Grep `.claude/memory/learnings/` for test patterns, framework conventions
2. Read `CLAUDE.md` for project test conventions (framework, file structure, naming)

## Process

### Phase 0: Setup

1. Parse `$ARGUMENTS` — what feature to implement
2. Detect test framework:
   - Python: look for `pytest.ini`, `pyproject.toml [tool.pytest]`, `conftest.py`
   - JS/TS: look for `jest.config.*`, `vitest.config.*`, `package.json` scripts
   - If unclear: ask user
3. Find existing test patterns: `Glob **/*test*` or `**/*spec*`
4. Report: "Using <framework>, tests in <directory>, naming pattern: <pattern>"

### Phase 1: RED — Write Failing Test

1. Write a test that describes the desired behavior
2. The test MUST:
   - Test ONE specific behavior (not a kitchen-sink test)
   - Have a descriptive name: `test_<what>_<when>_<then>` or `it('should <behavior>')`
   - Import the module/function that doesn't exist yet (or exists but lacks the feature)
3. Run the test: `bash <test command>`
4. **VERIFY RED**: The test MUST fail. If it passes → the feature already exists or the test is wrong. Report and stop.

### Phase 2: GREEN — Minimal Implementation

1. Write the MINIMUM code to make the test pass
2. Rules:
   - No extra features, no "while I'm here" improvements
   - No premature abstractions — hardcode if it makes the test pass
   - No error handling beyond what the test requires
3. Run the test again
4. **VERIFY GREEN**: The test MUST pass. If it fails:
   - Read the error carefully
   - Fix the implementation (not the test!)
   - Re-run. Max 3 attempts, then stop and report.

### Phase 3: REFACTOR

1. Now that the test passes, improve the code quality:
   - Remove duplication
   - Extract meaningful names
   - Simplify logic
2. Run ALL tests (not just the new one): `bash <test command --all>`
3. **VERIFY GREEN**: All tests must still pass after refactor

### Phase 4: Next Cycle (if applicable)

If the feature needs more test cases:
1. Identify the next behavior to test
2. Go back to Phase 1 (RED)
3. Repeat until feature is complete

Report each cycle:
```
Cycle 1: test_parse_valid_input → PASS (RED→GREEN→REFACTOR)
Cycle 2: test_parse_empty_input → PASS (RED→GREEN→REFACTOR)
Cycle 3: test_parse_malformed_input → PASS (RED→GREEN→REFACTOR)
```

### Phase 5: Final Report

```markdown
## TDD Report: <feature>

**Cycles**: N
**Tests added**: N
**All tests passing**: yes/no

| Cycle | Test | RED | GREEN | REFACTOR |
|-------|------|-----|-------|----------|
| 1 | test_... | fail | pass (1 attempt) | pass |
| 2 | test_... | fail | pass (2 attempts) | pass |
```

## Error Handling

- Test framework not found → ask user to install, report command
- Test passes in RED phase → feature already exists, stop and report
- GREEN fails after 3 attempts → stop, show errors, ask user for guidance
- Refactor breaks tests → revert refactor, keep GREEN state

## Rules

1. **NEVER write code before the test** — this is the cardinal rule
2. **NEVER modify a test to make it pass** — fix the implementation
3. **One behavior per cycle** — small, focused increments
4. **Run tests after EVERY change** — no "I think this works"
5. **Refactor is mandatory** — don't skip it, even if the code "works"
6. **All tests must pass** — not just the new one
