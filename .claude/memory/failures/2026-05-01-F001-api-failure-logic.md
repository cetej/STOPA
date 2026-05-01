---
id: F001
date: 2026-05-01
task: "PREKLAD — translation-only pipeline for NG-ROBOT RTT files"
task_class: pipeline
complexity: medium
tier: light
failure_class: logic
failure_agent: session
resolved: false
resolution_learning: ""
source: stop_failure_hook
---

## Trajectory

1. Session working on "PREKLAD — translation-only pipeline for NG-ROBOT RTT files" at tier:light
2. `StopFailure` event fired — API error ended the turn before normal Stop hook
3. `stop-failure-logger.py` captured payload and classified as `logic`

## Root Cause

Pending analysis. Raw error signal: `authentication_failed`

## Reflexion

Classification: `logic`. Next session should:
- `timeout` → back off (5-10 min), then retry; do not immediately re-run
- `resource` → STOP, do not retry automatically; check disk/memory first
- `logic` → read `.claude/memory/checkpoint.md` and resume cleanly

Run `/learn-from-failure session` if this recurs.
