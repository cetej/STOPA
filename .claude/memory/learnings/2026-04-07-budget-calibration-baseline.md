---
date: 2026-04-07
type: architecture
severity: medium
component: orchestration
tags: [budget, calibration, cost-tracking, measurement]
summary: "Budget calibration baseline: 7 historical tasks analyzed, no actual cost data available. Proposed measurement protocol using ccusage + session tagging."
source: auto_pattern
uses: 1
harmful_uses: 0
successful_uses: 0
confidence: 0.9
supersedes: 2026-04-04-gap-budget-calibration.md
verify_check: "Grep('Measurement Protocol', path='.claude/memory/learnings/2026-04-07-budget-calibration-baseline.md') → 1+ matches"
---

## Budget Calibration Baseline

### Observed Data (from budget.md)

7 historical tasks with tier assignments but NO actual API cost data:

| Task | Tier | Agents | Estimated Cost | Actual | Delta |
|------|------|--------|---------------|--------|-------|
| Initial System Build | deep | 7 | — | ? | ? |
| Karpathy AutoResearch | standard | 3/4 | — | ? | ? |
| Attention Residuals | standard | 4/4 | — | ? | ? |
| Czech Corrector audit | standard | 4/4 | — | ? | ? |
| Hook grep portability | light | 1 | — | ? | ? |
| Hook injection fix | light | 1 | — | ? | ? |
| Plugin sync (43 cmds) | light | 1 | — | ? | ? |

Only 1 task (Phase 1 Hygiene, 2026-03-24) has estimated costs: $1.00 for 44 agent spawns.

### Key Finding

Budget tracking is estimate-only — no actual cost comparison exists. The system cannot self-correct tier assignments because there is no feedback loop.

### Measurement Protocol

1. **Install ccusage**: `npm install -g ccusage` — parses Claude Code JSONL logs for actual token usage and cost
2. **Per-session tagging**: Add `task_id` field to budget.md event log entries
3. **Post-session comparison**: After each orchestrated task, run `ccusage --last-session` and compare with budget.md estimate
4. **Calibration factor**: `actual_cost / estimated_cost` per tier. After 10+ data points per tier, compute mean calibration factor
5. **Threshold adjustment**: If calibration factor consistently > 1.5 or < 0.5 for a tier, adjust tier cost assumptions

### Implementation Priority

Low — system works fine without calibration. Useful for optimization but not blocking. Install ccusage when convenient, start collecting data points.
