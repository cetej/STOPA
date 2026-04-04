---
name: eval
description: Use when grading or replaying harness traces to measure quality drift, detect regressions, or compare harness configurations. Trigger on 'eval trace', 'grade harness', 'replay run', 'harness drift'. Do NOT use for one-off verification (/verify) or writing tests (/tdd).
argument-hint: "[trace-file | harness-name | --list] [--replay] [--diff trace1 trace2] [--baseline] [--optim [run_id | --list | --latest | --diff run1 run2]] [--experiments [list | top-k N | pareto run_id | diff run1 run2]] [--meta [target]]"
tags: [testing, devops]
phase: verify
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash, Agent
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Edit
---

# Eval — Harness Trace Grader & Replayer

You grade harness execution traces to measure quality, detect regressions, and separate harness infrastructure quality from model output quality. Inspired by trace-based eval patterns from SWE-bench and OpenAI eval framework.

**Core insight:** Same input + different harness config = different results. This skill isolates WHY by comparing traces — not just outputs.

## Context Checklist

| Item | Why it matters |
|------|---------------|
| **Trace file or harness name** | Without scope, grading is unfocused |
| **Mode** | --list (browse traces), --replay (re-run), --diff (compare), --baseline (lock current as expected) |

<!-- CACHE_BOUNDARY -->

## Parse Arguments

From `$ARGUMENTS`, extract:
- **trace-file**: path to `.jsonl` file (e.g. `.harness/traces/2026-03-29-skill-audit.jsonl`)
- **harness-name**: if no file given, find latest trace for this harness
- **`--list`**: list all available traces with metadata — then STOP
- **`--replay`**: re-run the harness with same inputs and compare to original trace
- **`--diff <trace1> <trace2>`**: compare two traces side by side (harness drift analysis)
- **`--baseline`**: mark current trace as the expected baseline for future regression checks

If no arguments: run `--list` mode.

---

## Mode: --list (default if no args)

### Step 1: Scan for traces

```bash
ls .harness/traces/*.jsonl 2>/dev/null || echo "No traces found"
```

### Step 2: For each trace file, parse header record

Read first line of each `.jsonl` (header record with `"phase": 0`). Extract:
- `harness` name
- `ts` (timestamp)
- `model`
- `flags`

Then read last line (final record with `"phase": "final"`). Extract:
- `status` (complete/partial/failed)
- `phases_passed` / `phases_failed`

### Step 3: Display trace index

```
Available traces:
  1. 2026-03-29-skill-audit.jsonl      skill-audit  complete   5/5 phases  sonnet
  2. 2026-03-28-zachvev-pipeline.jsonl zachvev      partial    3/5 phases  sonnet
  3. 2026-03-27-skill-audit.jsonl      skill-audit  complete   5/5 phases  haiku

Run /eval <trace-file> to grade, /eval --diff <t1> <t2> to compare.
```

---

## Mode: Grade single trace (default when trace file given)

### Step 1: Load trace

Read all lines from the `.jsonl` file. Parse each JSON record.

### Step 2: Structural validation

Check trace completeness:

| Check | Pass condition | Flag if fail |
|-------|---------------|-------------|
| Header record present | `phase: 0, event: "start"` exists | INCOMPLETE |
| Final record present | `phase: "final", event: "end"` exists | TRUNCATED |
| No phase gaps | Phases N, N+1, N+2... all present | MISSING_PHASE |
| All phases have validation field | `"validation": "PASS\|FAIL"` in each record | UNVALIDATED |
| Preflight record present | `phase: "0.5"` exists | NO_PREFLIGHT |

### Step 3: Quality metrics

Compute from trace data:

| Metric | Formula | Meaning |
|--------|---------|---------|
| **pass_rate** | phases_passed / total_phases | Execution success rate |
| **retry_rate** | phases_with_retry / total_phases | How often phases needed retry |
| **preflight_score** | from preflight record `score` field | Infrastructure quality (0-5) |
| **phase_coverage** | phases_validated / total_phases | Fraction with explicit validation |
| **harness_health** | composite: pass_rate × phase_coverage × (preflight_score/5) | Overall harness quality score 0-1 |

### Step 4: Baseline comparison (if baseline exists)

Check for `.harness/traces/<harness-name>.baseline.jsonl`:
- If exists: compare harness_health score
  - Delta > +0.1: improvement ↑
  - Delta < -0.1: regression ↓ → WARN
  - Within ±0.1: stable →

### Step 5: Report

```
## Eval Report: <trace-file>
Harness:   <name>
Run date:  <ts>
Model:     <model>

Metrics:
  pass_rate:       5/5 (100%)
  retry_rate:      1/5 (20%) — Phase 3 retried once
  preflight_score: 4/5
  phase_coverage:  5/5 (100%)
  harness_health:  0.80

vs baseline:  0.80 → 0.75 (↓ -0.05) [within noise, no regression]

Phase timeline:
  Phase 1: PASS ✓  (dispatch)
  Phase 2: PASS ✓  (analysis)
  Phase 3: PASS ✓  (retry=true — schema mismatch on first attempt)
  Phase 4: PASS ✓  (synthesis)
  Phase 5: PASS ✓  (output)

Issues:
  ⚠ Phase 3 required retry — check validation criteria or input format
  ⚠ Preflight: output schema missing for Phase 2

Recommendation: /eval --baseline to lock this as new baseline if satisfied.
```

---

## Mode: --diff (compare two traces)

Compare two trace files to detect harness drift — what changed between runs.

### Step 1: Load both traces

Read all records from trace1 and trace2.

### Step 2: Phase-by-phase comparison

For each phase present in both traces:

| Phase | trace1 validation | trace2 validation | retry t1 | retry t2 | Drift |
|-------|------------------|------------------|----------|----------|-------|
| 1 | PASS | PASS | no | no | — |
| 2 | PASS | FAIL | no | yes | ↓ REGRESSION |
| 3 | PASS | PASS | yes | no | ↑ IMPROVEMENT |

### Step 3: Infrastructure comparison

| Metric | trace1 | trace2 | Delta |
|--------|--------|--------|-------|
| preflight_score | 4/5 | 3/5 | ↓ -1 |
| harness_health | 0.80 | 0.65 | ↓ -0.15 |
| model | sonnet | haiku | CHANGED |
| phases_passed | 5/5 | 4/5 | ↓ -1 |

### Step 4: Root cause classification

If drift detected, classify:
- **Model change**: different `model` in header → model quality diff, not harness
- **Preflight regression**: lower preflight_score → infrastructure degraded
- **Phase failure**: specific phase failed → isolate to that phase's inputs/validation
- **Retry increase**: more retries in trace2 → validation criteria may have tightened or input changed

### Step 5: Diff report

```
## Diff Report: trace1 vs trace2

Infrastructure:
  Model:     sonnet → haiku  (CHANGED — explains ~60% of output quality delta)
  Preflight: 4/5 → 3/5  (output schema lost for Phase 2)

Phase drift:
  Phase 2: PASS → FAIL  (REGRESSION — Phase 2 validation failed, retry needed)
  Phase 3: retry=true → retry=false  (IMPROVEMENT)

harness_health:  0.80 → 0.65  (↓ -0.15 regression)

Root cause: Model downgrade (sonnet→haiku) + missing Phase 2 output schema
Recommendation: Restore sonnet, add output schema for Phase 2
```

---

## Mode: --replay

Re-execute the harness with the same configuration as the original trace.

### Step 1: Load original trace header

Extract from header record:
- harness name
- model used
- flags (dry_run, trace)
- original timestamp

### Step 2: Check harness still exists

```bash
ls .claude/harnesses/<name>/HARNESS.md
```

If not found: STOP with error "Harness '<name>' not found. Cannot replay."

### Step 3: Run harness with --trace

Spawn sub-agent to run: `/harness <name> --trace`

New trace will be saved to `.harness/traces/<today>-<name>.jsonl`

### Step 4: Auto-diff

After replay completes, automatically run `--diff <original-trace> <new-trace>` and display the diff report.

---

## Mode: --baseline

Lock current trace as the expected baseline for regression detection.

### Step 1: Load trace

Read the trace file header to extract harness name.

### Step 2: Copy as baseline

```bash
cp <trace-file> .harness/traces/<harness-name>.baseline.jsonl
```

### Step 3: Confirm

Report: `Baseline locked: .harness/traces/<harness-name>.baseline.jsonl`
`Future /eval runs on <harness-name> will compare against this baseline.`

---

## Mode: --optim (optimization trace analysis)

Grade optimization runs (autoloop, autoresearch, self-evolve) from `.traces/` directory.
Meta-Harness-inspired: measures how well the proposer used trace data for causal reasoning.

### Sub-modes

- **`--optim --list`**: List all optimization trace directories
- **`--optim <run_id>`**: Grade specific optimization run
- **`--optim --latest`**: Grade most recent run
- **`--optim --diff <run1> <run2>`**: Compare two runs on same target

### Step 1: Scan for optimization traces

```bash
ls -d .traces/*/ 2>/dev/null || echo "No optimization traces found"
```

For each directory, read `iterations.jsonl` (last line) and `proposals.jsonl` to extract:
- Skill name (from run_id prefix: autoloop-, autoresearch-, self-evolve-)
- Target, iteration count, final metric, total keeps/discards

### Step 2: Quality metrics (for grading a single run)

| Metric | Formula | Meaning |
|--------|---------|---------|
| **proposal_quality** | proposals with non-null trace_evidence / total | How often proposer used trace data |
| **trace_utilization** | unique iterations referenced in proposals / total iterations | Coverage of trace evidence |
| **convergence_efficiency** | (final_metric - baseline) / iterations_used | Improvement per iteration |
| **plateau_escape_rate** | plateaus escaped / plateaus encountered | Trace-informed pivot effectiveness |
| **discard_to_keep_ratio** | discards / keeps | Lower is better — efficient exploration |

Parse from:
- `proposals.jsonl`: count records with/without `trace_evidence`
- `iterations.jsonl`: extract metrics, statuses, compute plateaus (3+ consecutive discards)
- `tools.jsonl`: count total tool calls, error rate

### Step 3: Optim report

```
## Optimization Eval: <run_id>
Skill:   autoloop
Target:  .claude/skills/critic/SKILL.md
Iters:   10 / 15 budget

Metrics:
  proposal_quality:       7/10 (70%) — trace evidence in 7 of 10 proposals
  trace_utilization:      8/10 (80%) — 8 iterations referenced in diagnoses
  convergence_efficiency: +0.82/iter
  plateau_escape_rate:    1/1 (100%) — escaped 1 plateau via trace-informed pivot
  discard_to_keep:        4:6

Timeline:
  Baseline: 85.2 → Final: 93.4 (+8.2)
  Keeps: 6 | Discards: 4 | Crashes: 0
  Plateaus: 1 (iter 5-7, escaped at iter 8 via strategy: simplify)

Trace effectiveness:
  Iterations WITH trace evidence:  avg delta +1.3
  Iterations WITHOUT trace evidence: avg delta +0.4
  → Trace-informed proposals 3.25× more effective
```

### Step 4: Optim diff (--optim --diff)

Compare two runs on the same target:

| Metric | run1 | run2 | Delta |
|--------|------|------|-------|
| convergence_efficiency | +0.82 | +0.45 | run1 better |
| proposal_quality | 70% | 30% | run1 more trace-informed |
| final_metric | 93.4 | 89.1 | run1 better |

Root cause: "run1 used trace evidence 2.3× more often, especially during plateau at iter 5-7"

---

## Mode: --experiments (unified experiment query CLI)

Meta-Harness-inspired unified query interface over ALL optimization experiments. This is the "CLI over logs" recommended by the Meta-Harness paper authors — enables structured browsing across runs without manual grep.

### Sub-modes

- **`--experiments list`**: Summary of all optimization runs
- **`--experiments top-k <N>`**: Best N iterations across all runs
- **`--experiments pareto <run_id>`**: Pareto frontier for a run (requires cost_metric)
- **`--experiments diff <run1> <run2>`**: Compare two optimization runs

### --experiments list

Scan all `.traces/*/iterations.jsonl` and performance records in `.claude/memory/performance/`:

```bash
ls -d .traces/*/ 2>/dev/null
ls .claude/memory/performance/*.json 2>/dev/null
```

Display summary table:

```
Optimization Experiments:
  #  Run ID                          Skill         Target              Best    Iters  Date
  1  autoloop-critic-1711900000      autoloop      critic/SKILL.md     93.4    10/15  2026-03-31
  2  autoresearch-rag-1711800000     autoresearch  src/chunking/       0.85    8/10   2026-03-30
  3  self-evolve-scout-1711700000    self-evolve   scout/SKILL.md      0.92    12/20  2026-03-29

Run /eval --experiments top-k 5 for best iterations, /eval --experiments pareto <run_id> for Pareto frontier.
```

### --experiments top-k N

Parse ALL `iterations.jsonl` files, collect all "keep" iterations, sort by metric (respecting direction), show top N:

```
Top 5 iterations across all runs:
  #  Run                         Iter  Metric  Hypothesis/Description      Commit
  1  autoloop-critic-1711900000  8     93.4    simplified scoring logic    c3d4e5f
  2  autoresearch-rag-1711800000 6     0.85    semantic-chunking           f4a5b6c
  3  autoloop-critic-1711900000  5     91.2    added error handling tests  a1b2c3d
  ...
```

### --experiments pareto <run_id>

Read `.traces/<run_id>/pareto.json`. If not found: "No Pareto data — run was not started with cost_metric."

If found, display the Pareto frontier:

```
Pareto Frontier: autoloop-critic-1711900000
  #  Metric  Cost   Commit   Description
  1  93.4    1240   c3d4e5f  simplified scoring (best accuracy)
  2  91.2    620    a1b2c3d  minimal variant (best cost)
  3  88.5    340    d4e5f6g  ultra-compact (lowest cost)

Non-dominated solutions only. No other candidate is both more accurate AND cheaper.
```

### --experiments diff <run1> <run2>

Compare two runs (same target preferred but not required):

```
Experiment Diff: run1 vs run2
  Target:     critic/SKILL.md (same)
  Skill:      autoloop vs autoloop
  Iterations: 10/15 vs 8/10
  Best:       93.4 vs 89.1 (+4.3 for run1)
  Kept:       6 vs 4
  Discarded:  4 vs 4
  Crashed:    0 vs 2

  Run1 used cost_metric: yes (Pareto: 3 solutions)
  Run2 used cost_metric: no

  Top approaches unique to run1: simplified scoring, error handling
  Top approaches unique to run2: parallel tests, caching
```

---

## Mode: --meta (cross-run trace synthesis)

AutoAgent-inspired: synthesize meta-patterns across ALL optimization runs. This is the "persistent meta-agent memory" that AutoAgent builds implicitly — here we build it analytically from trace data.

**Purpose:** Answer "What have I learned across all my optimization runs?" instead of grading individual runs.

### Sub-modes

- **`--meta`**: Analyze all runs in `.traces/`
- **`--meta <target>`**: Analyze only runs targeting a specific file/skill

### Step 1: Collect all optimization runs

```bash
ls -d .traces/*/ 2>/dev/null
```

For each run, parse `iterations.jsonl` and `proposals.jsonl` to extract:
- Skill type, target, date, iteration count, final metric, baseline metric
- All hypotheses with their status (keep/discard/crash)
- All `trace_evidence` fields from proposals
- Strategy types used (from proposals or self-evolve curriculum)

### Step 2: Strategy effectiveness analysis

Group all hypotheses by type/approach (extract from hypothesis text, categorize):

| Strategy category | Attempts | Keeps | Keep rate | Avg delta when kept |
|-------------------|----------|-------|-----------|---------------------|
| Prompt refinement | 12 | 3 | 25% | +0.8 |
| Tool addition | 5 | 4 | 80% | +2.1 |
| Simplification | 8 | 6 | 75% | +1.5 |
| Error handling | 4 | 1 | 25% | +0.3 |

**Top 3 successful strategies** — highest keep_rate with ≥3 attempts
**Top 3 failure modes** — lowest keep_rate with ≥3 attempts

### Step 3: Target fragility analysis

Group runs by target file:

| Target | Runs | Total iters | Best improvement | Crashes | Fragility |
|--------|------|-------------|-----------------|---------|-----------|
| critic/SKILL.md | 3 | 28 | +8.2 | 0 | low |
| scout/SKILL.md | 2 | 15 | +3.1 | 4 | high |

**Fragility** = crash_rate + revert_rate. High fragility = target resists optimization.

### Step 4: Temporal patterns

- **Improvement rate over time**: Are later runs more efficient than earlier ones? (convergence_efficiency trend)
- **Trace utilization trend**: Is proposal_quality improving across runs? (learning to use traces better)
- **Diminishing returns**: Are final deltas shrinking for same targets? (approaching optimum)

### Step 5: Meta report

```
## Cross-Run Meta-Analysis
Runs analyzed: 8 (autoloop: 4, autoresearch: 2, self-evolve: 2)
Period: 2026-03-15 → 2026-04-03
Total iterations: 62 | Total keeps: 28 (45%) | Total crashes: 3 (5%)

### What Works
1. Tool addition (80% keep rate, avg +2.1) — highest-leverage strategy
2. Simplification (75% keep rate, avg +1.5) — reliable, low-risk
3. Trace-informed proposals 2.8× more effective than blind proposals

### What Fails
1. Prompt refinement alone (25% keep rate) — diminishing returns after 2-3 edits
2. Error handling additions (25% keep rate) — usually adds complexity without metric gain
3. Proposals without trace_evidence: 18% keep rate vs 52% with evidence

### Target Health
- critic/SKILL.md: well-optimized, approaching plateau (last 2 runs: <1% improvement)
- scout/SKILL.md: fragile — 27% crash rate, needs structural refactor before optimization

### Recommendations
- For future autoloop runs: prioritize tool addition and simplification over prompt refinement
- scout needs /systematic-debugging before more /autoloop runs
- Consider running /self-evolve on critic (high baseline, good for adversarial hardening)
```

### Step 6: Optional — save to learnings

If meta-analysis reveals a strong, non-obvious pattern (e.g., "prompt refinement never works on files >200 LOC"), offer to save as a learning:

> "Save this finding as a learning for future optimization runs? (yes/no)"

If yes: write to `.claude/memory/learnings/` with type `best_practice`, source `auto_pattern`, tags matching the target components.

---

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "The trace file is too large so I'll just sample a few entries" | Sampling introduces selection bias; systematic regressions may hide in unsampled entries | Process all entries; use streaming/chunking if needed, but never skip data |
| "The scores look similar so there's no regression" | Small absolute differences can indicate systematic drift; statistical significance requires proper comparison | Compute deltas and flag any dimension where the change exceeds the noise threshold |
| "I'll skip the baseline comparison since this is the first eval run" | Without a baseline, there's no way to detect regressions in future runs; the first run IS the baseline | Always save the results as a baseline even if there's nothing to compare against yet |
| "The harness config changed but the traces are still comparable" | Config changes invalidate comparisons; different prompts, models, or parameters produce incomparable results | Flag config mismatches explicitly; compare only traces from matching configurations |

## Rules

1. **Read-only** — never modify trace files (append-only guarantee from /harness)
2. **Isolate harness quality from model quality** — always note if model changed between traces
3. **baseline.jsonl is sacred** — never overwrite without explicit `--baseline` flag
4. **Report in Czech** if user context is Czech
5. **Missing fields** — treat absent JSONL fields as "n/a", never fail on incomplete traces
6. **--optim is read-only** — optimization traces in `.traces/` are working data, never modify
