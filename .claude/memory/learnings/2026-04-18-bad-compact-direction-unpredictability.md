---
date: 2026-04-18
type: best_practice
severity: high
component: session
tags: [context-management, compaction, compact, session-management]
summary: Bad compacts happen when the model can't predict the next task direction — content outside the session's dominant theme gets dropped. Fix: trigger /compact proactively with an explicit direction hint before the topic changes.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.9
maturity: draft
related: [2026-04-01-autocompact-threshold.md, 2026-04-14-compact-timing-60pct.md]
verify_check: "manual"
skill_scope: [compact, checkpoint]
---

## Bad Compact Root Cause: Direction Unpredictability

Existing learnings say "compact at 60%." This learning explains WHY bad compacts happen even with good timing.

**Root cause**: Model summarizes based on the session's dominant theme. Content that doesn't fit that theme gets dropped. If your next message is off-theme ("now fix that warning we saw in bar.ts"), the model couldn't have known to preserve it.

**Compounding factor**: Due to context rot (~300-400k quality degradation), the model is at its LEAST intelligent exactly when autocompact fires (at 95%). Worst intelligence, worst context prediction.

**Fix**: Run `/compact` proactively BEFORE the topic changes, with a direction hint:
- `/compact focus on the auth refactor, drop the test debugging`
- `/compact I'm about to work on bar.ts warnings next`

This tells the model what to preserve for the NEXT task, not just what was important in the LAST task.

**How to apply**: In /compact skill, add explicit instruction to include direction hint when compacting at a task transition point.
