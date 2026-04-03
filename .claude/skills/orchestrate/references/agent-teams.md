# Agent Teams (standard 3+ / deep tier)

Use Agent Teams when 3+ independent subtasks exist in standard or deep tier:

```
Decision tree:
Independent subtasks?
├── 1-2 (any tier)       → Use parallel Agent() calls (simpler, cheaper)
├── 3+, standard tier    → Agent Teams (lite) — no dedicated QA, lead monitors quality
└── 3+, deep tier        → Agent Teams (full) — includes QA/reviewer teammate
```

## Lite vs Full variants

| Aspect | Lite (standard) | Full (deep) |
|--------|----------------|-------------|
| Max teammates | 4 | 8 |
| QA agent | No (lead reviews) | Yes (dedicated reviewer) |
| Plan approval | No (direct execution) | Yes (`mode: "plan"` — lead approves before execution) |
| Critic pass | 1× on final output | 2-3× (QA + critic skill) |

## Workflow

1. `TeamCreate` — initialize team namespace
2. `TaskCreate` — one task per subtask (with dependencies if any)
3. Spawn teammates using `Agent({team_name, name, model: "sonnet", ...})` — use **Spawn Template** below
4. Teammates self-claim tasks, do work, communicate via `SendMessage`
5. Lead (this orchestrator, on Opus) monitors, synthesizes findings
6. **Clean shutdown:** see Shutdown Protocol below
7. `TeamDelete` — cleanup

## Spawn Template

Every teammate spawn prompt MUST follow this structure:

```
## Goal
{one-line project goal — why this team exists, what the end result should be}

## Your Role: {teammate_name}
Role: {specialization}
Produces: {concrete deliverable}

## File Access Manifest
- WRITE: [{specific files/directories — ONLY you edit these}]
- READ:  [{shared reference files — do not modify}]
- FORBIDDEN: [{files owned by other teammates — never touch}]

## Your Process Frame
### MUST (obligations)
- {task-specific obligations}
- {convention obligations from CLAUDE.md}
- Respect File Access Manifest — WRITE only to your owned files
### MUST NOT (prohibitions)
- Do NOT edit files in FORBIDDEN list (owned by other teammates)
- Do NOT install new dependencies without reporting to lead
- Do NOT change public API signatures or architectural patterns
### AUTONOMY SCOPE
- Can: fix own bugs (max 3 attempts), add missing imports, refactor within owned files
- Cannot: architectural changes, new abstractions, scope expansion
- On uncertainty: STOP and report via SendMessage to lead

## Communication
- Send results to: {named teammate(s)} via SendMessage
- Receive from: {named teammate(s)} — what to expect
- When done: Mark your task complete via TaskUpdate, then go idle

## Context
{injected context from orchestrator — relevant code, decisions, constraints}

## Rules
- Include Status block (DONE/DONE_WITH_CONCERNS/NEEDS_CONTEXT/BLOCKED) in final message to lead
- If blocked for 3+ attempts → STOP and report to lead via SendMessage
```

Key principles:
- **File ownership** — each agent owns specific files, prevents overwrite conflicts
- **Named recipients** — explicitly state who receives what, no assumptions
- **Goal propagation** — agents wake up with zero context, always include the project goal
- **Context injection** — orchestrator loads memory ONCE, injects relevant parts per agent (saves 60-80% tokens)

## Shutdown Protocol

Clean shutdown prevents lost work and dangling state:

```
1. SendMessage({type: "shutdown_request"}) to each teammate
2. Wait for shutdown_response from each (max 60s)
3. If teammate rejects (approve: false, reason: "still working"):
   → Wait 30s, retry shutdown_request (max 2 retries)
4. Only after ALL teammates confirm → TeamDelete
5. If any teammate times out after retries → log warning, force TeamDelete
```

Never force-kill teammates mid-work — they may have uncommitted changes.

## Plan Approval Mode (deep tier only)

For deep tier Agent Teams, spawn teammates with `mode: "plan"`:
- Teammate first writes a plan → sends to lead for approval
- Lead reviews via `plan_approval_response` (approve/reject with feedback)
- Only after approval does teammate execute
- Prevents expensive rework — catches misunderstandings before code is written
- Skip for standard tier — the overhead isn't worth it for smaller tasks

## Rules for Agent Teams

- Lead = Opus (orchestrator), teammates = Sonnet (cheaper execution)
- `teammateMode: "in-process"` on Windows (no tmux)
- TeammateIdle hook enforces quality gates — exit 2 sends feedback
- Max teammates: 4 (standard) / 8 (deep) per team
- If task status lags (known limitation), nudge teammate via SendMessage
- No nested teams — teammates cannot spawn their own teams
- **Always use `subagent_type: "general-purpose"` for teammates** — Explore/Plan agents lack SendMessage tool, so they can't respond to shutdown_request and TeamDelete will fail

**When NOT to use Agent Teams:**
- Light tier (always use plain Agent() calls)
- Standard tier with 1-2 subtasks (Agent() is simpler and cheaper)
- Tasks with tight sequential dependencies (no parallelism benefit)
- Quick fixes where Agent() + result is faster

## Intermediate Offloading Convention (Deep Agents adoption)

Agent outputs that exceed **500 tokens** MUST be offloaded to `.claude/memory/intermediate/` instead of returned inline. This prevents context bloat in the orchestrator.

**Rules:**
- Agent output ≤500 tokens → return inline (direct Status block)
- Agent output >500 tokens → write to `.claude/memory/intermediate/<subtask-id>.json`, return only Status block + file path
- All intermediate files are ephemeral — cleaned up in Phase 6
- Directory `.claude/memory/intermediate/` is created at task start, deleted at task close
- Files follow the Findings Ledger schema below

**Agent prompt addition** (include in ALL agent spawn prompts):
```
If your output exceeds 500 tokens, write full results to
.claude/memory/intermediate/<subtask-id>.json and return only your Status block
with the file path. This keeps the orchestrator context lean.
```

## Findings Ledger (standard 3+ / deep tier)

When 3+ agents produce results, raw output floods the orchestrator's context. Use a findings ledger — agents write results to disk, orchestrator reads back only what's needed.

**How it works:**
1. Create `.claude/memory/intermediate/` directory at task start
2. Each agent writes its output to `.claude/memory/intermediate/<subtask-id>.json`:
   ```json
   {
     "subtaskId": "1",
     "agent": "auth-implementer",
     "status": "DONE",
     "summary": "Added JWT middleware to 3 routes",
     "filesChanged": ["src/auth/jwt.ts", "src/routes/api.ts"],
     "concerns": [],
     "details": "<full output if needed>"
   }
   ```
3. Orchestrator reads only `summary` + `status` + `concerns` fields for decision-making
4. Full `details` field read only when debugging failures or concerns
5. At task close (Phase 6): delete `.claude/memory/intermediate/` directory

**When to use:**
- Always in deep tier (5+ agents)
- In standard tier when 3+ agents run in parallel
- Skip for light tier and standard with ≤2 agents (direct return is fine)

**Context savings:** ~60-70% reduction in orchestrator context usage for deep tier tasks.
