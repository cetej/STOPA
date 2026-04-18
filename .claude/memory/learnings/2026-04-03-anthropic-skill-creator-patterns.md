---
date: 2026-04-03
type: best_practice
severity: high
component: skill
tags: [skill, description, triggers, evaluation]
summary: Anthropic official skill-creator defines 3-level progressive disclosure, 500-line SKILL.md limit, pushy descriptions, ALWAYS/NEVER yellow flag, and full eval+description optimization pipeline. STOPA gaps identified.
source: external_research
maturity: draft
uses: 0
harmful_uses: 0
confidence: 0.8
verify_check: "manual"
related: [2026-04-03-description-optimizer-plan.md]
successful_uses: 0
---

## Anthropic skill-creator patterns (from github.com/anthropics/skills)

### Verified patterns
1. **3-level progressive disclosure**: metadata (name+description, ~100 words, always in context) → SKILL.md body (on trigger) → bundled resources (on demand). STOPA partially implements via skills/commands split.
2. **500-line SKILL.md limit**: If approaching, extract to `references/` with pointers. STOPA violators: orchestrate (1476), critic (637), autoloop (600), autoresearch (599), eval (516).
3. **"Pushy" descriptions**: Anthropic says Claude undertriggers by default — descriptions should list specific contexts/edge cases. STOPA already does this with "Use when...Do NOT use..." but lacks edge-case listing.
4. **ALWAYS/NEVER yellow flag**: "If you write ALWAYS/NEVER in caps, that's a yellow flag — reframe and explain reasoning instead." STOPA has 50+ instances across skills; most could be reframed.
5. **Description optimizer**: `run_loop.py` with train/test split (60/40), 5 iterations, measures trigger rate per query (3x for reliability). Major STOPA gap.
6. **Eval harness for skills**: Spawn with-skill AND baseline runs simultaneously, grade with assertions, benchmark with mean±stddev. STOPA has /eval for harness traces but not for skill descriptions.

### Key differences (STOPA advantages)
- Shared memory system (learnings, decisions, state) — Anthropic has none
- Fleet-level audit (improve-all, M5 rubric) — Anthropic treats skills individually
- Negative trigger exclusions (Do NOT use for...) — Anthropic doesn't formalize this

### Action items from audit
- Refactor orchestrate into SKILL.md + references/ (1476 → <500 lines)
- Audit and reframe ALWAYS/NEVER patterns (50+ instances)
- Integrate description optimization loop from Anthropic's run_loop.py
- Add 500-line check to verify-sweep.py hook
