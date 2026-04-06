---
generated: 2026-04-07
cluster: hook-infrastructure
sources: 4
last_updated: 2026-04-07
---

# Hook Infrastructure & Security

> **TL;DR**: 70+ hooks across 13 lifecycle events form STOPA's runtime enforcement layer. 5 categories: safety, memory, tracing, workflow, notification. Hooks survive context compression — if a rule breaks things when violated, it belongs in a hook.

## Architecture Overview

STOPA hooks operate as the runtime enforcement layer for behavioral constraints — rules that cannot be enforced via prompts alone because they must survive context compression and model forgetting.

### Lifecycle Events (13 active)

| Event | # Hooks | Key hooks |
|-------|---------|-----------|
| SessionStart | 11 | checkpoint-check, memory-maintenance, auto-scribe, verify-sweep, improvement-funnel, skill-detector |
| PreToolUse | 5 | dippy (RTK), block-no-verify, config-protection, security-scan, tool-gate |
| PostToolUse | 20+ | activity-log, trace-capture, panic-detector, content-sanitizer, acceptance-gate, ruff-lint, skill-sync |
| UserPromptSubmit | 5 | skill-suggest, memory-whisper, correction-tracker, associative-recall |
| PermissionRequest | 1 | permission-auto-approve |
| PermissionDenied | 1 | permission-denied-logger |
| PostCompact | 1 | post-compact (checkpoint reminder) |
| Stop | 10 | completion-guard, scribe-reminder, cost-tracker, telegram-notify, session-summary, hebbian-consolidate |
| TaskCompleted | 1 | task-completed (auto-compound) |
| TeammateIdle | 1 | teammate-idle (quality gate) |
| StopFailure | 1 | stop-failure (API error recovery) |
| TaskCreated | 1 | task-created-gate (budget check) |

### 5 Functional Categories

1. **Safety**: config-protection, security-scan, block-no-verify, tool-gate, content-sanitizer, instruction-detector
2. **Memory**: memory-maintenance, memory-integrity-check, memory-brief, memory-whisper, auto-relate, graduation-check, learning-admission, uses-tracker, learnings-sync, hebbian-consolidate
3. **Tracing**: activity-log, trace-capture, session-trace, raw-capture, trace-bridge, session-summary, correction-tracker
4. **Workflow**: skill-suggest, skill-sync, skill-chain-engine, eval-trigger, auto-checkpoint-suggest, completion-guard, panic-detector, acceptance-gate, suggest-compact
5. **Notification**: telegram-notify, slack-notify, scribe-reminder, cost-tracker

## Key Failure Modes

1. **Silent timeout kill**: Process killed at timeout with no error to Claude — memory hooks may leave partial writes
2. **Stderr injection**: Hook stderr appears as system-reminder — instruction-detector.py monitors but has SessionStart gap
3. **Cascading state corruption**: Multiple hooks write shared files (activity-log, concept-graph.json) — no global integrity check
4. **Ordering dependencies**: Implicit ordering within lifecycle events (auto-scribe before memory-brief, trace-capture before session-trace)
5. **Windows specifics**: File locking from antivirus, path separator issues, GNU grep incompatibilities

## Security Layer (Agent Defense)

LlamaFirewall PromptGuard (BERT, 19-92ms, AUC 0.98) is ADOPT for PostToolUse injection scanning. CaMeL [UNTRUSTED] tagging is ADOPT as a PreToolUse blocking convention (ref: 2026-04-05-agent-defense-frameworks.md).

### Implementation Backlog

| Priority | Action | Effort | Dependency |
|----------|--------|--------|------------|
| 1 | PromptGuard into content-sanitizer.py | MED | pip install llamafirewall (~1GB model) |
| 2 | [UNTRUSTED] tagging in orchestrate/scout | LOW | none |
| 3 | CodeShield into security-scan.py | LOW | pip install llamafirewall |
| 4 | AlignmentCheck async audit | HIGH | Together API key |

## Testing Patterns

- **Isolated testing**: pipe mock JSON to stdin (`echo '{"tool_name":"Write",...}' | python hook.py`)
- **Dry-run mode**: `STOPA_TOOL_GATE=log` for tool-gate, some hooks check `DRY_RUN=1`
- **Debug via activity log**: `.claude/hooks/lib/activity-log.jsonl`
- **Traces**: `.claude/traces/` from trace-capture.py and session-trace.py

## Distribution: Local vs Plugin

| Aspect | Local (.claude/hooks/) | Plugin (stopa-orchestration/hooks/) |
|--------|------------------------|-------------------------------------|
| Count | 70+ | 24 (curated subset) |
| Config | .claude/settings.json | hooks.json in plugin |
| Scope | Development + production | Production-safe subset |

## Related Articles

- [general-security-environment](general-security-environment.md) — broader security posture
- [orchestration-multi-agent](orchestration-multi-agent.md) — trust boundaries in multi-agent execution

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-05-agent-defense-frameworks](../learnings/2026-04-05-agent-defense-frameworks.md) | 2026-04-05 | medium | LlamaFirewall PromptGuard ADOPT; CaMeL tagging ADOPT |
| [2026-04-07-hook-architecture-patterns](../learnings/2026-04-07-hook-architecture-patterns.md) | 2026-04-07 | high | 70+ hooks, 13 events, 5 functional categories |
| [2026-04-07-hook-failure-modes](../learnings/2026-04-07-hook-failure-modes.md) | 2026-04-07 | high | Silent timeout, stderr injection, cascading corruption |
| [2026-04-07-hook-testing-patterns](../learnings/2026-04-07-hook-testing-patterns.md) | 2026-04-07 | medium | Isolated testing, dry-run, activity log debugging |
