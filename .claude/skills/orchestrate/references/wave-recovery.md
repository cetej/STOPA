# Wave Recovery — Validation, Checkpoints, and Error Handling

## Agent Output Validation (Structured Contract)

After each agent completes and its result is saved via `/compact save-and-summarize`, validate the intermediate JSON:

1. **Status check**: `status` field must be one of: `complete` | `partial` | `failed`
   - If `status: "failed"` → log failure to `decisions.md`, skip downstream dependents that depend on this agent's output, alert user
   - If `status: "partial"` → check `outputs.needs_followup` — inject these items into next wave agents' context as explicit requirements
   - If `status: "complete"` → proceed normally

2. **Output coherence**: If agent was an `implementer` (made code changes):
   - `outputs.files_changed` should be non-empty — if empty but agent claimed success, flag as suspicious
   - Quick sanity: `git diff --name-only` should include the claimed files

3. **Handoff propagation**: Collect all `outputs.needs_followup` items from completed wave — these become **mandatory context** for Wave N+1 agents (inject under "Handoff from Wave N" section in their prompts)

4. **Circuit breaker**: If 2+ agents in the same wave return `status: "failed"` → STOP, present failures to user, ask for guidance before continuing

This validation prevents garbage-in-garbage-out between waves. Ground truth (git diff) trumps agent self-report.

## Wave Checkpoint (fault recovery, ref: arXiv:2603.12229)

After each wave completes, save incremental state so that a crash or context exhaustion doesn't lose completed work. This is lighter than a full `/checkpoint` — just state.md update + optional mini-save.

```
After Wave N completes (all agents returned, outputs validated):

1. Update state.md: mark all Wave N subtasks as `done` (with evidence summary)
2. Update budget.md: increment agent counter, log wave completion

3. IF wave >= 2 AND total agents spawned >= 3 (standard/deep tier):
   → Write mini checkpoint to .claude/memory/intermediate/wave-checkpoint.json:
     {
       "wave": N,
       "completedSubtasks": [1, 2, 3],
       "pendingSubtasks": [4, 5],
       "lastWaveAt": "<ISO 8601>",
       "agentsUsed": N,
       "resumeAction": "Launch Wave N+1 with subtasks [4, 5]"
     }

4. On crash recovery (checkpoint-resume dispatch rule):
   → Read wave-checkpoint.json if exists
   → Skip completed subtasks, resume from next pending wave
   → Log: "Resuming from wave checkpoint: Wave {N+1}, {M} subtasks remaining"
```

**Rules:**
- Light tier: skip wave checkpoints (too little state to justify overhead)
- Always update state.md regardless of tier — that's the ground truth
- Wave checkpoint file is ephemeral — deleted in Phase 6 cleanup
- Do NOT trigger full `/checkpoint` per wave — that's too expensive. Only at task boundaries.

## Sidecar Queue Drain (between waves)

Before launching Wave N+1, check for deferred suggestions from hooks:

1. Read `.claude/memory/intermediate/sidecar-queue.json` (if exists)
2. Process items sorted by priority (high first):
   - `compact_suggestion` → evaluate: if context health score ≥ 3, run `/compact` now
   - `checkpoint_suggestion` → if 70%+ subtasks complete, run `/checkpoint save` silently
   - `learning_suggestion` → note for Phase 6, don't act now
3. Clear the queue after processing
4. Log: "Sidecar queue drained: N items processed" (only if N > 0)

This replaces direct stdout injection from hooks — suggestions arrive at wave boundaries instead of mid-task, reducing context noise.

## Panic-Aware Recovery (between waves and after agent failures)

The panic detector hook (`panic-detector.py`) tracks edit-fail cycles and emits interventions via stdout. The orchestrator should actively read panic state at wave boundaries to make informed decisions:

1. **Between waves**: Read `.claude/memory/intermediate/panic-state.json` (if exists)
   - If `panic_score >= 7` (red): STOP current execution path. The subtask causing panic is likely mis-scoped or hitting an unknown constraint.
     - **Action**: Record the failing subtask + approach in state.md as `blocked:panic`
     - **Recovery options** (try in order):
       a. Reassign to a different agent with `Approach constraint: assume the obvious solution is wrong — find an alternative path`
       b. If reassignment also fails → escalate to user with panic episode log
     - Do NOT retry with the same approach — that's what caused the panic
   - If `panic_score >= 4` (yellow): Log advisory, continue but inject caution into next wave's agent prompts: `"Previous wave had difficulty — verify assumptions before implementing"`

2. **After agent failure** (status: "failed" from Agent Output Validation):
   - Read `.claude/memory/intermediate/panic-episodes.jsonl` for recent episodes
   - If 2+ episodes in last 10 minutes → the problem is likely architectural, not implementation
   - **Action**: Skip retry, log to "Tried and Failed" in state.md, escalate to user

3. **Episode data for checkpoint**: When `/checkpoint save` is triggered, pass panic episode count to the checkpoint — it feeds the "Tried and Failed" section automatically.

## Wave Re-open Protocol (ref: arXiv:2603.19138)

If a Wave N+1 agent reports `BLOCKED` or `DONE_WITH_CONCERNS` where the root cause traces back to a Wave N output:

1. **Identify the upstream subtask** that produced the problematic output
2. **Re-open it**: mark status back to `in_progress` in state.md, log the re-open reason
3. **Re-assign**: spawn a new agent for the re-opened subtask with additional context:
   - Original subtask prompt + original agent's output summary
   - The downstream agent's concern (what broke and why)
   - Instruction: "Your previous implementation caused [issue]. Fix the root cause, don't patch around it."
4. **Re-validate downstream**: after the re-opened subtask completes, re-run the blocked Wave N+1 agent
5. **Circuit breaker**: max 1 wave re-open per task. If a second re-open is needed → STOP, escalate to user

This prevents silent failures from propagating forward through waves. Without it, 46.5% of recovery attempts happen too late (final phase) when the cost of backtracking is highest.

## Wave Context Handoff via Scratchpad

When launching Wave N+1 agents, inject context efficiently using the scratchpad:

1. **Read the scratchpad**: Read `.claude/memory/intermediate/scratchpad.md` to get accumulated summaries of all previous waves' work.

2. **Inject scratchpad, not raw results**: Include the scratchpad table in Wave N+1 agent prompts under a "Previous Work" section:
   ```
   ## Previous Work (from waves 1-N)
   <paste scratchpad table here>

   Full details for any entry are in .claude/memory/intermediate/<id>.json
   — read ONLY if you need specific implementation details for your task.
   ```

3. **Selective full-load**: If a Wave N+1 agent's task explicitly depends on a specific Wave N result (e.g., "use the API schema from subtask-2"), load ONLY that specific JSON file's `details` field and inject it. Never load all previous wave details into one agent.

4. **Scratchpad size check**: If scratchpad exceeds 30 entries, spawn a Haiku agent to condense older entries into a "Waves 1-N summary" paragraph before injecting into new agents.
