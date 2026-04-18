---
date: 2026-04-18
type: best_practice
severity: high
component: session
tags: [context-management, rewind, session-management, cc-feature]
summary: After a failed approach, use /rewind (Esc×2) to jump back to before the failure and re-prompt with learnings — cleaner than appending "that didn't work, try X" which adds noise without removing the failed reasoning.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.9
maturity: draft
verify_check: "manual"
skill_scope: [checkpoint, compact, orchestrate]
---

## Rewind > Correction

After a failed approach, the instinct is to type "that didn't work, try X." This appends the correction to a context that already contains the failed reasoning, file reads, and incorrect conclusions — it adds signal but keeps the noise.

**Better**: Use `/rewind` (double-tap Esc) to jump back to just after the file reads (before the failed attempt), then re-prompt with the learnings from the failure.

Example:
- Failed: "try approach A" → approach A fails → type "A doesn't work, try B"
- Better: rewind to after file reads → "Don't use A, foo module doesn't expose it — go straight to B"

**Companion pattern** — "summarize from here": ask Claude to produce a handoff message (learnings from failed approach) BEFORE rewinding. Then rewind, paste the summary as context. This transfers insight without carrying the failed reasoning.

**Source**: Anthropic session management guide (2026-04-18). Described as "#1 signal of good context management."

**How to apply**: In /checkpoint and /compact skill docs, add rewind as explicit option when approach failed rather than context merely long.
