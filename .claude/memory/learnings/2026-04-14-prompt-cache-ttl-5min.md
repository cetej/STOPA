---
date: 2026-04-14
type: best_practice
severity: medium
component: session
tags: [tokens, cache, cost-optimization]
summary: Prompt cache TTL is 5 minutes. After 5min pause, next message reprocesses entire context at full cost. Compact or clear before stepping away.
source: external_research
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 1.0
maturity: draft
related: [2026-04-14-compact-timing-60pct.md, 2026-04-01-autocompact-threshold.md]
verify_check: "manual"
---

## Prompt Cache TTL = 5 Minutes

Claude Code uses prompt caching to avoid reprocessing unchanged context. The cache has a 5-minute timeout.

**Implication**: If you step away for >5 minutes, the next message reprocesses everything from scratch at full token cost. This explains "random usage spikes" after breaks.

**Mitigation**: Before stepping away, run `/compact` or `/checkpoint` + `/clear`. When returning after a break, start a fresh session with checkpoint resume rather than continuing a stale one.

**Note**: RTK's ScheduleWakeup already accounts for this — delays under 270s stay in cache, 300s+ pay the miss. This learning confirms the same principle applies to human pauses.

**Source**: Token management vlog (2026-04-14), consistent with Anthropic prompt caching documentation.
