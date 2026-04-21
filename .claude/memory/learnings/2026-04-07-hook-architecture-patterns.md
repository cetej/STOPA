---
date: 2026-04-07
type: architecture
severity: high
component: hook
tags: [hook, architecture, lifecycle, patterns]
summary: "STOPA hook architecture: 70+ hooks across 13 lifecycle events (SessionStart, PreToolUse, PostToolUse, UserPromptSubmit, Stop, etc). Hooks form 5 functional categories: safety, memory, tracing, workflow, and notification."
source: auto_pattern
maturity: draft
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 1.0
verify_check: "Grep('hooks', path='.claude/settings.json') → 1+ matches"
---

## Hook Architecture Patterns

### Lifecycle Events Used (13 total)

| Event | # Hooks | Purpose |
|-------|---------|---------|
| SessionStart | 11 | Checkpoint restore, memory maintenance, auto-scribe, verify-sweep, improvement funnel, skill detection |
| PreToolUse (Bash) | 2 | RTK rewrite (dippy), block --no-verify |
| PreToolUse (Write/Edit) | 2 | Config protection, security scan |
| PreToolUse (all) | 1 | Tool gate (permission enforcement) |
| PostToolUse (web) | 1 | Content sanitizer (injection defense) |
| PostToolUse (all) | 7 | Activity log, trace capture, session trace, suggest compact, observe, panic detector, instruction detector |
| PostToolUse (Bash:git commit) | 2 | Post-commit analysis, critic accuracy |
| PostToolUse (Write/Edit) | 7 | Acceptance gate, ruff lint, learnings sync, eval trigger, skill sync, checkpoint suggest, memory integrity, learning admission, auto-relate, graduation check |
| PostToolUse (Skill) | 4 | Skill usage tracker, chain engine, context tracker, impact tracker |
| PostToolUse (Read) | 2 | File read dedup, uses tracker |
| PermissionRequest | 1 | Auto-approve (known safe patterns) |
| PermissionDenied | 1 | Permission denied logger |
| PostCompact | 1 | Checkpoint reminder |
| Stop | 10 | Completion guard, scribe reminder, cost tracker, telegram notify, trace bridge, session summary, raw capture, graph consolidate, hebbian consolidate, compile trigger |
| TaskCompleted | 1 | Auto-compound analysis |
| TeammateIdle | 1 | Quality gate for teammate output |
| StopFailure | 1 | API error recovery |
| UserPromptSubmit | 5 | Skill suggest, memory whisper, mid-session capture, correction tracker, associative recall |
| TaskCreated | 1 | Task budget gate |

### 5 Functional Categories

1. **Safety hooks**: config-protection, security-scan, block-no-verify, tool-gate, content-sanitizer, instruction-detector
2. **Memory hooks**: memory-maintenance, memory-integrity-check, memory-brief, memory-whisper, auto-relate, graduation-check, learning-admission, uses-tracker, learnings-sync, hebbian-consolidate
3. **Tracing hooks**: activity-log, trace-capture, session-trace, raw-capture, trace-bridge, session-summary, correction-tracker
4. **Workflow hooks**: skill-suggest, skill-sync, skill-chain-engine, skill-context-tracker, eval-trigger, auto-checkpoint-suggest, completion-guard, panic-detector, acceptance-gate, suggest-compact
5. **Notification hooks**: telegram-notify, slack-notify, scribe-reminder, cost-tracker

### Key Pattern: Event-Driven Pipeline

Hooks form a pipeline per lifecycle event. Each hook is independent — failures in one don't block others (timeout-based isolation). This is critical: if panic-detector.py fails, activity-log.sh still runs.

### Performance Consideration

SessionStart has 11 hooks with total timeout budget ~75s. Most complete in <3s, but session startup can feel slow. The `improvement-funnel.sh` (10s) and `auto-scribe.py` (15s) are the heaviest.

### CC v2.1.x New Hook Events (added 2026-04)

Claude Code v2.1.x introduced 7 new hook events beyond the original 13. Mapped to STOPA's 5 functional categories:

| Event | Category | Purpose | STOPA coverage |
|-------|----------|---------|----------------|
| **CwdChanged** | memory | Fires when working directory changes — reactive env management (direnv-style) | not wired |
| **FileChanged** | memory | Fires on external file modification — reactive state sync | not wired |
| **TaskCreated** | workflow | Fires when sub-agent Task is spawned — budget gate, team tracking | `task-created-gate.sh` |
| **PostCompact** | memory | Fires after context compaction completes — checkpoint reminder, state flush | `post-compact.sh` |
| **StopFailure** | safety | Fires on API errors ending turns (HIGH priority) — failure logging, recovery guidance | `stop-failure.sh` + `stop-failure-logger.py` |
| **PermissionDenied** | safety | Fires after auto-mode classifier denials — feedback loop for `/less-permission-prompts` | partial (logger planned) |
| **Elicitation / ElicitationResult** | workflow | Intercepts structured input responses — form-fill, confirmation gates | not wired |

### Category Assignment Rules (for future event additions)

- **safety**: events that can block/invalidate actions (permission, failure, security)
- **memory**: events that trigger state reconciliation (file/dir changes, compaction)
- **tracing**: events capturing observability data (tool calls, metrics)
- **workflow**: events orchestrating multi-step tasks (task lifecycle, elicitation, skill chains)
- **notification**: events producing user-visible messages (stop, telegram, slack)

StopFailure receives dual handler: bash for user-visible recovery guidance, Python for structured failure record persistence (enables `/learn-from-failure` pattern matching).
