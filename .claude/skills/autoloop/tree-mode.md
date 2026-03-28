# Tree Exploration Mode — AutoLoop Extension

When `mode:tree` is specified, autoloop uses branching exploration instead of linear iteration.
Each "keep" variant becomes a potential parent for future experiments.

Inspired by AutoHarness (arXiv:2603.03329): uses **Thompson sampling** with Beta distribution for parent selection instead of deterministic formula. This naturally balances exploration (uncertain nodes get high-variance samples) with exploitation (proven nodes converge).

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
      "failed_children": 0,
      "total_attempts": 0,
      "description": "baseline",
      "status": "baseline"
    }
  ]
}
```

Tag baseline commit: `git tag autoloop-keep-0`.

## Parent Selection — Thompson Sampling

Before each iteration, select a parent variant using Thompson sampling with Beta distribution.

### Why Thompson sampling (not deterministic)

The old formula `score × (1 / (1 + children))` is deterministic — it always picks the same node, which causes the search to get stuck in local optima. Thompson sampling draws a **random sample** from each variant's Beta distribution, so:

- **Uncertain nodes** (few attempts) → high variance → occasionally sampled high → explored
- **Proven nodes** (many successes) → low variance, high mean → reliably selected
- **Failed nodes** (many failures) → low mean → rarely selected but not impossible

This is the same algorithm that achieved 100% legal action rates across 145 games in the AutoHarness paper.

### Algorithm

For each eligible variant `v`:

```
α = 1 + v.successful_children    # prior + observed successes
β = 1 + v.failed_children         # prior + observed failures
thompson_sample = Beta(α, β)       # random draw from Beta distribution
selection_score = thompson_sample × v.score
```

**Implementation** — run via Bash (Python stdlib, no deps):

```bash
python -c "
import json, random
with open('autoloop-archive.json') as f:
    archive = json.load(f)
eligible = [v for v in archive['variants'] if v['status'] in ('baseline', 'keep')]
scores = []
for v in eligible:
    alpha = 1 + v.get('successful_children', 0)
    beta = 1 + v.get('failed_children', 0)
    sample = random.betavariate(alpha, beta) * v['score']
    scores.append((sample, v['id']))
    print(f'  id={v[\"id\"]} α={alpha} β={beta} sample={sample:.2f} (score={v[\"score\"]})')
best = max(scores, key=lambda x: x[0])
print(f'SELECTED: {best[1]}')
"
```

### Selection process

1. Collect all variants with status `baseline` or `keep`
2. Run Thompson sampling (Bash command above) to get selected parent id
3. Read the selected variant's commit SHA
4. Reset working tree to that variant's commit: `git checkout <commit> -- .`
5. Increment selected parent's `total_attempts`
6. Record the parent_id for the new iteration

### Intuition for typical scenarios

| Scenario | α | β | Beta mean | Behavior |
|----------|---|---|-----------|----------|
| Fresh node (no children) | 1 | 1 | 0.50 | Uniform — high exploration |
| 2 successes, 0 failures | 3 | 1 | 0.75 | Skewed right — likely selected |
| 1 success, 3 failures | 2 | 4 | 0.33 | Skewed left — rarely selected |
| 5 successes, 5 failures | 6 | 6 | 0.50 | Centered but low variance — stable |

## Modified Loop Steps

Tree mode changes these steps from the main autoloop loop:

### Step 1 (Review) — additional reads
- Read `autoloop-archive.json` — understand the full tree
- Identify which parent was selected and why
- Check: has this parent's "direction" been explored? If yes, try something different

### Step 6 (Decide) — archive updates
On **keep**:
1. Add new variant to `variants[]` with incremented id, parent_id, score, generation, `failed_children: 0`, `total_attempts: 0`
2. Increment parent's `successful_children`
3. Tag commit: `git tag autoloop-keep-<id>`
4. If score > `best_score`: update `best_id` and `best_score`

On **discard**:
1. Still add to `variants[]` (with status `discard`) — dead ends are data
2. Increment parent's `failed_children`
3. Revert to parent's commit, NOT to the linear predecessor

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
