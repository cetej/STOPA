---
date: 2026-04-14
type: best_practice
severity: medium
component: session
tags: [tokens, compact, context-management]
summary: Compact at 60% context capacity, not at autocompact's 95%. After 3-4 compacts, quality degrades — do /clear + session summary + fresh start instead.
source: external_research
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 0.9
maturity: draft
related: [2026-04-01-autocompact-threshold.md, 2026-04-14-prompt-cache-ttl-5min.md]
verify_check: "manual"
---

## Compact Timing Rule

Autocompact triggers at ~95% context capacity, but by then output quality is already degraded ("lost in the middle" phenomenon — model attends to beginning and end, middle gets ignored).

**Rule**: Run `/compact` proactively at ~60% capacity. After 3-4 compacts in a row, switch to `/clear` + session summary + fresh start.

**Why**: Each compact loses some context fidelity. Compounding information loss after 3-4 rounds makes continuation less productive than a clean restart with a good summary.

**Source**: Token management vlog analysis (2026-04-14), confirmed by observed session behavior.
