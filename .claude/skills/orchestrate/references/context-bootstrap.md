# Context Bootstrap — Block-Scored Selection

After classifying the task, select context blocks using a scored manifest instead of grepping full files. This is the **lazy allocation** approach: read metadata first, fetch content only for top-scoring blocks.

## Step 1 — Read block manifest (page table)

Check if `.claude/memory/learnings/block-manifest.json` exists.
- **If yes**: read it — it's lightweight metadata only (no full file content). Use it for Steps 2-4.
- **If no**: fall back to grep-based retrieval from the table below. Run `python scripts/build-component-indexes.py` during next maintenance.

## Step 2 — Score blocks against current task

From the manifest `blocks` dict, filter `active: true` entries only. For each, compute a **context score**:

```
context_score = retrieval_score × keyword_match_bonus
```

Where:
- `retrieval_score` = precomputed in manifest (severity × recency)
- `keyword_match_bonus` = 2.0 if any tag or component matches the task type below, else 1.0

| Task Type | Match these tags/components |
|-----------|----------------------------|
| Bug fix | `type: bug_fix`, component matches affected module |
| Feature | `type: best_practice`, component matches affected module |
| Refactor | `type: architecture`, `anti_pattern` |
| Pipeline/workflow | tags: `pipeline`, `workflow` |
| Skill edit | component: `skill`, tags: `skill` |
| Memory/state | component: `memory`, `orchestration` |
| Hook/config | component: `hook`, tags: `settings` |

Also apply **synonym expansion**: if no matches on primary keywords, retry with 2-3 related terms (e.g., "validation" → "sanitization", "input checking"). Max 2 rounds.

## Step 3 — Apply token budget

Context budget for learnings: **~2 000 tokens** (standard tier), **~4 000 tokens** (deep tier).

Sort filtered blocks by `context_score` descending. Greedily add blocks until `sum(token_estimate)` would exceed budget. Stop there — **do NOT read lower-scoring blocks**.

This is the paged allocation: only top-N blocks get fetched, the rest stay on disk.

## Step 4 — Fetch selected blocks

Read the actual files for the selected top-N block IDs. Expand `related:` links (1-hop, max 3 extras per block) if budget allows.

Pass fetched content directly in Phase 4 agent prompts. Agents do NOT re-read memory.

## Context Budget Allocation (GSD-2 pattern)

Total usable context is model-dependent (200K for Opus). Reserve 10% for system overhead.
These are **targets, not hard limits** — the context health score system remains the primary control.

| Category | % of working budget | ~Tokens (200K model) | What fills it |
|----------|-------------------|---------------------|--------------|
| Summaries / learnings | 15% | ~27,000 | Block-scored selection above, critical-patterns.md |
| Inline agent results | 40% | ~72,000 | Agent outputs, /compact save-and-summarize results |
| Verification evidence | 10% | ~18,000 | Critic output, git diff, acceptance criteria checks |
| Overhead / planning | 35% | ~63,000 | Conversation turns, skill prompts, working memory |

**Rules:**
- If learnings injection would exceed 15%: raise min score threshold in block-scored selection
- If inline results exceed 40%: trigger auto-compact immediately (don't wait for health score 5+)
- Verification evidence is **protected**: never compact critic output before Phase 5 completes
- When health score hits 5+, compact inline results first (largest category), preserve verification

These percentages align with compact SKILL.md thresholds — see `AUTO_COMPACT_BUFFER` (13K) which
fires before inline results exceed their 40% allocation at standard context sizes.

## Step 5 — Also load (per task type)

| Task Type | Also load |
|-----------|-----------|
| Bug fix | `docs/TROUBLESHOOTING.md` (grep error message only) |
| Feature | Constitution check (Phase 3) |
| Refactor | Recent entries in `decisions.md` for the area |
| Pipeline/workflow | `docs/RLM_WORKFLOW_OPTIMIZER.md` (if exists) |
| Skill edit | `rules/skill-files.md`, `rules/skill-tiers.md` |
| Memory/state | `rules/memory-files.md` |

**Rules:**
- `critical-patterns.md` is always in the stable prefix — don't count it against the budget
- If manifest missing: run max 2 grep queries from the task type table (fallback)
- If no blocks score above 1.0: proceed without — don't force-load irrelevant context
- Agents receive the fetched content inline — they do NOT re-read memory files
