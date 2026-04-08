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

## Step 2: Partition into chunks

- Partition by **file** (not by line) — one agent owns all issues in its assigned files
- Chunk size: `ceil(total_files / num_agents)` — even distribution
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

Farm workers MAY append discovered patterns to a shared file:
- `.claude/memory/intermediate/farm-shared-notes.md` — append-only

Format per worker:
```
## Worker {N} — {timestamp}
- **Pattern**: <discovered pattern or edge case>
- **File**: <which file revealed this>
```

Post-sweep 1: orchestrátor reads `farm-shared-notes.md` and injects relevant patterns into sweep 2 agent prompts. This is opt-in — single-sweep operations skip (overhead > benefit).

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
