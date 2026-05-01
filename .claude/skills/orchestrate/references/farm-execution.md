# Phase 4 (farm tier): Farm Execution

Farm tier uses a different workflow from standard orchestration. Instead of decomposing into semantic subtasks,
it partitions work mechanically and runs agents in parallel sweeps.

## Step 0: Initialize Farm Ledger

**Before spawning any workers**, create the shared ledger for mid-run coordination:

Write to `.claude/memory/intermediate/farm-ledger.md` (overwrite any existing file):

```markdown
---
task_id: {task_id}
sweep: 1
created: {ISO-timestamp}
task: "{description}"
total_files: {N}
---

## Per-File Progress

| ts | worker | file | status | pattern |
|----|--------|------|--------|---------|

## Discovered Patterns

(Auto-populated by orchestrator after sweep 1 completes)
```

This file is **mandatory for farm tier**. Workers append one row per file. Orchestrator reads it
between sweeps and injects discovered patterns into sweep 2 agent prompts.

> **Why:** GEA (arXiv:2602.04837): shared group traces = 71.0% vs 56.7% SWE-bench, 2× tool
> diversity, 1.4 vs 5 repair iterations. Mid-run sharing outperforms final-output-only sharing
> because workers benefit from each other's patterns before encountering the same problem.

## Step 1: Generate work list

Run the verification command(s) to produce a problems/targets list:
```
Examples:
- Linter: ruff check . --output-format json → list of violations
- Type-checker: mypy . --json → list of type errors
- Custom: grep -rn "TODO\|FIXME" src/ → list of targets
- Pattern: find src -name "*.py" -exec grep -l "old_pattern" {} \; → files to migrate
```

Save output to `.claude/memory/intermediate/farm-worklist.json`:
```json
{
  "generatedAt": "2026-03-24T10:00:00",
  "command": "ruff check . --output-format json",
  "totalItems": 247,
  "items": [
    {"file": "src/foo.py", "line": 42, "rule": "E501", "message": "Line too long"},
    ...
  ]
}
```

## Step 1b: Classify item complexity (Parcae-inspired variable depth, arXiv:2604.12946)

Before partitioning, classify each work item's expected effort:

| Signal | Complexity | Agent effort budget |
|--------|-----------|-------------------|
| Single rule violation, 1-line fix (e.g., E501, W291) | **simple** | 1 attempt, no retry |
| Multi-line change, import reorg, or 2-3 related violations per file | **medium** | 1 attempt + 1 retry on failure |
| Cross-file dependency, type error chain, or 5+ violations per file | **complex** | 2 attempts + rescue to sweep 2 |

Classification heuristic (from worklist JSON):
- **simple**: `violations_per_file == 1` AND rule is in `[E501, W291, W293, E302, E303, E711]`
- **medium**: `violations_per_file in [2..4]` OR rule involves imports/types
- **complex**: `violations_per_file >= 5` OR violations reference other files

Store complexity per file in `farm-worklist.json`:
```json
{"file": "src/foo.py", "violations": 1, "complexity": "simple", "effort_budget": 1}
```

**Dispatch optimization**: Simple items get batched more aggressively per agent (up to 2× chunk size). Complex items get smaller chunks. This saves ~30% agent calls on mixed-complexity workloads vs uniform partitioning.

## Step 2: Partition into chunks

- Partition by **file** (not by line) — one agent owns all issues in its assigned files
- **Variable chunk sizing** (Parcae per-sequence depth): adjust chunk size by complexity
  - Simple-dominant chunks: `ceil(total_simple_files / num_agents) × 1.5` files per agent
  - Complex-dominant chunks: `ceil(total_complex_files / num_agents) × 0.7` files per agent
  - Mixed: standard `ceil(total_files / num_agents)`
- No two agents share the same file — zero conflict guarantee

## Step 3: Spawn Agent Teams

Use `TeamCreate` + spawn 5-8 teammates (sonnet), each with a file chunk:

```
Agent spawn prompt (farm worker):

## Goal
{describe the bulk improvement — e.g., "Fix all ruff E501 violations across the codebase"}

## Your Role: farm-worker-{N}
Role: Bulk code improver
Owns: {list of assigned files — ONLY these files}
Produces: Fixed files with all violations resolved

## Work Items
{paste the specific violations/targets for this agent's files}

## Rules
- Fix ONLY the listed violations — do not refactor, improve, or change anything else
- Do NOT edit files outside your ownership list
- Run the verification command on your files after fixing to confirm zero violations
- Write results to .claude/memory/intermediate/farm-worker-{N}.json

## Farm Ledger (mid-run sharing)

After completing EACH file (not at task end), append ONE line to the shared ledger:

  echo "| $(date +%H:%M:%S) | farm-worker-{N} | {file} | {fixed|failed|skipped} | {pattern} |" >> .claude/memory/intermediate/farm-ledger.md

`pattern` = one-line technique OTHER agents would benefit from. Most entries: `—`.
Good pattern example: `E501 in f-strings: split with backslash continuation on string literal`
Bad pattern: `fixed the line` (not reusable)

After every 5 files, READ the ledger: `cat .claude/memory/intermediate/farm-ledger.md`
Apply any patterns from the "Discovered Patterns" section to your remaining files.

## Verification
After all fixes, run: {verification command scoped to your files}
Report: files fixed, violations resolved, any that couldn't be fixed (with reason)
```

### Shared Discovery (CORAL-inspired, optional for multi-sweep)

Farm workers MAY append discovered patterns to the shared notes file:
- `.claude/memory/intermediate/shared/notes.md` — append-only (created by `ensure-shared-dir.sh` hook)

Format per worker:
```
## farm-worker-{N} — {timestamp}
- **Pattern**: <discovered pattern or edge case>
- **File**: <which file revealed this>
- **Fix**: <what worked, reusable for similar cases>
```

Post-sweep 1: orchestrátor reads `shared/notes.md` and injects relevant patterns into sweep 2 agent prompts. This is opt-in — single-sweep operations skip (overhead > benefit).

Stagnation detection: `stagnation-detector.py` hook monitors TSV results and injects `[stagnation-steering]` messages when iteration plateaus — farm workers benefit from this automatically if they write to `*-results.tsv`.

## Step 4: Collect & verify

1. After all agents complete, run the full verification command again
2. Compare: original count vs. remaining count

### Farm Ledger Review (before sweep 2)

Read `.claude/memory/intermediate/farm-ledger.md` and extract patterns:

```python
# Read ledger, extract non-trivial patterns
lines = [row for row in table_rows if row['pattern'] != '—']
patterns = [row['pattern'] for row in lines]
```

Write the "## Discovered Patterns" section in the ledger, then inject top-3 patterns into
sweep 2 agent prompts as a **Known Patterns** block (Latent Briefing — filter to relevant only,
do not pass all entries):

```
## Known Patterns (from sweep 1)
- {pattern_1}
- {pattern_2}
Apply these before attempting your own approach.
```

Also check ledger `status: failed` rows — if 3+ files failed with the same pattern, add to
sweep 2's skip list rather than retrying (coordination failure, not per-file failure).

3. If remaining > 0: partition remaining into a second sweep (max 2 sweeps)
4. Commit all changes with summary: `farm: fix {N} {rule} violations across {M} files`

## Step 5: Report

Log to `.claude/memory/state.md`:
```
## Farm Sweep Complete
- Command: ruff check .
- Before: 247 violations
- After: 3 violations (98.8% resolved)
- Agents: 6, Sweeps: 1
- Remaining: 3 violations in tightly-coupled code (manual review needed)
- Ledger: 244 rows, 3 patterns discovered, patterns injected into sweep 2: N/A (1 sweep)
```

Archive the farm ledger to `.claude/memory/intermediate/farm-ledger-{task_id}.md` (rename, don't delete)
for post-run analysis. The `/sweep` skill will clean up archived ledgers after 24h.

**Farm tier budget:** Count each agent spawn toward the agent limit (5-8). One critic pass at the end (not per-agent). If sweep 2 is needed, it counts as additional agent spawns.

## Optional: Strategy Constraints Mode (AHE Pattern 4 — Best-of-N)

Default farm tier is **partition mode**: N agents work on disjoint file chunks of the SAME problem with the SAME approach. Good for mechanical bulk work (linter fixes, type-checker errors).

Strategy Constraints mode is **opt-in**, useful when the same problem could be solved multiple competing ways and cross-variant comparison yields signal for the next iteration. Inspired by Agentic Harness Engineering (`outputs/ahe-pilot-2026-04-30.md` Pattern 4): "2 variants běží paralelně s mandatory orthogonal constraints. Cross-variant comparison = signal pro next iteration."

### When to use

- The work is **non-mechanical** (architecture choices, refactor strategies, UX rewrites where multiple valid approaches exist)
- You want **diverse outputs** for human/critic comparison rather than a uniform partition
- Sweep 2 would normally be a retry of failures — instead, treat it as alternative-strategy exploration

### Parameter

When invoking farm tier, pass `strategy_constraints: [...]` (array of N constraint strings, one per variant). When the array has length ≥ 2, the orchestrator switches from partition mode to **variant mode**:

- All N agents work on the **same problem** (no chunking)
- Each agent receives a different `strategy_constraints[i]` as a MANDATORY directive
- Constraints MUST be orthogonal (a variant satisfying one cannot also satisfy another)
- Output: N parallel solutions for cross-variant evaluation

### Example: refactor strategy

```yaml
strategy_constraints:
  - "STRUCTURAL ONLY: middleware, helper extraction, file split. Do NOT modify
     prompts, descriptions, or any *.md content this variant."
  - "GUIDANCE ONLY: prompts, skill descriptions, learnings, *.md tables. Do NOT
     create or modify Python files this variant."
```

Each variant is forced into one half of the design space. Cross-variant comparison reveals which axis the problem actually lives on.

### Example: bug fix approach

```yaml
strategy_constraints:
  - "DEFENSIVE: add validation at entry points, fail-fast on bad input. Do NOT
     change core logic."
  - "REWRITE: simplify or replace the broken code path. Do NOT add validation
     wrappers."
  - "INSTRUMENT: add logging/assertions to expose the failure. Do NOT fix it
     yet — produce a diagnostic-only variant."
```

### Mechanics (variant mode)

1. **Step 1 (work list):** Single problem statement, no per-file enumeration
2. **Step 2 (partition):** Skipped — every variant gets the full problem
3. **Step 3 (spawn):** N agents in parallel, agent `i` gets `strategy_constraints[i]` injected at top of prompt as: `## Mandatory Constraint (orthogonal to other variants)\n{constraint[i]}`
4. **Step 4 (collect):** Each variant writes results to `.claude/memory/intermediate/farm-variant-{i}.md` (different from partition's `farm-worker-{N}.json`). Orchestrator presents all N variants side-by-side for review or critic comparison.
5. **Step 5 (report):** Highlight which variant the critic prefers + why; do NOT auto-merge any variant — variant mode produces options, human or critic chooses.

### Anti-patterns

- **Non-orthogonal constraints**: variants converge on similar solutions despite the directive — wastes agent budget. If you cannot draft constraints that genuinely partition the design space, do NOT use this mode.
- **More than 3 variants**: AHE empirical finding — diminishing returns past N=3 (cross-comparison effort grows quadratically). Cap at 3 unless the use case explicitly justifies more.
- **Auto-merging best variant**: variant mode is a divergent step before convergent decision. The critic or user chooses, not the orchestrator. Auto-pick removes the value of multi-variant exploration.

### Status: documentation-only chip

This section documents the **convention** for `strategy_constraints[]`. The orchestrator's main SKILL.md does not yet have implementation code that switches partition→variant mode based on this parameter — that is a follow-up. Until then, this serves as the spec for the next implementation chip and as guidance when farm tier is invoked manually with these constraints in the prompt.
