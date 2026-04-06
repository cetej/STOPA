---
date: 2026-04-04
type: architecture
severity: medium
component: skill
tags: [compact-variant, measurement, SKILL0, gap]
summary: "GAP: No measurement data on SKILL.compact.md effectiveness — claimed ~80% token reduction and ~7% size, but no actual before/after data collected. Need baseline measurement protocol."
source: auto_pattern
uses: 0
harmful_uses: 0
confidence: 0.5
verify_check: manual
successful_uses: 0
---

## Knowledge Gap: Compact Variant Effectiveness Measurement

Identified during /compile 2026-04-04. SKILL0 Dynamic Curriculum claims:
- Compact variants are ~7% of full size (~500-800 tokens vs ~5-7K)
- Progressive withdrawal saves ~80% on repeat invocations

But no actual measurement exists:
- No before/after token counts from real sessions
- No quality comparison (does compact produce same quality output?)
- No measurement of how many skills actually have compact variants
- No data on how often skills are invoked 2+ times per session

**Action needed**: Create a measurement harness that tracks token usage per skill invocation across sessions.
