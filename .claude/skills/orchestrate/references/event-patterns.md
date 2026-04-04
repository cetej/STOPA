# Event Patterns — Preparation for KAIROS Integration

Source: CC KAIROS daemon mode (feature flag, not yet GA), Agent Teams communication patterns.

## Event Types for Agent Lifecycle

When KAIROS becomes available, the orchestrator should emit these events
to enable async monitoring, budget tracking, and circuit breaking.

### Defined Events

| Event | When | Payload |
|-------|------|---------|
| `orchestration_start` | Phase 0 begins | `{task_id, tier, goal, timestamp}` |
| `agent_spawn` | Agent() called | `{agent_id, subtask_id, wave, model, tier}` |
| `agent_plan_submitted` | Plan approval gate | `{agent_id, subtask_id, plan_summary}` |
| `agent_plan_approved` | Orchestrator approves | `{agent_id, subtask_id, approved: true}` |
| `agent_plan_rejected` | Orchestrator rejects | `{agent_id, subtask_id, feedback}` |
| `subtask_complete` | Agent returns DONE | `{subtask_id, status, confidence, files_changed}` |
| `subtask_failed` | Agent returns BLOCKED | `{subtask_id, blocked_on, error_class}` |
| `wave_complete` | All Wave N agents done | `{wave_number, subtasks_done, subtasks_failed}` |
| `budget_warning` | 80% of tier budget used | `{tier, agents_used, agents_max, pct}` |
| `circuit_break` | Circuit breaker triggered | `{breaker_id, reason, subtask_id}` |
| `critic_pass` | Critic approves | `{phase, scope, issues_found: 0}` |
| `critic_fail` | Critic rejects | `{phase, scope, issues}` |
| `tier_escalation` | Auto-escalation | `{from_tier, to_tier, reason}` |
| `orchestration_complete` | Phase 6 done | `{task_id, status, duration, cost}` |

### Event Format (JSON)

```json
{
  "event": "subtask_complete",
  "timestamp": "2026-04-04T10:30:00Z",
  "session_id": "abc123",
  "task_id": "refactor-auth",
  "payload": {
    "subtask_id": "1a",
    "status": "DONE",
    "confidence": 0.85,
    "files_changed": ["src/auth.py"]
  }
}
```

### Current Implementation (pre-KAIROS)

Until KAIROS is GA, events are logged to `.claude/memory/intermediate/events.jsonl`:
- One JSON object per line (append-only)
- Orchestrator appends after each state transition
- Useful for post-hoc analysis via `/eval` skill

### Future KAIROS Integration Points

When KAIROS daemon mode is available:
1. Events become push notifications to daemon
2. Daemon can interrupt orchestrator on budget_warning or circuit_break
3. Events enable cross-session orchestration (daemon resumes after crash)
4. GitHub webhook integration: external triggers can start orchestration
5. Events feed into auto-scheduling: daemon learns optimal timing for tasks

### TaskCompleted Hook Pattern (from CC Agent Teams)

Quality gate hook that runs after every subtask completion:

```
Hook: on_subtask_complete
Input: subtask result JSON
Logic:
  - Check confidence >= 0.7
  - Check files_changed matches expected
  - Check no FORBIDDEN files touched
Output:
  - exit 0 = accept subtask
  - exit 2 = reject + send feedback to agent
```

This pattern can be implemented as a STOPA hook in `.claude/hooks/` before KAIROS.
