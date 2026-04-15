---
name: autoloop
description: Use when iteratively optimizing a file or metric against a measurable target via Karpathy loop. Trigger on 'autoloop', 'optimize skill', 'auto-improve'. Do NOT use for one-shot edits, skill improvement with evals (/self-evolve), text/argument improvement (/autoreason), or code experimentation (/autoresearch).
context:
  - tree-mode.md
  - meta-mode.md
  - trace-review.md
argument-hint: <target file/scope> [goal] [verify:<command>] [guard:<command>] [cost_metric:<command>] [budget:N] [mode:linear|tree] [meta:true] [escalate:true]
discovery-keywords: [optimize iteratively, improve metric, karpathy loop, target score, auto-improve, iterate until]
context-required:
  - "target file or scope — one file to optimize (single-file mutation rule)"
  - "optimization goal — what to improve and in which direction"
  - "verify command — how to measure improvement; without it loop uses LLM-as-judge only"
tags: [orchestration, testing]
phase: build
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
effort: high
maxTurns: 50
disallowedTools: Agent
---

# AutoLoop — Autonomous Optimization Loop

Karpathy autoresearch pattern for Claude Code: constrain scope → define metric → iterate autonomously → keep/revert → compound gains.

## Two Modes

| Mode | Trigger | Metric source |
|------|---------|---------------|
| **File mode** | Target is a file path | Built-in structural scorer (SKILL.md) or LLM-as-judge |
| **Metric mode** | `verify:<command>` provided | External command output (test coverage, benchmark, bundle size...) |

## Population Mode (EGGROLL-inspired, opt-in)

When `population:N` is set (N=2-4), each iteration generates N candidate mutations instead of one. Each candidate is a rank-1 perturbation (one focused change along one axis). The best candidate is selected via population-normalized scoring, and only the winner is committed.

```
For iteration i with population:3:
  1. Read current state (Step 1: Review) — shared across all candidates
  2. Generate 3 candidate edits — each targets ONE axis:
     - Candidate A: structural change (reorder, change flow, add/remove sections)
     - Candidate B: content change (improve specific text, logic, or values)
     - Candidate C: simplification (remove redundancy, condense, delete dead code)
  3. PARALLEL VERIFY (Combee-inspired, arXiv:2604.04247):
     - Spawn N sub-agents (one per candidate) in parallel via Agent tool
     - Each agent: apply edit → run verify → record metric → revert edit
     - Aggregate results via z-score normalization: z_i = (metric_i - μ) / max(σ, 0.01)
     - Use `scripts/combee.py:aggregate_candidate_scores()` for ranking
  4. Re-apply and commit ONLY the highest z-score candidate (if it beats baseline)
  5. Log all candidates in TSV: append `pop_rank` column (1=winner, 2-N=discarded)
```

**Why this works** (EGGROLL Theorem 3 + Combee §3): rank-1 perturbations are sufficient because accumulated updates recover full-rank expressivity. Parallel evaluation (Combee) eliminates the N× serial delay — wall-clock cost drops from O(N×verify) to O(verify) per iteration. Augmented shuffling prevents the aggregator from losing high-value candidates under batch pressure.

**Constraints:**
- Population mode uses N× the verify calls per iteration — budget = `iterations × population`
- Candidates are generated sequentially (they share review context), but VERIFIED in parallel via Agent spawns
- NOT compatible with `mode:tree` (tree already branches)
- Default population:1 (standard single-candidate mode) — opt-in via `population:N` argument

## 8 Critical Rules (from Karpathy's autoresearch)

| # | Rule |
|---|------|
| 1 | **Loop until done** — run all iterations, never ask "should I continue?" |
| 2 | **Read before write** — understand full context before modifying |
| 3 | **One change per iteration** — atomic changes. If it breaks, you know why. **Confound isolation**: NEVER bundle structural changes (control flow, state, tools) with prompt changes (system prompt, instructions, few-shot) in one iteration. Structural first → verify → prompt second. (Meta-Harness arXiv:2603.28052: bundling caused regression in 2/2 attempts) |
| 4 | **Mechanical verification only** — no subjective "looks good." Use metrics |
| 5 | **Automatic rollback** — failed changes revert instantly via git |
| 6 | **Simplicity wins** — equal results + less code = KEEP |
| 7 | **Git is memory** — read `git log` + `git diff` before each iteration to learn from history |
| 8 | **When stuck, think harder** — re-read, combine near-misses, try radical changes |

## Context Checklist

If any item below is missing from `$ARGUMENTS`, ask **one question** before proceeding.

| Item | Why it matters |
|------|---------------|
| **Target file** | Without it, scope is undefined and loop mutates the wrong thing |
| **Goal** | Without direction, loop optimizes for arbitrary structural signals |
| **Verify command** | Without a metric, improvement is LLM-judged (less reliable; state this explicitly) |

<!-- CACHE_BOUNDARY -->

## Phase 0: Setup

### Parse input

From `$ARGUMENTS`, extract:
- **target**: file path OR scope glob (required)
- **goal**: what to optimize for (optional — inferred from file type if missing)
- **verify**: command that outputs the metric number (optional — triggers metric mode)
- **guard**: command that must always pass — safety net (optional)
- **budget**: iteration count (default: 10, override with `budget:N`)
- **direction**: `higher` or `lower` is better (auto-detected from goal keywords, or ask)
- **cost_metric**: bash command that outputs a cost number (e.g., token count, LOC, latency) — enables Pareto frontier tracking (accuracy vs cost)
- **mode**: `linear` (default) or `tree` — tree enables branching exploration (see `tree-mode.md`)
- **meta**: `true` enables metacognitive self-modification of scoring params (see `meta-mode.md`). Requires `mode:linear`.
- **escalate**: `true` enables Agent0-inspired escalation — on plateau, raise the bar instead of just exploring harder (see Escalation Phase)

If `meta:true` AND `mode:tree`: reject with error — these modes are mutually exclusive.

Examples:
```
/autoloop src/api/*.ts verify:"npm test -- --coverage | grep All | awk '{print $4}'" guard:"npm run typecheck" budget:20
/autoloop .claude/skills/critic/SKILL.md
/autoloop src/index.ts "reduce bundle size" verify:"npx esbuild src/index.ts --bundle --minify | wc -c" direction:lower
/autoloop .claude/skills/critic/SKILL.md verify:"python eval_skill.py" cost_metric:"wc -c < .claude/skills/critic/SKILL.md"
```

### Optimization State Load (RCL momentum)

Read `.claude/memory/optstate/autoloop.json` if it exists. Extract:
- `strategies_that_work` → prefer these approaches in early iterations
- `strategies_that_fail` → avoid these patterns
- `recurring_failure_patterns` → add to watchlist
- `change_ledger` → last 5 entries for "what was tried before"

If file doesn't exist: proceed normally (no prior state).

**UCB1 Strategy Recommendation (when optstate has 3+ ledger entries):**

Run `python scripts/ucb1-selector.py` to get data-driven strategy priority for this session.
Output overrides the default priority order in Phase 1 Step 1 (Review). If the script is
unavailable or optstate is empty, fall back to the default priority list.

UCB1 balances exploit (high avg_reward strategies) with explore (under-tried strategies).
Exploration constant c=1.41 (sqrt(2)) per Auer et al. 2002. Ref: ASI-Evolve (arXiv:2603.29640).

### Outcomes Replay (Experience Replay, arXiv:2604.08706)

Glob `.claude/memory/outcomes/autoloop-*.md`, sort by date desc, read last 5.
For each outcome file, extract:
- `## What Worked` → **positive-bias context** (read fully, use as preferred starting strategies)
- `## What Failed` → **anticuriculum** (read as "what to avoid", not as positive signal)
- `## Trajectory Summary` → skim for iteration count and convergence pattern

**Positive-bias rule:** When forming the initial approach in Phase 1, strategies from "What Worked" across recent outcomes take priority over optstate `strategies_that_work` (which is an aggregate). Concrete trajectory > statistical summary.

If no outcome files exist: proceed normally (first run on this skill — no replay possible).

Why: "Generate-then-discard" (ignoring prior trajectories) wastes 40% of compute. Moderate staleness from prior runs is stabilizing, not harmful. Ref: arXiv:2604.08706 Theorem 4.5.

### Precondition checks

```bash
# 1. Git repo exists?
git rev-parse --git-dir 2>/dev/null || echo "FAIL: not a git repo"

# 2. Clean working tree?
git status --porcelain
# → If dirty: warn and ask to stash/commit first

# 3. Stale lock files?
ls .git/index.lock 2>/dev/null && rm .git/index.lock
```

If any FAIL: stop and inform user. Do not enter the loop with broken preconditions.

### Detect mode

| Condition | Mode |
|-----------|------|
| `verify:` provided | **Metric mode** — use external command |
| Target is `*/SKILL.md` | **File mode** — built-in structural scorer |
| Target is other file | **File mode** — LLM-as-judge or custom scorer |

**Scalar fitness nudge:** If target is NOT `*/SKILL.md` AND no `verify:` provided, print:

> ⚠ No scalar metric defined. Autoloop works best with `verify:<command>` that outputs a number. Falling back to LLM-as-judge (higher cost, weaker signal).
>
> Common verify commands by file type:
> - `.py` → `pytest --tb=no -q | tail -1` or `python <script> | grep -oP '\d+\.?\d*'`
> - `.ts/.js` → `npm test 2>&1 | grep -oP '\d+ passing'`
> - `.md` → `wc -w < <file>` (word count as proxy)
> - bundle → `npx esbuild src/index.ts --bundle --minify 2>&1 | grep -oP '\d+' | tail -1`

Ask user once: "Provide a verify command, or continue with LLM-as-judge?" Then proceed with their choice.

### Initialize trace capture (Meta-Harness)

Follow `trace-review.md` → **Trace Initialization** section: create `.traces/<run_id>/`, write `trace-active.json` marker, purge old traces. This enables the `trace-capture.py` PostToolUse hook to record tool call inputs/outputs during the optimization run.

### Warm-start from prior runs (Meta-Harness pattern)

Check for prior autoloop runs on the same target:
```bash
# Find prior iterations.jsonl for same target
prior_run=$(ls -td .traces/autoloop-$(basename <target> .md)-*/iterations.jsonl 2>/dev/null | head -1)
if [ -n "$prior_run" ]; then
  prior_best=$(python -c "
import json, sys
lines = open('$prior_run').readlines()
best = max((json.loads(l) for l in lines if l.strip()), key=lambda x: x.get('metric', 0))
print(f\"{best['metric']}|{best.get('commit','HEAD')}\")
" 2>/dev/null)
  if [ -n "$prior_best" ]; then
    echo "⚡ Warm-start: prior run best=${prior_best%|*} at commit ${prior_best#*|}"
    # Optionally checkout that commit: git checkout ${prior_best#*|}
  fi
fi
```

If warm-start found: log origin in `trace-active.json` as `"warm_start": "<prior_run_id>"`.
The proposer can learn from the prior run's trace directory without repeating its experiments.

### Create feature branch

```bash
git checkout -b autoloop/$(basename <target> .md)-$(date +%s)
```

### Initialize TSV results log

```bash
echo "# metric_direction: <higher_is_better|lower_is_better>" > autoloop-results.tsv
if [ -n "$COST_METRIC" ]; then
  echo -e "iteration\tcommit\tmetric\tdelta\tcost\tpareto\tguard\tstatus\tdescription" >> autoloop-results.tsv
else
  echo -e "iteration\tcommit\tmetric\tdelta\tguard\tstatus\tdescription" >> autoloop-results.tsv
fi
```

### Initialize Pareto frontier (Meta-Harness pattern, if cost_metric provided)

When `cost_metric:` is set, track a Pareto frontier of non-dominated solutions (accuracy vs cost).
A candidate is **Pareto-dominated** if another candidate has both better metric AND lower cost.

```bash
# Initialize Pareto set
if [ -n "$COST_METRIC" ]; then
  echo '[]' > .traces/<run_id>/pareto.json
fi
```

**Pareto update logic** (run after every "keep" iteration):

**Deterministic alternative:** `Run: python scripts/loop-state.py pareto-update <pareto_path> --metric X --cost Y --iteration N` Returns JSON with `{added, frontier_size}`.

```python
import json
pareto = json.loads(open('.traces/<run_id>/pareto.json').read())
new = {"iter": N, "metric": metric, "cost": cost, "commit": commit}
# Remove candidates dominated by new
pareto = [p for p in pareto if not (new["metric"] >= p["metric"] and new["cost"] <= p["cost"])]
# Add new if not dominated by any existing
if not any(p["metric"] >= new["metric"] and p["cost"] <= new["cost"] for p in pareto):
    pareto.append(new)
open('.traces/<run_id>/pareto.json', 'w').write(json.dumps(pareto, indent=2))
```

During Step 1 (Review), when cost_metric is active, print the current Pareto frontier so the proposer can choose to optimize along either axis.

### Establish baseline (iteration 0)

Run verify/scorer on unmodified state. If `cost_metric:` set, also run cost command.
Record as baseline in TSV:
```
0	a1b2c3d	85.2	0.0	1240	yes	pass	baseline	initial state
```

### Best-of-N Approach Forking (opt-in, arXiv:2501.09686)

When `approaches:N` is set (N=2-3), before the iteration loop begins, fork N fundamentally different approaches and pick the best starting point. Unlike `population:N` (which varies mutations within an approach), this varies the STRATEGY itself.

**When to use:**
- Optimization target has multiple plausible strategies (e.g., skill file: restructure vs condense vs rewrite)
- Previous autoloop runs on same target stagnated (check optstate)
- Budget >= 6 iterations (need headroom for both forking AND subsequent iteration)
- NOT useful for single-axis optimization (just tuning a number) — use `population:N` instead

**Protocol:**
1. After baseline, generate N approach descriptions (1 sentence each):
   - Approach A: conservative (incremental refinement of current structure)
   - Approach B: restructural (change organization/flow, preserve content)
   - Approach C (if N=3): radical (simplify aggressively, different paradigm)

2. For each approach, spawn a parallel agent:
   ```
   Agent(model: haiku, prompt: "Apply approach '{description}' to {target}.
   Make ONE focused edit embodying this approach. Then run: {verify_command}.
   Report: the edit description + metric result.")
   ```

3. Collect N results, pick the one with best metric as starting point for iteration 1.
   - If all N are worse than baseline: start from baseline (approaches didn't help)
   - Log all N in TSV with status `approach_A`, `approach_B`, etc.

4. Continue to Phase 1 (Iteration Loop) from the winning approach's state.

**Cost:** N× one iteration cost for the forking phase. Amortized over the full run, this is typically <20% overhead for N=2.

**Interaction with population:N:** Approaches fork the STRATEGY (phase 0.5), population forks the MUTATIONS (per iteration). They compose: `approaches:2 population:2` = 2 starting strategies, then 2 mutations per iteration from the winning strategy. Budget accounting: `approaches × 1 + iterations × population`.

## Phase 1: Iteration Loop

For each iteration (1 to budget):

### Step 1: Review (git + traces as memory)

**Heartbeat stagnation check** (CORAL-inspired, before reading git log):

> **Hook-backed**: `stagnation-detector.py` PostToolUse hook monitors `autoloop-results.tsv` automatically
> and injects `[stagnation-steering:yellow/red]` messages. The check below is defense-in-depth —
> if you see a `[stagnation-steering]` message, follow it immediately.

**Deterministic alternative:** `Run: python scripts/loop-state.py stagnation <tsv_path>` Returns JSON with `{stagnant, consecutive_discards, exploration_weight, steering}`.

```
IF iteration > 4 AND consecutive_reverts >= 2:
  Read last 4 entries from autoloop-results.tsv
  IF all 4 statuses are "discard" or "crash":
    → Radical exploration mode: skip priorities 1-4, jump to priority 5 (simplify) or 6 (radical experiment)
    → Log in run diary: "Heartbeat: forcing radical shift after 4 consecutive failures"
  ELIF 3 of 4 are "discard":
    → Force strategy change: if last attempts were "exploit", switch to "explore" (or vice versa)
    → Log: "Heartbeat: strategy pivot after 3/4 discards"
```
Zero overhead when triggers don't fire — check is O(1) read from TSV tail.

**MUST complete ALL steps** — git history and traces are the primary learning mechanisms:

1. Read current state of in-scope files
2. Read last 10-20 entries from `autoloop-results.tsv`
3. Run `git log --oneline -10` — see recent experiments (kept vs reverted)
4. If last iteration was "keep": run `git diff HEAD~1` — understand WHAT worked
5. **If `.traces/<run_id>/` exists**: follow `trace-review.md` → Trace-Informed Review Protocol (grep traces for failed/successful iteration, read error outputs, mandatory diagnosis)
6. Decide: exploit success (variant of what worked) or explore new approach

**Priority order for next change:**
1. Fix crashes/failures from previous iteration
2. Exploit successes — try variants in same direction
3. Explore new approaches — untried in git history
4. Combine near-misses — two changes that individually didn't help
5. Simplify — remove code while maintaining metric
6. Radical experiment — when incremental changes stall

### Step 2: Modify (one atomic change)

Make ONE focused edit. The one-sentence test: if you need "and" to describe it, it's two changes — split them.

**Run Diary**: Append to `.claude/memory/intermediate/run-diary-<slug>.md`:
```
## Iteration <N>
**Tried**: <what changed and why>
```

Rules:
- **One change per iteration** — don't rewrite
- **Small, targeted edits** — a hypothesis, not a rewrite
- **Preserve structure** — never break YAML frontmatter or file format
- **In-scope only** — never modify guard/test files

### Step 2.5: Self-Revision Check (SD-ZERO inspired)

Before committing, review your own change for obvious errors:

1. **Re-read the diff** — `git diff` on modified files
2. **Answer 3 questions** (internally, don't output):
   - Does this change match my stated hypothesis from Step 1?
   - Could this break the file format / structure / imports?
   - Is this truly ONE atomic change, or did I sneak in extras?
3. **If any answer is NO** → fix before proceeding to Step 3
4. **If all YES** → proceed to Step 3

Time budget: <15 seconds. This is a fast sanity gate, not a full review.
Do NOT spawn a critic agent here — that defeats the purpose (SD-ZERO: self-revision is cheaper than external evaluation).

Log in run diary if self-revision caught something:
```
**Self-check**: caught <issue> — fixed before commit
```

**Anti-loop safeguard:** This step runs ONCE — check, optional fix, proceed. No retry loop. If the fix itself is wrong, the normal verify/discard cycle (Steps 4-6) catches it.

### Step 3: Commit (before verification)

```bash
# Stage ONLY in-scope files (never git add -A)
git add <specific-files>

# Check if there's actually something to commit
git diff --cached --quiet && echo "no-op" || \
git commit -m "experiment(<scope>): <one-sentence description>"
```

If nothing to commit: log as `no-op`, skip verify, next iteration.
If pre-commit hook blocks: fix issue and retry (max 2 attempts), then log as `hook-blocked`.

**Trace diff capture:** If traces active, follow `trace-review.md` → Diff Capture section.

### Step 4: Verify (mechanical only)

**Spot-check gate** (AutoAgent-inspired): If eval suite has **5+ cases** (metric mode with multi-case verify, or file mode with multiple scored dimensions), run a random subset of 2-3 cases first. Only proceed to full eval if spot-check passes. This saves compute on obviously broken changes — especially valuable in longer runs (10+ iterations).

```
IF eval_cases >= 5:
    spot_sample = random.sample(eval_cases, min(3, len(eval_cases)))
    spot_result = run_verify(spot_sample)
    IF spot_result regressed vs baseline:
        STATUS = "discard"  # Skip full eval, save time
        Log: "⚡ Spot-check failed on {len(spot_sample)} cases — skipping full eval"
        GOTO Step 6
    ELSE:
        proceed to full eval below
```

**Metric mode:** Run the verify command, extract the metric number.
**File mode:** Run the built-in scorer (see Scoring section).

Timeout: if verify exceeds 2x normal time, kill and treat as crash.

### Step 5: Guard (regression check)

**Only if `guard:` was configured.** Run guard command after successful verify.

- **Verify** = "Did the metric improve?" (the goal)
- **Guard** = "Did anything else break?" (the safety net)

Guard is pass/fail only (exit code 0 = pass). If guard fails:
1. Revert the change
2. Read guard output to understand WHAT broke
3. Rework the optimization to avoid the regression
4. Re-commit, re-verify, re-guard
5. Max 2 rework attempts, then discard

Do not modify guard or test files — changes to the measurement baseline invalidate all previous iterations and make before/after comparison meaningless. Always adapt the implementation instead.

#### Per-Axis Monotonicity Guard (opt-in, PaperOrchestra-inspired)

When `guard_axes: true` in arguments AND critic is used as guard (file mode), enforce per-dimension monotonicity:

```
IF guard_axes AND critic_scores_available:
    FOR each dimension in critic rubric (Correctness, Completeness, Quality, Safety, Coverage):
        IF score_new[dim] < score_prev[dim] - 0.5:
            AXIS_REGRESSION = true
            Log: "Axis regression: {dim} dropped {score_prev[dim]} → {score_new[dim]}"
    IF AXIS_REGRESSION:
        STATUS = "discard (axis regression)"
        # Even if overall metric improved — one dimension degraded significantly
```

Why 0.5 threshold: critic scores are 1-5, so 0.5 = 10% of scale. Smaller drops are noise; larger drops indicate a real trade-off that shouldn't be silently accepted. (arXiv:2604.05018 — PaperOrchestra Content Refinement agent accepts revisions only when no sub-axis regresses.)

### Step 6: Decide

```
IF metric improved AND (no guard OR guard passed):
    STATUS = "keep"
    # Commit stays. Update current_best.

ELIF metric improved AND guard failed:
    # Rework (max 2 attempts) — see Step 5
    IF rework succeeded: STATUS = "keep (reworked)"
    ELSE: STATUS = "discard" — revert

ELIF metric improved AND guard_axes detected axis regression:
    STATUS = "discard (axis regression)"
    git revert HEAD --no-edit
    Log: "Overall metric improved but per-axis monotonicity violated"

ELIF metric same or worse:
    STATUS = "discard"
    git revert HEAD --no-edit  # prefer revert (preserves history)
    # Fallback: git revert --abort && git reset --hard HEAD~1

ELIF crashed:
    # See Crash Recovery below
```

**Simplicity override:** If metric barely improved (+<0.1%) but adds complexity → discard.
If metric unchanged but code is simpler → keep.

### Step 7: Log to TSV

Append to `autoloop-results.tsv`:

**Deterministic alternative:** `Run: python scripts/loop-state.py tsv-append <tsv_path> --iteration N --metric X.X --status keep|discard|crash --description "..."` Returns JSON with delta computation.

```
iteration	commit	metric	delta	guard	status	description
5	c3d4e5f	88.3	+1.2	pass	keep	add error handling tests
6	-	87.1	-1.2	-	discard	refactor helpers (broke 2 tests)
7	-	0.0	0.0	-	crash	add integration tests (DB failed)
```

Valid statuses: `baseline`, `keep`, `keep (reworked)`, `discard`, `discard (axis regression)`, `crash`, `no-op`, `hook-blocked`

**Run Diary**: Update the current iteration entry:
```
**Result**: <metric delta, status>
**Analysis**: <why it worked or didn't>
**Next**: <what to try next based on this>
```

### Step 8: Check exit + status block

```
AUTOLOOP_STATUS:
  iteration: <N>
  score: <current>
  delta: <+/-N or 0>
  consecutive_reverts: <count>
  exploration_weight: <1.0|1.4|1.7|2.0>
  EXIT_SIGNAL: <true|false>
```

Exit when ANY:
- **Adaptive plateau** (Hyperagents-inspired): instead of hard stop, ramp exploration first:

  **Deterministic alternative:** `Run: python scripts/loop-state.py exploration-weight <tsv_path>` Returns JSON with `{consecutive_discards, exploration_weight, exit_signal}`.

  | consecutive_discards | exploration_weight | Strategy shift |
  |---------------------|-------------------|----------------|
  | 3 | 1.4 | Prioritize radical experiments over incremental |
  | 3 + `escalate:true` | **ESCALATE** | Trigger Escalation Phase (see below) instead of continuing |
  | 4 | 1.7 | Combine two prior near-misses into one attempt |
  | 5 | 2.0 | Try approach opposite to all prior keeps |
  | 6 | 2.0 | One last radical attempt |
  | 7 | **HARD STOP** | Adaptive exploration exhausted |

  When `exploration_weight > 1.0`: Step 1 (Review) MUST list ALL prior keep descriptions, identify common direction, and propose something structurally different.

- **Late-phase recovery** (ref: arXiv:2603.19138 — LLM agents concentrate 46.5% of backtracking in the final 10% of a session):
  When iteration ≥ 70% of budget, inject this self-check into Step 1 (Review):
  > "Re-evaluate early decisions: List paths you pruned or dismissed in iterations 1-3. Are any of them worth revisiting given what you now know? If yes, try one before continuing with incremental improvements."
  This counters the P1↔P2 lock-in loop where early pruning + path commitment prevent exploring viable alternatives.

### Escalation Phase (Agent0-inspired, optional)

Read `${CLAUDE_SKILL_DIR}/references/escalation-phase.md` for full escalation protocol (trigger, method per mode, logging).

Valid TSV statuses (updated): `baseline`, `keep`, `keep (reworked)`, `discard`, `crash`, `no-op`, `hook-blocked`, `divergence`, `escalation`

**Deterministic alternative:** `Run: python scripts/loop-state.py circuit-breaker --consecutive-reverts N --eval-cases N --skill-lines N --iteration N --max-iterations N` Returns JSON with `{stop, triggers}`.

- **Max score**: metric can't improve further
- **Budget**: iteration count hit limit
- **Crash loop**: 3 crashes in a row

Every 5 iterations, print progress summary:
```
=== AutoLoop Progress (iteration 15) ===
Baseline: 85.2 → Current: 92.1 (+6.9)
Keeps: 8 | Discards: 5 | Crashes: 2
```

### Advisor Checkpoint (at progress summary)

At the progress summary point (every 5 iterations), invoke the advisor checkpoint protocol from `${CLAUDE_SKILL_DIR}/../orchestrate/references/advisor-checkpoint.md`.

Spawn an Opus sub-agent with current trajectory data (baseline, best, keeps/discards, last 3 iteration summaries from TSV). Advisor returns strategic direction in ≤500 tokens. Incorporate DIRECTION into next hypothesis generation, add AVOID items to strategies-that-fail.

**Skip conditions:** budget ≤ 3, trend is "strong improving", or already used 3+ advisor consultations this run.

## Crash Recovery Protocol

| Failure | Response | Count as iteration? |
|---------|----------|-------------------|
| Syntax error | Fix immediately, re-commit | No |
| Runtime error | Attempt fix (max 3 tries), then revert + next | Yes |
| Resource exhaustion (OOM) | Revert, try smaller variant | Yes |
| Infinite loop / hang | Kill after timeout, revert | Yes |
| External dependency | Skip, log, try different approach | Yes |

On crash: always revert to last known-good state before continuing.

## Reward Hacking Detection

Read `${CLAUDE_SKILL_DIR}/references/reward-hacking.md` for full detection protocol (divergence signals, overfitting guard, on-divergence procedure).

Key signals monitored: complexity creep (>30% LOC growth), churn cycling (3 flip-flops), metric spike (>3x avg delta). On detection: pause loop, warn user, log `divergence` status.

## Phase 2: Final Validation (LLM-as-judge)

After loop ends, ONE semantic validation:

**Skill targets:**
> Evaluate on 3 dimensions (1-10): Trigger clarity, Instruction completeness, Integration quality.

**Other targets:**
> Does this file achieve its stated purpose clearly and completely? Score 1-10.

If validation score dropped below 5: warn — structural improvements may have hurt semantic quality.

## Phase 3: Report

```markdown
## AutoLoop Report: <target>

**Goal**: <goal>
**Mode**: file | metric (verify: <command>, guard: <command>)
**Iterations**: <used> / <budget>
**Branch**: autoloop/<name>

### Results Log

| Iter | Metric | Delta | Guard | Status | Description |
|------|--------|-------|-------|--------|-------------|
| 0 | 85.2 | — | pass | baseline | initial state |
| 1 | 87.1 | +1.9 | pass | keep | add auth edge case tests |
| ... |

### Pareto Frontier (if cost_metric was tracked)

| # | Metric | Cost | Commit | Description |
|---|--------|------|--------|-------------|
| 1 | 93.4 | 980 | c3d4e5f | simplified scoring |
| 2 | 91.2 | 620 | a1b2c3d | minimal variant |

Non-dominated solutions only. Use `/eval --experiments pareto <run_id>` to query later.

### Summary
- **Baseline**: <score> → **Best**: <score> (+<total delta>) | **Median (kept)**: <median>
- **Kept**: N | **Discarded**: M | **Crashes**: K
- **Validation score**: X/10
- **Exit reason**: budget | plateau | max score | crash loop
- **Guard failures**: N (reworked: M, discarded: K)

> **Why median?** Meta-Harness (arXiv:2603.28052) showed median is a more robust quality signal than best — best can be an outlier, median reflects typical iteration quality.
```

**Run Diary Summary**: Append `## Summary` section to `run-diary-<slug>.md` with key insight, best approach, dead ends. If significant findings: suggest `/scribe learning` with diary path.

**Trace deactivation:** If traces active, follow `trace-review.md` → Trace Deactivation section. Traces stay in `.traces/` for `/eval --optim` analysis.

### Performance Record

**Deterministic alternative:** `Run: python scripts/loop-state.py perf-record <tsv_path> --skill autoloop --slug <slug> --write` Generates and writes performance JSON.

Write a JSON file to `.claude/memory/performance/autoloop-<slug>-<timestamp>.json`:
```json
{
  "skill": "autoloop",
  "runId": "autoloop-<slug>-<timestamp>",
  "timestamp": "<ISO 8601>",
  "target": "<target file/scope>",
  "score_start": <baseline>,
  "score_end": <final>,
  "delta": <total delta>,
  "tokens_est": <iterations × 3500>,
  "iterations": <used>,
  "kept": <count>,
  "discarded": <count>,
  "crashed": <count>,
  "parent_run": <runId of parent if mode:tree, else null>,
  "exit_reason": "<budget|plateau|max_score|crash_loop>",
  "mode": "<linear|tree>",
  "branch": "autoloop/<name>"
}
```

Ask the user: "Merge branch `autoloop/<name>` into current branch, or discard?"

### Outcome Record (RCL credit loop)

Write an outcome record to `.claude/memory/outcomes/<date>-autoloop-<outcome>-<slug>.md`:

```markdown
---
skill: autoloop
run_id: autoloop-<slug>-<timestamp>
date: <YYYY-MM-DD>
task: "<goal>"
outcome: success | partial | failure
score_start: <baseline>
score_end: <final>
iterations: <used>
kept: <count>
discarded: <count>
exit_reason: <budget|plateau|max_score|crash_loop>
---

## Trajectory Summary
1. Baseline: <score>, <context>
2. Iter N: <change> → <delta> (<keep/discard>)
... (max 15 key iterations)

## Learnings Applied
- file: <learning-filename.md> | credit: helpful | evidence: <1-sentence why>
- file: <other.md> | credit: neutral | evidence: <why>

## What Worked (if outcome != failure)
- <key mutation that drove improvement>

## What Failed (if outcome != success)
- <key gap or wrong assumption>
```

**Outcome classification:** success = delta > 0 AND exit != crash_loop; partial = delta > 0 BUT exit == plateau/budget before target; failure = delta <= 0 OR crash_loop.

**Learnings Applied:** List every learning file that was Read/Grep'd during this run and influenced a decision. Assign credit: `helpful` if it led to a kept iteration, `harmful` if it led to a discarded one, `neutral` if consulted but not decisive.

### Optimization State Update

Read `.claude/memory/optstate/autoloop.json` at Phase 0 (Setup). After Phase 3 report, update it:

**Deterministic alternative:** `Run: python scripts/loop-state.py optstate-update <optstate_path> '<json_entry>'` Updates optimizer state with FIFO ledger.

```json
{
  "last_updated": "<YYYY-MM-DD>",
  "total_runs": <N+1>,
  "health": "exploration|developing|mature",
  "change_ledger": [
    {"date": "<date>", "run_id": "<id>", "mutations": ["<key changes>"], "effect": "<delta>", "outcome": "<outcome>"}
  ],
  "strategies_that_work": ["<patterns that led to kept iterations>"],
  "strategies_that_fail": ["<patterns that led to discards>"],
  "recurring_failure_patterns": ["<repeated failure modes>"],
  "optimization_velocity": {"stage": "exploration|development|refinement", "trend": "improving|flat|declining"}
}
```

Keep `change_ledger` max 20 entries (FIFO). Merge new run data with existing — don't overwrite, append and summarize.

### Per-Iteration Attribution (lightweight PP)

After each KEEP/DISCARD decision, append a structured attribution to `proposals.jsonl`:

```jsonl
{"iteration": N, "status": "keep", "attribution": {"learning": "<filename.md>", "credit": "helpful", "evidence": "..."}}
{"iteration": N, "status": "discard", "diagnosis": {"gap": "<what was missing>", "failure_class": "logic|assumption|integration"}}
```

This replaces RCL's expensive dual-trace (2× execution) with a lightweight post-hoc reflection step.

## Scoring: SKILL.md (built-in)

Read `${CLAUDE_SKILL_DIR}/references/scoring-heuristic.md` for the full 15-point structural scorer (12 positive signals S1-S12, 4 negative signals N1-N4) with bash implementation.

Summary: checks trigger conditions in description, frontmatter completeness, process/error sections, memory references, line count, output format, and guidelines sections.

## Scoring: Generic files

For non-SKILL.md files without `verify:`, create a custom scoring function based on the goal:
- Design 8-12 checks worth ~15 points total using grep/wc/regex
- If automated checks aren't possible, fall back to LLM-as-judge (warn about higher cost)

## Budget Awareness

1. Read `.claude/memory/budget.md` before starting
2. This does NOT count as an agent spawn (runs in main context)
3. Log the autoloop run to budget event log when done
4. Estimated cost: ~2-5k tokens per iteration + ~5k for final validation
