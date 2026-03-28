---
name: eval-runner
description: Discover and execute behavioral eval cases for skills, collect results into TSV, produce report
phases: 5
estimated_tokens: 30K-60K
output_template: template.md
---

# Eval Runner — Behavioral Skill Testing Harness

Runs eval cases from `.claude/evals/` against real skills, measures correctness and efficiency, appends results to persistent TSV.

## Arguments

- `--skill <name>` — run only cases for this skill (e.g., `--skill critic`)
- `--tags <tag>` — run only cases with matching eval-tag (e.g., `--tags quality_review`)
- `--dry-run` — discover and report cases without executing them (stops after Phase 1)
- No arguments — run all discovered cases

---

## Phase 1: Discovery (deterministic)

- **Action**: Glob `.claude/evals/**/*.md`. For each file, read YAML frontmatter. Extract: `id`, `skill`, `title`, `eval-tags`, `ideal_steps`, `ideal_tool_calls`, `max_acceptable_steps`, `fixture`.
- **Filter**: If `--skill` argument provided, keep only matching skill. If `--tags` argument, keep only cases where eval-tags intersect with requested tags.
- **Model**: haiku
- **Output file**: `.harness/eval-phase1_discovery.json`
- **Output schema**:

```json
{
  "_meta": {"phase": 1, "timestamp": "ISO8601", "model": "haiku"},
  "cases_found": 9,
  "filter_applied": "none",
  "cases": [
    {
      "id": "critic-001",
      "skill": "critic",
      "title": "Catches deliberate flaws in a synthetic skill file",
      "eval_tags": ["quality_review", "file_operations"],
      "ideal_steps": 8,
      "ideal_tool_calls": 5,
      "max_acceptable_steps": 14,
      "fixture": "inline",
      "case_file": ".claude/evals/critic/case-001-catches-flaws.md"
    }
  ]
}
```

- **Validation**: `cases_found >= 1` (count), all cases have required frontmatter fields (schema)

If `--dry-run`: output discovery JSON, print case summary table, STOP here.

---

## Phase 2: Fixture Setup (deterministic)

- **Action**: For each case:
  - `fixture: inline` → extract the fenced code block under `## Fixture` section. Write to `.harness/eval-fixtures/<id>-fixture.md`.
  - `fixture: live-repo` → record fixture path as `.` (STOPA project root). No file extraction needed.
- **Model**: haiku
- **Output file**: `.harness/eval-phase2_fixtures.json`
- **Output schema**:

```json
{
  "_meta": {"phase": 2, "timestamp": "ISO8601", "model": "haiku"},
  "fixtures_prepared": 9,
  "fixtures": [
    {
      "id": "critic-001",
      "fixture_type": "inline",
      "fixture_path": ".harness/eval-fixtures/critic-001-fixture.md"
    },
    {
      "id": "scout-001",
      "fixture_type": "live-repo",
      "fixture_path": "."
    }
  ]
}
```

- **Validation**: Every case has a fixture entry (completeness). For inline fixtures, file exists at `fixture_path` (exit code of `ls`).

---

## Phase 3: Execution (LLM — parallel sub-agents)

- **Action**: For each case, spawn a sub-agent (sonnet). Max 3 concurrent agents per round.
- **Sub-agent instructions**:

```
You are an eval executor. Your job:

1. Read the case file: {case_file}
2. Read the fixture at: {fixture_path}
3. Execute the skill invocation described in the case's "## Invocation" section
4. After skill completes, check each assertion from "## Assertions" table:
   - "contains" → check if output contains the expected string/pattern
   - "not_contains" → check output does NOT contain the string
   - "count" → check numeric count meets threshold
   - "range" → check numeric value falls in range
5. Count your total tool calls during skill execution (approximate)
6. Return a JSON result object (do NOT write to any files)
```

- **Model**: sonnet (for sub-agents)
- **Output file**: `.harness/eval-phase3_results.json`
- **Output schema**:

```json
{
  "_meta": {"phase": 3, "timestamp": "ISO8601", "model": "sonnet"},
  "results": [
    {
      "id": "critic-001",
      "skill": "critic",
      "status": "PASS",
      "assertions_passed": 5,
      "assertions_total": 6,
      "assertion_details": [
        {"id": "A1", "passed": true, "evidence": "Verdict: WARN"},
        {"id": "A2", "passed": true, "evidence": "Output contains WARN"},
        {"id": "A5", "passed": false, "evidence": "Description flagging not found in output"}
      ],
      "actual_steps": 9,
      "actual_tool_calls": 6,
      "ideal_steps": 8,
      "ideal_tool_calls": 5,
      "max_acceptable_steps": 14,
      "within_step_budget": true,
      "efficiency_ratio": 0.89,
      "raw_output_preview": "first 300 chars of skill output..."
    }
  ]
}
```

- **Efficiency ratio**: `min(1.0, ideal_steps / actual_steps)`. If `actual_steps > max_acceptable_steps` → `within_step_budget: false`.
- **Status derivation**: From case file's `## Scoring` section (e.g., "5-6 pass: PASS, 3-4: PARTIAL, 0-2: FAIL"). If sub-agent errors out → `status: "ERROR"`.
- **Validation**: Every case has a result (completeness). All `status` values are in `["PASS", "PARTIAL", "FAIL", "ERROR"]` (schema).

---

## Phase 4: TSV Collection (deterministic)

- **Action**: Transform Phase 3 results into TSV rows. Append to `.claude/memory/eval-results.tsv`. Create file with header row if it doesn't exist.
- **TSV header**:

```
# eval-runner results — append only
# columns: run_date, run_id, case_id, skill, status, assertions_passed, assertions_total, actual_steps, ideal_steps, efficiency_ratio, within_budget, notes
```

- **Row format**: One row per case. Tab-separated values.
- **run_id**: Generated as `run-YYYYMMDD-HHMMSS` from Phase 3 `_meta.timestamp`.
- **Model**: haiku
- **Output file**: `.harness/eval-phase4_tsv.json` (confirmation with row count)
- **Validation**: TSV row count increased by exactly `cases_run` (count)

---

## Phase 5: Report (template)

- **Action**: Fill `template.md` with data from Phases 1, 3, 4.
- **Compute aggregates**:
  - Pass rate: `PASS count / total cases`
  - Avg efficiency: mean of all `efficiency_ratio` values
  - Per-skill summary: group by skill, compute per-skill pass rate and avg efficiency
  - Failing assertions: list all assertions that failed across all cases
- **Model**: haiku
- **Output file**: `.harness/report.md`
- **Validation**: No `{{PLACEHOLDER}}` remaining (completeness). Report ≤ 300 lines (format).
- **Post-report**: Update `.claude/memory/budget.md` event log with estimated eval run cost.

---

## Efficiency Ratio Interpretation

| Ratio | Label | Meaning |
|-------|-------|---------|
| 1.0 | Optimal | Skill used exactly the ideal number of steps |
| 0.80-0.99 | Good | Slightly more steps, within normal variance |
| 0.60-0.79 | Acceptable | Somewhat over ideal, investigate skill instructions |
| < 0.60 | Inefficient | Significant over-stepping, review and optimize |
| over max_acceptable | Over Budget | Exceeds hard limit, flagged as failing efficiency |

---

## Circuit Breakers

- Sub-agent timeout: 3 minutes per case → status: ERROR, continue to next
- 3 consecutive ERROR statuses → STOP Phase 3, proceed to Phase 4-5 with partial results
- Budget exceeded (token limit) → STOP, save partial results

## Memory Integration

- `.claude/memory/state.md` — updated during run: "Running harness: eval-runner, Phase N/5"
- `.claude/memory/budget.md` — event log entry after completion
- `.claude/memory/eval-results.tsv` — persistent behavioral test history
