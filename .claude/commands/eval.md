---
name: eval
description: Use when grading or replaying harness traces to measure quality drift, detect regressions, or compare harness configurations. Trigger on 'eval trace', 'grade harness', 'replay run', 'harness drift'. Do NOT use for one-off verification (/verify) or writing tests (/tdd).
argument-hint: "[trace-file | harness-name | --list] [--replay] [--diff trace1 trace2] [--baseline]"
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

## Rules

1. **Read-only** — never modify trace files (append-only guarantee from /harness)
2. **Isolate harness quality from model quality** — always note if model changed between traces
3. **baseline.jsonl is sacred** — never overwrite without explicit `--baseline` flag
4. **Report in Czech** if user context is Czech
5. **Missing fields** — treat absent JSONL fields as "n/a", never fail on incomplete traces
