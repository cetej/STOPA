# Agent Execution — Phase 4 Details

**Workspace model (informal, LLM-driven):** When planning a deep-tier task, think of each subtask as operating in four zones — `B_ctx` (immutable grounding refs), `B_work` (owned write targets), `B_sys` (shared memory like state.md), `B_ans` (final deliverables). Per-subtask contracts (`reads_from`/`writes_to`) are a planning concept only — no runtime validator enforces them. Use the disjointness and readability checks later in this file to verify contracts manually before spawning agents.

## Pre-Spawn: Task Directory Setup (LLM Wiki v2 — Gap 3: shared/private scoping)

Before spawning the first agent wave, create the task directory for memory isolation:

```
.claude/memory/intermediate/{task-id}/     ← agent private scratch
.claude/memory/intermediate/shared/        ← cross-agent shared findings
```

Where `task-id` is a slug from the Phase 1 goal (lowercase, underscores, max 32 chars).
If `intermediate/{task-id}/manifest.json` already exists and is <1h old, append timestamp suffix.

Write `intermediate/{task-id}/manifest.json`:
```json
{"task_id": "<slug>", "created": "<ISO datetime>", "tier": "<tier>", "agents": []}
```

Also ensure `intermediate/shared/` exists (it persists across tasks).

### Agent Directory Scoping

Each agent's File Access Manifest includes scoped paths:

```
## File Access Manifest
- WRITE: [.claude/memory/intermediate/{task-id}/{subtask-id}.json, <owned source files>]
- READ:  [.claude/memory/intermediate/shared/, <reference files>]
- SHARED_WRITE: [.claude/memory/intermediate/shared/] — only for cross-agent findings
- FORBIDDEN: [.claude/memory/intermediate/{task-id}/<other-subtask>.json]
```

Rules:
- Each agent owns exactly ONE output file in `{task-id}/`
- Agents may read `shared/` freely
- Agents may write to `shared/` ONLY when explicitly granted `SHARED_WRITE` (findings that affect other agents)
- Self-organizing agents (exploratory) get READ on the full `{task-id}/` directory (they discover relevant files)

## Context Assembly Protocol (Latent Briefing, ref: 2026-04-11)

Before building the `Context:` section for any agent, categorize available information into 4 categories. Speculative orchestrator reasoning (dead-end hypotheses, exploration trails, rejected alternatives) degrades worker accuracy — aggressive filtering on hard tasks improves accuracy by +3pp while saving 49-65% tokens (Latent Briefing: KV Cache Compaction for Multi-Agent Systems).

### Category 1: FACTS (always include)
- Scout findings: file locations, dependency map, API signatures
- Prior wave RESULTS: concrete outputs (code changes, test results, metrics)
- Learnings: block-scored selection (from context-bootstrap.md)
- Key conventions: from CLAUDE.md, grounding_refs

### Category 2: TASK (always include)
- Subtask description, criterion, done_when
- Scoped files (context_scope contents)
- Upstream dependencies' concrete outputs

### Category 3: REASONING (include selectively — omit for light/farm)
- 1-2 sentences of high-level rationale: WHY this decomposition, WHY this approach
- STRIP: exploration trail, hypothesis testing, rejected alternatives, dead ends, planning deliberation
- Rule: if you can't say it in 2 sentences, it's exploration, not rationale

### Category 4: FAILURES (only when directly relevant to THIS subtask)
- WHAT failed and WHY (1 sentence each) — to prevent worker from repeating
- STRIP: full failure trajectory, debugging steps, intermediate states
- Include only if the failure is on the same file/module as the current subtask

### Tier-Based Context Strategy

| Tier | Include | Strip | Learnings Budget |
|------|---------|-------|-----------------|
| light | Facts + Task | Everything else | ~1,000 tokens (top-2 blocks) |
| standard | Facts + Task + key Rationale | Exploration, failures (unless relevant) | ~2,000 tokens (top-5) |
| deep | All 4 categories, light filtering | Only raw exploration trails | ~4,000 tokens (top-8 + hybrid) |
| farm | Pattern + file list only | All reasoning, all failures | ~500 tokens (top-1 if relevant) |

**Anti-pattern**: Dumping the orchestrator's full planning trace into agent context. Workers need clean signal — not the orchestrator's cognitive trail. More context ≠ better context.

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
  ## Execution Chain (MBIF-inspired call chain tracking)
  - Task: <overall goal from state.md>
  - Chain so far: [<agent-1-role: 1-line result>, <agent-2-role: 1-line result>, ...]
  - You are: step <N> of <max for tier> (light=1, standard=4, deep=8)
  - Wave: <current wave> of <total waves>
  - Remaining budget: <from budget.md — agents/critics left>

  ## Context (assembled per Context Assembly Protocol above)
  ### Facts
  <scout findings, prior wave results, key conventions — concrete verified information only>
  ### Rationale (omit for light/farm tier)
  <1-2 sentences: WHY this approach was chosen — not HOW the orchestrator explored options>
  ### Avoid (only if directly relevant to THIS subtask)
  <WHAT failed previously and WHY — 1 sentence each, to prevent repetition>

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

  ## Live Alert Protocol (deep tier only — REMOVE this section for light/standard/farm)
  If you discover something that affects OTHER agents' work (breaking API change, shared
  dependency problem, security issue), IMMEDIATELY:
  1. Append to .claude/memory/intermediate/shared/alerts.jsonl
  2. SendMessage to lead with type + summary + files_affected
  Do NOT wait until done — early alert prevents duplicate/wasted work by other agents.

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

## Self-Organizing Agent Template (exploratory tasks)

When `task_style == exploratory` (classified in Phase 1), use this lighter template instead of the full prescribed template above. The agent receives the mission and quality goal — it decides HOW to approach it.

```
Agent(subagent_type: "general-purpose", prompt: "
  ## Mission
  <overall goal from state.md — what needs to be accomplished>

  ## Quality Goal
  <what a good result looks like — not HOW to get there>

  ## Context (assembled per Context Assembly Protocol — Facts section only for light/farm)
  ### Facts
  <scout findings, prior results, conventions — concrete verified information>
  ### Rationale (omit for light/farm tier)
  <1-2 sentences WHY — not the orchestrator's exploration trail>

  ## Scope
  - Files/directories in scope: <list>
  - Standards to check against: <file paths if applicable>
  - Time/budget constraint: step <N> of <max>, budget remaining: <from budget.md>

  ## Constraints (what NOT to do)
  - Do NOT edit any files — this is analysis/research only
  - <any task-specific constraints>

  Figure out the best approach yourself — what to read, what to check, in what order.

  IMPORTANT: All project context you need is provided above. Do NOT read .claude/memory/ files.

  LAST ACTION: End with Status block:
  ## Status
  - code: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
  - concerns: <if applicable>
")
```

**Key differences from structured template:**
- No prescribed steps (MUST/MUST NOT/AUTONOMY SCOPE replaced by mission + quality goal)
- No File Access Manifest (agent discovers relevant files itself)
- No Execution Chain framing (agent decides its own sequence)
- Constraints section is minimal — only hard limits
- Results in broader exploration, more issues found (+8% quality on exploratory tasks)

**When to use which:**

| task_style | Template | Reason |
|------------|----------|--------|
| `exploratory` | Self-organizing (above) | Agent discovers what matters — finds unexpected issues |
| `structured` | Full prescribed (above) | Steps ensure consistent, well-formatted output |
| Mixed (some subtasks each) | Per-subtask choice | Exploratory subtasks get self-org, structured get prescribed |

**Farm tier exception:** Always use structured template — mechanical tasks need prescribed steps regardless.

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

## Live Findings Broadcast (deep tier, GEA-inspired)

During deep tier execution, agents may discover cross-cutting findings (breaking API changes,
shared dependency issues, security concerns) that affect other running agents. Instead of waiting
for wave completion, agents broadcast these immediately.

**Mechanism:**
1. Agent writes alert to `intermediate/shared/alerts.jsonl` (append):
   ```json
   {"ts": "<ISO>", "agent": "<subtask-id>", "type": "breaking_change|dependency|security|scope_change", "summary": "<1-sentence>", "files_affected": ["<paths>"]}
   ```
2. Agent sends `SendMessage(to: "<team-lead-name>", summary: "Alert: <type>", message: "<1-sentence summary + files>")` to orchestrator lead

**Orchestrator response to alert:**
- `breaking_change` or `security`: evaluate whether running agents need to stop. If their WRITE files overlap with `files_affected` → send interrupt message. Otherwise → inject alert as READ context for next wave.
- `dependency` or `scope_change`: log to scratchpad, inject as context into next wave agents. No interrupt.

**Agent prompt addition** (deep tier only — add after `## Your Process Frame` section):
```
## Live Alert Protocol (deep tier)
If you discover something that affects OTHER agents' work (breaking API change, shared
dependency problem, security issue), IMMEDIATELY:
1. Append to .claude/memory/intermediate/shared/alerts.jsonl
2. SendMessage to lead with summary
Do NOT wait until you're done — early alert prevents duplicate/wasted work.
```

**When NOT to use:**
- Farm tier: mechanical fixes, no cross-file discoveries
- Light/standard tier: single-wave or simple coordination — alerts add overhead without benefit
- Agent already in final status reporting (use `concerns` field in Status block instead)

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
