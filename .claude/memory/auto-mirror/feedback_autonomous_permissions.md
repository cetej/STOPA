---
name: Autonomous permissions v3
description: User wants minimal approval friction — auto-approve most ops, ask only for irreversible/external-facing actions
type: feedback
---

Permission hook v3.0: auto-approve GitHub write (push, PR, issue, comment), Chrome interaction, Playwright, Telegram reply, Gmail drafts, Google Drive read.

**Why:** User finds step-by-step approval annoying and context-breaking. Most operations are reversible (git revert, delete PR) or local-only.

**How to apply:** Only ask for truly irreversible or externally-visible actions: GitHub merge/fork, Gmail send, Calendar create/update/delete, file uploads to external services. Everything else flows autonomously.
