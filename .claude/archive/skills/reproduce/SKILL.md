---
name: reproduce
description: Use when creating a standalone reproduction of a bug or failure — a failing test or script that proves the issue exists. Trigger on 'reproduce', 'repro', 'create failing test', 'prove the bug'. Do NOT use for fixing the bug (/fix-issue), full TDD cycles (/tdd), or crash triage (/incident-runbook).
argument-hint: [bug description, issue number, error message, or 'last failure']
discovery-keywords: [reproduce bug, failing test, repro script, prove issue, minimal reproduction, reprodukuj, reprodukce, bug exists]
tags: [debugging, testing]
phase: verify
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
model: sonnet
effort: medium
maxTurns: 15
input-contract: "user or orchestrator → bug description + optional issue URL → non-empty"
output-contract: "failing test or script → test file → project test directory or temp script"
effects: ["failing test exists and fails on current code", "reproduction is minimal and deterministic"]
---

# Reproduce — Standalone Issue Reproduction

You create a minimal, deterministic reproduction of a bug. You produce a failing test or script that proves the issue exists. You do NOT fix it.

## The Iron Law

```
PRODUCE THE FAILURE. STOP. HAND OFF.
```

Your job ends when the reproduction fails reliably. Fixing is someone else's job (/fix-issue, /tdd, manual).

<!-- CACHE_BOUNDARY -->

## Why This Skill Exists

Reproduction is a distinct atomic skill (arXiv:2604.05013 — "Scaling Coding Agents via Atomic Skills"). Embedding reproduction inside fix pipelines creates two problems:
1. Fix-issue skips reproduction under time pressure ("I see the bug, let me just fix it")
2. TDD couples reproduction with implementation — you can't stop after RED
3. Systematic-debugging is read-only — it diagnoses but cannot create artifacts

Standalone reproduction forces the discipline: prove the bug exists before touching production code.

## Process

### Step 1: Understand the failure

Parse ARGUMENTS:
- If issue number/URL → fetch with `gh issue view`
- If error message → search codebase for origin
- If "last failure" → check git log, test output, CI logs

Extract:
- **What fails**: expected vs actual behavior
- **Where**: which module/function/endpoint
- **When**: always, intermittent, under specific conditions
- **Severity**: crash, wrong output, data corruption, performance

### Step 2: Locate the affected code

Quick scout (not full /scout — targeted):
```
Grep: error message keywords in codebase
Glob: test files near affected module
```

Identify:
- The function/method exhibiting the bug
- Existing test infrastructure (framework, patterns, test directory)
- Input data that triggers the failure (from issue, logs, or inference)

### Step 3: Create the reproduction

Choose reproduction format based on context:

**Option A: Test case** (preferred — integrates into CI)
- Use the project's test framework (pytest, jest, vitest, unittest...)
- Follow existing test naming conventions
- Name: `test_<module>_<bug_description>` or `test_reproduce_issue_<N>`
- Arrange: set up the minimal state that triggers the bug
- Act: call the function/endpoint with the triggering input
- Assert: check for the expected (correct) behavior — the assertion MUST FAIL on current code

**Option B: Standalone script** (when test framework is impractical)
- Self-contained, no external dependencies beyond the project
- Exits with non-zero code on failure
- Prints clear output: what was expected vs what happened
- Filename: `repro_<issue>.py` or `repro_<description>.sh`

**Minimality principle**: strip everything not needed to trigger the failure. If 3 lines reproduce the bug, don't write 30. The reproduction should be the SMALLEST possible proof.

### Step 4: Validate the reproduction

Run the reproduction:
1. It MUST fail on current code → proves the bug exists
2. If it passes → your reproduction doesn't capture the actual bug. Go back to Step 3.
3. Run it 3× to confirm determinism (unless testing intermittent behavior)

Show the failure output verbatim — this is the proof.

### Step 5: Validate it's the RIGHT failure

Cross-check:
- Does the failure match the reported symptoms?
- Does the assertion test the correct behavior (not a side effect)?
- Would fixing the bug make this test pass? (mental simulation)

If the test fails for a DIFFERENT reason than the reported bug → it's a false reproduction. Fix the test to target the actual issue.

### Step 6: Report and hand off

```
## Reproduction Report

**Bug**: [1-sentence description]
**Source**: [issue URL / error message / user report]

### Reproduction
**File**: [path to failing test/script]
**Framework**: [pytest / jest / standalone / ...]
**Run command**: [exact command to trigger]

### Failure Output
```
[verbatim test/script output showing the failure]
```

### Failure Analysis
**Fails because**: [1-sentence root cause hypothesis]
**Fix scope**: [which files/functions likely need changes]

### Handoff
- To fix: `/fix-issue` or manual edit → then re-run this test
- To TDD: `/tdd` can use this as the RED test
- To investigate deeper: `/systematic-debugging`
```

## Composition with Other Skills

This skill is designed as an **atomic building block** (arXiv:2604.05013):

| Pipeline | Reproduce role |
|----------|---------------|
| `/orchestrate` → bug fix | Step 1: `/reproduce` → Step 2: `/fix-issue` (with reproduction as input) |
| `/systematic-debugging` → fix | `/systematic-debugging` diagnoses → `/reproduce` creates artifact → developer fixes |
| `/tdd` enhancement | `/reproduce` creates RED test → `/tdd` picks up from GREEN phase |
| CI regression | `/reproduce` creates regression test → commit to prevent recurrence |

Orchestrate dispatch hint: when a bug-fix subtask has no existing test, spawn `/reproduce` BEFORE `/fix-issue`.

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "The bug is obvious, I'll just fix it" | Without reproduction you can't prove the fix works | Create the failing test first — it takes 2 minutes |
| "I'll write the test and the fix together" | Coupling reproduction with fix means you never validated the test catches the bug | Write test, watch it fail, STOP. Hand off. |
| "Existing tests cover this" | If existing tests covered it, the bug would have been caught | Write a NEW test that specifically targets this failure |
| "Can't reproduce — must be environment-specific" | You haven't tried hard enough yet | Check env vars, configs, data state. Try Docker/isolation. |
| "The reproduction is complex, let me simplify later" | Complex reproduction = you don't understand the bug yet | Simplify NOW — find the minimal trigger |

## Red Flags

STOP and re-evaluate if any of these occur:
- Writing production code instead of test code
- Reproduction passes on current code (it should FAIL)
- Reproduction has more than 30 lines (probably not minimal)
- Spending more than 10 minutes without a failing test
- Modifying existing tests to make them fail (create NEW tests)

## Verification Checklist

- [ ] Reproduction file exists at a sensible path
- [ ] Running the reproduction produces a FAILURE on current code (shown in output)
- [ ] Failure matches the reported bug symptoms (not a different error)
- [ ] Reproduction is minimal — removing any line breaks it or makes it pass
- [ ] Reproduction is deterministic (fails consistently, not flaky)
- [ ] Run command is documented and copy-pasteable
- [ ] No production code was modified

## Rules

- You NEVER fix the bug — only reproduce it
- Always show the actual failure output as proof
- If you can't reproduce after 3 approaches: report that explicitly with what you tried
- Prefer test-framework tests over standalone scripts (CI integration)
- Follow the project's existing test conventions (naming, location, framework)
- Report in Czech if user's request is in Czech
