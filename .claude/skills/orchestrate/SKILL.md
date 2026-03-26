---
name: orchestrate
description: Use when a task requires multiple steps or touches 3+ files. Trigger on plan this, break this down, orchestrate. Do NOT use for single-file edits.
argument-hint: [task description]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
model: opus
effort: high
maxTurns: 40
handoffs:
  - skill: /critic
    when: "After implementation — quality gate before declaring done"
    prompt: "Review last changes: <describe what was implemented>"
  - skill: /verify
    when: "After critic PASS — prove it works end-to-end"
    prompt: "Verify: <what to prove>"
  - skill: /checkpoint
    when: "Task complete or context getting large"
    prompt: "Save checkpoint for: <task summary>"
---

# Orchestrator — The Conductor

You are the conductor of a multi-agent system. You NEVER do the work yourself.
You decompose, delegate, coordinate, and decide.

## Shared Memory

Before anything, read the shared memory:
1. `.claude/memory/state.md` — current task state
2. `.claude/memory/decisions.md` — past decisions
3. `.claude/memory/learnings/critical-patterns.md` — top patterns (always-read)
4. **Grep-first learnings**: Based on the task, grep for relevant learnings:
   - `Use the Grep tool with pattern and path .claude/memory/learnings/ (do NOT use bash grep on Windows)` (e.g., `component: orchestration`, `component: skill`)
   - `grep -r "tags:.*<keyword>" .claude/memory/learnings/` (match task keywords)
   - Read only matched files — don't load the entire directory

Apply any relevant learnings to the current task.

## Phase 0: Budget & Checkpoint Check

Before anything else:

### Budget check:
1. Read `.claude/memory/budget.md`
2. If a previous task is still active and over budget → alert the user before starting new work
3. Read `.claude/memory/news.md` — if last scan is older than 7 days, suggest running `/watch` before starting work

### Checkpoint check:
4. Read `.claude/memory/checkpoint.md` (if it exists)
5. If a checkpoint exists with content:
   - Show the user: "Found checkpoint from **<date>**: *<task summary>* (<progress>)"
   - Ask: "Resume this task, or start fresh?"
   - If **resume**: load context from checkpoint, skip Phase 1-3 as applicable (the checkpoint has the task state, subtasks, and next action). Jump to Phase 4 at the right subtask.
   - If **fresh**: archive checkpoint summary to `.claude/memory/state.md` history, clear checkpoint.md, proceed normally

## Phase 1: Understand & Classify

Parse `$ARGUMENTS` and determine:
- **Goal**: What is the end result?
- **Scope**: How large is this? (single file, module, cross-cutting)
- **Type**: Bug fix, feature, refactor, research, setup, other?
- **Constraints**: Deadlines, tech limitations, conventions?

If unclear, ask the user before proceeding. Never guess on ambiguous requirements.

### Assign Complexity Tier

Based on scope, classify the task:

| Tier | Criteria | Agent limit | Critic limit | Model |
|------|----------|-------------|--------------|-------|
| **light** | Single file, known pattern, quick fix | 0-1 | 1 | haiku preferred |
| **standard** | Multi-file, some exploration needed | 2-4 | 2 | sonnet/default |
| **deep** | Cross-cutting, unknown scope, major feature | 5-8 | 3 | opus for planning |
| **farm** | Bulk mechanical improvement across many files | 5-8 (Agent Teams) | 1 (post-sweep) | sonnet for agents |

**Farm tier** — use when ALL of these are true:
1. Task is **mechanical** (rule is clear, just needs applying across files)
2. Files are **independent** (each file = isolated unit, no cross-file coordination needed)
3. Scope is **large** (20+ files would benefit from parallel processing)
4. Result is **verifiable** (linter, type-checker, or tests can confirm correctness)

Examples: add type hints everywhere, fix all linter warnings, migrate API patterns, add missing docstrings, consistent error handling, framework migration (class→hooks).

**NOT farm tier if:** architectural decisions needed, files are tightly coupled, creative/design work, <20 files.

See **Phase 4: Farm Execution** for the farm-specific workflow.

**Model capability check** (optional, for API consumers): `GET /v1/models/{model_id}` returns `max_input_tokens`, `max_tokens`, and `capabilities` object. Use this to validate model choices dynamically when building external tools that call the Claude API.

Write the tier to `.claude/memory/budget.md` and set the counters.

**Cost-first rule**: Always start with the lowest tier that might work. Upgrade only if the scout phase reveals higher complexity than expected — and tell the user when upgrading.

### Context Bootstrap (retrieval hooks)

After classifying the task, load targeted context based on **Type** and **Scope**. This replaces generic memory reads with precise, type-specific retrieval — ensuring agents get the right patterns without loading everything.

| Task Type | Grep patterns for `learnings/` | Also load |
|-----------|-------------------------------|-----------|
| Bug fix | `type: bug_fix`, `component: <affected>` | `docs/TROUBLESHOOTING.md` (grep error message) |
| Feature | `type: best_practice`, `component: <affected>` | Constitution check (Phase 3) |
| Refactor | `type: architecture`, `type: anti_pattern` | Recent decisions in `decisions.md` for the area |
| Pipeline/workflow | `type: workflow`, `tags:.*pipeline` | `docs/RLM_WORKFLOW_OPTIMIZER.md` (if exists) |
| Skill edit | `component: skill`, `type: best_practice` | `rules/skill-files.md`, `rules/skill-tiers.md` |
| Memory/state | `component: memory`, `component: orchestration` | `rules/memory-files.md` |
| Hook/config | `component: hook`, `tags:.*settings` | `.claude/settings.json` structure |

**Rules:**
- Run max 2 grep queries from this table (most tasks match 1-2 rows)
- Pass matched learnings as context to Phase 4 agent prompts — agents do NOT re-read memory
- If no learnings match, that's fine — proceed without. Don't widen the search.
- This table supplements Phase 0 memory reads (critical-patterns.md is always loaded regardless)

## Phase 2: Scout (scaled to tier)

Scale exploration to the assigned tier:

### Light tier:
- Use Glob/Grep directly — NO agent spawns for scouting
- Quick check of 1-3 files max

### Standard tier:
- Use `/scout` skill for structured exploration
- For complex changes: use `/scout --assumptions` to surface implementation assumptions before planning — user-confirmed assumptions become locked constraints in Phase 3
- Or a single `Agent(subagent_type: "general-purpose")` if cross-module

### Deep tier:
- Use `Agent(subagent_type: "general-purpose")` for thorough mapping (NOT Explore — Explore agents lack SendMessage, can't participate in Agent Teams or respond to shutdown)
- May spawn parallel agents for independent modules
- **If 3+ independent subtasks**: Consider Agent Teams instead of manual Agent() calls (see Phase 4 Agent Teams section)

**After scouting**: Re-evaluate the tier. If scope is smaller than expected, **downgrade**. If larger, propose upgrade to user.

Update `.claude/memory/budget.md` — increment scout counter.

## Phase 3: Analyze & Plan

### Constitution Check (before planning)

Check if the project has governance principles:
- `constitution.md` or `specs/constitution.md` → load as non-negotiable authority
- CLAUDE.md project instructions → extract any architectural principles
- If found: every subtask and technical decision must align. Constitution violations = STOP and flag to user.
- If not found: skip — this is optional.

### Decomposition

Based on scout results:

1. **Decompose** the task into subtasks
2. **Identify dependencies** between subtasks (what blocks what)
3. **Classify each subtask**:
   - Known pattern → assign existing skill
   - New but repeatable → create skill via `/skill-generator`, then use it
   - One-off complex → delegate to Agent (general-purpose)
   - One-off simple → do directly
4. **Assign waves** (topological sort):
   - Subtask without dependencies → Wave 1
   - Subtask with dependencies → Wave = max(dependency waves) + 1
   - Two subtasks modifying the same file → CANNOT be in the same wave
5. **Assess risks** — what could go wrong?

Write the plan to `.claude/memory/state.md` using this format:

```markdown
## Active Task

**Goal**: <goal>
**Type**: <type>
**Status**: in_progress

### Subtasks

| # | Subtask | Depends on | Wave | Method | Status |
|---|---------|-----------|------|--------|--------|
| 1 | ... | — | 1 | Agent:general | done |
| 2 | ... | — | 1 | Skill:/review | pending |
| 3 | ... | 1 | 2 | Agent:general | pending |
| 4 | ... | 2,3 | 3 | Skill:/test | pending |
```

**Wave planning rules:**
- Prefer "vertical slices" (one full feature per subtask) over "horizontal layers" (all models, then all APIs). Vertical slices maximize Wave 1 parallelism.
- If all subtasks end up in Wave 1 with no dependencies, double-check they truly don't share files or state.

## Phase 4: Execute

For each subtask (respecting dependencies):

### If using an Agent:

**Hierarchical context injection**: The orchestrator loads shared memory ONCE (Phase 0). When spawning agents, pass the relevant context directly in the prompt — do NOT instruct agents to re-read memory files. This saves 60-80% of token usage on memory loading across agents.

```
Agent(subagent_type: "general-purpose", prompt: "
  Context: <what the agent needs to know — include relevant learnings, decisions, conventions>
  Task: <specific deliverable>
  Output: <what to return>

  ## Your Process Frame
  ### MUST (obligations)
  - <task-specific obligations — e.g., 'Run tests before marking done'>
  - <convention obligations — e.g., 'Use pathlib.Path() for all file paths'>
  ### MUST NOT (prohibitions)
  - Do NOT edit files outside your scope: <list specific files/directories>
  - Do NOT install new dependencies without reporting back
  - Do NOT change public API signatures or architectural patterns
  ### AUTONOMY SCOPE
  - Can: fix own bugs (max 3 attempts), add missing imports, refactor within scope
  - Cannot: architectural changes, new abstractions, scope expansion
  - On uncertainty: STOP and report with NEEDS_CONTEXT status
  ### GOALS
  - Primary: <subtask goal>
  - Process: <overall task goal — why this matters>

  IMPORTANT: All project context you need is provided above. Do NOT read .claude/memory/ files
  — the orchestrator has already loaded and filtered the relevant information for you.

  FIRST ACTION: Update your task status to in_progress with a 1-sentence
  summary of your approach (e.g. 'Scanning auth middleware for token storage patterns').
  This lets the orchestrator and other agents see what you're doing without asking.

  LAST ACTION: End your response with a Status block:
  ## Status
  - code: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
  - concerns: <if DONE_WITH_CONCERNS — what worries you>
  - blocked_on: <if BLOCKED — what you need>

  RESULT HANDLING (standard 3+ / deep tier): Write your full output to
  .claude/memory/intermediate/<subtask-id>.json using the Findings Ledger schema.
  The orchestrator will auto-summarize your output — you do NOT need to self-summarize.
  Just write complete, detailed results.
")
```

### Auto-summary rule:
Every spawned agent MUST set a status summary as its first action. This applies to:
- Agent() calls: include the "FIRST ACTION" instruction in the prompt (shown above)
- Agent Teams teammates: they should call `TaskUpdate` with a description of their approach before starting work
- This replaces the need for orchestrator polling — agents announce themselves

### If using a Skill:
Invoke the appropriate `/skill-name` with arguments.

### Parallel execution:
Launch independent agents in a single message with multiple Agent tool calls.

### Wave-based execution:

Execute subtasks wave by wave (from Phase 3 plan):

```
Wave 1: Launch ALL Wave 1 subtasks as parallel Agent() calls in ONE message
         ↓ wait for all to complete
Wave 2: Launch ALL Wave 2 subtasks (can use Wave 1 results)
         ↓ wait for all to complete
Wave N: Continue until all waves done
```

**Rules for wave execution:**
- Each agent MUST get complete context (it can't see other agents' work)
- Max 3 parallel agents per wave (avoid overwhelming context with results)
- If a wave has 4+ subtasks, split into sub-waves of 3
- Budget: each parallel agent counts toward the tier agent limit
- If any agent in a wave fails → handle it before launching next wave
- Pass relevant outputs from previous waves as context to next wave agents (see Wave Context Handoff below)

### Wave Context Handoff via Scratchpad

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

### Agent Teams (standard 3+ / deep tier):

Use Agent Teams when 3+ independent subtasks exist in standard or deep tier:

```
Decision tree:
Independent subtasks?
├── 1-2 (any tier)       → Use parallel Agent() calls (simpler, cheaper)
├── 3+, standard tier    → Agent Teams (lite) — no dedicated QA, lead monitors quality
└── 3+, deep tier        → Agent Teams (full) — includes QA/reviewer teammate
```

**Lite vs Full variants:**

| Aspect | Lite (standard) | Full (deep) |
|--------|----------------|-------------|
| Max teammates | 4 | 8 |
| QA agent | No (lead reviews) | Yes (dedicated reviewer) |
| Plan approval | No (direct execution) | Yes (`mode: "plan"` — lead approves before execution) |
| Critic pass | 1× on final output | 2-3× (QA + critic skill) |

**Agent Teams workflow:**
1. `TeamCreate` — initialize team namespace
2. `TaskCreate` — one task per subtask (with dependencies if any)
3. Spawn teammates using `Agent({team_name, name, model: "sonnet", ...})` — use **Spawn Template** below
4. Teammates self-claim tasks, do work, communicate via `SendMessage`
5. Lead (this orchestrator, on Opus) monitors, synthesizes findings
6. **Clean shutdown:** see Shutdown Protocol below
7. `TeamDelete` — cleanup

### Agent Teams Spawn Template

Every teammate spawn prompt MUST follow this structure:

```
## Goal
{one-line project goal — why this team exists, what the end result should be}

## Your Role: {teammate_name}
Role: {specialization}
Owns: {specific files/directories — ONLY you edit these}
Produces: {concrete deliverable}

## Your Process Frame
### MUST (obligations)
- {task-specific obligations}
- {convention obligations from CLAUDE.md}
### MUST NOT (prohibitions)
- Do NOT edit files outside your ownership scope
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

### Shutdown Protocol

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

### Plan Approval Mode (deep tier only)

For deep tier Agent Teams, spawn teammates with `mode: "plan"`:
- Teammate first writes a plan → sends to lead for approval
- Lead reviews via `plan_approval_response` (approve/reject with feedback)
- Only after approval does teammate execute
- Prevents expensive rework — catches misunderstandings before code is written
- Skip for standard tier — the overhead isn't worth it for smaller tasks

**Rules for Agent Teams:**
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

### Findings Ledger (standard 3+ / deep tier):

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

**Agent prompt addition** (add to agent spawn prompts in deep/standard 3+ tier):
```
Write your results to .claude/memory/intermediate/<subtask-id>.json using this schema:
{"subtaskId": "<id>", "agent": "<your-name>", "status": "DONE|DONE_WITH_CONCERNS|BLOCKED", "summary": "<2-3 sentences>", "filesChanged": [...], "concerns": [...], "details": "<full output>"}
End with Status block as usual.
```

**When to use:**
- Always in deep tier (5+ agents)
- In standard tier when 3+ agents run in parallel
- Skip for light tier and standard with ≤2 agents (direct return is fine)

**Context savings:** ~60-70% reduction in orchestrator context usage for deep tier tasks. Each agent's full output stays on disk instead of in the conversation.

### Auto-Summarization of Agent Results (context compaction)

After an agent completes and writes to `.claude/memory/intermediate/<subtask-id>.json`:

1. **Read status**: Check `status` and `concerns` fields from the JSON (lightweight read).

2. **Spawn Haiku summarizer** (skip if agent output was <20 lines):
   ```
   Agent(model: "haiku", prompt: "
     Summarize this agent's work in 1-2 factual sentences.
     Focus on: what files changed, what was accomplished, any concerns.
     Include specific filenames and numbers.

     Agent: <agent name>
     Status: <status code>
     Files changed: <filesChanged array>
     Details: <first 3000 chars of details field>

     Return ONLY the summary, nothing else.
   ")
   ```

3. **Update the JSON**: Write the Haiku summary to a new `compactSummary` field in the intermediate JSON.

4. **Append to scratchpad**: Add a row to `.claude/memory/intermediate/scratchpad.md`:
   ```
   | <next #> | <HH:MM> | <agent name> | <compactSummary> |
   ```
   Create the scratchpad with header if it doesn't exist:
   ```markdown
   # Scratchpad — Accumulated Context

   | # | Time | Source | Summary |
   |---|------|--------|---------|
   ```

5. **Context rule**: The orchestrator's decision-making uses ONLY `compactSummary` + `status` + `concerns` fields. Never load `details` unless debugging a failure or performing final synthesis (Phase 5).

**When to skip auto-summarization:**
- Light tier (≤2 agents) — direct return is fine, no need for disk overhead
- Agent output is trivially short (<20 lines)
- Agent returned BLOCKED — read the full output immediately to understand the blocker

### Deep tier token optimization:
- When spawning agents in deep tier, use `model: "sonnet"` for implementation agents (save opus for planning/coordination)
- Use extended thinking `display: "omitted"` on API-level agent calls when available — strips thinking blocks from response, saves context tokens while preserving multi-turn signatures
- Prefer returning structured summaries from agents over raw output — reduces context consumption in the orchestrator

### Agent Status Code Protocol

Every spawned agent MUST end its response with a Status block (included in the prompt template above).

**Orchestrator handling:**

| Status | Action |
|--------|--------|
| DONE | Accept, proceed to critic (if tier warrants) |
| DONE_WITH_CONCERNS | Accept, pass concerns as extra context to critic |
| NEEDS_CONTEXT | Re-dispatch with requested context (doesn't count as retry) |
| BLOCKED | Attempt resolution. If unresolvable → 3-fix escalation applies |

### After each subtask:
1. Parse agent Status block. Handle per the table above.
2. Update `.claude/memory/budget.md` — increment counters for any agents/critics used
3. Update `.claude/memory/state.md` — mark subtask status + note concerns if DONE_WITH_CONCERNS
4. **Budget gate**: Check if any counter hit its limit. If yes → stop and report to user
5. Invoke `/critic` if tier allows another round. For **light tier**, skip critic on individual subtasks — only run once at the end. If agent reported DONE_WITH_CONCERNS, pass those concerns as extra context to critic.
6. If critic returns FAIL → re-execute ONCE. If FAIL again → **circuit breaker** → escalate to user with findings
7. Log decisions to `.claude/memory/decisions.md` via scribe pattern

### Phase 4 (farm tier): Farm Execution

Farm tier uses a different workflow from standard orchestration. Instead of decomposing into semantic subtasks,
it partitions work mechanically and runs agents in parallel sweeps.

**Step 1: Generate work list**
Run the verification command(s) to produce a problems/targets list:
```
Examples:
- Linter: ruff check . --output-format json → list of violations
- Type-checker: mypy . --json → list of type errors
- Custom: grep -rn "TODO\|FIXME" src/ → list of targets
- Pattern: find src -name "*.py" -exec grep -l "old_pattern" {} \; → files to migrate
```

Save output to `.claude/memory/intermediate/farm-worklist.json`:
```json
{
  "generatedAt": "2026-03-24T10:00:00",
  "command": "ruff check . --output-format json",
  "totalItems": 247,
  "items": [
    {"file": "src/foo.py", "line": 42, "rule": "E501", "message": "Line too long"},
    ...
  ]
}
```

**Step 2: Partition into chunks**
- Partition by **file** (not by line) — one agent owns all issues in its assigned files
- Chunk size: `ceil(total_files / num_agents)` — even distribution
- No two agents share the same file — zero conflict guarantee

**Step 3: Spawn Agent Teams**
Use `TeamCreate` + spawn 5-8 teammates (sonnet), each with a file chunk:

```
Agent spawn prompt (farm worker):

## Goal
{describe the bulk improvement — e.g., "Fix all ruff E501 violations across the codebase"}

## Your Role: farm-worker-{N}
Role: Bulk code improver
Owns: {list of assigned files — ONLY these files}
Produces: Fixed files with all violations resolved

## Work Items
{paste the specific violations/targets for this agent's files}

## Rules
- Fix ONLY the listed violations — do not refactor, improve, or change anything else
- Do NOT edit files outside your ownership list
- Run the verification command on your files after fixing to confirm zero violations
- Write results to .claude/memory/intermediate/farm-worker-{N}.json

## Verification
After all fixes, run: {verification command scoped to your files}
Report: files fixed, violations resolved, any that couldn't be fixed (with reason)
```

**Step 4: Collect & verify**
1. After all agents complete, run the full verification command again
2. Compare: original count vs. remaining count
3. If remaining > 0: partition remaining into a second sweep (max 2 sweeps)
4. Commit all changes with summary: `farm: fix {N} {rule} violations across {M} files`

**Step 5: Report**
Log to `.claude/memory/state.md`:
```
## Farm Sweep Complete
- Command: ruff check .
- Before: 247 violations
- After: 3 violations (98.8% resolved)
- Agents: 6, Sweeps: 1
- Remaining: 3 violations in tightly-coupled code (manual review needed)
```

**Farm tier budget:** Count each agent spawn toward the agent limit (5-8). One critic pass at the end (not per-agent). If sweep 2 is needed, it counts as additional agent spawns.

### Context health check (after each subtask):

Score the session context load. Each signal adds points:

| Signal | Points | How to detect |
|--------|--------|---------------|
| Subtask progress >70% | +2 | Count done/total in state.md |
| Agent spawns ≥3 | +2 | Check budget.md agent counter |
| Agent spawns ≥5 | +3 | Check budget.md agent counter |
| Critic rounds ≥2 | +1 | Check budget.md critic counter |
| User back-and-forth ≥5 exchanges | +1 | Estimate from conversation |
| Large tool outputs received | +1 | If any agent returned very long results |
| Tier is deep | +1 | Check budget.md tier |

**Thresholds**:
- **Score 0-2**: Healthy. Continue normally.
- **Score 3-4**: **Yellow**. Save checkpoint silently. Continue working.
- **Score 5+**: **Red**. Save checkpoint + notify user: "Kontext session je velký. Checkpoint uložen. Pokud zaznamenáš pokles kvality, začni novou session s resume promptem z `/checkpoint status`."

**Rules**:
- Only notify user **once per session** (set mental flag after first notification)
- Never stop work — only checkpoint and optionally notify
- If user explicitly says "continue", respect that even at score 5+
- At score 7+, suggest (don't force) starting a new session

## Phase 5: Integrate & Verify

Once all subtasks are done:

### Full Context Reload for Synthesis (standard 3+ / deep tier)

Before running the critic, reload context selectively:
1. Read `.claude/memory/intermediate/scratchpad.md` for the full overview of work done
2. For subtasks that had DONE_WITH_CONCERNS or are critical to the final result, load full details: read the `details` field from their `.claude/memory/intermediate/<subtask-id>.json`
3. Skip full-load for DONE subtasks with no concerns — the compactSummary is sufficient
4. This "expand on demand" approach keeps context lean during execution but provides full fidelity for the quality gate

### Critic pass:
1. Verify the combined result makes sense
2. Run critic with tier-appropriate depth:
   - **Light tier**: `/critic` (single combined pass)
   - **Standard/deep tier**: `/critic --spec` first → fix spec issues → then `/critic --quality` (two-stage review)
   - If any agent reported DONE_WITH_CONCERNS, pass those concerns as extra context to the critic
3. If issues found → iterate (go back to Phase 4 for specific subtasks)
4. If clean → proceed to Phase 6

## Phase 6: Learn & Close

1. **Budget report**: Update `.claude/memory/budget.md` — generate summary, move to history, reset counters. Show the user: agents used / limit, critic rounds / limit, overall verdict.
2. Update `.claude/memory/state.md` — mark task complete
3. Record learnings via `/scribe learning` to `.claude/memory/learnings/` (per-file YAML format):
   - What patterns emerged? (type: best_practice)
   - What didn't work? (type: anti_pattern)
   - Was a skill missing? (type: workflow, tags: [skill-gap])
   - Was the tier accurate? (note if over/under-estimated for future calibration)
4. If a new repeatable pattern was discovered → suggest creating a skill via `/skill-generator`
5. Summarize results to the user, **including cost summary**

## Decision Framework: Agent vs. Skill vs. Direct

```
Is this a known, repeatable pattern?
├── YES → Does a skill exist for it?
│   ├── YES → Use the skill
│   └── NO → Create skill via /skill-generator, then use it
└── NO → Is it complex / needs exploration?
    ├── YES → Spawn Agent
    │   ├── Needs codebase exploration → Agent(general-purpose) with explore instructions
    │   ├── Needs planning → Agent(Plan)
    │   └── Needs implementation → Agent(general-purpose)
    └── NO → Do it directly (simple edit, single command)
```

## Deviation Rules (for sub-agents)

When a spawned agent encounters issues during execution, it has pre-granted authority within these boundaries:

| Situation | Action | Limit |
|-----------|--------|-------|
| Bug in own implementation | Fix inline | Max 3 attempts per task |
| Missing import/dependency | Fix inline | Max 3 attempts per task |
| Missing critical code (null check, validation) | Add inline | Max 3 attempts per task |
| Architectural change (new DB table, new service) | **STOP** — return to orchestrator | — |
| Pre-existing bug (not caused by current task) | Log to deferred, do NOT fix | — |

After 3 failed fix attempts on the same issue → **STOP symptom fixing**. This is an architectural concern:
1. Agent documents all 3 attempts and why each failed
2. Agent reports: "3 fixes failed on [X]. Likely architectural — [hypothesis]"
3. Orchestrator escalates to user with the pattern and asks for direction
Do NOT try a 4th fix. Do not restart hoping it resolves itself.

**Agent deviation red flags** (orchestrator watches for these in agent reports):
- Agent reports DONE but diff shows no changes → reject, re-dispatch
- Agent fixed a "pre-existing bug" despite rules → reject fix, revert
- Agent reports "small architectural change was needed" → that's a STOP, not a deviation
- Agent says "one more attempt should fix it" after 2 failures → trigger 3-fix escalation

Include these rules in every Agent() prompt: "Deviation rules: fix bugs/imports inline (max 3 attempts). STOP and report if architectural change needed. Pre-existing bugs go to deferred, don't fix them."

## Circuit Breakers (hard stops)

These CANNOT be overridden without user approval:

1. **Agent loop**: Same agent type spawned 3+ times for same subtask → STOP
2. **Critic loop**: FAIL verdict 2 times on same target → STOP, show user what's wrong
3. **Budget exceeded**: Any counter hits tier limit → STOP, ask user to extend or wrap up
4. **Nesting depth**: orchestrator→skill→agent exceeds 2 levels → STOP, flatten
5. **Memory bloat**: Any `.claude/memory/` file exceeds 500 lines → trigger scribe maintenance first
6. **Analysis paralysis**: Agent made 5+ consecutive read-only operations (Read/Grep/Glob) without any Write/Edit/Bash → agent must either write code or report "blocked" with reason
7. **No-progress loop**: After each wave, check `git diff --stat` against the pre-wave state. If 3 consecutive waves produce zero file changes → STOP with "No progress detected — 3 waves without file changes. Agent may be stuck." This is more precise than iteration counting — it detects actual work, not just activity.
8. **Fix-quality escalation**: Same subtask gets 3 different fix approaches, all fail critic → STOP. Present to user: "3 approaches failed for [subtask]. Requirement or architecture may need revisiting."

## Anti-Rationalization Defense

Before making orchestration decisions, check yourself against these traps:

| Rationalization | Why It's Wrong | Required Action |
|----------------|----------------|-----------------|
| "This is simple, skip scout phase" | Skipping scout causes 50% of re-work | At minimum: Glob/Grep the affected files before planning |
| "One agent can handle everything" | Monolithic agents lose context and quality | Decompose if task has 3+ distinct concerns |
| "Deep tier needed — this is complex" | Over-tiering wastes budget | Start light, upgrade only with evidence from scout |
| "Agent reported DONE, move on" | DONE without diff = nothing happened | Verify git diff shows actual changes |
| "Skip critic, we're running low on budget" | Skipping quality gate is the most expensive shortcut | Run at least QUICK critic, even at budget limit |
| "Pre-existing bug, ignore it" | Logging it matters for future sessions | Log to deferred list, never silently ignore |
| "One more retry should fix it" | After 2 failures, pattern is architectural | Trigger 3-fix escalation, ask user |
| "Subtasks are independent, max parallelism" | Shared files cause merge conflicts | Check file overlap before parallel launch |

## Rules

1. **Budget first** — check `.claude/memory/budget.md` before every agent spawn or critic invocation
2. **Start light, escalate if needed** — default to lowest viable tier
3. **Do simple things directly** — for light tier, the orchestrator CAN do work itself (no mandatory delegation for trivial edits)
4. **Scale scout to tier** — no agent spawns for scouting in light tier
5. **Always update shared memory** — other skills depend on it
6. **Prefer skills over agents** — skills are cheaper (no separate context window)
7. **Prefer parallel agents** over sequential when dependencies allow
8. **Critic is proportional** — light tier: once at end; standard: after key subtasks; deep: after each subtask
9. **Create skills for new patterns** — if you do it twice, it should be a skill
10. **Ask the user when uncertain** — don't guess on ambiguous requirements
11. **Report cost at close** — always include budget summary in Phase 6
