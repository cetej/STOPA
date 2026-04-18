---
name: Rewind
type: tool
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [cc-session-management-1m-context]
tags: [context-management, session, cc-feature]
---

# Rewind

> Claude Code slash command (Esc×2 or /rewind) that jumps back to any previous message and drops all subsequent messages from context.

## Key Facts

- Invocation: double-tap Esc or `/rewind` in Claude Code (ref: sources/cc-session-management-1m-context.md)
- Effect: all messages after the rewind point are dropped from context — not moved, not summarized, deleted
- Primary use case: approach failed → rewind to just after file reads → re-prompt with learnings. Better than appending "that didn't work, try X" (which adds noise without removing the failed reasoning)
- Companion pattern: "summarize from here" — ask Claude to produce a handoff message before rewinding (message from future-self to past-self), then rewind and paste as context
- Best signal of good context management according to Anthropic (ref: sources/cc-session-management-1m-context.md)

## Relevance to STOPA

Rewind is the surgical alternative to compact/clear when only part of the session needs to be dropped. STOPA /checkpoint and /compact don't currently document rewind as an option — it should be in the session branching point decision tree.

## Mentioned In

- [CC Session Management & 1M Context](../sources/cc-session-management-1m-context.md)
