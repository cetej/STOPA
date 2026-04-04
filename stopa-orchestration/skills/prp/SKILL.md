---
name: prp
description: Use when preparing task context for handoff between sessions or sub-agents. Trigger on 'prp', 'context packet', 'prepare handoff'. Do NOT use for brainstorming or documenting completed work.
argument-hint: <task description> [--scope file|module|project]
tags: [session, orchestration]
phase: plan
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - Write
  - TodoWrite
effort: medium
---

# /prp — Prompt-Ready Packet Generator

Generate a self-contained task context document optimized for AI consumption. A PRP gives any Claude session everything it needs to execute a task — no codebase re-scanning needed.

## When to Use

- Handing off a task to a new session (context too large, session ending)
- Delegating complex subtasks to sub-agents
- Preparing context for `/orchestrate` on a well-scoped task
- Documenting a task for async execution

<!-- CACHE_BOUNDARY -->

## Process

### Phase 1: Scope Identification

Understand the task:
1. What needs to be done? (from user input or active checkpoint)
2. What's the acceptance criteria?
3. What's the estimated complexity? (light/standard/deep)

### Phase 2: Context Gathering

Scan the codebase for relevant context. Gather:

| Category | What to include |
|----------|----------------|
| **Architecture** | Relevant patterns, directory structure, key abstractions |
| **Key files** | Files that will be read or modified (with paths + brief purpose) |
| **Dependencies** | External libs, APIs, services involved |
| **Constraints** | Rules from CLAUDE.md, coding conventions, known gotchas |
| **Prior art** | Similar features, relevant decisions from memory |
| **Test strategy** | How to verify the task is done correctly |

Use sub-agents (Explore) for broad scanning. Keep context focused — include only what's needed for THIS task.

### Phase 3: PRP Generation

Output format:

```markdown
# PRP: [Task Title]

Generated: [date]
Complexity: light | standard | deep
Target: /orchestrate | sub-agent | new session

## Objective
[1-2 sentences: what to do and why]

## Acceptance Criteria
1. [Testable criterion]
2. [Testable criterion]
3. [...]

## Context Map

### Key Files
| File | Purpose | Action |
|------|---------|--------|
| `path/to/file.py` | [what it does] | read / modify / create |

### Patterns to Follow
- [Pattern 1 with example from codebase]
- [Pattern 2]

### Constraints
- [From CLAUDE.md or project rules]
- [From dependencies or API limits]

## Implementation Hints
- [Approach suggestion if non-obvious]
- [Known gotcha or edge case]
- [Reference to similar code]

## Verification
- [ ] [How to verify criterion 1]
- [ ] [How to verify criterion 2]

## Open Questions
- [Anything the executor should clarify before starting]
```

### Phase 4: Delivery

Save the PRP to `output/prp-[task-name].md` and display a summary.

If the user wants immediate execution: feed the PRP content directly as a prompt to `/orchestrate`.

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll skip context gathering since I know this codebase well" | PRPs are consumed by fresh sessions or sub-agents with no codebase knowledge; assumed context makes them unusable | Always run Phase 2 scanning; include file paths, patterns, and constraints explicitly |
| "The acceptance criteria are implicit — the task description is specific enough" | Implicit criteria mean the executor decides what 'done' looks like, producing divergent results | Write at least 3 explicit testable acceptance criteria, even for seemingly clear tasks |
| "I'll dump the full file contents into the PRP since the executor will need them" | Full dumps bloat PRP context, push critical instructions out of the context window, and go stale | Reference files by path with a one-line purpose note; only paste short critical snippets |
| "The PRP doesn't need a verification section since the executor can figure that out" | Without explicit verification steps, executors declare done based on confidence rather than evidence | Include a Verification checklist mapping each criterion to a concrete check command or test |
| "I'll skip the open questions section since I don't want to block the handoff" | Undocumented blockers surface mid-execution, forcing the sub-agent to halt or make silent assumptions | List every unresolved question explicitly so the executor knows when to stop and ask |

## Quality Rules

- **Completeness**: Someone with NO prior context should be able to execute the task from the PRP alone
- **Conciseness**: Include only relevant context — no filler, no "nice to know"
- **Accuracy**: Verify file paths exist, imports are correct, patterns are current
- **Actionability**: Every section should help the executor make progress, not just inform
- **No code dumps**: Reference files by path, don't paste full contents unless they're short and critical
