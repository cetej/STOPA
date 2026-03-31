---
name: compact
description: Use when context is bloated with large tool results or agent outputs. Trigger on compact, save results, context too large. Not for small tasks.
argument-hint: "save-and-summarize <id> | save <id> | summarize <id> | load <id> | scratchpad | cleanup"
tags: [session, memory]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
effort: medium
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
     "agentRole": "<scout | researcher | implementer | reviewer | null>",
     "status": "<complete | partial | failed>",
     "summary": null,
     "outputs": {
       "files_changed": [],
       "decisions_made": [],
       "issues_found": [],
       "needs_followup": []
     },
     "fullContent": "<the complete result>"
   }
   ```

   **Field rules:**
   - `agentRole`: set when result comes from an orchestrated agent; `null` for direct tool results
   - `status`: `complete` = agent finished successfully; `partial` = useful output but incomplete; `failed` = error or no useful output
   - `outputs.files_changed`: list of file paths the agent modified (empty for read-only agents)
   - `outputs.decisions_made`: key decisions made during execution (1-liner each)
   - `outputs.issues_found`: problems discovered (for downstream agents/critic)
   - `outputs.needs_followup`: explicit handoff items for next wave agents
   - When saving direct tool results (not agent outputs), set `agentRole: null`, `status: "complete"`, and leave `outputs` arrays empty

3. **Generate summary**: Spawn a Haiku sub-agent:
   ```
   Agent(model: "haiku", prompt: "
     Compress this tool/agent result into a factual summary (2-4 sentences max).

     PRESERVE VERBATIM (never paraphrase these):
     - File paths and line numbers
     - Function/class/variable names
     - Error messages and stack traces
     - Numeric values (counts, sizes, scores)
     - Decision outcomes (what was chosen and why)
     - Status codes and flags

     OMIT:
     - Repetitive grep/glob matches (state count + first example instead)
     - Raw diff hunks (state files changed + nature of change instead)
     - Boilerplate tool output formatting

     Content type: <type — see Smart Compaction Rules>
     Source: <source>
     Content: <fullContent — truncate to first 4000 chars if longer>

     Return ONLY the compressed summary, nothing else.
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

## Smart Compaction Rules

Before summarizing, classify the content type and apply type-specific rules:

| Content Type | Action | Reason |
|-------------|--------|--------|
| Grep/Glob results (>20 matches) | Compact: keep count + first 3 examples | Bulk is recoverable via re-run |
| Agent status/report | Keep as-is (don't compact) | Already summarized by the agent |
| Code diffs (>50 lines) | Compact: files changed + nature of change | Full diff preserved on disk |
| Error output / stack traces | Keep full error message + trace | Critical for debugging |
| Decisions / plans / architecture notes | Keep as-is (don't compact) | Context-bearing, not bulk data |
| JSON/data dumps | Compact: schema + row count + 1 sample | Structure matters more than raw data |

In `save-and-summarize`, pass the detected content type to the Haiku prompt:
`"Content type: <type>. Apply preservation rules accordingly."`

This ensures Haiku knows whether to preserve detail (errors, decisions) or aggressively compress (grep bulk, data dumps).

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

## Process

1. Identify large tool results and agent outputs in context
2. Save critical results to disk files
3. Summarize remaining context with Haiku
4. Report what was compacted and where files were saved

## Rules

1. Never discard results without saving to disk first
2. Always report what was compacted and file locations
3. Log compaction pattern to `.claude/memory/learnings/<date>-<desc>.md` with YAML frontmatter if discovered

## Error Handling

- **ID already exists**: append `-v2`, `-v3` etc. to avoid overwriting
- **Haiku agent returns empty**: use placeholder `[No summary generated — content preserved in JSON]`
- **File not found in `load`**: list available IDs from `.claude/memory/intermediate/` directory
- **Content too small (<20 lines)**: skip with message "Content too small to compact"
