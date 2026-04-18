---
date: 2026-04-18
type: architecture
severity: medium
component: orchestration
tags: [context-management, compaction, memory, pipeline, hooks]
summary: CC uses 5 graduated compression layers (Budget Reduction → Snip → Microcompact → Context Collapse → Auto-Compact), each targeting a different pressure type. Apply lightest first, heaviest last. STOPA /compact jumps straight to aggressive summarization — adopt progressive strategy.
source: external_research
uses: 1
successful_uses: 0
harmful_uses: 0
confidence: 0.65
maturity: draft
skill_scope: [compact, checkpoint, orchestrate]
verify_check: manual
---

## Detail

From arXiv:2604.14228 (Dive into Claude Code). CC's 5-layer compaction:
1. **Budget Reduction** — per-message size limits, replaces oversized content with references
2. **Snip** — removes older history segments when token pressure first appears
3. **Microcompact** — cache-aware fine-grained compression
4. **Context Collapse** — read-time projection over history (non-destructive to storage)
5. **Auto-Compact** — model-generated summary, triggered only after layers 1-4 insufficient

Key principle: no single strategy addresses all pressure types. Each layer has a specific trigger condition and cost.

**STOPA gap**: `/compact` currently jumps to model-summary (layer 5) without attempting layers 2-4 first. This wastes tokens when lighter compression would suffice.

**Why:** Multi-layer approach allows reversible, targeted compression before expensive model summarization. Avoids destroying useful context prematurely.

**How to apply:** In `/compact` skill, add pre-check: if context < 70% window, try snip-style (remove oldest tool results > 2K tokens) before triggering full Auto-Compact. Layer 1 (size limits) is already partially implemented via `/checkpoint` summary pattern.
