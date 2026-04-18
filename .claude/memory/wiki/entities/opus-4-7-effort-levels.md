---
name: Opus 4.7 Effort Levels
type: concept
first_seen: 2026-04-18
last_updated: 2026-04-18
sources: [claude-opus-4-7-best-practices]
tags: [model, effort, thinking, claude-code, token-efficiency]
---

# Opus 4.7 Effort Levels

> The effort level system for Claude Opus 4.7 in Claude Code, where `xhigh` is the recommended default and `max` shows diminishing returns.

## Key Facts

- Default effort level is `xhigh` — best balance of autonomy and intelligence for most coding/agentic tasks (ref: sources/claude-opus-4-7-best-practices.md)
- `max` effort shows diminishing returns and is more prone to overthinking (ref: sources/claude-opus-4-7-best-practices.md)
- Opus 4.7 uses **adaptive thinking** (optional per step) rather than fixed thinking budgets (ref: sources/claude-opus-4-7-best-practices.md)
- Response length automatically matches task complexity — no longer needs explicit length steering (ref: sources/claude-opus-4-7-best-practices.md)
- More judicious subagent spawning than prior Opus versions (ref: sources/claude-opus-4-7-best-practices.md)
- Reduced tool usage in favor of reasoning compared to prior models (ref: sources/claude-opus-4-7-best-practices.md)

## Relevance to STOPA

STOPA's orchestration tiers and model selection rules should use `xhigh` as default for Opus 4.7 tasks; `max` is not worth the overhead. Adaptive thinking changes how thinking budget guidance applies — no longer set a fixed budget.

## Mentioned In

- [Best Practices for Using Claude Opus 4.7 with Claude Code](../sources/claude-opus-4-7-best-practices.md)
