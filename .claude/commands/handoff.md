---
name: handoff
description: Use when capturing findings from completed sessions (especially remote/mobile) into persistent memory. Trigger on 'handoff', 'zapiš z session', 'capture findings'. Do NOT use for active session checkpoints (/checkpoint).
argument-hint: <paste session output, summary, or describe what was done>
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
model: haiku
effort: low
maxTurns: 10
disallowedTools: Agent, Bash
---

# Handoff — Cross-Session Knowledge Capture

Capture findings, decisions, and learnings from completed sessions into persistent memory files. Unlike `/checkpoint` (which overwrites a single file for session continuity), handoff **appends** to durable storage that survives across sessions.

## When to Use

- After a mobile/remote session that analyzed something
- When pasting findings from another conversation
- When multiple sessions produced results that need consolidation
- End of any session with insights worth preserving beyond checkpoint

## When NOT to Use

- Mid-session progress saving → use `/checkpoint`
- Preparing context for a future task → use `/prp`
- Recording a single decision or learning → use `/scribe`

## Process

### Step 1: Parse Input

Read `$ARGUMENTS`. The input is one of:
- **Pasted text** — session output, summary, or findings copied by user
- **Description** — user describes what sessions covered ("analyzoval jsem 3 studie o X")
- **Multiple items** — user lists several session results

If input is vague (< 10 words, no specifics), ask ONE clarifying question:
> "Co bylo hlavním zjistěním? / What were the key findings?"

### Step 2: Extract Knowledge Units

From the input, identify distinct knowledge units. Each unit is one of:

| Type | Goes to | Format |
|------|---------|--------|
| **Finding/Learning** | `learnings/<date>-<slug>.md` | YAML frontmatter + body |
| **Decision** | `decisions.md` (append) | Decision entry format |
| **Reference** | `decisions.md` or inline in learning | Link/pointer to source |
| **Action item** | `state.md` (append to backlog) | One-liner with context |

Most handoff inputs produce **1-3 learnings** and optionally a decision or action item.

### Step 3: Check for Duplicates

Before writing each unit:
1. Grep `learnings/` for matching component + tags
2. If similar learning exists, **update it** (merge new info) instead of creating duplicate
3. If a decision supersedes an older one, note the supersession in the new entry

### Step 4: Write to Persistent Storage

#### Learnings (primary output)

Create files in `.claude/memory/learnings/` using scribe format:

**Filename**: `<YYYY-MM-DD>-<short-slug>.md`

```markdown
---
date: YYYY-MM-DD
type: best_practice | architecture | workflow | bug_fix | anti_pattern
severity: critical | high | medium | low
component: <relevant area>
tags: [tag1, tag2, tag3]
source: handoff
---

## Zjisteni
What was found or learned.

## Kontext
Where this came from (which session, what was analyzed).

## Aplikace
How to apply this in future work.
```

The `source: handoff` tag distinguishes these from in-session learnings.

#### Decisions (if applicable)

Append to `.claude/memory/decisions.md`:

```markdown
### YYYY-MM-DD — <Decision Title>
- **Context**: <what was analyzed/discussed>
- **Decision**: <what was decided>
- **Rationale**: <why>
- **Source**: handoff from remote session
```

#### Action Items (if applicable)

Append to `.claude/memory/state.md` under Backlog:

```markdown
- [ ] <action item> (from handoff YYYY-MM-DD)
```

### Step 5: Report

Output a summary:

```
## Handoff Complete

Captured from: <brief description of source session(s)>

### Written:
- N learnings → learnings/<filenames>
- N decisions → decisions.md
- N action items → state.md

### Key points preserved:
- <bullet 1>
- <bullet 2>
```

## Batch Mode

When user describes multiple sessions at once:

1. Process each session's findings as a separate batch
2. Number the sessions in output: "Session 1: ..., Session 2: ..."
3. Cross-reference if findings overlap (merge, don't duplicate)
4. Single summary report at the end covering all sessions

## Error Handling

- **Input too vague**: Ask one clarifying question, then proceed with what's available
- **Duplicate learning exists**: Merge new information into existing file, note update date
- **decisions.md near limit (>10 entries)**: Warn user, suggest `/scribe maintenance`
- **Conflicting findings across sessions**: Record both with note about the conflict

## Rules

1. **Append, never overwrite** — handoff adds to memory, never replaces
2. **Preserve specifics** — numbers, names, URLs, dates must survive verbatim
3. **Source attribution** — every entry notes it came from handoff + session context
4. **Czech or English** — match the language of the input
5. **One file per distinct topic** — don't cram unrelated findings into one learning
6. **Read before write** — always read target files first to avoid duplication
