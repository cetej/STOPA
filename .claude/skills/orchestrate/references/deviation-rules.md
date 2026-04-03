# Deviation Rules (for sub-agents)

When a spawned agent encounters issues during execution, it has pre-granted authority within these boundaries:

| Situation | Action | Limit |
|-----------|--------|-------|
| Bug in own implementation | Fix inline | Max 3 attempts per task |
| Missing import/dependency | Fix inline | Max 3 attempts per task |
| Missing critical code (null check, validation) | Add inline | Max 3 attempts per task |
| Architectural change (new DB table, new service) | **STOP** — return to orchestrator | — |
| Pre-existing bug (not caused by current task) | Log to deferred, do NOT fix | — |

## Error Classification (before counting fix attempts)

Classify the error BEFORE counting it toward the 3-fix budget:

| Error Type | Examples | Action |
|------------|---------|--------|
| **Infrastructure** | ENOENT, EACCES, ENOSPC, OOM, ModuleNotFoundError, "command not found" | IMMEDIATE STOP — do NOT retry. Report: "Infrastructure error: [type]. Cannot be fixed by code changes." |
| **Transient** | Rate limit (429), timeout, 503, connection refused | Retry ONCE with 5s delay. If fails again → treat as infrastructure |
| **Logic** | Wrong output, assertion failure, test fail, type error | Normal 3-fix escalation below |

Infrastructure errors do NOT count toward the 3-fix attempt budget. They are a separate failure mode — retrying wastes LLM budget on unrecoverable states.

After 3 failed **logic** fix attempts on the same issue → **STOP symptom fixing**. This is an architectural concern:
1. Agent documents all 3 attempts and why each failed
2. Agent reports: "3 fixes failed on [X]. Likely architectural — [hypothesis]"
3. Orchestrator escalates to user with the pattern and asks for direction
Do NOT try a 4th fix. Do not restart hoping it resolves itself.

## Agent deviation red flags (orchestrator watches for these in agent reports)

- Agent reports DONE but diff shows no changes → reject, re-dispatch
- Agent fixed a "pre-existing bug" despite rules → reject fix, revert
- Agent reports "small architectural change was needed" → that's a STOP, not a deviation
- Agent says "one more attempt should fix it" after 2 failures → trigger 3-fix escalation

Include these rules in every Agent() prompt: "Deviation rules: fix bugs/imports inline (max 3 attempts). STOP and report if architectural change needed. Pre-existing bugs go to deferred, don't fix them."
