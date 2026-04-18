---
date: 2026-04-18
type: bug_fix
severity: medium
component: hook
tags: [panic-detector, false-positive, calm-steering, signal-quality]
summary: Panic-detector yellow fired ~20×/day on edit_velocity + scope_creep alone (0 failures). Fixed by requiring a failure-based signal (bash_fails|edit_fail_cycle) for yellow. False positives erode calm-steering signal credibility per calm-steering.md ("2 yellows = pattern is real").
source: user_correction
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.85
maturity: draft
failure_class: logic
failure_agent: panic-detector
task_context:
  task_class: bug_fix
  complexity: low
  tier: light
verify_check: "Grep('bash_fails|edit_fail_cycle', path='.claude/hooks/panic-detector.py') → 2+ matches in yellow elif"
skill_scope: [panic-detector]
---

## What happened

Commit 113993f added task-style gating (`YELLOW_THRESHOLD_STRUCTURED = 6`) to reduce panic false positives during structured work. But `task_style` is only written to `state.md` by `/orchestrate` — direct bulk-edit workflows never invoke it, so `task_style` stayed `"unknown"` and gating never applied.

Deeper issue: yellow fired on 4 pts (edit_velocity:3 + scope_creep:1) with **0 failures in window**. The detector's stated purpose (docstring line 7-9, 12-13) is edit→FAIL→edit→FAIL cycles. No failures = not panic, just fast productive work.

## Fix

`.claude/hooks/panic-detector.py:482-484` — added guard on yellow elif:
```python
and any(s.startswith(('bash_fails', 'edit_fail_cycle')) for s in signals)
```

Red threshold unchanged (7+ pts already requires failure signals to accumulate).

## Takeaways

1. **Signal-based gating > state-based gating**: Relying on task_style (written by ONE skill) to gate behavior means the gate fails silently when that skill isn't invoked. Prefer gates based on data the detector ALREADY has (signals list), not data it must fetch from elsewhere.
2. **Always test on real traces**: Commit 113993f looked correct in isolation. Checking `panic-episodes.jsonl` would have revealed all episodes had `task_style: unknown`.
3. **False-positive cost compounds**: `calm-steering.md` says "2 yellows in one session means the pattern is real" — once false positives erode that signal, the true-positive detector is also degraded.
