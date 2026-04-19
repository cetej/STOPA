---
name: reference_claude_nerfing_analysis
description: AMD Senior AI Director analysis of Claude thinking budget degradation Jan-Mar 2026 — validates STOPA external guardrail design
type: reference
---

AMD Senior AI Director analysis of Claude session logs (Jan-Mar 2026):

**Observed metrics:**
- Median thinking dropped ~2,200 → ~600 chars
- API requests up 80x (Feb→Mar) — less thinking = more retries = more token burn
- reads-per-edit dropped 6.6x → 2.0x — model stops researching before editing
- 173 "should I continue" bailouts in 17 days (0 before Mar 8)
- Self-contradiction in reasoning tripled
- CLAUDE.md conventions ignored under reduced thinking budget
- Peak degradation at 5pm/7pm PST — hypothesis: GPU-load-sensitive thinking allocation

**Why:** Confirms user's direct experience with Claude quality degradation. Validates STOPA's architectural decision to use external enforcement (hooks, invariants, verification checklists) rather than relying on model's internal discipline.

**How to apply:**
- STOPA guardrails (core-invariants, panic-detector, verify-before-done) are not overhead — they compensate for variable model quality
- reads-per-edit metric could be tracked by a hook as quality signal
- Off-peak hours (late night PST) may yield better results for complex tasks
- When model quality degrades, external context engineering matters more, not less
