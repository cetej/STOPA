---
source: auto-correction
times_corrected: 2
---

# Context

Add invariant I10 to STOPA `commit-invariants.md` per AHE Pattern 8 (LLM Config Hands-Off Rule).

**Context**: AHE pilot report at `outputs/ahe-pilot-2026-04-30.md` Pattern 8. AHE explicitly states "LLM config changes consistently cause broad, hard-to-diagnose regressions" and bans modifying model/temperature/reasoning_effort during evolution. STOPA has invariants I1-I9 but no equivalent.

**AHE quote** (`_ahe-pilot/agentic-harness-engineering/agents/evolve_agent/evolve_prompt.md` lines 229-241)
