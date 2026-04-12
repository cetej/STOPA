---
name: Atomic Skills Paper
description: arXiv:2604.05013 — 5 atomic coding skills (localize, edit, test-gen, reproduce, review) with joint RL yield +18.7%; led to /reproduce and /generate-tests skills
type: reference
---

## Scaling Coding Agents via Atomic Skills (Ma et al., 2026)

**Paper:** arXiv:2604.05013
**Core idea:** Train on 5 atomic skills instead of composite benchmarks → +18.7% average, generalizes to unseen tasks.

**5 atomic skills:**
1. Code Localization → `/scout` (full coverage)
2. Code Editing → embedded in orchestrate agent delegation (deliberate)
3. Unit Test Generation → **NEW: `/generate-tests`** (+31.5% gain — largest improvement)
4. Issue Reproduction → **NEW: `/reproduce`**
5. Code Review → `/critic` (superset)

**Implementation in STOPA (2026-04-11):**
- Created `/reproduce` skill — standalone failing test/script, then stop
- Created `/generate-tests` skill — pure test gen for existing code
- Added atomic skill routing to orchestrate Phase 3 step 3a
- Full bugfix pipeline: `/reproduce` → `/fix-issue` → `/generate-tests` → `/critic`
- Pre-refactor safety net: `/generate-tests` → refactor → re-run tests

**Key method:** GRPO (Group Relative Policy Optimization) — within-group reward normalization handles different reward scales across skills. Single-task RL underperforms joint training.

**Why:** Isolated test generation had the largest gain (+31.5%) — validating that decoupling test writing from implementation is high-value.
