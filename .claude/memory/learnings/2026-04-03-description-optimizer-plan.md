---
date: 2026-04-03
type: architecture
severity: high
component: skill
tags: [skill, description, evaluation, optimization]
summary: Plan to integrate Anthropic's description optimization pipeline into STOPA — automated trigger rate measurement with train/test split to prevent overfitting.
source: external_research
uses: 1
harmful_uses: 0
confidence: 0.7
verify_check: "manual"
---

## Description Optimizer Integration Plan

### What Anthropic has
`scripts/run_loop.py` — automated pipeline:
1. Generate 20 eval queries (10 should-trigger, 10 should-not-trigger)
2. Split 60/40 train/test
3. Each query runs 3x against `claude -p` to measure trigger rate
4. Claude proposes description improvements
5. Iterate max 5 times, select best by TEST score (not train — prevents overfitting)
6. Output: `best_description` + before/after scores

### Integration options for STOPA

**Option A: Adopt Anthropic's run_loop.py directly**
- Pro: battle-tested, already works
- Con: requires `claude -p` CLI, doesn't understand STOPA's negative trigger convention

**Option B: Custom STOPA description optimizer**
- Build on Anthropic's approach but add:
  - Negative trigger testing (should NOT fire for adjacent skills)
  - Conflict pair awareness (evolve↔self-evolve, critic↔pr-review etc.)
  - Integration with existing /self-evolve skill
- Input: skill name + list of known conflict pairs
- Output: optimized description with measured trigger/non-trigger rates

**Option C: Add to /self-evolve as a phase**
- /self-evolve already does adversarial co-evolution
- Add "Phase 0: Description optimization" before eval case generation
- Reuse existing infrastructure

### Recommended: Option B first, then merge into /self-evolve

### Next steps
1. Copy Anthropic's run_loop.py and adapt for STOPA conventions
2. Build conflict pair registry (from the audit: 12 known pairs)
3. Add to /skill-generator as an optional phase after skill creation
4. Future: automated periodic sweep of all descriptions
