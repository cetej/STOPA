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

### Structured Verdict (machine-parseable)

Always include this JSON block — it enables automated quality gates in /orchestrate, skill-chain-engine, and dimensional drift tracking in /eval.

**PARROT principle (arXiv:2604.11626):** Structured multi-dimensional critique with rationale BEFORE scoring prevents reward hacking and enables targeted fixes. Each dimension gets a rationale (WHY this score) and a refine suggestion (HOW to fix).

```json
{
  "verdict": "PASS|WARN|FAIL",
  "score": 3.8,
  "dimensions": {
    "correctness": {"score": 4, "weight": 0.30, "rationale": "All milestones verified with tool output", "refine": null},
    "completeness": {"score": 3, "weight": 0.25, "rationale": "M3 unverified — no test covers new path", "refine": "Add test for the new auth middleware path"},
    "quality": {"score": 4, "weight": 0.20, "rationale": "Clean code, follows project patterns", "refine": null},
    "safety": {"score": 2, "weight": 0.15, "rationale": "No rate limiting on new endpoint", "refine": "Add rate limit middleware to POST /api/users"},
    "test_coverage": {"score": 3, "weight": 0.10, "rationale": "Existing tests pass but no new tests added", "refine": "Add integration test for token expiry edge case"},
    "depth": {"score": null, "weight": 0, "rationale": null, "refine": null}
  },
  "blockers": [],
  "security_concerns": [],
  "logic_errors": [],
  "suggestions": ["..."],
  "pressure_penalty": 0.0,
  "consensus_tag": null
}
```

**Dimension fields:**
- `score`: 1-5 integer (null if dimension inactive, e.g. depth when not in deep tier)
- `weight`: float from selected weight profile
- `rationale`: 1 sentence — WHY this score, grounded in evidence. MUST be written BEFORE the score (PARROT consistency: rationale predicts score, not post-hoc justifies it)
- `refine`: null if PASS (score >= 4), otherwise a specific actionable fix suggestion targeting THIS dimension. Used by orchestrator for Generate→Critique→Refine loop — the orchestrator can pass `refine` strings directly to the worker as targeted instructions.

**Scoring protocol (PARROT-inspired):**
1. For each dimension, write the `rationale` first (what you observed)
2. Then derive the `score` from the rationale (not the other way around)
3. If rationale suggests problems but score is high → consistency violation → lower the score
4. If rationale is positive but score is low → consistency violation → raise the score

**Fail-closed override rule:** If `security_concerns` is non-empty OR `logic_errors` is non-empty → verdict MUST be "FAIL" regardless of score. Unparseable JSON = auto-FAIL.

**Dimensional drift tracking:** `/eval` can compare `dimensions` across runs to detect which specific dimension is degrading. Example: correctness stable at 4 but safety dropping from 4→3→2 across 3 runs = targeted intervention on safety, not full re-review.

This block is MANDATORY for STANDARD and DEEP paths. For QUICK path, include a minimal version: `{"verdict": "PASS|WARN|FAIL", "score": 4.0}`.

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
