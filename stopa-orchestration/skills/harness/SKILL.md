---
name: harness
description: Use when running a deterministic, repeatable process from a harness definition. Trigger on 'run harness', 'execute pipeline'. Do NOT use for ad-hoc tasks.
argument-hint: "[harness-name] [--dry-run] [--trace]"
context-required:
  - "harness name — required; use /harness with no args to list available"
  - "input parameters — specific to the harness; check harness definition for required fields"
tags: [testing, devops]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
model: sonnet
effort: high
maxTurns: 50
---

# Harness — Deterministic Process Runner

You are the harness dispatcher. You run fixed-phase processes with programmatic validation.

## How it works

Unlike `/orchestrate` (dynamic plans, LLM decides steps), harnesses have **fixed phases in fixed order**. Each phase has clear inputs, actions, validation criteria, and outputs. No phase can be skipped.

## Context Checklist

If any item below is missing from `$ARGUMENTS`, ask **one question** before proceeding.

| Item | Why it matters |
|------|---------------|
| **Harness name** | Without it, dispatch cannot route — run with no args to list available harnesses |
| **Input parameters** | Each harness has required inputs; check its definition before running |

## Phase 0: Dispatch

### Read shared context

Read `.claude/memory/learnings.md` — apply relevant patterns to harness execution. Known anti-patterns may affect phase ordering or validation strategy.

### Parse input

From `$ARGUMENTS`, extract:
- **harness name**: which harness to run (e.g., `skill-audit`, `zachvev-pipeline`)
- **`--dry-run`**: if present, preview execution plan without running phases (see Phase 1b)
- **`--trace`**: if present, save per-phase JSONL trace to `.harness/traces/` for eval/replay
- If empty: list available harnesses and let user choose

### List available harnesses

```bash
# Scan for harnesses
ls .claude/harnesses/*/HARNESS.md
```

For each found harness, display:
- Name (from frontmatter)
- Description
- Number of phases
- Estimated token cost

### Load engine

Read `.claude/harnesses/_engine.md` — this contains shared execution logic.

### Load harness

Read `.claude/harnesses/<name>/HARNESS.md` — this contains the specific phases.

### Trace initialization (only if `--trace`)

If `--trace` was passed:
1. Create `.harness/traces/` directory if not exists
2. Set trace path: `.harness/traces/<YYYY-MM-DD>-<harness-name>.jsonl`
3. Write header record (one JSON per line):
   ```json
   {"ts": "<ISO-8601>", "phase": 0, "phase_name": "dispatch", "event": "start", "harness": "<name>", "model": "<model>", "flags": {"dry_run": false, "trace": true}}
   ```

## Phase 0.5: Pre-flight Quality Check

Before execution, assess harness setup quality. This score measures **harness infrastructure quality** independent of model quality — runtime config can shift results more than model differences.

Run each check and record result:

| # | Check | How | Points |
|---|-------|-----|--------|
| 1 | CLAUDE.md or AGENTS.md present | `Glob CLAUDE.md` / `Glob AGENTS.md` | +1 |
| 2 | Harness has `requires:` section with env vars listed | Grep `requires:` in HARNESS.md | +1 |
| 3 | Every phase has `validation:` criteria defined | Count phases with validation block | +1 |
| 4 | Every phase has `outputs:` schema or path defined | Check output definitions per phase | +1 |
| 5 | Context budget OK (session-stats.json < 70%, or file absent = assume OK) | Read `.claude/memory/session-stats.json` | +1 |

Display result before proceeding:

```
Harness Quality: N/5
✓ CLAUDE.md present
✓ 3/3 phases have validation criteria
⚠ Phase 2 missing output schema → results may be unparseable by /eval
✓ Context budget: 42% (session-stats.json)
```

**Gate:**
- Score **< 3**: WARN — "Harness quality is low (N/5). Results may be unreliable or unrepeateable. Continue? (y/n)"
- Score **≥ 3**: proceed silently (just show the score block)

If `--trace` active: append quality check record:
```json
{"ts": "<ISO>", "phase": "0.5", "phase_name": "preflight", "event": "quality_check", "score": N, "checks": {"claude_md": true, "requires": true, "validation": true, "output_schema": false, "context_budget": true}}
```

## Phase 1: Check for resume

Check if `.harness/` directory exists with prior results:
- If yes: find last valid phase output, offer to resume from next phase
- If no: start fresh, create `.harness/` directory

## Phase 1b: Dry-run preview (only if `--dry-run`)

If `--dry-run` was passed in `$ARGUMENTS`, show the execution plan and STOP:

1. Parse all phases from HARNESS.md
2. For each phase, display:
   ```
   Phase N/M: <name> (<type>)
     inputs:  <expected input files/data from prior phases>
     outputs: <output file path>
     model:   <model to use>
   ```
3. Validate phase connectivity: each phase's expected inputs must match a prior phase's output
4. Estimate total cost: count phases × model tier (haiku ≈ $0.05, sonnet ≈ $0.15, opus ≈ $0.50 per phase)
5. Print summary:
   ```
   Phases: N total (M deterministic, K llm, J parallel)
   Estimated cost: ~$X.XX
   Resume point: <phase N if .harness/ exists, otherwise "fresh start">
   ```
6. **STOP** — do not proceed to Phase 2. Exit with message: "Dry run complete. Run without --dry-run to execute."

## Phase 2: Execute phases sequentially

For each phase in HARNESS.md:

1. **Announce**: "Phase N/M: <name> (<type>)"
2. **Load inputs**: Read outputs from previous phases in `.harness/`
3. **Set model**: Use model specified in phase, or default per engine rules
4. **Execute**: Run the phase action (deterministic, LLM, parallel, template)
5. **Save**: Write output to `.harness/phaseN_<name>.json`
6. **Validate**: Run validation checks
7. **Report**: "Phase N: PASS ✓" or "Phase N: FAIL ✗ — <reason>"
8. **Trace** (only if `--trace` active): append record to trace JSONL:
   ```json
   {"ts": "<ISO>", "phase": N, "phase_name": "<name>", "type": "<deterministic|llm|parallel|template>", "event": "complete", "validation": "PASS|FAIL", "tool_calls": ["Read:path/file.py", "Bash:pytest"], "output_path": ".harness/phaseN_<name>.json", "retry": false, "tokens_est": null}
   ```
   If retry occurred, set `"retry": true` and add `"retry_reason": "<brief reason>"`.

If validation fails:
- Save error context to `.harness/error.md`
- Retry once with adjusted approach
- If 2nd fail: STOP, report to user with diagnosis

## Phase 3: Generate output

If harness has `output_template`:
- Load template from harness directory
- Fill with data from all phases
- Validate no `{{MISSING}}` placeholders remain
- Save final output

## Phase 4: Cleanup and report

1. Update `.claude/memory/state.md` — harness completed
2. Report summary: phases passed/failed, key findings, output location
3. If issues found: suggest next actions
4. **Trace finalization** (only if `--trace` active):
   - Append final record:
     ```json
     {"ts": "<ISO>", "phase": "final", "event": "end", "status": "complete|partial|failed", "phases_passed": N, "phases_failed": M, "harness": "<name>"}
     ```
   - Report to user: `Trace saved → .harness/traces/<date>-<name>.jsonl  (use /eval to grade or replay)`

## Parallel sub-agents

When a phase specifies `- **Parallelism**: max N`:
- Spawn up to N sub-agents via Agent tool
- Each gets context from prior phases + their specific slice of work
- Collect and merge results
- Validate merged output

## Cost control

- Track tokens per phase
- If budget from `.claude/memory/budget.md` would be exceeded: WARN before expensive phases
- Prefer haiku for mechanical work, sonnet for reasoning

## Rules

1. **Never skip phases** — execute in order, even if a phase seems unnecessary
2. **Always validate** — every phase output must pass its validation
3. **Save everything** — all intermediate results go to `.harness/`
4. **Fail fast** — don't continue past a failed validation without user consent
5. **Be transparent** — show progress after each phase
6. **Trace is append-only** — never overwrite or delete trace records
