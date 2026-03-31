---
name: self-evolve
description: "Use when iteratively improving a skill through adversarial co-evolution with auto-generated eval cases. Trigger on 'self-evolve', 'evolve skill', 'improve skill with evals'. Do NOT use for learning audits (/evolve) or file optimization (/autoloop)."
argument-hint: <target-skill> [budget:N] [bootstrap:true|false]
tags: [orchestration, testing, code-quality]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
model: sonnet
effort: high
maxTurns: 50
handoffs:
  - skill: /scribe
    when: "Evolution produced reusable findings or architectural decisions"
    prompt: "Record: <key finding from self-evolve>"
  - skill: /critic
    when: "Quality gate within the co-evolution loop"
    prompt: "Review skill changes: <skill path>"
---

# Self-Evolve — Adversarial Co-Evolution Loop

Inspired by Agent0 (AIMING Lab): dual-agent co-evolution where a Curriculum agent
generates increasingly difficult eval cases and an Executor agent improves the target
skill to handle them.

**When to use vs alternatives:**
- `/self-evolve` — "Make this skill better via adversarial testing" (eval-driven improvement)
- `/autoloop` — "Make this file better" (metric-driven optimization of any file)
- `/evolve` — "Audit accumulated learnings" (correction pattern analysis, no code changes)
- `/autoresearch` — "Which approach works best?" (hypothesis exploration)

## Shared Memory

Read first:
- `.claude/memory/state.md` — current task context
- `.claude/memory/budget.md` — remaining budget

## Input

Parse `$ARGUMENTS`:
- **target-skill**: skill name (e.g., `critic`, `scout`) — maps to `.claude/skills/<name>/SKILL.md`
- **budget**: max co-evolution rounds (default: 6, max: 12)
- **bootstrap**: if `true` and no eval cases exist, generate initial cases via `/autoharness` (default: false)

Validation:
- Verify `.claude/skills/<target>/SKILL.md` exists
- Parse budget as integer, clamp to [1, 12]
- Parse bootstrap as boolean

## Process

### Phase 0: Setup

1. Read target skill: `.claude/skills/<target>/SKILL.md`
2. Check for eval cases: `.claude/evals/<target>/`
   - If cases exist: count them, read structure
   - If no cases AND bootstrap=true: delegate to `/autoharness` to generate 3-5 initial cases
   - If no cases AND bootstrap=false: ERROR — "No eval cases found. Run with bootstrap:true or create cases in .claude/evals/<target>/"
3. Create evolution branch: `git checkout -b self-evolve/<target>`
4. Run baseline eval: execute all cases, record pass_rate
5. Initialize evolution log:

| Round | pass_rate | cases_total | action | delta | notes |
|-------|-----------|-------------|--------|-------|-------|
| 0 | baseline | N | baseline | 0.0 | initial state |

### Phase 1: Co-Evolution Loop

Repeat for `budget` rounds (default 6):

#### Step 1: Grade

Run all eval cases against current skill version.
- Record: pass_rate, list of failing case IDs
- If pass_rate = 100% for 2nd consecutive round after curriculum added cases: **CONVERGENCE** — exit loop

#### Step 2: Curriculum Decision

Two modes based on current state:

**If pass_rate < 100% (failures exist):**
- Do NOT generate new cases — focus Executor on fixing existing failures
- Prioritize: oldest failing case first (it has been failing longest)
- Output: "Curriculum: FIX mode — {N} cases failing, targeting case-{ID}"

**If pass_rate = 100% (all passing):**
- Curriculum agent generates 1-2 NEW harder cases
- Case generation strategy (pick one per round):
  - **Edge case**: unusual input that tests boundary conditions
  - **Adversarial**: input designed to exploit known weaknesses or ambiguities in the skill
  - **Scale**: larger/more complex input than existing cases
  - **Composition**: combine patterns from multiple existing cases
- Write new cases to `.claude/evals/<target>/case-{NNN}/`
- Each case needs: `input.md` (scenario), `expected.md` (expected behavior), `eval.md` (grading criteria)
- Output: "Curriculum: ESCALATE mode — added case-{ID} ({strategy})"

#### Step 3: Executor

Modify target skill to fix failures OR handle new cases.
- **Single atomic edit per round** — one conceptual change only
- Read the failing case(s) to understand what is expected
- Read the skill to identify what is missing or wrong
- Make the minimal edit that addresses the failure
- Commit before running eval: `git commit -m "self-evolve round {N}: {description}"`

#### Step 4: Critic Gate (every 2 rounds)

Run `/critic` on accumulated skill changes:
- `git diff self-evolve/<target>..HEAD -- .claude/skills/<target>/SKILL.md`
- If FAIL verdict: `git revert HEAD` — undo last Executor edit
- If WARN: continue but note concern
- If PASS: proceed

#### Step 5: Re-Grade

Run all eval cases (including any new ones from Step 2) against modified skill.
- Record new pass_rate
- Compare against previous round

#### Step 6: Keep/Revert

- If pass_rate improved or held steady with new harder cases: KEEP
- If pass_rate decreased: `git revert HEAD` (revert Executor's change)
- Log result to evolution table

#### Step 7: Circuit Breaker Check

- 3 consecutive reverts: **STOP** — "Executor unable to improve, report to user"
- Max 20 eval cases total reached: **STOP** — "Case explosion cap"
- Target skill >500 lines: **STOP** — "Complexity cap reached"
- Budget exhausted: exit loop normally

### Phase 2: Synthesis Report

Write `self-evolve-<target>.md` to project root:

```
## Self-Evolve Report: <target>

**Rounds**: N / budget
**Final pass_rate**: X% (baseline: Y%)
**Cases**: Z total (M original + K generated)
**Exit reason**: convergence | budget | circuit-breaker

### Evolution Log
| Round | pass_rate | cases_total | action | delta | notes |
|-------|-----------|-------------|--------|-------|-------|
...

### Cases Generated
| Case | Strategy | Round Added | Status |
|------|----------|-------------|--------|
...

### Skill Diff Summary
<summary of key changes made to the skill>

### Key Findings
- <what patterns were hard to handle>
- <what types of cases exposed weaknesses>
- <recommendations for further improvement>
```

Record performance to `.claude/memory/intermediate/self-evolve-<target>.json`:
```json
{
  "target": "<target>",
  "date": "YYYY-MM-DD",
  "rounds": N,
  "baseline_pass_rate": Y,
  "final_pass_rate": X,
  "cases_original": M,
  "cases_generated": K,
  "exit_reason": "convergence|budget|circuit-breaker",
  "reverts": R
}
```

### Phase 3: Handoff

1. Present summary to user in chat
2. Show full diff: `git diff main..self-evolve/<target> -- .claude/skills/<target>/`
3. Ask user: "Merge improvements to main?"
   - Yes: `git checkout main && git merge self-evolve/<target>`
   - No: keep branch for later review
4. Suggest: "Record findings via /scribe?" if key patterns discovered

## Eval Case Format

Each case lives in `.claude/evals/<target>/case-{NNN}/` with three files:

**input.md** — The scenario to test:
```markdown
# Scenario: <descriptive name>
<description of the situation, inputs, context>
```

**expected.md** — Expected behavior:
```markdown
# Expected Behavior
- <what the skill should do>
- <what output or side-effects are expected>
```

**eval.md** — Grading criteria:
```markdown
# Grading Criteria
- [ ] <criterion 1>
- [ ] <criterion 2>
Pass threshold: all criteria checked
```

## Rules

1. **Eval cases are sacred** — once created, NEVER modify existing cases. Only add new ones.
2. **Single edit per round** — Executor makes ONE conceptual change, not a batch rewrite.
3. **Curriculum escalates only on 100%** — do not pile on new cases while existing ones fail.
4. **Critic gates prevent drift** — quality review every 2 rounds catches skill degradation.
5. **Git is memory** — every change committed, revertable, diffable.
6. **User approves merges** — never auto-merge to main.
7. **Budget is hard** — no exceeding max rounds, no "just one more".
8. **Compose, don't duplicate** — use /autoharness for bootstrapping, /critic for gates, /eval patterns for grading.

## Circuit Breakers

| Trigger | Action |
|---------|--------|
| 3 consecutive reverts | STOP + report to user |
| 20 eval cases reached | STOP + no more curriculum generation |
| Skill >500 lines | STOP + warn about complexity |
| Budget exhausted | Normal exit with report |
| Critic FAIL 2x on same issue | STOP + escalate to user |

## Anti-Patterns

- **Case explosion**: Curriculum generates too many cases — metric becomes pass_rate on unreasonable workload. Cap at 20.
- **Executor gaming**: Skill becomes over-fitted to specific eval case wording. Critic gate catches this.
- **Complexity creep**: Each round adds lines — skill becomes unmaintainable. 500-line cap enforces discipline.
- **Premature convergence**: 100% pass_rate on easy cases does not equal good skill. Curriculum must generate genuinely harder cases, not variations.
