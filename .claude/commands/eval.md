---
name: eval
description: Use when grading or replaying harness traces to measure quality drift, detect regressions, or compare harness configurations. Trigger on 'eval trace', 'grade harness', 'replay run', 'harness drift'. Do NOT use for one-off verification (/verify) or writing tests (/tdd).
argument-hint: "[trace-file | harness-name | --list] [--replay] [--diff trace1 trace2] [--baseline] [--optim [run_id | --list | --latest | --diff run1 run2]]"
tags: [testing, devops]
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

## Rules

1. **Read-only** — never modify trace files (append-only guarantee from /harness)
2. **Isolate harness quality from model quality** — always note if model changed between traces
3. **baseline.jsonl is sacred** — never overwrite without explicit `--baseline` flag
4. **Report in Czech** if user context is Czech
5. **Missing fields** — treat absent JSONL fields as "n/a", never fail on incomplete traces
6. **--optim is read-only** — optimization traces in `.traces/` are working data, never modify
