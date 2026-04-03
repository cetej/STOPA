# Adaptive Difficulty Calibration (Agent0 curriculum pattern)

After each batch ASSESS, calibrate difficulty based on performance. This creates co-evolutionary pressure: easy success → harder challenges, consistent failure → relaxed constraints.

**Compute keep_rate**: `keeps_in_batch / iterations_in_batch`

| keep_rate | Decision | Action |
|-----------|----------|--------|
| >50% | **ESCALATE** | Tighten target by 10% OR add secondary guard metric (LOC, cyclomatic complexity) |
| 20-50% | **HOLD** | Continue as-is, no calibration needed |
| <20% | **SIMPLIFY** | Widen target tolerance by 10% OR remove secondary metrics |

**ESCALATE actions** (pick the most relevant):
- Tighten numeric target: `new_target = current_target * 1.1` (if higher-is-better) or `* 0.9` (lower-is-better)
- Add complexity guard: reject iterations where target file LOC grows >20% from baseline
- Require monotonic improvement: discard iterations that don't beat the PREVIOUS iteration (not just best-so-far)

**SIMPLIFY actions** (pick the most relevant):
- Widen target tolerance: `new_target = current_target * 0.9` (higher-is-better) or `* 1.1` (lower-is-better)
- Remove secondary guard metrics added by prior ESCALATE
- Allow bigger hypothesis deltas (relax single-file mutation to 2 files if needed)

**Caps:**
- Max 2 ESCALATEs per run — after that, HOLD regardless of keep_rate
- Max 1 SIMPLIFY per run — if already simplified and still <20%, let ASSESS handle (PIVOT/ABORT)
- SIMPLIFY cannot undo more than 1 prior ESCALATE level

**Difficulty tracking:**
- `difficulty_level` starts at 1.0, +0.1 per ESCALATE, -0.1 per SIMPLIFY
- Log to TSV: add `difficulty_level` to each iteration row after calibration
- Log calibration decision to Run Diary: `[CALIBRATE] keep_rate=X%, decision=ESCALATE|HOLD|SIMPLIFY, difficulty=Y`

**Interaction with ASSESS decisions:**
- If ASSESS = PROCEED or ABORT → skip calibration (loop is ending)
- If ASSESS = REFINE → calibration runs, but only HOLD or ESCALATE (never SIMPLIFY during refinement)
- If ASSESS = PIVOT → reset difficulty_level to 1.0 (fresh start with new approach)
