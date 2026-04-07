---
name: Whispering Pattern
type: concept
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [claude-subconscious-research]
tags: [hooks, memory, session, context-injection]
---
# Whispering Pattern

> Technique for injecting background agent guidance into Claude Code sessions via stdout from a UserPromptSubmit hook — prepended to user prompt context before Claude processes each message.

## Key Facts

- Mechanism: hook writes guidance to stdout; Claude Code reads hook stdout and prepends to user prompt context (ref: sources/claude-subconscious-research.md)
- Three modes: `whisper` (default, agent messages only), `full` (full memory blocks on first prompt then diffs), `off` (ref: sources/claude-subconscious-research.md)
- One-step lag: guidance prepared from previous interaction's transcript (ref: sources/claude-subconscious-research.md)
- Predecessor (pre-v1.3.0): writing to CLAUDE.md — caused 49K+ char token bloat (ref: sources/claude-subconscious-research.md)
- Operates on UserPromptSubmit + PreToolUse hooks for mid-workflow updates (ref: sources/claude-subconscious-research.md)

## Relevance to STOPA

Reference pattern for STOPA hook design. Stdout injection is the correct delivery mechanism for hook-based context; CLAUDE.md append causes token bloat. If STOPA ever implements a background context agent, this pattern is the baseline.

## Mentioned In

- [Claude Subconscious — Technical Architecture Deep Dive](../sources/claude-subconscious-research.md)
