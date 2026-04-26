---
name: orchestrate-light
description: Use when task is clearly LIGHT tier — single file, mechanical fix, known pattern (typo, rename, bump version, simple update). Trigger on 'fix typo', 'quick fix', 'rename', 'bump', 'tweak', 'oprav typo'. Do NOT use for multi-file changes (use /orchestrate), vague specs (/brainstorm), or research (/scout, /deepresearch). Auto-escalates to /orchestrate if scope expands.
argument-hint: [task description]
discovery-keywords: [typo, rename, quick, light, simple, mechanical, single-file, oprav, přejmenuj]
tags: [orchestration, planning]
phase: plan
user-invocable: true
allowed-tools: Read, Glob, Grep, Agent, TodoWrite
deny-tools: [Bash, Write, Edit]
permission-tier: coordinator
model: haiku
effort: low
maxTurns: 15
max-depth: 1
input-contract: "user → task description (single concrete change) → light tier confirmable"
output-contract: "1-2 file modifications via 1 worker agent → state.md updated"
preconditions:
  - "task scope is single file OR mechanical change across <5 files"
  - "no architectural decisions required"
handoffs:
  - skill: /critic
    when: "After implementation — quick quality gate"
    prompt: "Review last change: <describe>"
  - skill: /orchestrate
    when: "Tier classification reveals scope > light (2+ files, exploration needed)"
    prompt: "<original task — escalated from /orchestrate-light>"
---

# Orchestrate-Light — Lightweight Orchestrator (Haiku)

Lightweight orchestrator for **light tier only** (single file, known pattern, mechanical fix). Inspired by ParaManager (arXiv:2604.17009): small model + standardized worker interface beats large model + heterogeneous APIs.

**COORDINATOR TOOL RESTRICTION**: NO Bash/Write/Edit. Delegate via Agent.

## Pre-Flight: Tier Verification (HARD GATE)

Before any work: classify task tier. If NOT light → STOP and recommend `/orchestrate`.

| Light tier signal | NOT-light signal |
|-------------------|------------------|
| "fix typo", "rename X to Y", "bump version", "update string" | "refactor", "redesign", "implement feature", "audit" |
| Single file estimable from task description | Cross-cutting, unclear scope, 6+ files |
| Mechanical pattern (no design decision) | Architectural choice required |
| Glob count of affected files: 1 | Glob shows 5+ files |

If task description is ambiguous → run 1 Glob/Grep MAX to estimate file count. If >5 files or design unclear: **STOP**, output:
```
This task exceeds light tier (estimated <N> files / requires <reason>).
Recommend: /orchestrate <original task>
```

## Workflow (compressed — single wave, single agent)

### Phase 1: Read shared memory + classify

1. Read `.claude/memory/state.md`, `.claude/memory/budget.md`, `.claude/memory/learnings/critical-patterns.md`
2. Grep relevant learnings: `Grep pattern="<keyword from task>" path=".claude/memory/learnings/"` — read matches only
3. Confirm light tier (see Pre-Flight)

### Phase 2: Mini scout (max 3 tool calls)

- 1× Glob for affected files
- 1× Grep for relevant pattern (to confirm change site)
- 1× Read of primary affected file (first 50 lines or relevant section)

If mini scout reveals scope > light → escalate to `/orchestrate`.

### Phase 3: Plan (single subtask, no decomposition)

Write to `.claude/memory/state.md`:
```yaml
---
task_id: <slug>
goal: "<task>"
type: light
tier: light
status: in_progress
subtasks:
  - {id: "st-1", description: "<task>", criterion: "<verifiable check>", done_when: "<machine-checkable command>", context_scope: ["<file>"], depends_on: [], wave: 1, method: "Agent:general", status: "pending"}
---
## Active Task
**Goal**: <task>
**Tier**: light
**Subtask**: st-1 — <description>
**Done when**: <machine-checkable>
```

Skip dependency graph (single subtask).

### Phase 4: Execute (1 agent, haiku)

Spawn ONE worker agent (haiku):

```
Agent(subagent_type: "general-purpose", prompt: "
  ## Task
  <subtask.description>

  ## Context
  - File: <context_scope[0]>
  - Pattern to change: <details from scout>
  - Done when: <subtask.done_when>

  ## File Access Manifest
  - WRITE: [<context_scope[0]>]
  - READ:  [related-test-file if exists]
  - FORBIDDEN: [everything else]

  ## Constraints
  - Single mechanical change — do NOT refactor adjacent code
  - Do NOT add type hints, docstrings, or 'improvements' beyond the task
  - Match existing style (see CLAUDE.md § Code Editing Discipline)

  IMPORTANT: All context is provided above. Do NOT spawn sub-agents.

  LAST ACTION: end with Status block:
  ## Status
  - code: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
  - file_changed: <path or 'none'>
  - verification: <output of done_when check>
", model: "haiku")
```

Do NOT use parallel agents (light tier = 1 agent max).

### Phase 5: Verify + critic

1. Parse Status block; if BLOCKED or NEEDS_CONTEXT → escalate to `/orchestrate`
2. Verify `done_when` condition holds (run the check)
3. Invoke `/critic` (single pass): `Skill /critic args:"Review last change: <subtask>"`
4. If critic FAIL once → re-spawn worker with critic feedback (max 1 retry)
5. If FAIL twice → STOP, escalate to `/orchestrate` for deep analysis

### Phase 6: Close

1. Update state.md: subtask status → `done` (or `failed`), append artifacts
2. Update budget.md: increment light-tier counter, log model: haiku, agent_count: 1
3. Append routing trace to `.claude/memory/routing-traces.jsonl`:
   ```json
   {"date": "<today>", "task_class": "light_fix", "model": "haiku", "tier": "light", "files_changed": 1, "wave": 1, "critic_score": "<PASS|FAIL>", "orchestrator": "haiku-light"}
   ```
4. NO heartbeat cleanup needed (light tier doesn't create one)
5. NO `/sweep` (light tier doesn't trigger entropy)
6. NO `/scribe` learning unless critic FAIL'd or pattern is novel

## Auto-Escalation Conditions (immediate)

Trigger automatic escalation to `/orchestrate` if:
- Mini scout reveals 5+ affected files
- Worker reports `BLOCKED` or `NEEDS_CONTEXT`
- 2× critic FAIL
- File Access Manifest WRITE list grows during execution
- Agent requests sub-agent (which it shouldn't — but if it does)

Escalation message:
```
/orchestrate-light has hit a complexity boundary. Escalating to /orchestrate:
Reason: <one sentence>
Original task: <task>
Work done so far: <subtask status, artifacts>
```

## Circuit Breakers (HARD STOPS)

1. **Tier mismatch**: scope > light → STOP, escalate
2. **Agent loop**: 1× FAIL on subtask → STOP (light tier has only 1 retry budget)
3. **Budget exceeded**: light tier limit hit → STOP
4. **Infrastructure error** (ENOENT, EACCES, OOM): IMMEDIATE STOP, escalate
5. **Self-spawning**: agent tries to spawn sub-agents → STOP (max-depth=1)

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|----------------|-----------|------------|
| "I'll just escalate to /orchestrate immediately" | /orchestrate-light exists to handle light tier cheaply; default escalation defeats purpose | Confirm light tier first; escalate only if scope verifiable >light |
| "Skip mini scout — it's just a typo" | Untested assumptions cause 50% rework | Always run 1 Glob + 1 Grep minimum |
| "Add type hints while I'm here" | Scope creep; user didn't ask | Do ONLY the requested change; mention extras in response |
| "Spawn 2 agents in parallel for speed" | Light tier = 1 agent max | If task needs 2 agents → it's standard tier, escalate |
| "Skip critic, it's a 1-line change" | Even 1-line changes break things; critic is cheap with haiku | Always run /critic |

## Red Flags (STOP and re-evaluate)

- Mini scout returned 6+ matching files
- Worker requested SHARED_WRITE or wider scope
- Critic flagged "incomplete" or "missing tests"
- Task description contains "and also" / "while you're at it"
- Agent reported DONE but git diff is empty

## Verification Checklist

- [ ] Tier verified as light BEFORE planning
- [ ] Mini scout completed (≤3 tool calls)
- [ ] Single subtask with verifiable `done_when`
- [ ] Worker spawned with haiku model + File Access Manifest
- [ ] Critic ran once and passed (or 1 retry succeeded)
- [ ] state.md + budget.md + routing-traces.jsonl updated
- [ ] No scope expansion during execution

## Rules

1. Light tier ONLY — escalate on first sign of complexity
2. 1 agent max, haiku model, max 1 retry
3. No parallel waves (single subtask)
4. Mini scout BEFORE planning (3 calls budget)
5. Match existing code style (per CLAUDE.md § Code Editing Discipline)
6. Mention dead code, don't delete it (Karpathy Rule 2)
7. Trace every change to user request (Karpathy Rule 3)
8. Auto-escalate on BLOCKED / NEEDS_CONTEXT / 2× FAIL

## Cost Profile (vs full /orchestrate)

Based on POC (issue #18, 2026-04-26):
- Haiku orchestrator: ~$0.43–0.55 per light task
- Opus orchestrator (current /orchestrate): ~$3.20–4.45 per same task
- **Expected savings**: ~85–90 % per light-tier orchestration

Note: this is empirically validated only on plan-quality + simple execute. Production rollout requires P3 A/B test (20 real tasks, threshold ≥90 % task success vs Opus, ≥50 % cost reduction).

## When to use full /orchestrate instead

- Task touches 2+ files
- Task requires architectural decision
- Task is exploratory (audit, research, scout-heavy)
- Light tier escalated automatically
- User explicitly requested standard/deep tier
