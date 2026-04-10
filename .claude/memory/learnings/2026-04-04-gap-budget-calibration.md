---
date: 2026-04-04
type: architecture
severity: medium
component: orchestration
tags: [budget, calibration, cost-tracking, gap]
summary: "GAP: No data on budget tracking accuracy — estimated costs vs actual API costs are never compared. Budget tier assignments may be systematically over- or under-estimating."
source: auto_pattern
uses: 1
harmful_uses: 0
confidence: 0.65
verify_check: manual
successful_uses: 0
---

## Knowledge Gap: Budget Tracking Calibration

Identified during /compile 2026-04-04. The budget system tracks estimated costs per agent call, but:
- No comparison against actual Anthropic API billing
- No validation that tier assignments (light/standard/deep) predict actual cost ranges
- ccusage MCP integration exists but is not used for calibration
- No feedback loop from actual costs to tier thresholds

**Action needed**: Run ccusage after a representative session and compare actual vs estimated costs. Document calibration factor.
