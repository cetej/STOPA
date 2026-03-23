---
name: prp
description: >
  Generate a Prompt-Ready Packet (PRP) — an AI-optimized task context document that gives any Claude session
  everything it needs to execute a task without re-reading the entire codebase.
  Use when handing off work between sessions, delegating to sub-agents, or preparing context for /orchestrate.
  Trigger on 'prp', 'context packet', 'prepare handoff', 'task brief', 'připrav kontext'.
  Do NOT use for brainstorming (use /brainstorm), for simple tasks that don't need context prep, or for
  documenting completed work (use /scribe).
user-invocable: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Agent
  - Write
  - TodoWrite
---

# /prp — Prompt-Ready Packet Generator

Generate a self-contained task context document optimized for AI consumption. A PRP gives any Claude session everything it needs to execute a task — no codebase re-scanning needed.

## When to Use

- Handing off a task to a new session (context too large, session ending)
- Delegating complex subtasks to sub-agents
- Preparing context for `/orchestrate` on a well-scoped task
- Documenting a task for async execution

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

## Quality Rules

- **Completeness**: Someone with NO prior context should be able to execute the task from the PRP alone
- **Conciseness**: Include only relevant context — no filler, no "nice to know"
- **Accuracy**: Verify file paths exist, imports are correct, patterns are current
- **Actionability**: Every section should help the executor make progress, not just inform
- **No code dumps**: Reference files by path, don't paste full contents unless they're short and critical
