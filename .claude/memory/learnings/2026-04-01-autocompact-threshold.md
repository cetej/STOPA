---
date: 2026-04-01
type: best_practice
severity: medium
component: orchestration
tags: [context-management, compaction, long-sessions]
summary: Setting CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70 triggers context compaction earlier (default ~95%), preventing quality degradation in long sessions. Verified from CC source leak.
source: external_research
uses: 0
harmful_uses: 0
confidence: 0.6
verify_check: "Grep('AUTOCOMPACT_PCT_OVERRIDE', path='~/.claude/settings.json') → 1+ matches"
---

## AUTOCOMPACT_PCT_OVERRIDE=70

Default CC compaction threshold is ~95% of context window. This means compaction fires
only when the window is nearly full, by which point output quality has already degraded.

Setting to 70% triggers compaction earlier — smaller but more frequent summarization cycles.

**Source**: CC source leak analysis (cli.js.map, 2026-03-31). Corroborated by multiple
independent analyses of the leaked TypeScript source.

**4-tier compaction model**:
1. Snip — historical truncation preserving prompt cache
2. Microcompaction — time/size clearing of tool results
3. Full compaction — conversation summarization (controlled by this threshold)
4. Reactive collapse — emergency on API 413

**How to apply**: Already set in `~/.claude/settings.json` env section.
Monitor long session quality over next week to confirm improvement.
Revert to default if early compaction causes loss of important recent context.
