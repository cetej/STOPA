---
name: self-evolve
description: "Use when iteratively improving a skill through adversarial co-evolution with auto-generated eval cases. Trigger on 'self-evolve', 'evolve skill', 'improve skill with evals'. Do NOT use for learning audits (/evolve) or file optimization (/autoloop)."
argument-hint: <target-skill> [budget:N] [bootstrap:true|false] [meta:true|false]
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

Inspired by Agent0 (AIMING Lab) + HyperAgents (Meta, arXiv:2603.19461): dual-agent
co-evolution where a Curriculum agent generates increasingly difficult eval cases and
an Executor agent improves the target skill to handle them.

**Model empathy principle** (AutoAgent-validated): Same-model pairings (meta=Claude, task=Claude)
outperform cross-model pairings because the meta-agent writes harnesses the inner model
actually understands — shared weights enable implicit reasoning about the task agent's
behavior. Always prefer same-model-family for Curriculum and Executor agents.

**v2 additions (HyperAgents-inspired):**
- `meta:true` — metacognitive self-modification (tune own parameters + create new strategies). See `meta-mode.md`.
- Heterogeneous sub-agents — Curriculum (Haiku) and Executor (Sonnet) run as separate agents with specialized prompts
- Curriculum Critic — quality gate on generated eval cases before Executor sees them
- Persistence — evolved meta-parameters survive across runs

**When to use vs alternatives:**
- `/self-evolve` — "Make this skill better via adversarial testing" (eval-driven improvement)
- `/autoloop` — "Make this file better" (metric-driven optimization of any file)
- `/evolve` — "Audit accumulated learnings" (correction pattern analysis, no code changes)
- `/autoresearch` — "Which approach works best?" (hypothesis exploration)

## Shared Memory

Read first:
- `.claude/memory/state.md` — current task context
- `.claude/memory/budget.md` — remaining budget

<!-- CACHE_BOUNDARY -->

## Input

Parse `$ARGUMENTS`:
- **target-skill**: skill name (e.g., `critic`, `scout`) — maps to `.claude/skills/<name>/SKILL.md`
- **budget**: max co-evolution rounds (default: 6, max: 12)
- **bootstrap**: if `true` and no eval cases exist, generate initial cases via `/autoharness` (default: false)
- **meta**: if `true`, enable metacognitive self-modification mode (default: false). See `meta-mode.md`.

Validation:
- Verify `.claude/skills/<target>/SKILL.md` exists
- Parse budget as integer, clamp to [1, 12]
- Parse bootstrap as boolean
- Parse meta as boolean

## Process

### Phase 0: Setup

1. Read target skill: `.claude/skills/<target>/SKILL.md`
2. Check for eval cases: `.claude/evals/<target>/`
   - If cases exist: count them, read structure
   - If no cases AND bootstrap=true: delegate to `/autoharness` to generate 3-5 initial cases
   - If no cases AND bootstrap=false: ERROR — "No eval cases found. Run with bootstrap:true or create cases in .claude/evals/<target>/"
3. **Load evolved parameters** (if `meta:true`):
   - Check `.claude/memory/intermediate/self-evolve-meta/<target>.json`
   - If exists: load params as defaults. Print: `♻ Loaded evolved parameters from previous run (v{version}).`
   - If not: use hardcoded defaults (strategy weights all 0.25, critic_frequency=2, etc.)
   - Initialize meta sandbox and meta-log.tsv per `meta-mode.md`
4. Create evolution branch: `git checkout -b self-evolve/<target>`
5. Run baseline eval: execute all cases, record pass_rate
5a. **Trace initialization:** Create `.traces/self-evolve-<target>-<timestamp>/` with `diffs/` subdir. Write `trace-active.json` marker: `{"skill":"self-evolve","run_id":"self-evolve-<target>-<timestamp>","target":"<target>","trace_dir":".traces/...","started":"<ISO>","current_iteration":0}`. Purge traces >7 days: `find .traces/ -maxdepth 1 -mtime +7 -exec rm -rf {} + 2>/dev/null || true`
6. Initialize evolution log:

| Round | pass_rate | cases_total | action | delta | notes |
|-------|-----------|-------------|--------|-------|-------|
| 0 | baseline | N | baseline | 0.0 | initial state |

### Phase 1: Co-Evolution Loop

Repeat for `budget` rounds (default 6):

#### Step 1: Grade

Run all eval cases against current skill version.
- Record: pass_rate, list of failing case IDs
- If pass_rate = 100% for 2nd consecutive round after curriculum added cases: **CONVERGENCE** — exit loop

#### Step 2: Curriculum Decision (Haiku sub-agent)

Spawn a **Haiku** sub-agent with adversarial-thinking system prompt:
> "You are a red-team curriculum designer. Your job is to find weaknesses, edge cases,
> and failure modes in the target skill. Think like an attacker — what inputs would
> break this skill? What assumptions does it make that could be violated?"

Two modes based on current state:

**If pass_rate < 100% (failures exist):**
- Do NOT generate new cases — focus Executor on fixing existing failures
- Prioritize: oldest failing case first (it has been failing longest)
- Output: "Curriculum: FIX mode — {N} cases failing, targeting case-{ID}"

**If pass_rate = 100% (all passing):**
- **Read executor failure traces** (if `.traces/self-evolve-<target>-*/` exists): `grep "iteration" .traces/self-evolve-<target>-*/tools.jsonl | grep -v "exit.*0"` to find what inputs caused the Executor to struggle. Use these failure patterns to generate MORE targeted adversarial cases — not generic edge cases.
- Curriculum agent generates 1-2 NEW harder cases
- Strategy selection: weighted random from available strategies (default equal weights, tunable via meta-mode):
  - **Edge case**: unusual input that tests boundary conditions
  - **Adversarial**: input designed to exploit known weaknesses or ambiguities in the skill
  - **Scale**: larger/more complex input than existing cases
  - **Composition**: combine patterns from multiple existing cases
  - *(+ custom strategies if meta-mode has added them)*
- Write new cases to `.claude/evals/<target>/case-{NNN}/`
- Each case needs: `input.md` (scenario), `expected.md` (expected behavior), `eval.md` (grading criteria)
- Output: "Curriculum: ESCALATE mode — added case-{ID} ({strategy})"

#### Step 2.5: Curriculum Critic (Sonnet sub-agent, only on ESCALATE)

When Curriculum generates new cases, spawn a **Sonnet** sub-agent as quality gate (reasoning-heavy task — Haiku insufficient for semantic eval quality assessment):
> "You evaluate eval case quality. Score each case 1-5 on these criteria:
> (a) Is it genuinely harder than existing cases? (b) Is it realistic — would this
> scenario occur in practice? (c) Is expected.md achievable — can a skill reasonably
> handle this? (d) Are grading criteria in eval.md clear and unambiguous?"

- Score threshold: ≥3 to accept (tunable via meta-mode: range 2-4)
- If rejected: Curriculum agent generates a replacement (max 2 retries)
- If 2 retries exhausted: skip case generation this round, proceed to Executor in FIX mode
- Log: "Curriculum Critic: case-{ID} score={N}/5 → {accepted|rejected}"

#### Step 3: Executor (Sonnet sub-agent)

Spawn a **Sonnet** sub-agent with surgical-editing system prompt:
> "You are a precision code editor. Your job is to make the MINIMAL change that fixes
> the failing test case. One conceptual change only. Read the failure carefully,
> understand the root cause, and make the smallest edit that addresses it. Preserve
> existing behavior — do not refactor, do not add features beyond what the case requires."

- **Single atomic edit per round** — one conceptual change only
- **Read execution trace** (if `.traces/self-evolve-<target>-*/tools.jsonl` exists): `grep "iteration":<round> .traces/.../tools.jsonl` to see WHERE the skill broke during the failing eval case execution — tool calls, outputs, exit codes. This shows the exact failure point, not just the final grade.
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

#### Step 7: Meta-Mode Check (only if `meta:true`, every 3 rounds)

Per `meta-mode.md`: analyze strategy effectiveness, convergence rate, revert ratio.
Propose ONE parameter change or ONE new custom strategy. Log to `meta-log.tsv`.
Apply in sandbox, evaluate next round, keep or revert.

#### Step 8: Circuit Breaker Check

- 3 consecutive reverts: **STOP** — "Executor unable to improve, report to user" (tunable via meta-mode: 2-5)
- Max 20 eval cases total reached: **STOP** — "Case explosion cap" (tunable via meta-mode: 10-30)
- Target skill >500 lines: **STOP** — "Complexity cap reached"
- Budget exhausted: exit loop normally
- Meta circuit breaker: 3 consecutive meta-changes drop score → disable meta-mode, revert to original params

### Phase 2: Synthesis Report

**Trace deactivation:** `rm -f .claude/memory/intermediate/trace-active.json`. Traces stay in `.traces/` for `/eval --optim` analysis and auto-purge after 7 days.

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
  "reverts": R,
  "meta_mode": true|false,
  "meta_changes": N,
  "custom_strategies_created": []
}
```

**If `meta:true`**: Present meta-modifications summary per `meta-mode.md`, then ask:
> "Persist evolved parameters for future `/self-evolve <target>` runs? (yes/no)"
If yes: write to `.claude/memory/intermediate/self-evolve-meta/<target>.json`

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
