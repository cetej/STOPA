---
skill: koder
date: 2026-04-21
task: "Add doom-loop Signal 6 to panic-detector.py from ml-intern port"
outcome: success
project: STOPA
task_file: T-2026-04-21-001.md
files_changed:
  - .claude/hooks/panic-detector.py
  - .claude/hooks/test_panic_detector.py
  - .claude/memory/learnings/2026-04-21-doom-loop-signal-from-ml-intern.md
  - .claude/tasks/koder-queue/T-2026-04-21-001.md
exit_reason: completed
---

## What Was Done

- Added `import hashlib` to panic-detector.py
- Added `args_hash` field to `extract_event()`: MD5[:12] of `json.dumps(tool_input, sort_keys=True)`
- Added two module-level helpers before `compute_signals()`: `detect_identical_consecutive(sigs, threshold=3)` and `detect_repeating_sequence(sigs)` — ported from huggingface/ml-intern, using plain `(str, str)` tuples instead of ToolCallSignature dataclass
- Added Signal 6 doom-loop block at end of `compute_signals()`: identical consecutive → +3/`doom_identical:<tool>`, repeating sequence → +2/`doom_sequence:<A->B>`
- Updated yellow gate to accept `doom_` prefix alongside `bash_fails`, `edit_fail_cycle`
- Added doom_suffix construction in `main()` that appends Czech pattern description to both yellow and red messages when doom signal present
- Set task status to `done` in T-2026-04-21-001.md
- Written learning file `.claude/memory/learnings/2026-04-21-doom-loop-signal-from-ml-intern.md`

## Verification

```
=== panic-detector Signal 6 tests ===

TC1: identical consecutive triggers
  PASS: doom_identical:Grep in signals
  PASS: score >= 3 (got 4)

TC2: repeating sequence triggers
  PASS: doom_sequence:* in signals
  PASS: pattern is Read->Bash (got doom_sequence:Read->Bash)
  PASS: score >= 2 (got 3)

TC3: no false positive on productive work
  PASS: no doom_* signals on productive diverse work

TC4: infra errors excluded from doom
  PASS: no doom_* signals when events are infra-excluded

Results: 7 passed, 0 failed
```

Line count: 526 → 610 (exactly at +15% I2 budget limit).
Syntax check: `python -c "import ast; ast.parse(...)"` → Syntax OK.
All 5 existing signal labels still grep-present.

## What Failed (if any)

None. First attempt succeeded on all 4 test cases.
