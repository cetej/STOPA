# Cost Gate (Pre-Execution ROI Check)

After decomposition is complete and waves are assigned, validate that the planned agent count has positive ROI. This is the final gate before committing resources (ref: arXiv:2603.12229 — actual speedup ≈ 75% of Amdahl's theoretical maximum due to coordination overhead).

```
From the subtask table, compute:
  T = total subtasks
  I = Wave 1 subtask count (independent)
  p = I / T
  n = planned agent count for this task (from tier)

  theoretical_speedup = 1 / ((1-p) + p/n)
  estimated_speedup = theoretical_speedup × 0.75   # empirical discount
  cost_multiplier = n × 1.15                        # 15% coordination overhead per agent
  roi = estimated_speedup / cost_multiplier

  IF roi < 0.5:
    WARN: "Planned {n} agents would cost {cost_multiplier:.1f}× for {estimated_speedup:.1f}× speedup (ROI={roi:.2f}).
    Recommend: reduce to {recommended_n} agents or single-agent execution."
    Offer user: proceed / downgrade

  Log to budget.md: "Cost gate: n={n}, p={p:.2f}, ROI={roi:.2f}, decision={proceed|downgrade}"
```

**Recommended agent count** (`recommended_n`): iterate n from 1 to planned, pick n with highest `roi`. Typically:
- p=0.9 → 4 agents optimal (ROI peaks ~0.59)
- p=0.5 → 2 agents optimal (ROI peaks ~0.63)
- p=0.2 → 1 agent optimal (any more destroys ROI)

**Rules:**
- Light tier: skip this check (1 agent, ROI is always 1.0)
- Farm tier: skip (p≈1.0 by definition, ROI is always positive)
- If user says "proceed" despite low ROI → respect the decision, log it
- Re-run this check if tier was auto-escalated during execution
