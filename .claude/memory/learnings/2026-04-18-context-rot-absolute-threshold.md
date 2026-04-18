---
date: 2026-04-18
type: best_practice
severity: medium
component: session
tags: [context-management, context-rot, compaction, token-efficiency]
summary: Anthropic confirms context rot begins at ~300-400k tokens on 1M context model (30-40%), not at 60-95% thresholds previously used. Proactive compact should trigger earlier than assumed.
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.8
maturity: draft
related: [2026-04-01-autocompact-threshold.md, 2026-04-14-compact-timing-60pct.md]
verify_check: "manual"
skill_scope: [compact, checkpoint, orchestrate]
---

## Context Rot Absolute Threshold

Previous learnings used relative thresholds (60% proactive, 70% env var, 95% autocompact). This adds the absolute number from Anthropic.

**Threshold**: ~300-400k tokens on 1M context. Highly task-dependent.

**Implication for STOPA**: 
- 300k/1M = 30%, 400k/1M = 40% — significantly earlier than the 60% proactive threshold
- For simple tasks (minimal tool calls), 60% is fine
- For heavy tool-call sessions (many file reads, long agent outputs), target 30-40%
- AUTOCOMPACT_PCT_OVERRIDE=70 (existing setting) is still a good safety net but may not prevent quality degradation in tool-heavy sessions

**How to apply**: In /orchestrate, when spawning deep-tier tasks, prefer subagents for any chunk >100k tokens of intermediate output — don't accumulate it in the parent session.

**Source**: Anthropic session management guide (2026-04-18).
