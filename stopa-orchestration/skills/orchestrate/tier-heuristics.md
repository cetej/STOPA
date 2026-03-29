# Tier Selection Heuristics — Learned from History

This file is auto-updated by the `workflow-optimization-check` scheduled task.
It extracts patterns from budget.md task traces to improve tier predictions.

## How to Use

Before assigning a tier in Phase 1, check these heuristics. If the current task matches a pattern, use the recommended tier. If no match, fall back to the default heuristic rules.

## Heuristics (auto-populated)

_No heuristics extracted yet. This file will be populated once 20+ task traces are collected in budget.md._

### Expected Format (for scheduled task)

Each heuristic should follow this pattern:

```
### H<N>: <Pattern Name>
- **Pattern:** <task_type> + <scope_indicator>
- **Recommended tier:** light | standard | deep | farm
- **Confidence:** <N traces> / <N matching>
- **Evidence:** "Task X used <tier>, completed in <N> agents with <verdict>"
- **Last updated:** YYYY-MM-DD
```

## Fallback Rules (always valid)

If no heuristic matches:
1. Single file, known pattern → light
2. 2-5 files, some exploration → standard
3. 6+ files, unknown scope → deep
4. 20+ independent files, mechanical change → farm
5. When in doubt → start light, escalate if scout reveals more

## Override Signal

If the user explicitly requests a tier ("use deep tier"), always honor that over heuristics.
