---
date: 2026-04-08
type: best_practice
severity: high
component: skill
tags: [skill-design, validation, prompt-quality, critic, hardstop]
summary: "Structured numbered validation rules with explicit error/warning tiers, executed by the LLM itself, with hard-stop before output delivery — stronger than advisory self-check. Python scripts decoupled to CI/CD only."
source: external_research
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.7
verify_check: "manual"
---

# LLM-Native Validation — Hard-Stop Before Delivery

## Context

From Seedance 2.0 Shot Design skill (v1.8.1+). Originally used `validate_prompt.py` (Python). After ClawHub security platform flagged Python execution patterns, refactored to LLM-native 7-rule checklist. Python script retained for developer/CI use only.

## Pattern

```
Step 4: Mandatory Validation (CANNOT BE SKIPPED)
- Rule ①: Length check (hard limit)
- Rule ②: Temporal logic check (timestamp coverage)
- Rule ③: Professional terminology presence
- Rule ④: Filler word hard-block (❌ error, not warning)
- Rule ⑤: Asset reference limits
- Rule ⑥: Style/optical conflict matrix
- Rule ⑦: Platform-specific term disambiguation

If ANY ❌ error → rewrite prompt, re-validate, loop until all pass.
Prompt with ❌ error MUST NOT be shown to user.
```

## Key Design Choices

1. **Numbered rules** — agent can't skip individually
2. **Tiered severity** — ❌ error (rewrite required) vs ⚠️ warning (advisory)
3. **Hard delivery gate** — failed validation = output suppressed, not just flagged
4. **Anti-rationalization defense** in skill body: "Skipping this step = delivering defective product"

## Application to STOPA

`/critic` currently returns PASS/FAIL but is advisory. `/klip` has no validation layer.

Consider adding LLM-native validation gate to `/klip`:
- Rule 1: prompt length 60-200 words
- Rule 2: at least 1 camera movement term
- Rule 3: no filler words (masterpiece/ultra-HD/8K alone)
- Rule 4: no style conflicts (photorealistic + cartoon, etc.)

**Why:** Hard-stop gates prevent low-quality outputs from reaching the API and wasting credits. More reliable than advisory self-checks which agents rationalize away.
