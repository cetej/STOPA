---
date: 2026-04-07
type: anti_pattern
severity: high
component: hook
tags: [hook, failure-modes, timeout, error-handling]
summary: "Hook failure modes: timeout kills silently (no error to Claude), stderr output becomes system-reminder injection vector, cascading failures when shared state corrupted."
source: auto_pattern
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 0.85
verify_check: "Grep('timeout', path='.claude/settings.json') → 1+ matches"
---

## Hook Failure Modes

### 1. Silent Timeout Kill

Hooks have timeout limits (2-15s). When exceeded, the process is killed with no error message to Claude. This means:
- A hook that works in testing but is slow on large repos will silently fail in production
- No indication to Claude that the hook ran but didn't complete
- Memory hooks that timeout leave partial writes (data corruption risk)

**Mitigation**: Keep hooks fast (<3s target), write atomic (temp file + rename), log timeout events to `.claude/hooks/lib/hook-errors.log`

### 2. Stderr Injection

Hook stderr output appears as `<system-reminder>` to Claude. A malicious or buggy hook could:
- Inject arbitrary instructions via stderr
- Override behavioral rules through crafted error messages
- The `instruction-detector.py` hook monitors for this, but it runs PostToolUse — cannot catch SessionStart injection

**Mitigation**: content-sanitizer.py handles web content; instruction-detector.py handles general PostToolUse. Gap: SessionStart hooks have no sanitizer.

### 3. Cascading State Corruption

Multiple hooks write to shared files (activity-log, learnings/, concept-graph.json). If one hook corrupts a shared file:
- Subsequent hooks reading that file may crash or produce wrong output
- memory-integrity-check.py catches some cases but runs only on Write/Edit to memory/
- No global integrity check across all shared state

**Mitigation**: memory-integrity-check.py for memory files; concept-graph.json has no integrity check.

### 4. Hook Ordering Dependency

Hooks within the same lifecycle event run sequentially in settings.json order. Undocumented dependencies:
- `auto-scribe.py` (SessionStart) must run before `memory-brief.sh` to update learnings
- `trace-capture.py` (PostToolUse) must run before `session-trace.py` for consistent traces
- `skill-sync.sh` must run after Write/Edit to keep commands/ and skills/ in sync

Reordering hooks in settings.json can break these implicit dependencies.

### 5. Windows-Specific Issues

- File locking: antivirus can lock files that hooks try to read/write
- Path separators: some hooks use hardcoded `/` paths that fail on Windows
- The `grep -oP` portability fix (learning from 2026-03-31) was needed because bash hooks used GNU-specific regex
