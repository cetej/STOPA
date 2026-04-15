---
name: autoharness
description: "Use when a skill or command repeatedly fails with the same error patterns and you need to auto-generate validators or constraints that prevent recurrence. Analyzes failure traces, extracts patterns, creates harness rules. Trigger on 'autoharness', 'generate validator', 'auto-constraint', 'opakuje se stejná chyba'. Do NOT use for one-off fixes, manual validation, debugging a single failure (/systematic-debugging), or iterative skill improvement (/self-evolve)."
argument-hint: <target-skill> [iterations:N] [scope:action-filter|action-verifier|policy] [escalate:true]
tags: [testing, orchestration]
phase: verify
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
model: sonnet
effort: high
maxTurns: 30
---

# AutoHarness — Automatic Constraint Synthesis

Inspired by AutoHarness (arXiv:2603.03329): instead of telling LLM "don't do X", generate **code that prevents X**. Observes failures, synthesizes a Python validator, iterates until 100% pass rate.

## Three Harness Types

| Type | How it works | When to use |
|------|-------------|-------------|
| **action-filter** | Generates set of legal outputs; skill picks from them | Output is one of N known-good options |
| **action-verifier** | Skill proposes output; code validates + returns feedback on invalid | Most common — catches format/schema/logic errors |
| **policy** | Deterministic code replaces LLM entirely | Simple transforms where LLM is overkill |

Default: `action-verifier` (most broadly useful).

<!-- CACHE_BOUNDARY -->

## Phase 0: Setup

### Parse input

From `$ARGUMENTS`, extract:
- **target**: skill name or command to generate harness for (required)
- **iterations**: max refinement rounds (default: 5)
- **scope**: harness type — `action-filter`, `action-verifier`, or `policy` (default: `action-verifier`)

If target is empty → list skills with known failure patterns (grep learnings for `type: bug_fix`).

### Understand target

1. Read the target skill file:
   ```
   Glob: .claude/commands/<target>.md
   Glob: .claude/skills/<target>/SKILL.md
   ```
2. Extract: expected inputs, outputs, validation criteria, tool permissions
3. If target is a bash command (not a skill): note its expected stdin/stdout format

### Create working directory

```bash
mkdir -p .autoharness/<target>
```

Initialize state file `.autoharness/<target>/state.json`:
```json
{
  "target": "<target>",
  "scope": "action-verifier",
  "iteration": 0,
  "max_iterations": 5,
  "failures_collected": 0,
  "pass_rate": 0.0,
  "status": "collecting"
}
```

## Phase 1: Failure Collection

Gather evidence of what goes wrong. **Minimum 3 failures required** to proceed.

### Sources (check all, in order)

1. **Learnings** — grep for target-related failures:
   ```
   Grep: component:<target> in .claude/memory/learnings/
   Grep: tags:.*<target> in .claude/memory/learnings/
   ```
   Extract: what failed, error message, expected vs actual

2. **Git history** — reverted/fixed commits:
   ```bash
   git log --oneline --all --grep="<target>" --grep="fix" --grep="revert" --all-match | head -20
   git log --oneline --all --grep="<target>" | head -20
   ```
   For each relevant commit: `git show <sha>` to extract the error pattern

3. **Troubleshooting docs** — if `docs/TROUBLESHOOTING.md` exists:
   ```
   Grep: <target> in docs/TROUBLESHOOTING.md
   ```

4. **Eval failures** — if `.claude/evals/<target>/` exists:
   ```
   Glob: .claude/evals/<target>/*.md
   ```
   Extract failed test cases

### Failure taxonomy

Classify each failure using standard categories (from autoresearch):

| Category | Examples |
|----------|---------|
| SYNTAX | Invalid JSON, broken YAML, malformed output |
| SCHEMA | Missing required fields, wrong types |
| LOGIC | Valid format but semantically wrong |
| DEPENDENCY | Missing imports, undefined references |
| FORMAT | Wrong encoding, line endings, whitespace |
| CONSTRAINT | Violated business rules (too long, out of range) |

### Output

Save to `.autoharness/<target>/failures.json`:
```json
[
  {
    "id": 1,
    "source": "learning|git|troubleshooting|eval",
    "category": "SYNTAX|SCHEMA|LOGIC|...",
    "input_summary": "what was the input",
    "expected": "what should have happened",
    "actual": "what actually happened",
    "error_message": "exact error text",
    "severity": "critical|high|medium|low"
  }
]
```

**Gate**: If fewer than 3 failures collected → STOP. Report: "Not enough failure data for `<target>`. Found N failures. Need at least 3 to synthesize a reliable harness. Try running the skill more, or manually add failure cases to `.autoharness/<target>/failures.json`."

## Phase 2: Harness Generation (Iterative Refinement)

### Initialize validator

Generate first version of `.autoharness/<target>/validator.py`:

**For action-verifier** (default):
```python
"""
Auto-generated validator for: <target>
Scope: action-verifier
Generated: <date>
Failures addressed: <N>
"""
import sys
import json

def validate(output: str) -> tuple[bool, str]:
    """
    Validate output from <target>.
    Returns (is_valid, feedback_message).
    If invalid, feedback explains WHY and suggests fix.
    """
    # Check 1: <derived from failure #1>
    # Check 2: <derived from failure #2>
    # ...
    return True, "OK"

if __name__ == "__main__":
    data = sys.stdin.read()
    valid, msg = validate(data)
    print(json.dumps({"valid": valid, "message": msg}))
    sys.exit(0 if valid else 1)
```

**For action-filter**:
```python
def legal_actions(context: str) -> list[str]:
    """Return all legal outputs given the current context."""
    # Derived from failure patterns
    return [...]
```

**For policy**:
```python
def decide(input_data: str) -> str:
    """Deterministic decision — replaces LLM call entirely."""
    # Derived from observed input→output patterns
    return output
```

### Critical rules for generated code

1. **No try-except blocks** — errors must surface explicitly (from paper)
2. **No LLM calls** — validator must be pure Python, zero inference cost
3. **No external dependencies** — stdlib only (json, re, pathlib, sys)
4. **Explicit feedback** — on failure, message MUST explain what's wrong and how to fix
5. **One check per failure** — each captured failure maps to exactly one validation check

### Refinement loop

For each iteration (1 to max_iterations):

1. **Test** — run validator against ALL captured failures:
   ```bash
   python .autoharness/<target>/validator.py < test_input_N.txt
   ```
   Record: pass/fail for each test case

2. **Score** — pass_rate = passed / total

3. **Exit check** — if pass_rate == 1.0 → proceed to Phase 3

4. **Refine** — spawn Haiku sub-agent with:
   - Current validator code
   - Failed test cases (max 5, sampled)
   - Error messages from failed runs
   - Instruction: "Fix the validator to catch these failures. Keep existing passing checks. Add ONE new check per failed case."
   - **Confound isolation**: Each refinement round changes EITHER validation logic OR error messages/thresholds, never both. If structural validator changes AND threshold tuning are both needed, do structural first → verify → threshold second. (Meta-Harness arXiv:2603.28052: bundling different change types caused regression in 2/2 attempts)

5. **Save** — write updated validator, increment iteration

6. **Log** — append to `.autoharness/<target>/refinement.tsv`:
   ```
   iteration	pass_rate	checks_added	changes_summary
   1	0.33	2	Added JSON schema check, field presence check
   2	0.67	1	Added string length constraint
   3	1.00	0	All checks passing
   ```

### Circuit breaker

If after max_iterations, pass_rate < 0.8 → STOP with analysis:
- Which failures remain uncaught?
- Are they LLM-judgment-dependent (can't be coded deterministically)?
- Suggest: split into codeable vs judgment-dependent checks

## Phase 3: Validation on Novel Data

Prevent overfitting to captured failures.

### Generate test cases

Spawn Haiku sub-agent to generate 3-5 **novel** test inputs that:
- Are similar to but distinct from captured failures
- Include 1-2 valid inputs (should pass) and 2-3 invalid inputs (should fail)
- Cover edge cases not in training set

### Run validation

```bash
for f in .autoharness/<target>/novel_*.txt; do
  python .autoharness/<target>/validator.py < "$f"
done
```

### Assess

- **False positives** (valid input rejected): validator is too strict → refine
- **False negatives** (invalid input passed): validator is too lenient → refine
- Threshold: >80% accuracy on novel data → PASS
- One refinement round allowed if close (60-80%)
- Below 60% → STOP, report that failures are too diverse for automated synthesis

## Phase 3.5: Adversarial Escalation (Agent0-inspired, optional)

**Trigger:** `escalate:true` flag AND Phase 3 passed (>80% novel data accuracy).
**Concept:** After the validator passes all tests, a "red team" agent tries to break it. Inspired by Agent0's co-evolutionary curriculum: when the executor masters current challenges, the curriculum must escalate.

### Red Team Generation

Spawn a Sonnet sub-agent as adversarial curriculum generator with this prompt:

> You are a red team tester. Your goal is to find inputs that BYPASS the validator — inputs that are INVALID but the validator incorrectly accepts (false negatives).
>
> Here is the validator code: [include validator.py]
> Here are the failure categories it checks: [include failures.json categories]
>
> Generate 5 adversarial test cases that:
> 1. Are structurally similar to valid inputs (pass basic format checks)
> 2. But contain subtle errors the validator might miss (edge cases, boundary values, Unicode, empty strings, extreme lengths)
> 3. Each targets a DIFFERENT weakness in the validator
>
> For each test case, explain WHY you think it will bypass the validator.

### Red Team Evaluation

1. Run each adversarial input through the validator
2. Score: `bypass_rate = bypassed / total_adversarial`

| bypass_rate | Action |
|-------------|--------|
| 0% | Validator is robust — proceed to Phase 4 |
| 1-40% | Refinement round: add checks for bypassed cases, re-test |
| 41-100% | Validator has fundamental gaps — back to Phase 2 with adversarial cases added to failures.json |

### Escalation Loop

- Max 2 escalation rounds (red team → refine → red team again)
- Each round, the red team agent sees PREVIOUS bypasses and must find NEW weaknesses
- After 2nd round: proceed to Phase 4 regardless (diminishing returns)

### Log

Append to `refinement.tsv`:
```
adversarial_1	0.60	3	Red team found 3/5 bypasses: Unicode normalization, empty array, negative index
adversarial_2	0.20	2	Red team found 1/5 bypasses: nested null in optional field
```

## Phase 4: Integration

### Save artifacts

1. **Validator script** → `.autoharness/<target>/validator.py` (already saved)
2. **Test suite** → `.autoharness/<target>/tests/` (failures + novel cases)
3. **Metadata** → update `state.json` with final pass_rate, iteration count

### Integration options (present to user)

**Option A: Hook integration** (for action-verifier scope)
Propose adding to `.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "tool == 'Write' || tool == 'Edit'",
      "command": "python .autoharness/<target>/validator.py",
      "description": "Auto-validate <target> output"
    }]
  }
}
```

**Option B: Standalone script** (for all scopes)
Keep as utility: `python .autoharness/<target>/validator.py < input.txt`

**Option C: Inline in skill** (for policy scope)
Replace the relevant LLM step in the skill with the generated code.

### Log learning

Write to `.claude/memory/learnings/`:
```yaml
---
date: <today>
type: best_practice
severity: medium
component: <target>
tags: [autoharness, validator, constraint-synthesis]
summary: "Auto-generated validator for <target> catches <N> failure patterns with <pass_rate>% accuracy. <scope> type."
uses: 0
harmful_uses: 0
---
```

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "The skill only failed once so autoharness is overkill" | Single failures often represent systematic patterns; autoharness catches the class of failures, not just the instance | Check failure logs for pattern recurrence; if 2+ failures share a root cause, autoharness is justified |
| "I'll write the validator by hand since I understand the failure pattern" | Hand-written validators encode the author's assumptions; auto-generated ones discover unexpected edge cases | Let Phase 2 generate the initial validator; hand-tune only after the auto-generated version is baselined |
| "The pass rate is above threshold so I can skip adversarial escalation" | Above-threshold pass rates can hide fragile validators that break on novel inputs; adversarial testing reveals brittleness | Always run at least one adversarial round (Phase 3.5) even when the pass rate looks good |
| "I'll skip the integration step since the validator works in isolation" | Validators that aren't integrated into the skill's runtime are never executed; they become stale documentation | Complete Phase 4 integration; a validator that doesn't run automatically provides zero protection |

### Report

Output to user:

```
## AutoHarness Report: <target>

| Metric | Value |
|--------|-------|
| Failures collected | N |
| Refinement iterations | M |
| Final pass rate (training) | X% |
| Novel data accuracy | Y% |
| Harness type | action-verifier |
| Checks generated | K |

### Failure Categories Covered
- SYNTAX: N checks (JSON validation, format)
- SCHEMA: N checks (required fields, types)
- LOGIC: N checks (semantic constraints)

### Integration
Validator saved to: `.autoharness/<target>/validator.py`
Recommended integration: [Hook / Standalone / Inline]

### Uncovered Patterns
- [Any failures that couldn't be automated]
```
