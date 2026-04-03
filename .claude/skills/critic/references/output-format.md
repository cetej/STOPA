# Critic Report — Full Output Format (STANDARD / DEEP)

```markdown
## Critic Report: <target>
**Triage path**: STANDARD / DEEP
**Pipeline**: Selector (N milestones) -> Verifier (X pass, Y fail) -> Reviewer (Z concerns) -> Judge

### Impact Radius

| Changed File | Direct Dependents | Risk |
|-------------|-------------------|------|
| src/auth/jwt.ts | src/routes/api.ts, src/middleware/auth.ts | high (auth path) |

**Blast radius**: N files changed -> M dependents affected

### Dynamic Verification Results

| Check | Files | Status | Output |
|-------|-------|--------|--------|
| Python import | src/auth.py | PASS | -- |
| Type check | src/auth.py, src/api.py | FAIL | src/api.py:15: incompatible type |

**Milestone overrides:** (list any Phase 2 PASS->FAIL overrides, or "none")

### Milestone Summary

| # | Assignment Goal | Verdict | Key Evidence |
|---|----------------|---------|--------------|
| M1 | ... | PASS/FAIL | ... |

### Reviewer Concerns

| # | Category | Concern |
|---|----------|---------|
| C1 | ... | ... |

### Scoring Rubric

| Criteria | Weight | Score (1-5) | Evidence |
|----------|--------|-------------|----------|
| Correctness | 0.30 | ? | |
| Completeness | 0.25 | ? | |
| Code Quality | 0.20 | ? | |
| Safety | 0.15 | ? | |
| Test Coverage | 0.10 | ? | |
| **Weighted Average** | | **?.?** | |

### Verdict: PASS / WARN / FAIL

### Issues Found

| # | Severity | Category | Description | Location |
|---|----------|----------|-------------|----------|
| 1 | high | correctness | ... | file:line |

### Inline Annotations

Quote specific code and annotate with issue IDs from the Issues table:

> `if (user.role === "admin") return true;`  (auth.ts:42)
**[#1] high/correctness:** Bypasses all permission checks for admins -- needs granular resource-level validation.

Rules for annotations:
- Every issue from the Issues table SHOULD have a corresponding annotation
- Quote the exact code being critiqued (with file:line)
- Reference the issue ID so annotations link back to the summary table
- Keep annotations concise -- problem + why it matters

### What's Good
- <positive observations -- always include>

### Recommendations
1. <specific, actionable fix>

### Verdict Rationale
<why PASS/WARN/FAIL -- what drove the scores, which milestones/concerns were decisive>

### Gate Proposals

If the same issue type was found 2+ times in this review (or across recent reviews), propose a new quality gate:

| Proposed Gate | Check | Evidence |
|---------------|-------|----------|
| <gate name> | <how to verify> | <issue #s that triggered this> |

If no new gates warranted, write: "No new gates proposed."

If `quality-gates.md` exists, append approved proposals to its Gate Proposal Log.

### Reflector Summary (for /scribe)
- **Error type:** [logic bug | missing case | wrong abstraction | spec misread | none]
- **Root cause:** [1 sentence -- what caused the issues, or "N/A" if PASS with no issues]
- **Correct approach:** [what should have been done differently, or "N/A"]
- **Key insight:** [what to remember for future sessions -- fill this even on PASS, because clean reviews produce insights about good patterns that inform future reviews]
- **Learnings activated:** [list any learnings/ files that were retrieved during review, or "none"]
```

**Reflector Summary rules:**
- Always include at end of STANDARD/DEEP reports (skip for QUICK)
- "Key insight" is mandatory -- even clean PASS reviews produce insights about good patterns
- "Learnings activated" helps /scribe track which learnings are being used (drives `uses` counter)
