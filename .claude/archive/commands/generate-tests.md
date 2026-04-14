---
name: generate-tests
description: Use when generating tests for existing code without implementing new features. Trigger on 'generate tests', 'add tests', 'test coverage', 'write tests for'. Do NOT use for TDD with new implementation (/tdd), bug reproduction (/reproduce), or test-then-fix workflows (/fix-issue).
argument-hint: [file, module, function, or directory to generate tests for — e.g. 'tests for utils.py', 'cover the auth module']
discovery-keywords: [test generation, add coverage, test suite, unit tests, testuj, přidej testy, pokrytí, cover existing code, missing tests]
tags: [testing, code-quality]
phase: verify
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
model: sonnet
effort: medium
maxTurns: 25
input-contract: "user or orchestrator → file/module/function path → exists in codebase"
output-contract: "test file(s) → project test directory → all tests pass on current code"
effects: ["new test files exist covering specified code", "all new tests pass on current code", "no production code modified"]
---

# Generate Tests — Pure Test Generation for Existing Code

You generate comprehensive test suites for existing code. You do NOT implement new features or modify production code. Tests must pass on the current implementation — they capture existing behavior.

## The Iron Law

```
ALL GENERATED TESTS MUST PASS ON CURRENT CODE
```

You are documenting behavior that EXISTS, not behavior you wish existed. If a test fails, the test is wrong — not the code.

<!-- CACHE_BOUNDARY -->

## Why This Skill Exists

Test generation is a distinct atomic skill (arXiv:2604.05013 — "Scaling Coding Agents via Atomic Skills"). TDD couples test writing with implementation. But many real-world needs are pure test generation:
- Adding coverage to legacy code before refactoring
- Generating regression tests before a migration
- Documenting implicit behavior of undocumented functions
- Strengthening CI gates on untested modules

The paper shows that joint training on isolated test generation (separate from code editing) yields +31.5% improvement — the largest gain among all 5 atomic skills.

## Process

### Step 1: Analyze the target

Parse ARGUMENTS to identify what to test:
- Specific file(s) → read them fully
- Module/directory → glob for all source files, read public APIs
- Function name → locate with grep, read context

Understand the code:
- **Public API**: functions, classes, methods exposed to callers
- **Input types**: what parameters, what ranges, what edge cases
- **Output types**: return values, side effects, exceptions
- **Dependencies**: what does the code call? Mock candidates vs real integration
- **Implicit contracts**: what does the code assume about its inputs?

### Step 2: Discover test infrastructure

```
Glob: **/test*/**  **/tests/**  **/*_test.*  **/*test_*.*  **/*.spec.*
```

Identify:
- Test framework (pytest, jest, vitest, unittest, go test, etc.)
- Test patterns (fixtures, factories, mocking conventions)
- Test location convention (co-located vs separate test directory)
- Existing test configuration (conftest.py, jest.config, etc.)
- Coverage tool if present (pytest-cov, istanbul, etc.)

If no test infrastructure exists: set it up first (minimal config), then proceed.

### Step 3: Design test matrix

For each function/method/class under test, identify test cases across these dimensions:

**Core behavior** (must have):
- Happy path with typical inputs
- Return value / output correctness
- State changes / side effects

**Boundary conditions** (should have):
- Empty inputs ([], "", None, 0)
- Single element inputs
- Maximum/minimum values
- Off-by-one scenarios

**Error handling** (should have):
- Invalid input types
- Missing required parameters
- Expected exceptions / error responses

**Integration points** (if applicable):
- Interaction with dependencies
- Correct delegation to sub-components

**Mutation resilience** (paper-inspired — "tests must fail on semantically plausible buggy variants"):
- For critical functions: mentally simulate common bugs (off-by-one, wrong operator, swapped args) and verify at least one test would catch each

Prioritize: core behavior → boundaries → errors → integration → mutation. Don't generate 50 trivial tests when 12 meaningful ones cover more.

### Step 4: Generate tests

Write tests following project conventions:

**Naming**: `test_<function>_<scenario>_<expected>` or project convention
**Structure**: Arrange-Act-Assert (AAA) pattern
**Independence**: each test runs in isolation, no shared mutable state
**Readability**: test name + assertion message should explain what broke without reading the test body

**Grouping**: one test file per source module, test classes/describes per function if the function has 4+ test cases.

**Mocking strategy**:
- Mock external I/O (network, filesystem, databases) unless integration tests are explicitly requested
- Don't mock the code under test
- Don't mock internal helpers — test through the public API
- Use the project's existing mock patterns

### Step 5: Run and validate

Run the full new test suite:
1. **ALL tests MUST pass** on current code
2. If any test fails → the test is wrong. Fix the test, not the code.
3. Run existing tests too — ensure no regressions from test infrastructure changes

Show the test run output as proof.

### Step 6: Coverage analysis (if tools available)

If coverage tool is present:
- Run coverage on the target module WITH new tests
- Report lines/branches covered vs uncovered
- Highlight any critical uncovered paths

If no coverage tool: skip this step, don't install one without asking.

### Step 7: Report

```
## Test Generation Report

**Target**: [file/module/function tested]
**Framework**: [pytest / jest / ...]
**Tests written**: [N tests in M files]

### Test Matrix

| Function | Happy Path | Boundaries | Errors | Integration | Total |
|----------|-----------|-----------|--------|-------------|-------|
| func_a   | 2         | 3         | 1      | 0           | 6     |
| func_b   | 1         | 2         | 2      | 1           | 6     |

### Coverage (if measured)
**Before**: X% lines, Y% branches
**After**: X% lines, Y% branches
**Delta**: +Z% lines, +W% branches

### All Tests Pass
```
[test run output]
```

### Not Covered (conscious omissions)
- [reason for skipping: private internal, trivial getter, etc.]
```

## Composition with Other Skills

| Pipeline | Generate-tests role |
|----------|-------------------|
| Pre-refactoring safety net | `/generate-tests` → then refactor with confidence |
| Post-implementation coverage | `/tdd` or `/fix-issue` → `/generate-tests` for untested edges |
| `/orchestrate` quality gate | Add as subtask: "generate tests for changed modules" |
| Audit / compliance | `/generate-tests --coverage` → coverage report for stakeholders |
| Pre-migration insurance | `/generate-tests` → `/scout` → migrate → re-run tests |

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "This code is too messy to test" | Messy code is the code that MOST needs tests before you can safely refactor it | Test the public API surface — internal mess is the code's problem, not yours |
| "I need to refactor first to make it testable" | Refactoring without tests = flying blind | Write characterization tests first (test current behavior, even if ugly) |
| "100% coverage is the goal" | Coverage without meaningful assertions is theater | Focus on behavior-covering tests, not line-covering tests |
| "I'll mock everything for isolation" | Over-mocking tests your mocks, not your code | Mock I/O boundaries only — test real logic with real objects |
| "A failing test means I found a bug" | No — you're documenting EXISTING behavior, not DESIRED behavior | Fix the test to match actual behavior. Report the bug separately (/reproduce) |
| "Let me also fix this bug I found" | Scope creep — you're generating tests, not fixing bugs | Document the bug as a comment in the test, hand off to /reproduce or /fix-issue |

## Red Flags

STOP and re-evaluate if any of these occur:
- Modifying production code to make tests pass
- Writing tests that fail on current code (except if targeting a known bug — use /reproduce instead)
- Generating more than 30 tests for a single function (test design issue)
- Mocking more than 3 layers deep (testing your mocks, not the code)
- Spending more time on test infrastructure than on actual tests

## Verification Checklist

- [ ] All new tests pass on current code (shown in output)
- [ ] Existing tests still pass (no regressions from setup changes)
- [ ] Tests follow project naming and location conventions
- [ ] Each test has a clear name describing what it verifies
- [ ] No production code was modified
- [ ] Edge cases and boundaries are covered (not just happy path)
- [ ] Mock usage is minimal and limited to I/O boundaries

## Rules

- You NEVER modify production code — only create test files
- All tests must pass on current code — failing tests mean you wrote the test wrong
- Follow the project's existing test patterns, framework, and conventions
- If you discover a bug while testing: note it in the report, don't fix it
- Prefer fewer meaningful tests over many trivial ones
- Don't install new test frameworks without asking — use what's already there
- Report in Czech if user's request is in Czech
