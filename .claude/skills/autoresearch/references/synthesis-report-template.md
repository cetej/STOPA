# Synthesis Report Template

Write to `outputs/autoresearch-<slug>.md`:

```markdown
# AutoResearch Report: <question>

**Date:** <YYYY-MM-DD>
**Experiments:** <used> / <budget>
**Branch:** autoresearch/<slug>
**Best result:** <metric> (baseline: <baseline>, improvement: <+X / +X%>)
**Best hypothesis:** <name>

## Experiment Log

| # | Hypothesis | Metric | Delta | Status | Notes |
|---|-----------|--------|-------|--------|-------|
| 0 | baseline | 0.72 | — | baseline | initial state |
| 1 | ... | ... | ... | ... | ... |

## What Worked

<Top performing approaches with analysis of why — cite experiment numbers>

## What Didn't Work

<Failed approaches and why — equally important for future reference>

## Unexpected Discoveries

<Anything surprising that emerged from experiments>

## Recommended Approach

<The best implementation, with rationale and experiment evidence>

## Open Questions

<What wasn't tested, what would need more experiments>

## Reward Hacking Incidents

<Any divergence flags triggered, how they were resolved>

## Difficulty Calibration History

| Batch | keep_rate | Decision | difficulty_level | Action taken |
|-------|-----------|----------|-----------------|--------------|
| 1 | 75% | ESCALATE | 1.1 | Tightened target to 0.85 |
| 2 | 30% | HOLD | 1.1 | — |
```
