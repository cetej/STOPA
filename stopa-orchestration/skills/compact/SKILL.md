---
name: compact
description: "Use when a long-running workflow accumulates large tool results or agent outputs that bloat context. Trigger on 'context is getting large', 'save and summarize results', 'compact context'. Do NOT use for small tasks with <3 tool results or when context is healthy."
argument-hint: "save-and-summarize <id> | save <id> | summarize <id> | load <id> | scratchpad | cleanup"
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Context Compaction — Save, Summarize, Reload

Manage context by saving large results to disk and keeping only lightweight summaries in the conversation. Inspired by Dexter AI's context compaction pattern.

## Core Principle

```
Large result → save to disk → Haiku summarizes → summary stays in context
Final synthesis → load full data from disk → rich answer
```

## Operations

Parse `$ARGUMENTS` to determine which operation to run:

### `save-and-summarize <id>` (primary interface)

The combined operation — use this by default.

1. **Identify content**: Take the content to compact. This is either:
   - The last large tool result in the conversation (50+ lines)
   - The last agent output
   - Content explicitly passed in the conversation

2. **Save to disk**:
   ```bash
   mkdir -p .claude/memory/intermediate
   ```
   Write to `.claude/memory/intermediate/<id>.json`:
   ```json
   {
     "id": "<id>",
     "savedAt": "<ISO 8601 timestamp>",
     "source": "<tool name, agent name, or 'manual'>",
     "summary": null,
     "fullContent": "<the complete result>"
   }
   ```

3. **Generate summary**: Spawn a Haiku sub-agent:
   ```
   Agent(model: "haiku", prompt: "
     Summarize this result in 1-2 factual sentences.
     Focus on: what was learned, what changed, key data points.
     Include specific numbers/filenames if present.

     Source: <source>
     Content: <fullContent — truncate to first 4000 chars if longer>

     Return ONLY the summary sentence(s), nothing else.
   ")
   ```

4. **Update JSON**: Write the Haiku summary to the `summary` field.

5. **Append to scratchpad**: Add a row to `.claude/memory/intermediate/scratchpad.md`:
   ```markdown
   | <next #> | <HH:MM> | <source> | <summary> |
   ```
   If scratchpad doesn't exist, create it with header:
   ```markdown
   # Scratchpad — Accumulated Context

   | # | Time | Source | Summary |
   |---|------|--------|---------|
   ```

6. **Return only the summary** to the caller. The full content is on disk.

### `save <id>`

Save without summarizing (for when you'll summarize later or content is already small).

Run only steps 1-2 from `save-and-summarize`.

### `summarize <id>`

Generate summary for an already-saved result.

1. Read `.claude/memory/intermediate/<id>.json`
2. If `summary` is already set, return it (don't re-summarize)
3. Run steps 3-6 from `save-and-summarize`

### `load <id>`

Reload full content for synthesis or detailed inspection.

1. Read `.claude/memory/intermediate/<id>.json`
2. Return the `fullContent` field
3. Use case: final synthesis step, debugging, or when summary wasn't enough

### `scratchpad`

Show accumulated work without loading full content.

1. Read `.claude/memory/intermediate/scratchpad.md`
2. If it doesn't exist, report "No scratchpad entries yet."
3. Return the table as-is

### `cleanup`

Delete all intermediate files.

1. Delete all files in `.claude/memory/intermediate/`
2. Report count of deleted files
3. Use at task close or when starting fresh

## Circuit Breakers

- **Scratchpad max 50 entries**: If scratchpad exceeds 50 rows, delete the oldest 25 rows (full data remains in JSON files). Log: "Scratchpad trimmed: oldest 25 entries archived."
- **Don't compact small results**: If content is <20 lines, skip — overhead of summarization exceeds benefit. Save directly if needed.
- **JSON file size**: If `fullContent` would exceed 100KB, truncate to first 100KB with note "[TRUNCATED at 100KB]"

## Usage Pattern for Other Skills

Any skill or workflow can use compaction:

```
1. When you receive a large result (50+ lines):
   → /compact save-and-summarize <unique-id>
   → Continue working with the returned summary

2. When you need full details for final synthesis:
   → /compact load <id>

3. To see what work has been done:
   → /compact scratchpad

4. At task close:
   → /compact cleanup
```

## When NOT to Compact

- Results under 20 lines (cheaper to keep in context)
- Data you need to reference verbatim in the next step
- Already-summarized agent status blocks
- Simple Grep/Glob results with few matches
