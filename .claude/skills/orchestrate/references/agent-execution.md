# Agent Execution — Phase 4 Details

## Agent Prompt Template

**Hierarchical context injection**: The orchestrator loads shared memory ONCE (Phase 0). When spawning agents, pass the relevant context directly in the prompt — do NOT instruct agents to re-read memory files. This saves 60-80% of token usage on memory loading across agents.

**Diversity framing** (deep tier only, ref: arXiv:2603.19138 — P2 lock-in at 97.6% means parallel agents independently converge on identical solutions):
When spawning 2+ agents in the same wave for the **deep** tier, vary their reasoning frame to reduce convergence:
- Agent 1: default framing (as below)
- Agent 2: add `Approach constraint: prefer the simplest possible solution — minimize abstractions and dependencies`
- Agent 3: add `Approach constraint: consider what could go wrong first — design for failure modes, then build the happy path`
This is NOT about different tasks — each agent still has its own subtask. It's about preventing identical reasoning patterns when agents share similar context.

```
Agent(subagent_type: "general-purpose", prompt: "
  Context: <what the agent needs to know — include relevant learnings, decisions, conventions>
  Task: <specific deliverable>
  Output: <what to return>

  ## File Access Manifest (ref: arXiv:2603.12229 — concurrent writes are the #1 consistency failure)
  - WRITE: [<files this agent owns — only it edits these>]
  - READ:  [<files for reference — do not modify>]
  - FORBIDDEN: [<files owned by other agents — do NOT touch under any circumstances>]

  ## Your Process Frame
  ### MUST (obligations)
  - <task-specific obligations — e.g., 'Run tests before marking done'>
  - <convention obligations — e.g., 'Use pathlib.Path() for all file paths'>
  - Respect File Access Manifest — WRITE only to your owned files
  ### MUST NOT (prohibitions)
  - Do NOT edit files in FORBIDDEN list (owned by other agents in this wave)
  - Do NOT edit READ-only files (shared reference, not your scope)
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

## Auto-summary rule

Every spawned agent MUST set a status summary as its first action. This applies to:
- Agent() calls: include the "FIRST ACTION" instruction in the prompt (shown above)
- Agent Teams teammates: they should call `TaskUpdate` with a description of their approach before starting work
- This replaces the need for orchestrator polling — agents announce themselves

## Parallel execution

Launch independent agents in a single message with multiple Agent tool calls.

## Pre-launch disjointness check (before ANY parallel spawn)

Before launching 2+ agents in the same wave, verify their WRITE file lists don't overlap:

1. Collect the WRITE list from each agent's File Access Manifest
2. Compute pairwise intersection: `agent_A.WRITE ∩ agent_B.WRITE`
3. **If overlap = 0** → safe to parallelize
4. **If overlap > 0** → sequentialize the overlapping agents (launch one, wait, launch next)
   - Log: `"Disjointness conflict: agents {A, B} both write to {files} — forcing sequential"`
   - The agent that runs second gets the first agent's output as READ context

This check is mandatory for standard/deep tiers. Farm tier already has zero-conflict guarantee via file partitioning.

## Wave-based execution

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
- **Validate agent outputs** before passing to next wave (see wave-recovery.md)
- Pass relevant outputs from previous waves as context to next wave agents (see wave-recovery.md)
- **Wave checkpoint** after each completed wave (see wave-recovery.md)

## Plan Approval Gate (deep tier, inspired by CC Agent Teams)

For deep tier subtasks with high risk or uncertainty, spawn the agent in **plan-first mode**:

1. Agent receives subtask with instruction: "FIRST: Write a 3-5 line plan of your approach. Do NOT start implementation until orchestrator confirms."
2. Agent writes plan to `.claude/memory/intermediate/<subtask-id>-plan.json`
3. Orchestrator reads the plan and either:
   - **Approves**: Sends follow-up message "Plan approved. Proceed with implementation."
   - **Rejects with feedback**: "Plan rejected. Issue: <reason>. Revised approach: <guidance>"
4. Agent proceeds only after approval

**When to use Plan Approval Gate:**
- Subtasks touching 5+ files
- Subtasks involving architectural decisions
- Subtasks where the orchestrator is uncertain about the right approach
- Deep tier tasks with `DONE_WITH_CONCERNS` history on similar work

**When to skip:**
- Light/standard tier (overhead not worth it)
- Mechanical subtasks (linting, formatting, migrations)
- Subtasks with well-defined, narrow scope

## Structured Agent Output Format (P5)

Instead of parsing raw markdown from agents, instruct agents to write structured results:

```json
{
  "subtask_id": "1a",
  "status": "DONE",
  "confidence": 0.85,
  "files_changed": ["src/auth.py", "tests/test_auth.py"],
  "findings": [
    "Token validation was missing expiry check",
    "Added 2 test cases for edge conditions"
  ],
  "concerns": [],
  "suggestions_for_next_wave": [
    "Integration test should verify full auth flow"
  ],
  "metrics": {
    "lines_added": 45,
    "lines_removed": 12,
    "tests_passed": true
  }
}
```

**Usage:** Add to agent prompt template:
```
RESULT FORMAT: Write your structured result to
.claude/memory/intermediate/<subtask-id>.json using the schema above.
Include confidence (0.0-1.0) reflecting how certain you are the work is correct.
```

**Orchestrator benefits:**
- Parse `confidence` to decide if critic review is needed (< 0.7 → always critic)
- Aggregate `files_changed` across agents for disjointness validation
- Use `suggestions_for_next_wave` as context injection for downstream agents
- `metrics` feed into budget tracking
