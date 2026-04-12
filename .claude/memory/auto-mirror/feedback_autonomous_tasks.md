---
name: feedback_autonomous_tasks
description: Scheduled tasks must be fully autonomous — report findings as status, never generate action lists for approval
type: feedback
---

Scheduled tasks must run autonomously and report results, never generate "Actions" lists requiring manual approval.

**Why:** User finds step-by-step approval in scheduled tasks impractical — defeats the purpose of automation. Repeated known findings (like "SNYK_TOKEN not set") are especially annoying.

**How to apply:**
- Task output = status report with facts, not approval requests
- Missing env vars (SNYK_TOKEN etc) = skip that check silently
- Known/repeated findings = note in report file, no notification
- New critical findings = Telegram alert with recommendation
- Safe changes (graduation, pruning) = apply directly, report what was done
- Ambiguous cases = note in report for user to read at leisure
- Never use phrases like "flag for review", "action needed", "please run X"
