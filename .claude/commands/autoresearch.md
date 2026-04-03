---
name: autoresearch
description: "Use when experimentally verifying hypotheses through code iteration with measurable outcomes. Trigger on 'autoresearch', 'experiment', 'try approaches'. Do NOT use for literature review (/deepresearch) or file optimization (/autoloop)."
argument-hint: <research question> eval:<command> [target:<dir>] [budget:N] [hypotheses:<list>] [cost_metric:<command>]
context-required:
  - "research question — specific and answerable, not vague topic"
  - "eval command — locked scoring script; without it the loop cannot start"
  - "target path — one file or directory to mutate"
context:
  - trace-review.md
tags: [research, testing]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch
model: sonnet
effort: high
maxTurns: 50
handoffs:
  - skill: /scribe
    when: "Experiments produced reusable findings or architectural decisions"
    prompt: "Record: <key finding from autoresearch>"
  - skill: /scribe
    when: "PIVOT decision made or 3+ crashes of same failure category"
    prompt: "Record failure learning: <failure category + what was tried + why it failed>"
  - skill: /deepresearch
    when: "Need deeper literature review before more experiments"
    prompt: "Research: <topic that emerged from experiments>"
---

# AutoResearch — Experimental Hypothesis Loop

Claudini-inspired pattern: given a research question + evaluation script, autonomously propose approaches, implement them as code, run experiments, measure results, and iterate. Combines deepresearch (parallel agents, literature) with autoloop (iterate, measure, keep/revert).

**When to use this vs. alternatives:**
- `/autoresearch` — "Which approach works best?" (code experiments with measurable outcomes)
- `/deepresearch` — "What does the literature say?" (evidence gathering, no code)
- `/autoloop` — "Make this file better" (optimize one target, not explore approaches)

## Non-Code Applications

The loop works for anything measurable — not just code. The three files stay the same, only the content changes:

| Domain | Mutable target (`train.py`) | Locked eval (`prepare.py`) | Metric |
|--------|---------------------------|--------------------------|--------|
| **Prompt engineering** | `system-prompt.txt` | `eval_prompt.py` (LLM-as-judge or regex) | accuracy % |
| **Marketing copy** | `landing-page.md` | `eval_copy.py` (5 binary questions) | score 0–1 |
| **Config tuning** | `config.yaml` | `bench.py` | latency ms |
| **Trading strategy** | `strategy_params.json` | `backtest.py` | Sharpe ratio |
| **ML hyperparams** | `hparams.yaml` | `train_eval.py` | validation loss |

Real-world results: Shopify Liquid engine +53% parse speed (93 commits), portfolio site 50ms→25ms (4 minutes), baseball pitch velocity R² 0.44→0.78.

> **The edge is in picking the right metric.** Give the loop a bad metric and it will confidently optimize the wrong thing. Anything where "better" is subjective (brand design, UX) doesn't work — skip it.

## Four Roles — All Required

The loop works because these four roles are strictly separated. Blur any boundary and the loop fails.

| Role | What you provide | What the agent controls |
|------|-----------------|------------------------|
| **Mutable target** | `target:` path (one file) | Yes — edited every iteration |
| **Locked eval** | `eval:` command | NEVER — agent cannot touch this |
| **Direction** | research question + hypotheses | Reads only, does not modify |
| **Memory** | git history + TSV log | Commits wins, resets losses |

**The locked eval is the most commonly skipped and most important part.** Without it, the agent optimizes the test instead of optimizing the target.

## Three Non-Negotiable Conditions

The loop only functions when ALL THREE hold simultaneously:

1. **Numeric scoring** — output must be measurable as a single number (binary yes/no questions aggregated into a percentage work well)
2. **Automated evaluation** — scoring runs without human intervention; no "looks good to me"
3. **Single-file mutation** — only the target file changes per iteration; everything else locked

If any condition is missing: **stop and fix it before starting the loop.**

## 8 Experiment Rules

| # | Rule |
|---|------|
| 1 | **One hypothesis per iteration** — test one idea at a time. If it needs "and" to describe, split it |
| 2 | **Measure, don't judge** — use the eval command, not subjective assessment |
| 3 | **Git is memory** — commit before running, read history before proposing |
| 4 | **Name your hypotheses** — every experiment gets a human-readable name tracked in the log |
| 5 | **Negative results are results** — "this doesn't work" is valuable, log it properly |
| 6 | **Literature-informed, not literature-bound** — use web search to seed ideas, not to skip experiments |
| 7 | **Automatic rollback** — failed experiments revert instantly, preserving the log |
| 8 | **Detect reward hacking** — if the metric improves but something smells off, pause and flag |

## Shared Memory

Before starting:
1. Read `.claude/memory/state.md` — current task context
2. Grep `.claude/memory/learnings/` for topic-relevant patterns (max 3 queries by component/tags)
3. Read `.claude/memory/budget.md` — check remaining budget

<!-- CACHE_BOUNDARY -->

## Phase 0: Research Setup

### Parse input

From `$ARGUMENTS`, extract:
- **question**: the research question (required)
- **eval**: command that outputs a scalar metric (required — no eval = refuse to start)
- **target**: directory or file scope for experiments (default: current directory)
- **budget**: max experiment count (default: 10)
- **hypotheses**: optional comma-separated list of approaches to try first
- **cost_metric**: bash command that outputs a cost number (e.g., token count, LOC, latency) — enables Pareto frontier tracking (accuracy vs cost). Same pattern as autoloop.
- **direction**: `higher` or `lower` is better (auto-detect from question keywords, or ask)

Examples:
```
/autoresearch "best chunking strategy for RAG" eval:"python eval_rag.py | grep F1 | awk '{print $2}'" target:src/chunking/ budget:8
/autoresearch "fastest JSON parser for our schema" eval:"python bench.py" hypotheses:"orjson,ujson,msgspec"
/autoresearch "optimal prompt structure for classification" eval:"python eval_prompt.py --metric accuracy"
```

### program.md fallback

If `program.md` exists in the target directory, read it before parsing `$ARGUMENTS`. Use it as the source of truth for question, hypotheses, and constraints. CLI arguments override `program.md` values (CLI takes precedence). This enables "setup once, run many" workflow.

Expected `program.md` format:
```markdown
# Goal
Optimize JSON parsing throughput for our schema (MB/s, higher is better)

# Hypotheses
- orjson (drop-in replacement)
- msgspec with schema validation
- ujson for pure speed

# Rules
- Only edit src/parsers/json_handler.py
- Do not change the public API
- Keep Python 3.11 compatibility
```

Parse: first heading text or "Goal:" line → `question`; bulleted list under "Hypotheses:" or "Approaches:" → `hypotheses`; list under "Rules:" or "Constraints:" → constraints logged to TSV notes.

### Eval criteria design (if user needs help)

**The edge is in the metric.** A precise, measurable metric compounds over 50+ iterations. A vague one wastes every experiment. Before designing criteria, ask: "Can I write a unit test for this?" If yes, it's a good criterion.

If `eval:` command is a grading script that the user wants help designing, apply these rules:

- **3-6 binary questions** — below 3 creates loopholes, above 6 causes checklist gaming
- Every question must be answerable yes/no without subjective judgment
- Strong: "Does headline include a specific number?" — testable
- Weak: "Is the copy compelling?" — subjective, unscoreable
- Test on 3 samples before starting the loop; scoring must be consistent

Example for landing page copy:
```
1. Does headline include specific number or measurable result? (y/n)
2. Completely free of buzzwords? (y/n)
3. CTA uses specific action verb tied to product outcome? (y/n)
4. First sentence names specific pain point? (y/n)
5. Total copy between 80-150 words? (y/n)
Score = count(yes) / 5
```

Score = percentage of yes answers. 5 questions = 0.2 increments, making progress visible.

### Precondition checks

```bash
# 1. Git clean?
git status --porcelain | head -5
# → If dirty: warn and ask to stash/commit first

# 2. Eval command works on baseline?
eval_output=$(<eval_command> 2>&1)
# → Must produce a parseable number. If not: stop, show output, ask user to fix.

# 3. Stale lock files?
ls .git/index.lock 2>/dev/null && rm .git/index.lock
```

If eval command fails on baseline: **STOP**. The user must provide a working eval command before experiments can begin.

### Create experiment branch



Follow `trace-review.md` → **Trace Initialization** section: create `.traces/<run_id>/`, write `trace-active.json` marker (skill:"autoresearch"), purge old traces. This enables the `trace-capture.py` PostToolUse hook to record tool call inputs/outputs during the experiment run.

```bash
git checkout -b autoresearch/<slug>-$(date +%s)
```

### Record baseline

```bash
baseline_metric=$(<eval_command> | grep -oP '[\d.]+' | tail -1)
baseline_loc=$(find <target> -name '*.py' -o -name '*.ts' -o -name '*.js' | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
```

### Initialize experiment log

```bash
echo "# question: <question>" > autoresearch-log.tsv
echo "# eval: <eval_command>" >> autoresearch-log.tsv
echo "# direction: <higher_is_better|lower_is_better>" >> autoresearch-log.tsv
echo "# baseline: <baseline_metric>" >> autoresearch-log.tsv
if [ -n "$COST_METRIC" ]; then
  echo -e "iteration\thypothesis\tcommit\tmetric\tdelta\tcost\tpareto\tstatus\tnotes\tdifficulty_level" >> autoresearch-log.tsv
else
  echo -e "iteration\thypothesis\tcommit\tmetric\tdelta\tstatus\tnotes\tdifficulty_level" >> autoresearch-log.tsv
fi
echo -e "0\tbaseline\t$(git rev-parse --short HEAD)\t${baseline_metric}\t0.0\tbaseline\tinitial state" >> autoresearch-log.tsv
```

## Phase 1: Literature Scout (optional, ≤5 minutes)

Quick web search to seed hypotheses — NOT a full deepresearch run.

1. Run 2-3 WebSearch queries related to the research question
2. Skim top results (WebFetch on max 2 most relevant)
3. Extract: known approaches, common pitfalls, reported metrics
4. Add to hypothesis queue (don't replace user-provided ones)

**Skip this phase if:**
- User provided explicit hypotheses
- Question is purely implementation-specific (no external knowledge needed)
- Budget ≤ 3 (not enough iterations to justify research time)

## Phase 2: Experiment Loop

The loop runs in **batches**. After each batch, a strategic ASSESS step decides the next action.

**Batch size**: `ceil(budget / 3)` iterations per batch (e.g., budget 10 → batches of 4, 3, 3).

For each iteration (1 to budget):

### Step 1: Review (git as memory)

**MUST complete ALL steps** before proposing:

1. Read `autoresearch-log.tsv` — full experiment history
2. Run `git log --oneline -10` — see what was tried
3. If last experiment was "keep": run `git diff HEAD~1` — understand WHAT worked
4. Identify: what's been tried, what worked, what failed, what's unexplored
5. **If `.traces/<run_id>/` exists**: follow `trace-review.md` → Trace-Informed Review Protocol (grep traces for failed/successful iteration, read error outputs, mandatory hypothesis diagnosis)

### Step 2: Hypothesize

Propose ONE named hypothesis based on:
- Prior experiment results (exploit successes, avoid repeated failures)
- Literature scout findings (if Phase 1 ran)
- User-provided hypotheses (try these first)
- Combinations of partial successes

Format:
```
HYPOTHESIS: <name>
RATIONALE: <why this might work, based on prior results>
APPROACH: <what code changes to make>
EXPECTED EFFECT: <prediction — helps detect reward hacking later>
```

**Run Diary**: Append to `.claude/memory/intermediate/run-diary-<slug>.md`:
```
## Experiment <N>: <hypothesis-name>
**Tried**: <approach and rationale>
```

### Step 3: Implement

Make code changes. Rules:
- **One hypothesis per iteration** — atomic changes
- **Single-file mutation** — only ONE target file changes per iteration; everything else locked. This is non-negotiable. If a hypothesis requires changing 2+ files, split it into sequential hypotheses.
- **Never modify the eval script** — that's the ground truth. If you modify it, the entire experiment history is invalidated.

### Step 4: Commit (before running)

```bash
git add <specific-files>
git diff --cached --quiet && echo "no-op" || \
git commit -m "experiment(<hypothesis-name>): <one-sentence description>"
```

**Trace diff capture:** If traces active, follow `trace-review.md` → Diff Capture section.

### Step 5: Run eval

**Spot-check gate** (AutoAgent-inspired): If the eval script runs multiple test cases (e.g., iterates over a dataset), and total eval time exceeded 30s at baseline, run on a random subset of 2-3 cases first. Only proceed to full eval if spot-check doesn't regress.

```
IF baseline_eval_time > 30s AND eval has identifiable cases:
    Run eval on 2-3 random cases → spot_metric
    IF spot_metric regressed vs best-so-far:
        STATUS = "discard"  # Skip full eval
        Log: "⚡ Spot-check failed — skipping full eval (saved ~{baseline_eval_time}s)"
        GOTO Step 6
```

Full eval:
```bash
metric=$(<eval_command> 2>&1 | grep -oP '[\d.]+' | tail -1)
```

Timeout: 5× the baseline eval time. If exceeded, kill and treat as crash.

### Step 6: Evaluate

Compare to **best-so-far** (not just previous iteration):

```
IF metric improved vs best-so-far AND direction matches:
    STATUS = "keep"
    Update best_metric, best_commit

ELIF metric same or worse:
    STATUS = "discard"
    git revert HEAD --no-edit

ELIF crashed / no output:
    STATUS = "crash"
    git revert HEAD --no-edit
```

### Step 7: Reward hacking check

After every "keep", check:

| Signal | Threshold | Action |
|--------|-----------|--------|
| **LOC creep** | Target LOC grew >30% from baseline | Flag |
| **Churn cycling** | 3 consecutive keep→revert→keep on similar diffs | Flag |
| **Metric spike** | Delta >3× running average of positive deltas | Flag |
| **Prediction mismatch** | Result contradicts EXPECTED EFFECT from Step 2 | Flag |

**Overfitting guard** (AutoAgent-inspired): After every "keep", ask: "If this exact eval case disappeared, would this change still be a worthwhile improvement?" If NO → flag as overfitting, log `divergence`.

On flag: pause, print warning, ask user to confirm.

### Step 8: Log to TSV

```
iteration	hypothesis	commit	metric	delta	status	notes
3	orjson-parser	f4a5b6c	0.847	+0.032	keep	3x faster than json.loads
4	msgspec-schema	-	0.815	-0.032	discard	type validation overhead
```

Valid statuses: `baseline`, `keep`, `discard`, `crash`, `no-op`, `divergence`

**Run Diary**: Update current experiment entry with `**Result**`, `**Analysis**`, `**Next**`.

### Step 9: Check exit conditions

Exit when ANY:
- **Budget exhausted**: iteration count hit limit
- **Plateau**: 6 consecutive discards (raised from 4 — mid-loop rescue fires at 3, giving 3 more after rescue)
- **Solved**: metric hit theoretical maximum or user-defined target
- **Crash loop**: 3 crashes in a row
- **ASSESS decision**: PROCEED issued (skip remaining budget, go to synthesis)

Every 3 iterations, print progress:
```
=== AutoResearch Progress (iteration 6/10) ===
Question: best chunking strategy for RAG
Baseline: 0.72 → Best: 0.85 (+0.13)  [hypothesis: semantic-chunking]
Keeps: 3 | Discards: 2 | Crashes: 1
```

### Step 10: Batch ASSESS — Strategic Decision Point

**Trigger:** After each batch completes (every `ceil(budget/3)` iterations), pause and assess.

Review the experiment log holistically:

```
=== BATCH ASSESS (after iteration <N>/<budget>) ===
Baseline: <baseline> → Best: <best> (+<delta>)
Kept: <K> | Discarded: <D> | Crashed: <C>
Improvement trend: <improving | flat | declining>
Remaining budget: <remaining> iterations
```

**Decision matrix:**

| Condition | Decision | Action |
|-----------|----------|--------|
| Best metric meets target OR improvement trend strong | **PROCEED** | Exit loop → Phase 3 synthesis. Remaining budget saved. |
| Some improvement but plateauing, AND approaches remain untested | **REFINE** | Keep current best. Narrow focus: try variations of best-performing hypothesis only. Continue next batch. |
| No meaningful improvement AND >50% budget spent | **PIVOT** | Keep current best as fallback. Spawn research rescue agent (see below). Reset hypothesis queue with new direction. Continue next batch. |
| All experiments crash or produce garbage | **ABORT** | Exit loop → Phase 3 with failure analysis. |

**On PIVOT:**
1. Version current artifacts: rename `autoresearch-log.tsv` → `autoresearch-log-v<N>.tsv`
2. Spawn research rescue agent (Sonnet) with WebSearch:
   - Prompt: "We're trying to improve <metric> for <question>. Approaches tried: <list from TSV>. All scored ≤<best>. Find fundamentally different approaches."
3. Agent writes to `outputs/autoresearch-rescue-<N>.md`
4. Create new experiment log, carry over baseline = current best
5. Continue loop with fresh hypotheses

**On REFINE:**
1. Log the refinement decision to run diary
2. Generate hypothesis variations: parameter tuning, combination of top-2 approaches, edge case optimization
3. Continue next batch with narrowed focus

**Forced PROCEED:** If 2 consecutive PIVOTs produced no improvement, force PROCEED with whatever best exists. Don't waste remaining budget.

**Run Diary**: Log each ASSESS decision with rationale:
```
## ASSESS after batch <N>
**Decision**: PROCEED | REFINE | PIVOT | ABORT
**Rationale**: <why this decision>
**Best so far**: <metric> via <hypothesis>
```

### Step 10.5: Adaptive Difficulty Calibration (Agent0 curriculum pattern)

After each batch ASSESS, calibrate difficulty based on performance. This creates co-evolutionary pressure: easy success → harder challenges, consistent failure → relaxed constraints.

**Compute keep_rate**: `keeps_in_batch / iterations_in_batch`

| keep_rate | Decision | Action |
|-----------|----------|--------|
| >50% | **ESCALATE** | Tighten target by 10% OR add secondary guard metric (LOC, cyclomatic complexity) |
| 20-50% | **HOLD** | Continue as-is, no calibration needed |
| <20% | **SIMPLIFY** | Widen target tolerance by 10% OR remove secondary metrics |

**ESCALATE actions** (pick the most relevant):
- Tighten numeric target: `new_target = current_target * 1.1` (if higher-is-better) or `* 0.9` (lower-is-better)
- Add complexity guard: reject iterations where target file LOC grows >20% from baseline
- Require monotonic improvement: discard iterations that don't beat the PREVIOUS iteration (not just best-so-far)

**SIMPLIFY actions** (pick the most relevant):
- Widen target tolerance: `new_target = current_target * 0.9` (higher-is-better) or `* 1.1` (lower-is-better)
- Remove secondary guard metrics added by prior ESCALATE
- Allow bigger hypothesis deltas (relax single-file mutation to 2 files if needed)

**Caps:**
- Max 2 ESCALATEs per run — after that, HOLD regardless of keep_rate
- Max 1 SIMPLIFY per run — if already simplified and still <20%, let ASSESS handle (PIVOT/ABORT)
- SIMPLIFY cannot undo more than 1 prior ESCALATE level

**Difficulty tracking:**
- `difficulty_level` starts at 1.0, +0.1 per ESCALATE, -0.1 per SIMPLIFY
- Log to TSV: add `difficulty_level` to each iteration row after calibration
- Log calibration decision to Run Diary: `[CALIBRATE] keep_rate=X%, decision=ESCALATE|HOLD|SIMPLIFY, difficulty=Y`

**Interaction with ASSESS decisions:**
- If ASSESS = PROCEED or ABORT → skip calibration (loop is ending)
- If ASSESS = REFINE → calibration runs, but only HOLD or ESCALATE (never SIMPLIFY during refinement)
- If ASSESS = PIVOT → reset difficulty_level to 1.0 (fresh start with new approach)

### Mid-loop research agent (escape hatch)

Automatically triggered by PIVOT decision (see Step 10 above). Can also trigger independently if stuck (3+ consecutive discards within a batch):
1. Spawn ONE research sub-agent (Sonnet) with WebSearch
2. Prompt: "We're trying to improve <metric> for <question>. Approaches tried: <list from TSV>. All scored ≤<best>. Find alternative approaches we haven't tried."
3. Agent writes suggestions to `outputs/autoresearch-rescue-<N>.md`
4. Read suggestions, add to hypothesis queue
5. Continue loop

This is the key difference from autoloop — autoresearch can break out of local optima by consulting external knowledge.

## Phase 3: Synthesis Report

**Trace deactivation:** If traces active, follow `trace-review.md` → Trace Deactivation section. Traces stay in `.traces/` for `/eval --optim` analysis.

After loop ends, write to `outputs/autoresearch-<slug>.md`:

```markdown
# AutoResearch Report: <question>

**Date:** <YYYY-MM-DD>
**Experiments:** <used> / <budget>
**Branch:** autoresearch/<slug>
**Best result:** <metric> (baseline: <baseline>, improvement: <+X / +X%>)
**Best hypothesis:** <name>

## Experiment Log

| # | Hypothesis | Metric | Delta | Status | Notes |
|---|-----------|--------|-------|--------|-------|
| 0 | baseline | 0.72 | — | baseline | initial state |
| 1 | ... | ... | ... | ... | ... |

## What Worked

<Top performing approaches with analysis of why — cite experiment numbers>

## What Didn't Work

<Failed approaches and why — equally important for future reference>

## Unexpected Discoveries

<Anything surprising that emerged from experiments>

## Recommended Approach

<The best implementation, with rationale and experiment evidence>

## Open Questions

<What wasn't tested, what would need more experiments>

## Reward Hacking Incidents

<Any divergence flags triggered, how they were resolved>

## Difficulty Calibration History

| Batch | keep_rate | Decision | difficulty_level | Action taken |
|-------|-----------|----------|-----------------|--------------|
| 1 | 75% | ESCALATE | 1.1 | Tightened target to 0.85 |
| 2 | 30% | HOLD | 1.1 | — |
```

## Phase 4: Handoff

1. Present the report summary in chat (best result, key finding, branch name)
2. Write performance record to `.claude/memory/performance/autoresearch-<slug>-<timestamp>.json`:
   ```json
   {
     "skill": "autoresearch", "runId": "autoresearch-<slug>-<timestamp>",
     "timestamp": "<ISO 8601>", "target": "<target dir>",
     "score_start": <baseline>, "score_end": <best>,
     "delta": <improvement>, "tokens_est": <iterations × 5000>,
     "iterations": <used>, "kept": <count>, "discarded": <count>, "crashed": <count>,
     "parent_run": null, "exit_reason": "<budget|plateau|solved|crash_loop>",
     "mode": "research", "branch": "autoresearch/<slug>",
     "difficulty_escalations": 0, "difficulty_simplifications": 0,
     "final_difficulty_level": 1.0, "guards_active": []
   }
   ```
3. Ask user: "Merge branch `autoresearch/<slug>` into current, or keep for review?"
4. Update `.claude/memory/budget.md` with experiment costs
5. If significant findings: suggest `/scribe` to record learnings

## Budget Tiers

| Tier | Experiments | Literature | When |
|------|-----------|-----------|------|
| **quick** | 3-5 | skip | Few known approaches to compare |
| **standard** | 8-12 | 2-3 searches | Open question, moderate search space |
| **deep** | 15-20 | full scout + mid-loop rescue | Complex problem, large search space |
| **industrial** | 50-100+ | minimal (known approaches) | Shopify-style bulk optimization; eval is fast (<1s), target is a single file, approach space is large |

Default to **standard**. Infer from budget argument if provided.

## Failure Taxonomy

Classify every crash/error into a category. This enables smarter recovery decisions.

| Category | Pattern | Recovery | Repairable? |
|----------|---------|----------|-------------|
| **DEPENDENCY** | ImportError, ModuleNotFoundError | `pip install` missing package, retry | Yes (1 attempt) |
| **RESOURCE** | OOM, CUDA out of memory, disk full | Reduce batch size / data size, retry | Yes (1 attempt) |
| **TIMEOUT** | Eval exceeds 5× baseline time | Kill, reduce scope, retry | Yes (1 attempt) |
| **DATA** | FileNotFoundError, empty dataset, corrupt input | Check paths, verify data exists | Yes (if path issue) |
| **DIVERGENCE** | NaN, Inf, metric outside expected range | Revert, flag for manual review | No — revert only |
| **SYNTAX** | SyntaxError, IndentationError | Fix and retry | Yes (1 attempt) |
| **LOGIC** | Assertion failed, wrong output shape | Revert, log as "approach incompatible" | No — revert only |
| **EVAL_BROKEN** | Eval script itself errors | STOP — ground truth corrupted | No — STOP |
| **ENVIRONMENT** | Permission denied, port in use, antivirus lock | Retry with delay | Yes (2 attempts) |
| **UNKNOWN** | Unclassified error | Revert, log full stderr | No — revert only |

**Repairability rule:** If the same failure category occurs 3+ times across the run, mark it as **non-repairable** for remaining iterations. Don't waste budget retrying a systemic issue.

**Auto-classification:** Parse stderr/stdout against category patterns. Log category in TSV `notes` column.

## Error Handling

| Failure | Response |
|---------|----------|
| Eval command fails on baseline | STOP — user must fix eval before experiments begin |
| Eval produces no number | STOP — show raw output, ask user to fix grep pattern |
| All experiments crash | STOP after 3rd crash, report what happened |
| 3+ crashes of same category | Mark category non-repairable, skip similar hypotheses |
| Agent rescue returns nothing | Continue with random perturbation strategy |
| Budget exceeded | Stop, synthesize what you have, note truncation |
| Git conflict on revert | `git revert --abort && git reset --hard <best_commit>` |

## Anti-Patterns to Avoid

| Temptation | Why Wrong | Do Instead |
|------------|-----------|------------|
| "Let me try 5 things at once" | Can't attribute improvement | One hypothesis per iteration |
| "The metric went up, ship it" | Might be reward hacking | Check secondary signals |
| "This approach is obviously better" | Subjective ≠ measured | Run the eval |
| "Let me tweak the eval script" | Destroys ground truth — all prior rounds invalidated | Never modify eval |
| "I'll clean up the code while I'm at it" | Conflates optimization with refactoring | Stay in scope |
| "I'll add a 2nd file to this iteration" | Violates single-file mutation, can't isolate cause | Split into two sequential hypotheses |

## Known Failure Modes (Karpathy Loop-Specific)

| Mode | Signal | Mitigation |
|------|--------|------------|
| **Goodharting** | Metric improves but output quality degrades; agent finds technical pass without real improvement | Reduce criterion count, tighten definitions, review outputs manually after 5+ keeps |
| **Eval brittleness** | Scoring produces inconsistent results for same input; crashes on edge cases | Harden eval script before loop starts; test on 3 diverse samples |
| **Convergence plateau** | Improvement slows dramatically after 20-30 rounds; marginal gains < 0.01 per iteration | This is a natural ceiling — synthesize results rather than continuing. Consider redesigning eval criteria or running a new loop with different constraints |
| **Eval over-specification** | 7+ criteria → agent games the checklist, output passes but reads mechanically | Keep to 3-6 binary questions |
| **Criterion vagueness** | Subjective criteria ("compelling", "good") → inconsistent scores across samples | Replace with testable yes/no questions |
