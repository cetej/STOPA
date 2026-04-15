# Phase 4 (farm tier): Farm Execution

Farm tier uses a different workflow from standard orchestration. Instead of decomposing into semantic subtasks,
it partitions work mechanically and runs agents in parallel sweeps.

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
```

**Farm tier budget:** Count each agent spawn toward the agent limit (5-8). One critic pass at the end (not per-agent). If sweep 2 is needed, it counts as additional agent spawns.
