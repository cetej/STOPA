---
name: handoff
description: Use when capturing findings from completed sessions (especially remote/mobile) into persistent memory. Trigger on 'handoff', 'zapiš z session', 'capture findings'. Do NOT use for active session checkpoints (/checkpoint).
argument-hint: <paste session output, summary, or describe what was done>
tags: [session, memory]
phase: ship
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

<!-- CACHE_BOUNDARY -->

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

### Step 4b: Optional Managed Memory Bridge Dual-Write

After each successful learning/decision file write in Step 4, ALSO call `mcp__stopa-memory__memstore_write_memory(path=<remapped>, content=<same>)` IF that tool is in your available tool list. Skip silently if not — bridge is opt-in.

**Path remap**: strip `.claude/memory/` prefix. `.claude/memory/learnings/2026-04-25-foo.md` → `/learnings/2026-04-25-foo.md`.

**Failure handling**: log `[memstore] WARN: <reason>` to stderr and continue. Local write is canonical.

Skip dual-write for: state.md (ephemeral backlog), files >100 kB. Full pattern and rationale: `stopa-memory-mcp/INTEGRATION.md`. Tracking: STOPA#26.

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

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll save everything in one big learning file since it all came from the same session" | Unrelated findings in one file create retrieval noise; future grep by component or tag returns false matches | Create one file per distinct topic; each file maps to one component or decision domain |
| "I'll skip the duplicate check since this is fresh information from a different session" | Sessions often rediscover the same patterns; duplicates dilute confidence scoring and pollute grep results | Always grep `learnings/` for matching component + tags before writing a new file |
| "The session summary is clear enough, I don't need to extract specific knowledge units" | Narrative summaries are not machine-retrievable; only structured YAML learnings are useful to future sessions | Parse the input and produce at least one typed knowledge unit (finding, decision, or action item) |
| "I'll rewrite the existing learning file to include the new info" | Overwriting destroys the original's source and date provenance; future sessions cannot trace the history | Merge by appending a dated update section inside the existing file, preserving original content |
| "The findings are probably already in decisions.md so I won't bother checking" | Assuming coverage leads to both gaps (missing new info) and silent staleness (old info not updated) | Read the target files first; then write only what's genuinely new or update what's changed |

## Rules

1. **Append, never overwrite** — handoff adds to memory, never replaces
2. **Preserve specifics** — numbers, names, URLs, dates must survive verbatim
3. **Source attribution** — every entry notes it came from handoff + session context
4. **Czech or English** — match the language of the input
5. **One file per distinct topic** — don't cram unrelated findings into one learning
6. **Read before write** — always read target files first to avoid duplication
