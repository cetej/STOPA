# Tree Exploration Mode — AutoLoop Extension

When `mode:tree` is specified, autoloop uses branching exploration instead of linear iteration.
Each "keep" variant becomes a potential parent for future experiments.

## Archive Structure

Initialize `autoloop-archive.json` alongside the TSV:

```json
{
  "best_id": 0,
  "best_score": <baseline>,
  "current_generation": 0,
  "variants": [
    {
      "id": 0,
      "parent_id": null,
      "commit": "<baseline-sha>",
      "score": <baseline>,
      "generation": 0,
      "successful_children": 0,
      "description": "baseline",
      "status": "baseline"
    }
  ]
}
```

Tag baseline commit: `git tag autoloop-keep-0`.

## Parent Selection

Before each iteration, select a parent variant from the archive:

```
selection_score(v) = v.score × (1 / (1 + v.successful_children))
```

This balances exploitation (high score) with exploration (penalizes over-breeding).
A variant with score 90 and 3 children scores **lower** than one with score 88 and 0 children.

**Selection process:**
1. Collect all variants with status `baseline` or `keep`
2. Compute `selection_score` for each
3. Pick the highest-scoring variant
4. Reset working tree to that variant's commit: `git checkout <commit> -- .`
5. Record the parent_id for the new iteration

## Modified Loop Steps

Tree mode changes these steps from the main autoloop loop:

### Step 1 (Review) — additional reads
- Read `autoloop-archive.json` — understand the full tree
- Identify which parent was selected and why
- Check: has this parent's "direction" been explored? If yes, try something different

### Step 6 (Decide) — archive updates
On **keep**:
1. Add new variant to `variants[]` with incremented id, parent_id, score, generation
2. Increment parent's `successful_children`
3. Tag commit: `git tag autoloop-keep-<id>`
4. If score > `best_score`: update `best_id` and `best_score`

On **discard**:
1. Still add to `variants[]` (with status `discard`) — dead ends are data
2. Revert to parent's commit, NOT to the linear predecessor

### Step 8 (Exit) — tree-specific conditions
In addition to standard exit conditions:
- **All parents explored**: every variant with `successful_children < 2` has been tried as parent
- **Generation depth**: `current_generation > budget / 2` — prevent depth-first rabbit holes

## Top-N Stepping Stones

Maintain the **top-3** variants by score. These are never pruned:
- Git tags `autoloop-keep-<id>` protect their commits
- Listed prominently in the report

## Tree Report

Add after the standard Results Log in Phase 3:

```
### Exploration Tree

baseline (85.2)
├── [1] add-auth-tests (87.1) ★
│   ├── [3] expand-auth-coverage (88.5) ★★
│   └── [5] auth-edge-cases (86.9)
├── [2] refactor-helpers (84.0) ✗
└── [4] simplify-imports (87.3) ★
    └── [6] tree-shake (89.1) ★★★ ← BEST

Legend: ★=keep, ✗=discard, ★★★=best
Generations: 3 | Variants: 7 | Stepping stones: 3
```

Build this by traversing `variants[]` as a tree rooted at id=0.

## Cleanup Options

After report, ask user:
1. **Keep best only** — checkout best variant's commit, delete branch artifacts
2. **Keep all** — leave all tags and the archive for future exploration
3. **Discard all** — revert to baseline, clean up everything
