---
name: self-evolve
description: "Use when iteratively improving a skill through adversarial co-evolution with auto-generated eval cases. Trigger on 'self-evolve', 'evolve skill', 'improve skill with evals'. Do NOT use for learning audits (/evolve) or file optimization (/autoloop)."
argument-hint: <target-skill> [budget:N] [bootstrap:true|false] [meta:true|false] [group:N] [mode:skill|system]
discovery-keywords: [improve skill, evolve skill, skill quality, adversarial eval, co-evolution, benchmark skill]
tags: [orchestration, testing, code-quality]
phase: review
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
- **mode**: `skill` (default) or `system`. When `system`: target is the STOPA orchestration system itself (`.claude/rules/*.md` + skill routing descriptions). See System Mode section below.

Validation:
- Verify `.claude/skills/<target>/SKILL.md` exists
- Parse budget as integer, clamp to [1, 12]
- Parse bootstrap as boolean
- Parse meta as boolean
- Parse mode as string (default: `skill`). Valid values: `skill`, `system`.
  - If `mode: system`: `target-skill` is ignored. Target is STOPA itself. Bootstrap generates system-level eval cases.
- **group**: number of parallel evolution branches (default: 1 = standard single-branch). Clamp to [1, 3].
  - If group > 1: read `references/group-evolution.md` for parallel branch protocol (GEA-inspired)
  - Group mode uses git worktrees for isolation, shared eval cases, tournament selection every 2 rounds
  - Prerequisite: at least 1 prior single-branch run on this target (optstate must exist)

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
4. **Load optstate** (UCB1 strategy data):
   - Read `.claude/memory/optstate/self-evolve.json` (if exists)
   - Check `strategies_that_work` and `recurring_failure_patterns` for this target
   - If previous runs hit same circuit breaker: warn user and suggest different approach
   - If optstate doesn't exist: skill proceeds normally with equal-weight defaults
5. Create evolution branch: `git checkout -b self-evolve/<target>`
6. Run baseline eval: execute all cases, record pass_rate
5a. **Trace initialization:** Create `.traces/self-evolve-<target>-<timestamp>/` with `diffs/` subdir. Write `trace-active.json` marker: `{"skill":"self-evolve","run_id":"self-evolve-<target>-<timestamp>","target":"<target>","trace_dir":".traces/...","started":"<ISO>","current_iteration":0}`. Purge traces >7 days: `find .traces/ -maxdepth 1 -mtime +7 -exec rm -rf {} + 2>/dev/null || true`
6. Initialize evolution log:

| Round | pass_rate | cases_total | action | delta | notes |
|-------|-----------|-------------|--------|-------|-------|
| 0 | baseline | N | baseline | 0.0 | initial state |

### Phase 1: Co-Evolution Loop

Repeat for `budget` rounds (default 6):

#### Adaptive Mutation Strength σ (EGGROLL three-regime principle)

EGGROLL (Oxford/MILA 2026) proves ES operates in three regimes based on perturbation scale σ:
- **Linearization** (σ too small): converges but explores nothing new
- **Critical** (σ just right): optimal signal-to-noise ratio
- **Divergence** (σ too large): updates diverge, wasted compute

Map to self-evolve mutation scope:

| Round state | σ regime | Executor instruction modifier |
|-------------|----------|-------------------------------|
| pass_rate < 50% | **Small σ** — linearization | "Fix the single most obvious failure. Change at most 3 lines." |
| pass_rate 50-90% | **Medium σ** — critical | "Make one targeted structural change. Up to 10 lines." (default) |
| pass_rate 100%, escalating | **Large σ** — exploration | "Consider a structural refactor of one section. Up to 20 lines." |
| 2+ consecutive reverts | **Reduce σ** | "Previous changes were too aggressive. Make a smaller, more focused edit." |

The σ modifier is injected into the Executor sub-agent system prompt (Step 3) to control edit granularity. This prevents the common failure mode where Executor makes huge rewrites on early rounds (divergence) or tiny tweaks when exploration is needed (linearization).

#### Step 1: Grade

Run all eval cases against current skill version.
- Record: pass_rate, list of failing case IDs
- If pass_rate = 100% for 2nd consecutive round after curriculum added cases: **CONVERGENCE** — exit loop

#### Step 2: Curriculum Decision (Haiku sub-agent)

Spawn a **Haiku** sub-agent with adversarial-thinking system prompt:
> "You are a red-team curriculum designer. Your job is to find weaknesses, edge cases,
> and failure modes in the target skill. Think like an attacker — what inputs would
> break this skill? What assumptions does it make that could be violated?"

**Cross-run context injection** (if optstate exists):
Include in Curriculum agent prompt:
- `strategies_that_work` from optstate → "Strategies that worked on previous runs of this target: {list}"
- `recurring_failure_patterns` from optstate → "Known recurring failures to target: {list}"
- `per_target.<target>.dominant_strategy` → "Most effective strategy historically: {strategy}"
This steers Curriculum toward proven approaches while UCB1 handles exploration/exploitation balance.

Two modes based on current state:

**If pass_rate < 100% (failures exist):**
- Do NOT generate new cases — focus Executor on fixing existing failures
- Prioritize: oldest failing case first (it has been failing longest)
- Output: "Curriculum: FIX mode — {N} cases failing, targeting case-{ID}"

**If pass_rate = 100% (all passing):**
- **Read executor failure traces** (if `.traces/self-evolve-<target>-*/` exists): `grep "iteration" .traces/self-evolve-<target>-*/tools.jsonl | grep -v "exit.*0"` to find what inputs caused the Executor to struggle. Use these failure patterns to generate MORE targeted adversarial cases — not generic edge cases.
- Curriculum agent generates 1-2 NEW harder cases
- Strategy selection via **UCB1 selector** (GEA-inspired, arXiv:2602.04837):
  - Run: `python scripts/ucb1-selector.py .claude/memory/optstate/self-evolve.json --top 1 --json`
  - If optstate doesn't exist or insufficient data: fall back to equal-weight random
  - UCB1 balances exploitation (strategies that worked before) with exploration (untried strategies)
  - Available strategies:
  - **Edge case** (UCB1 category: `explore_new`): unusual input that tests boundary conditions
  - **Adversarial** (UCB1 category: `fix_crashes`): input designed to exploit known weaknesses or ambiguities in the skill
  - **Scale** (UCB1 category: `exploit_success`): larger/more complex input than existing cases
  - **Composition** (UCB1 category: `combine`): combine patterns from multiple existing cases
  - *(+ custom strategies if meta-mode has added them — map to nearest UCB1 category)*
  - **Strategy-to-UCB1 mapping**: Edge→explore_new, Adversarial→fix_crashes, Scale→exploit_success, Composition→combine. Meta-mode can override via `strategy_ucb1_map` in evolved params.
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

- If pass_rate improved or held steady with new harder cases: check regression below, then KEEP
- If pass_rate decreased: `git revert HEAD` (revert Executor's change)
- Log result to evolution table

**Per-case regression detection** (PaperOrchestra-inspired, arXiv:2604.05018):
When pass_rate improves, diff the individual case results:
```
passing_before = {cases that passed in previous round}
passing_after  = {cases that pass now}
regressions    = passing_before - passing_after  # cases that STOPPED passing
new_passes     = passing_after - passing_before   # cases that STARTED passing
regression_count = len(regressions)

IF regression_count > 0:
    Log: "Regression: {regression_count} previously-passing cases now FAIL: {list}"
    IF len(new_passes) - regression_count >= 2:
        KEEP — net gain is sufficient to justify regression
        Log: "Net gain +{net} cases — keeping despite {regression_count} regressions"
    ELSE:
        git revert HEAD
        Log: "Net gain insufficient (+{net}) — reverting to avoid regression"
```

Run: `python scripts/loop-state.py regression '{"dim1": score1}' '{"dim1": prev1}' --threshold 0.5`
Returns JSON with `{has_regression, regressions, improvements}`. Use this instead of manual set arithmetic.

Why net >= 2 threshold: a single net gain could be noise; two+ indicates genuine improvement that outweighs the regression.
- **UCB1 ledger update**: After each keep/revert decision, record strategy outcome for UCB1:
  ```
  Append to optstate change_ledger: {
    "round": N,
    "target": "<target>",
    "strategy": "<strategy used this round — edge/adversarial/scale/composition>",
    "mutations": ["<1-sentence description of what Executor changed>"],
    "outcome": "success" (kept + pass_rate up) | "partial" (kept + same) | "failure" (reverted),
    "pass_rate_delta": <float>
  }
  ```
  This feeds UCB1 on next run — strategies that consistently produce kept changes get higher scores.

#### Step 7: Meta-Mode Check (only if `meta:true`, every 3 rounds)

Per `meta-mode.md`: analyze strategy effectiveness, convergence rate, revert ratio.
Propose ONE parameter change or ONE new custom strategy. Log to `meta-log.tsv`.
Apply in sandbox, evaluate next round, keep or revert.

#### Step 7b: Heartbeat Reflection Check (every 2 rounds, nezávisle na meta-mode)

CORAL-inspired mid-run steering — catches unproductive exploration BEFORE circuit breaker fires.

> **Hook-backed**: `stagnation-detector.py` PostToolUse hook monitors result files and injects
> `[stagnation-steering:yellow/red]` messages automatically. If you see one, follow it immediately.
> The in-skill check below is defense-in-depth for cases where TSV format differs.

```
IF last 2 rounds were both "discard" OR "crash":
  1. PAUSE — do NOT iterate further automatically
  2. Read last 4-6 entries from change_ledger (optstate)
  3. Generate reflexion note (1-3 sentences):
     - What did I try? Why did it fail? What should I try differently?
  4. Write reflexion to run diary under `**Heartbeat Reflection**:`
  5. Switch strategy for NEXT round: pick least-used strategy from UCB1

Run: `python scripts/loop-state.py stagnation <evolution-log.tsv> --window 2`
Returns JSON with `{stagnant, consecutive_discards, steering}`. Use this instead of manually inspecting the last 2 rounds.

IF pass_rate stagnates (delta < 0.5% across last 4 rounds):
  1. Inject "skill consolidation" prompt:
     - Extract what worked (kept rounds) into 3-5 bullet points
     - Write to shared trace buffer (readable by other group-evolution branches)
  2. Reset exploration: set exploration_weight to 2.0 for next 2 rounds

ELSE: continue normally — zero overhead when triggers don't fire
```

**Difference from Step 7**: Meta-mode tunes parameters (learning rate, strategy weights). Heartbeat changes *direction* — forces strategy switch or consolidation when iteration loop stagnates. Both can fire independently.

**Advisor consultation (at heartbeat):** When the heartbeat fires (every 5 rounds), also invoke the advisor checkpoint protocol from `${CLAUDE_SKILL_DIR}/../orchestrate/references/advisor-checkpoint.md`. Spawn an Opus sub-agent with current pass_rate trajectory, kept/discarded rounds, and eval case distribution. Advisor suggests strategic direction for next rounds. Skip if budget ≤ 3 or already used 3+ consultations.

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
**Final pass_rate**: X% (baseline: Y%) | **Median pass_rate (all rounds)**: Z%
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

Run: `python scripts/loop-state.py perf-record <evolution-log.tsv> --skill self-evolve --slug <target> --write`
Generates and writes performance JSON from the evolution log.

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
5. Write outcome record (see Outcome Record section below)
6. Update optimization state (see Optimization State section below)

### Outcome Record (RCL credit loop)

Write to `.claude/memory/outcomes/<date>-self-evolve-<outcome>-<target>.md`:

```markdown
---
skill: self-evolve
run_id: self-evolve-<target>-<timestamp>
date: <YYYY-MM-DD>
task: "Evolve <target> skill"
outcome: success | partial | failure
score_start: <baseline_pass_rate>
score_end: <final_pass_rate>
iterations: <rounds>
kept: <count>
discarded: <reverts>
exit_reason: <convergence|budget|circuit-breaker>
---

## Trajectory Summary
1. Baseline: <pass_rate>%, <N> cases
2. Round N: <FIX/ESCALATE> → <delta> (<keep/revert>)
... (max 15 key rounds)

## Learnings Applied
- file: <learning.md> | credit: helpful | evidence: <why>

## What Worked (if outcome != failure)
- <key edit pattern or strategy>

## What Failed (if outcome != success)
- <what the executor couldn't handle>
```

### Optimization State Update

Read `.claude/memory/optstate/self-evolve.json` at Phase 0 (Setup, step 4). Use it to:
- Know what strategies worked on this target before (UCB1 scores inform Curriculum strategy selection)
- Avoid repeating failed approaches
- Check if previous runs hit same circuit breaker

After Phase 3, update optstate:

Run: `python scripts/loop-state.py optstate-update .claude/memory/optstate/self-evolve.json '<json_entry>'`
Updates optimizer state with FIFO ledger (max 20 entries).

```json
{
  "last_updated": "YYYY-MM-DD",
  "total_runs": N,
  "health": "improving|stable|degrading",
  "change_ledger": [/* max 20 FIFO — accumulated from Step 6 UCB1 ledger updates this run */],
  "strategies_that_work": ["edge case on boundary validation", "composition for multi-step flows"],
  "strategies_that_fail": ["scale on simple skills — adds noise"],
  "recurring_failure_patterns": ["critic rejects curriculum cases >50% of rounds"],
  "optimization_velocity": {"stage": "early|middle|plateau", "trend": "up|flat|down"},
  "per_target": {
    "<target>": {
      "last_pass_rate": 0.85,
      "best_pass_rate": 0.92,
      "runs": 3,
      "dominant_strategy": "adversarial"
    }
  }
}
```
UCB1 selector reads `change_ledger` on next run → strategies that consistently produced kept changes get higher exploration/exploitation scores.

### Replay Buffer from Outcomes (RCL failure replay)

At Phase 0, after loading eval cases:

1. Read `memory/outcomes/` filtered by `skill: self-evolve` AND target matches AND `outcome != success`
2. Extract failure patterns from "What Failed" sections
3. Cross-reference with existing eval cases — identify gaps
4. If failed outcomes describe failure modes not covered by current cases:
   - Generate 1-2 targeted replay eval cases covering those modes
   - Add to eval suite with source note: `# Source: replay from outcome <run_id>`
5. Reserve at least 30% of eval budget for these replay cases
6. **Graduation**: if a replay case passes 3× consecutive across runs, mark as graduated (no longer priority)
7. **Eviction**: if a replay case fails 5× consecutive post-reflection, mark as intractable and skip
8. **Optstate feedback loop**: After replay case generation, update optstate:
   - Add generated replay case descriptions to `recurring_failure_patterns` (so future runs know what was problematic)
   - If a replay case graduates: add the strategy that fixed it to `strategies_that_work`
   - If a replay case is evicted: add the failure mode to `strategies_that_fail` with note "intractable after 5 attempts"

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

1. **Eval cases are sacred** — do not modify existing eval cases, because changing them retroactively invalidates all prior improvement measurements and makes it impossible to track genuine progress. Only add new ones.
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

Run: `python scripts/loop-state.py circuit-breaker --consecutive-reverts N --eval-cases N --skill-lines N --iteration N --max-iterations 20`
Returns JSON with `{stop, triggers}`. Use this instead of manual threshold checks.

## Anti-Patterns

- **Case explosion**: Curriculum generates too many cases — metric becomes pass_rate on unreasonable workload. Cap at 20.
- **Executor gaming**: Skill becomes over-fitted to specific eval case wording. Critic gate catches this.
- **Complexity creep**: Each round adds lines — skill becomes unmaintainable. 500-line cap enforces discipline.
- **Premature convergence**: 100% pass_rate on easy cases does not equal good skill. Curriculum must generate genuinely harder cases, not variations.

## System Mode (`mode: system`)

Meta-optimization of STOPA itself — treating the orchestration system as a "program.md" (ref: Karpathy, No Priors 2026-03-20). Instead of evolving a single skill, evolves the system configuration: rules, skill routing, and behavioral patterns.

**Concept**: Different program.mds (STOPA configurations) produce different research velocities. System mode runs auto-research on STOPA's own configuration to find better orchestration patterns.

### System Mode Phase 0: Setup (replaces standard Phase 0)

1. **Target files** (the "program.md"):
   - `.claude/rules/*.md` — behavioral rules and invariants
   - `.claude/skills/*/SKILL.md` — skill `description:` fields (routing triggers)
   - `.claude/rules/skill-tiers.md` — tier assignments
   - `CLAUDE.md` — project-level orchestration config
2. **Eval cases**: `.claude/evals/system/`
   - If no cases exist AND bootstrap=true: generate 5 representative task descriptions covering:
     - Simple single-file edit (should NOT trigger orchestrate)
     - Multi-file refactor (should trigger orchestrate)
     - Research question (should route to deepresearch, not scout)
     - Ambiguous task (triage should classify correctly)
     - Edge case with mismatched keywords
   - Each case: `input.md` (task description), `expected.md` (correct routing + tier), `eval.md` (grading: correct skill selected? correct tier? correct model?)
3. **Baseline eval**: Run all system eval cases, measure:
   - Routing accuracy: % of tasks routed to correct skill
   - Tier accuracy: % of tasks assigned correct budget tier
   - Token cost estimate: sum of estimated tokens across all task routings
4. **Load system optstate**: `.claude/memory/optstate/system-evolve.json`

### System Mode Curriculum Strategies

- **Routing confusion**: task descriptions that expose ambiguity between similar skills (e.g., scout vs deepresearch, critic vs peer-review)
- **Tier miscalibration**: tasks where budget tier assignment is wrong (too heavy or too light)
- **Description drift**: skill descriptions that have grown stale or misleading
- **Rule conflict**: rules in different `.claude/rules/*.md` files that contradict each other

### System Mode Executor

Instead of editing a single SKILL.md, the Executor can:
- Adjust skill `description:` fields to improve routing accuracy
- Modify rule priorities or wording in `.claude/rules/*.md`
- Update tier assignments in `skill-tiers.md`
- Add `discovery-keywords:` to improve fuzzy matching

**Constraints**:
- NEVER modify skill workflow body (only description/frontmatter)
- NEVER delete rules — only clarify or reprioritize
- NEVER change more than 2 files per round
- All changes must be sync'd (commands/ ↔ skills/ invariant)

### System Mode Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| Routing accuracy | measured at Phase 0 | +5% or 95%+ |
| Tier accuracy | measured at Phase 0 | +5% or 90%+ |
| Token cost estimate | measured at Phase 0 | -10% or stable |

### System Mode Circuit Breakers

Standard circuit breakers apply, plus:
- System routing accuracy drops below baseline: STOP + revert all changes
- More than 3 rule files modified in a single run: STOP
- Any core-invariant rule modified: STOP + user approval required
