---
name: Autonomy preferences
description: User wants maximum autonomy — no step-by-step approval, autonomous agents, auto-approve most actions, scheduled tasks self-sufficient
type: feedback
originSessionId: 16b10457-62ed-45b8-91c1-49616a4950d4
---
User strongly prefers autonomous operation. Consolidated from multiple corrections:

1. **No step-by-step approval** — finds it annoying, wants agents running outside sessions
2. **Permission hook v3.0**: auto-approve GitHub write, Chrome, Playwright, Telegram, Gmail draft; ask only for merge/send/calendar
3. **Eval system must be fully autonomous** — no manual commands, self-triggering, self-improving
4. **Scheduled tasks must be autonomous** — report status, never generate action lists for approval
5. **Cross-project handoff**: save memory to TARGET project's auto-memory, not just current

**Why:** User is experienced, trusts the system, and context-switches frequently. Interruptions for approval break flow.

**How to apply:** Default to action. Only pause for destructive/irreversible operations (merge, send, delete). Scheduled tasks should complete and report, not ask.
