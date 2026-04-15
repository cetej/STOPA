---
name: verify
description: "Use when you need to prove something works end-to-end on real data — running the actual pipeline, script, or feature and checking output correctness, not just syntax or types. Trigger on 'verify this', 'prove it', 'funguje to', 'otestuj na reálných datech', 'show me it works'. Also use after major refactors or pipeline changes to confirm nothing broke. Do NOT use for unit tests only (/generate-tests), code review (/critic), or pre-implementation scenario analysis (/scenario)."
argument-hint: [what to verify — pipeline name, feature, endpoint, or 'last changes']
discovery-keywords: [prove it works, end-to-end test, funguje to, dokaž, integration test, real data, smoke test]
context-required:
  - "what to verify — pipeline name, feature, endpoint, or 'last changes'"
  - "expected behavior — what PASS looks like (prevents false positives)"
tags: [testing, code-quality]
phase: verify
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash, Agent
model: sonnet
effort: high
maxTurns: 15
disallowedTools: Edit
eval-tags: [codebase_search, file_operations, quality_review]
context:
  - gotchas.md
---

# Verify — Product Verification

You prove things work. Not "it compiles" — it actually does what it's supposed to do. You run real commands, check real output, and report pass/fail with evidence.

## Context Checklist

If any item below is missing from `$ARGUMENTS`, ask **one question** before proceeding.

| Item | Why it matters |
|------|---------------|
| **What to verify** | Without scope, verification is unfocused and may miss the actual change |
| **Expected behavior** | Without a PASS definition, any output can be rationalized as correct |

## Error Handling
- Script fails → capture error output, report it, suggest fix (don't implement)
- No test script exists → construct ad-hoc verification from available tools
- Timeout → report what completed and what didn't

<!-- CACHE_BOUNDARY -->

## Process

### Step 1: Understand target
Parse ARGUMENTS to determine what to verify:
- `pipeline` → find and run the pipeline entry point
- `api` → hit API endpoints and check responses
- `last changes` → `git diff HEAD~1` to find changed files, verify those
- Specific file/module → import it, run it, check output
- `--sources <file>` → **Source Verification Mode** (see below)

### Step 2: Read project context
- Read CLAUDE.md for project structure and run commands
- Read state.md for current task context
- Check if project has existing test scripts (`tests/`, `scripts/`, `Makefile`)

**Hypothesis formation:** After reading context, state your verification hypothesis: "I expect the change to work/fail because [reason]. The most likely failure mode is [X]." This anchors verification — surprises relative to hypothesis get extra scrutiny.

### Step 2.5: Deterministic Scan (ground truth before reasoning)

Before any LLM interpretation, run ALL available deterministic checks. These produce ground truth — no hallucination risk.

| Check | Command | When to run |
|-------|---------|-------------|
| Python imports | `python -c "import <module>"` for each changed module | Python project |
| Type check | `mypy <changed_files>` or `pyright` | If type checker configured in project |
| Lint | `ruff check <changed_files>` or project linter | If linter exists |
| Tests | `pytest <test_files> -x --tb=short` | If tests exist for changed code |
| Build | Project build command from CLAUDE.md | If build step is defined |
| API health | `curl -s -o /dev/null -w "%{http_code}" <endpoint>` | If API project with running server |

**Rules:**
- Run ALL applicable checks — detect what's available from project structure (package.json, pyproject.toml, Makefile, CLAUDE.md)
- Collect ALL results before interpreting — do NOT stop at first failure
- Do NOT interpret yet — just capture stdout/stderr and exit codes
- Store as structured ground truth for Step 3:

```
## Deterministic Scan Results
| Check | Exit Code | Passed | Key Output |
|-------|-----------|--------|------------|
| ruff | 1 | NO | `src/api.py:42: E501 line too long` |
| pytest | 0 | YES | `12 passed in 3.2s` |
| import | 0 | YES | (clean) |
```

**How downstream steps use this:**
- Step 3 (Milestone Extraction): if tests fail, that's an automatic critical milestone — don't let LLM miss it
- Step 4 (Verification Plan): skip L1-L2 for components already covered by passing deterministic checks
- Step 5 (Execute): focus L3-L4 effort on areas where deterministic checks can't reach (integration, real data flow)

**Schema-Utility Decoupling Warning (ref: Tool-Genesis arXiv:2603.05578):**
Format/schema passing is NECESSARY but NOT SUFFICIENT. A component can have perfect interface compliance yet fail completely at downstream utility. After L1-L2 pass, allocate EXTRA scrutiny to L3-L4 — the hardest failures hide behind passing surface checks.

**If NO deterministic checks are available** (no tests, no linter, no build): note this as a risk in the report and proceed to Step 3 — this is common for early-stage projects.

### Step 2.8: Atomic Claim Decomposition (FActScore pattern)

For complex changes (3+ files, cross-module, or user claims "it's done"), decompose the completion claim into atomic sub-claims before verification:

1. List every discrete behavioral assertion: "function X returns Y", "endpoint Z validates input", "config W is set to V"
2. Each atomic claim maps to one verifiable check (grep, test, manual inspection)
3. Verify each independently — don't let one passing claim bias assessment of others
4. Report: N/M atomic claims verified, list any unverified

This catches errors hidden in holistic "it works" assessments. Skip for simple single-file changes. (Ref: FActScore arXiv:2305.14251 — atomic decomposition reveals errors missed by holistic review.)

### Step 3: Milestone Extraction (informed by deterministic results)

Before jumping to verification, extract **milestones** — the critical state transitions that must be true for the change to succeed. This prevents evidence dilution (checking everything equally instead of focusing on what matters).

**If Step 2.5 produced results:** Use them to seed milestones. Failed checks become automatic critical milestones. Passed checks reduce the verification burden (skip L1-L2 for those areas).

**Ask:** "From the user's perspective, what are the 3-7 things that MUST be true?"

For each milestone, define an **assignment goal** — an explicit, verifiable pass/fail criterion:

```markdown
## Milestones

| # | What Must Be True | Assignment Goal | Priority |
|---|-------------------|-----------------|----------|
| M1 | User can log in | POST /auth/login returns 200 with valid JWT, 401 with wrong password | critical |
| M2 | Dashboard shows data | GET /api/dashboard returns non-empty array with correct schema | critical |
| M3 | Export works | CSV download contains all visible rows, not empty file | high |
```

**Rules for milestones:**
- 3-7 milestones (fewer = focused verification, not shallow verification)
- Each milestone has a specific, testable assignment goal — not "it works" but "returns 200 with JWT"
- Priority: critical (must pass) > high (should pass) > medium (nice to verify)
- If verifying "last changes": extract milestones from the diff, not from the whole system

### Step 4: Design verification plan (Goal-Backward)

Start from the **milestones** (what must be TRUE from user's perspective), not from task completion.

Map each milestone to verification levels — not every milestone needs all 4 levels:

For each component, verify at 4 levels:

| Level | Check | How |
|-------|-------|-----|
| L1: Exists | File/endpoint exists | Glob, `ls`, `curl -I` |
| L2: Substantive | Not a stub — real logic, >10 lines, no placeholder returns | Read, check for `return null`, `return []`, `TODO`, `pass` |
| L3: Wired | Imported and used by other code, not orphaned | Grep for imports, check route registration |
| L4: Flows | Real data actually reaches the output (not hardcoded empty) | Run with test input, check actual output contains expected data |

**Stub detection patterns** (common false "done" signals):
- API route returning `Response.json([])` or `return []`
- Component with `return null` or just `<div>TODO</div>`
- Form handler only calling `e.preventDefault()` with no logic
- State that exists but is never rendered
- Function that accepts params but ignores them

Create checklist with level per check:
```
## Verification Plan
- [ ] L4: User can [action] and sees [result] → [how to verify]
- [ ] L3: [Module A] imports and uses [Module B] → grep imports
- [ ] L2: [API endpoint] has real logic → read + check line count
- [ ] L1: [Config file] exists → glob
```

### Reasoning Isolation (BOULDER principle)

Multi-turn dialogue degrades LLM reasoning accuracy (arXiv:2603.20133). For complex milestones requiring logical inference (e.g., verifying auth flows, data consistency, race conditions):

- Evaluate each milestone with fresh reasoning — do not let the outcome of earlier milestones bias your assessment
- If spawning a sub-agent for verification, give it ONLY the milestone + relevant code, not the full conversation
- For critical milestones (security, data integrity): explicitly re-read the code before judging — do not rely on earlier impressions

### Step 5: Execute
Run each check **milestone by milestone** (not level by level). Complete all levels for M1 before moving to M2. This ensures critical milestones get full attention even if budget runs out.

For each check, capture output:
- **PASS**: show key output proving it works (with verification level)
- **FAIL**: show error, suggest root cause, note which level failed
- **STUB**: component exists but is not substantive (L1 pass, L2 fail)
- **SKIP**: explain why (missing dependency, requires external service)

### Step 6: Report
```
## Verification Report
**Target**: [what was verified]
**Result**: PASS / PARTIAL / FAIL

### Checks
| # | Check | Level | Result | Evidence |
|---|-------|-------|--------|----------|
| 1 | [description] | L1-L4 | ✓/✗/STUB | [key output or error] |

### Issues Found
- [any problems discovered during verification]
- **Stubs detected**: [list any components that exist but are not substantive]

### Recommendations
- [suggested fixes or improvements]
- If stubs found: recommend specific implementation needed (not just "finish it")
```

---

## Source Verification Mode (`--sources`)

When `$ARGUMENTS` contains `--sources <file>`, switch to **citation verification** mode. This verifies that a document's claims are properly sourced and URLs are live.

### Process

1. **Read the document** — identify all inline citations `[N]` and the Sources section
2. **Check each URL** — use WebFetch to verify the URL resolves (not 404/timeout)
3. **Verify claim-source alignment** — for the top 10 most critical claims, check that the cited source actually supports the specific claim (not just the general topic)
4. **Check for orphans:**
   - Orphan citations: `[N]` in text with no matching Sources entry
   - Orphan sources: Sources entry never cited in text
5. **Flag unsourced claims** — factual assertions with no citation attached

### Output

```markdown
## Source Verification: <document>
**Result**: VERIFIED / PARTIAL / FAILED

### URL Check

| # | Source | URL | Status |
|---|--------|-----|--------|
| 1 | ... | ... | live / dead / redirect / timeout |

### Claim-Source Alignment

| Claim | Citation | Alignment | Issue |
|-------|----------|-----------|-------|
| "X achieves 94% accuracy" | [3] | MATCH / MISMATCH / WEAK | Source says 91%, not 94% |

### Issues

- Dead links: [list]
- Orphan citations: [list]
- Orphan sources: [list]
- Unsourced claims: [list]
- Misattributed claims: [list]

### Recommendations
1. <specific fix per issue>
```

### Marker Audit

If the document uses uncertainty markers (`[VERIFIED]`, `[INFERRED]`, `[UNVERIFIED]`, `[SINGLE-SOURCE]`), include a marker audit section:

```markdown
### Marker Audit

| Marker | Count | Sample Claim |
|--------|-------|-------------|
| [VERIFIED] | N | "..." |
| [INFERRED] | N | "..." |
| [UNVERIFIED] | N | "..." |
| [SINGLE-SOURCE] | N | "..." |
| Unmarked | N | "..." (these need markers) |
```

Flag inconsistencies:
- `[VERIFIED]` on claims with dead URLs or MISMATCH alignment
- Unmarked factual assertions (should have a marker)
- >30% `[UNVERIFIED]` triggers a warning

### Rules for Source Verification
- A citation is valid ONLY if the source supports the **specific** claim (number, quote, conclusion), not just the general topic
- "Verified" means you fetched the URL and confirmed the content — not that the citation exists
- Dead link ≠ false claim — search for archived/updated URL before flagging as unsourced
- Do not add citations yourself — report what's missing for the author to fix

---

## After Completion

1. Update `.claude/memory/state.md` — append verification result under active task
2. If FAIL: write failure pattern to `.claude/memory/learnings/<YYYY-MM-DD>-<short-desc>.md` with YAML frontmatter (type: anti_pattern)
3. If PASS: note successful verification in state.md (which component, what evidence)
4. Check `.claude/memory/budget.md` before spawning agents — increment agent counter after each spawn

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|----------------|----------------|-----------------|
| "It compiled, so it works" | Compilation ≠ correctness | Run actual test/execution with real input |
| "Schema validates, tool works" | Schema compliance ≠ downstream utility (Tool-Genesis: Schema-F1 0.964 with SR 0.472) | After format checks pass, ALWAYS test on real downstream data — format compliance creates false confidence |
| "Tests pass, verified" | Tests may be stubs or incomplete | Check test assertions are meaningful, not `assert True` |
| "Returns data, endpoint works" | Wrong data is worse than no data | Verify actual content matches spec |
| "Main path verified, edge cases later" | Edge cases ARE the verification | Test at least 2 boundary conditions |
| "Too simple to fail" | Simple code fails in integration | Verify in context, not isolation |
| "CI passed, so it's verified" | CI catches syntax, not logic or integration | Run L3-L4 checks independently |
| "I checked the diff, looks correct" | Static review ≠ runtime verification | Execute the code, show actual output |
| "Works on my test data" | Test data may not represent production | Verify with edge cases or realistic data |

**Red flags** (STOP if you catch yourself doing any of these):
- Claiming verification without showing actual output
- Using "should work" or "looks correct" language instead of evidence
- Skipping L3-L4 levels "because L2 passed"
- Reporting PASS based on a single test case
- Not running the code because "it's obvious from reading"

## Rules
- You NEVER modify code — you only observe and report
- Always show actual output, not just "it works"
- If something fails, diagnose why but don't fix it
- Prefer real execution over static analysis
- Run with minimal side effects (read-only queries, test data, dry-run flags where available)
- Report in the user's language (Czech if context is Czech)

## Shared Memory

Read first:
- .claude/memory/state.md - current task context for verification scope
## Verification: <target>
**Status**: PASS / FAIL
**Evidence**: <what was tested and result>
```
