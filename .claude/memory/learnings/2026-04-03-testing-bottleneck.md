---
date: 2026-04-03
type: best_practice
severity: medium
component: orchestration
tags: [verification, testing, workflow, bottleneck]
summary: "Code generation is no longer the bottleneck — verification and testing are. Allocate proportional effort to proving correctness."
source: external_research
uses: 1
harmful_uses: 0
confidence: 1.0
verify_check: "Grep('Verification is the bottleneck', path='.claude/skills/orchestrate/SKILL.md') -> 1+ matches"
related: [2026-04-03-smart-tool-overuse.md]
successful_uses: 0
---

## Testing as the New Bottleneck (Simon Willison, Lenny's Podcast, 2026-04-02)

With GPT 5.1 and Claude Opus 4.5 crossing the reliability threshold in Nov 2025, code generation compressed from weeks to hours. The critical path shifted: **usability testing and quality verification** are now the bottleneck, not code writing.

**Key insight:** Agent-generated code needs human validation and real-world usage before deployment. Rapid prototype generation creates cognitive demands requiring careful verification management.

**STOPA implementation:** Added as orchestrate Rule #13: "Verification is the bottleneck, not generation — allocate proportional effort to proving correctness." Reinforces existing /verify and /tdd skills.

**How to apply:** When estimating subtask effort in orchestrate, weight verification/testing at least equal to implementation. Don't skimp on critic rounds just because code was generated quickly.
