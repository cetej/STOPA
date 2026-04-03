# Phase 6: Learn & Close — Details

## Execution trace capture

Append a structured trace row to the Budget History table:

| Field | Source | Example |
|-------|--------|---------|
| Task | Phase 1 goal | "Add JWT auth to API" |
| Type | Phase 1 classification | feature / bug_fix / refactor / research |
| Planned→Actual Tier | Phase 1 vs. final tier (note if escalated) | standard→deep |
| Agents | budget.md counter | 4/4 |
| Critics | budget.md counter | 2/2 |
| Files | `git diff --stat` count | 7 |
| Critic Verdict | Final critic result | PASS 8/10 |
| Agent Graph | Actual execution order | scout→plan→2×exec→critic→fix→critic |
| Duration | Approximate wall time | ~25min |
| Verdict | Overall outcome | complete / partial / escalated |

Write the trace as a new row in the Budget History table. Use the **extended format**:
```markdown
| <Task> | <Type> | <Planned→Actual> | <Agents> | <Critics> | <Files> | <Critic Score> | <Duration> | <Verdict> |
```

**Why:** These traces enable future tier selection heuristics. After 20+ traces, patterns emerge (e.g., "bug_fix tasks with <5 files never need deep tier").

## Trace milestone check

Count rows in Budget History table of `.claude/memory/budget.md`.

- **If >= 20 rows**: automatically run trace analysis inline (do NOT just suggest — execute it):
  1. Read all Budget History rows
  2. Group by Type: for each type (bug_fix, feature, refactor, research), compute:
     - Most common planned tier
     - % of tasks where planned == actual tier (accuracy)
     - Average files changed per tier
     - Average critic score per tier
  3. Generate heuristics table: e.g., "bug_fix < 5 files → always light tier"
  4. Write heuristics to `.claude/skills/orchestrate/tier-heuristics.md` (create if not exists)
  5. Report to user: "Trace analysis complete — N heuristics extracted. See `tier-heuristics.md`."
- **If 15-19 rows**: note "N/20 traces collected — approaching Phase 2 milestone."
- **If < 15 rows**: no action needed.

## Learnings capture

Record learnings via `/scribe learning` to `.claude/memory/learnings/` (per-file YAML format):
- What patterns emerged? (type: best_practice)
- What didn't work? (type: anti_pattern)
- Was a skill missing? (type: workflow, tags: [skill-gap])
- Was the tier accurate? (note if over/under-estimated for future calibration)

If a new repeatable pattern was discovered → suggest creating a skill via `/skill-generator`.

## Entropy sweep (standard/deep tier, auto)

If `git diff --stat` shows 5+ files changed in this session, auto-invoke `/sweep --scope blast-radius --auto` to clean up stale docs, dead code, and contradictions. This runs AFTER critic pass (so the code is correct) but BEFORE declaring done to user. Skip if tier is light or farm.
