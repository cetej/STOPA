---
date: 2026-04-02
type: anti_pattern
severity: critical
component: orchestration
tags: [audit, verification, cross-cutting]
summary: "Audit/refactor that changes shared interfaces (API envelope, response format) MUST verify ALL consumers, not just the changed layer. Wave 3 audit broke 70 JS calls by only running pytest."
source: user_correction
confidence: 1.00
uses: 2
harmful_uses: 0
verify_check: "manual"
successful_uses: 0
---

## Cross-cutting changes require cross-cutting verification

### Incident
NG-ROBOT wave 3 audit added response envelope to Python API. JS frontend was never updated.
~70 broken fetch calls. Entire UI non-functional. User discovered it, not the audit process.

### Systemic failure
- Critic only reviewed the layer that changed (Python)
- Verify step only ran backend tests (pytest)
- No step checked the other side of the API contract (JS frontend)

### Rule for all orchestrated audits
1. Identify ALL consumers of the interface being changed
2. Verify EACH consumer after the change — not just the producer
3. For web apps: backend test + browser smoke test = minimum
4. Cross-cutting changes (response format, auth, middleware) need proportionally wider verification

**Why:** Audit is supposed to improve quality. An audit that breaks things is worse than no audit — it creates false confidence.

**How to apply:** When /critic or /verify runs after an audit wave, explicitly check: "Did this change affect an interface boundary? If yes, verify both sides."
