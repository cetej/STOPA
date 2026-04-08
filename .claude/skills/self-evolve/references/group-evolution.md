# Group Evolution — Parallel Branch Design (GEA-inspired)

> Reference: arXiv:2602.04837 (Weng et al. 2026). Activated by `self-evolve <target> --group N`.
> Default N=1 (standard single-branch). N=2-3 for group evolution.

## When to Use

- Target skill has plateaued on single-branch evolution (2+ runs without improvement)
- Target skill is complex (>200 lines) with multiple independent failure modes
- optstate shows `recurring_failure_patterns` that single-branch can't crack

**Do NOT use when:**
- First evolution run on a target (baseline single-branch first)
- Target skill is simple (<100 lines, <10 eval cases)
- Budget is constrained (group evolution costs N× single-branch)

## Architecture

```
Phase 0: Setup (shared)
  ├── Load eval cases, optstate, replay buffer
  ├── Create N git worktrees: self-evolve/<target>-branch-{1..N}
  └── Each branch gets DIFFERENT strategy bias from UCB1 top-N

Phase 1: Parallel Co-Evolution (per-branch, 2 rounds each)
  ├── Branch 1: Executor (Sonnet) — strategy bias: UCB1 rank #1
  ├── Branch 2: Executor (Sonnet) — strategy bias: UCB1 rank #2
  └── Branch N: Executor (Sonnet) — strategy bias: UCB1 rank #N
  (Curriculum is SHARED — one Haiku agent generates cases for all branches)

Tournament Round (every 2 rounds):
  ├── Grade ALL branches against ALL eval cases
  ├── Compute branch scores: pass_rate × (1 + unique_fixes / total_fixes)
  │   (unique_fixes = fixes this branch found that others didn't)
  ├── Share traces: each branch reads all other branches' patches + outcomes
  ├── Prune: drop worst branch, keep top N-1
  └── Spawn: create new branch from best branch + unexplored strategy

Phase 2-3: Synthesis & Handoff (shared)
  ├── Final tournament: select best branch
  ├── Optional: merge non-conflicting patches from runner-up into winner
  ├── Diff, report, ask user to merge
  └── Update optstate with per-branch strategy outcomes
```

## File Isolation

Each branch works on its own git worktree to avoid edit conflicts:

```
.claude/worktrees/
  self-evolve-<target>-branch-1/    ← worktree 1
  self-evolve-<target>-branch-2/    ← worktree 2
```

Shared state lives in the main worktree:
- `.claude/evals/<target>/` — eval cases (READ for all branches)
- `.claude/memory/intermediate/gea-<target>/` — shared trace buffer

### Shared Trace Buffer Schema

Each branch appends after every keep/revert:
```json
{
  "branch": 1,
  "round": 3,
  "strategy": "adversarial",
  "patch_summary": "Added boundary check for empty input in validate() step",
  "files_changed": [".claude/skills/<target>/SKILL.md"],
  "functions_changed": ["validate_input"],
  "outcome": "success",
  "pass_rate_delta": +0.08
}
```

Branches read the full trace buffer at start of each round. This is the GEA
"group experience sharing" mechanism — each branch sees what others tried.

## Branch Selection (Performance-Novelty, v1: Jaccard proxy)

For tournament rounds, rank branches using:

```
score(i) = pass_rate(i) × sqrt(novelty(i) + 0.01)
```

Where `novelty(i)` = mean Jaccard distance of branch i's `functions_changed` set
from all other branches' sets:

```
jaccard_dist(A, B) = 1 - |A ∩ B| / |A ∪ B|
```

No embedding model needed — pure set operations on changed function names.

## Budget

| Branches | Rounds per branch | Tournament rounds | Total Executor calls | vs Single-branch |
|----------|------------------|-------------------|---------------------|------------------|
| 1 (default) | 6 | 0 | 6 | 1.0× |
| 2 | 4 | 2 | 10 | 1.67× |
| 3 | 3 | 2 | 11 | 1.83× |

Budget = `N × rounds_per_branch + tournament_overhead`. Keep under 2× single-branch cost.

## Circuit Breakers

- All branches hit same failing case for 3 rounds → STOP, escalate
- No branch improves pass_rate for 2 consecutive tournament rounds → STOP
- Total eval cases exceed 20 → STOP (same as single-branch)
- Git worktree creation fails → fall back to single-branch

## Limitations (v1)

- No patch synthesis (Option A: winner-takes-all only)
- Curriculum agent is shared (not per-branch) — limits diversity
- Worktree cleanup may leave stale branches on crash (use `/sweep` to clean)
- Performance-Novelty uses Jaccard proxy, not true embedding distance

## Future (v2)

- Patch synthesis: Haiku agent merges non-conflicting patches from top-2 branches
- Per-branch Curriculum: each branch has its own adversarial agent
- True Performance-Novelty with embedding distance (`scripts/performance-novelty-selector.py`)
- Cross-target group evolution: evolve 2-3 related skills simultaneously
