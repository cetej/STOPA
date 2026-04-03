# Reward Hacking Detection

Track secondary signals alongside the primary metric. Check after every "keep" iteration:

## Divergence signals

| Signal | Check | Threshold | How to detect |
|--------|-------|-----------|---------------|
| **Complexity creep** | `wc -l` of target files | >30% growth from baseline | `baseline_loc` recorded in Phase 0, compare each iteration |
| **Churn cycling** | Last 3 iterations alternate keep→revert→keep on similar changes | 3 consecutive flip-flops | Parse TSV for status pattern + `git diff` similarity |
| **Metric spike** | Delta suddenly >3x the running average delta | Anomalous jump | Compare current delta to mean of prior positive deltas |

## Overfitting guard (AutoAgent-inspired)

After every "keep", before proceeding, ask: **"If this exact eval case disappeared, would this change still be a worthwhile improvement?"**
- If YES -> genuine improvement, proceed
- If NO -> flag as potential overfitting, log `divergence` status, warn user

## On divergence detected

1. **Pause the loop** -- do not auto-continue
2. Print warning with evidence:
   ```
   WARNING: REWARD HACKING SUSPECTED
   Signal: <which signal triggered>
   Evidence: <e.g., "LOC grew 85->142 (+67%) while metric improved only +0.3">
   Recommendation: inspect last 3 commits manually
   ```
3. Ask user: "Continue, rollback last N, or stop?"
4. Log `divergence` as TSV status for the flagged iteration
