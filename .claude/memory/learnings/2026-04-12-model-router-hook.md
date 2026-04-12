---
date: 2026-04-12
type: architecture
severity: high
component: hook
tags: [model-selection, orchestration, cost-optimization, automation]
summary: Created model-router.py PreToolUse hook and model-perf-tracker.py PostToolUse hook. Router analyzes Agent prompts for model signals (file count, keywords, failure context) and recommends optimal model via additionalContext. Tracker records per-model success rates and auto-tunes haiku-first threshold.
source: auto_pattern
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.7
skill_scope: [orchestrate]
verify_check: "Glob('.claude/hooks/model-router.py') → 1+ matches"
---

## Model Router + Performance Tracker Hooks

**Problem:** STOPA's TARo per-subtask model routing (SKILL.md lines 652-695) is purely instructional — depends on orchestrator reading and following rules. No harness-level enforcement.

**Solution:** Two hooks working in tandem:

1. **model-router.py** (PreToolUse, matcher: Agent):
   - Extracts WRITE manifest file count, keyword signals, failure context
   - 0-1 files → haiku, 2-5 → sonnet, 6+ → opus
   - Security/auth/payment keywords → opus override
   - FAILED context → upgrade +1 tier
   - Returns additionalContext recommendation (doesn't block)
   - Respects explicit model (only warns on 2+ tier gap)

2. **model-perf-tracker.py** (PostToolUse, matcher: Agent):
   - Classifies subtask type from prompt
   - Extracts success/failure from agent output status block
   - Updates model-routing.json with per-model success rates
   - Auto-tunes haiku_first_threshold (3.0-4.0 range) based on haiku success rate

**State:** `.claude/memory/optstate/model-routing.json` — cross-session performance data.

**Limitation:** PreToolUse hooks CANNOT modify tool_input parameters. They can only advise via additionalContext. The orchestrator still decides.
