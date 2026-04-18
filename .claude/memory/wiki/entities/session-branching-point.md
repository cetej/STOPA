---
name: Session Branching Point
type: concept
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [cc-session-management-1m-context]
tags: [context-management, session, decision-framework]
---

# Session Branching Point

> The decision point after every Claude Code turn: 5 options for what to do with the accumulated context.

## Key Facts

5 options after each turn (ref: sources/cc-session-management-1m-context.md):
1. **Continue** — send next message, context grows
2. **Rewind** (Esc×2) — jump back, drop messages after that point
3. **Clear** (/clear) — start fresh, you write the distilled brief
4. **Compact** (/compact) — lossy auto-summary, model chooses what matters; steer with `/compact focus on X, drop Y`
5. **Subagent** — delegate next chunk to isolated Agent with fresh context; only result returns

Decision heuristics:
- New task → /clear (or new session)
- Failed approach → /rewind to before the failed attempt
- Context > 60% → /compact proactively with direction hint
- Intermediate output not needed later → subagent (mental test: "tool output or conclusion?")
- Continuing related work → continue (e.g., docs after implementation)

## Relevance to STOPA

This 5-option model should inform /checkpoint, /compact, and /orchestrate skills — they currently don't frame the choice explicitly. A decision table in the checkpoint skill would help.

## Mentioned In

- [CC Session Management & 1M Context](../sources/cc-session-management-1m-context.md)
