---
date: 2026-04-03
type: best_practice
severity: medium
component: orchestration
tags: [tool-use, efficiency, cost-optimization, SMART]
summary: "SMART gate: before spawning agent or tool call, ask 'Is this answerable from loaded context?' Eliminates ~20% unnecessary calls, especially in light tier."
source: external_research
maturity: draft
uses: 0
harmful_uses: 0
confidence: 0.7
verify_check: "Grep('Tool Necessity Check', path='.claude/skills/orchestrate/SKILL.md') -> 1+ matches"
related: [2026-04-03-testing-bottleneck.md]
successful_uses: 0
---

## SMART Tool Overuse Mitigation (arXiv:2502.11435)

LLM agents tend to reflexively call external tools even for tasks solvable from parametric knowledge ("tool overuse"). The SMART framework adds a metacognitive step: at each decision point, the agent generates a rationale explaining *why* a tool is or is not needed.

**Key numbers:** 24% fewer tool calls, 37% performance improvement, 7B models reaching 70B-scale quality.

**STOPA implementation:** Added as "Tool Necessity Check (SMART gate)" in orchestrate Decomposition step 4 and Rule #12. Prompt-level gate — no fine-tuning needed. Especially impactful in light tier where direct resolution should be the default.

**How to apply:** Before every agent spawn or non-trivial tool call, ask: "Is this answerable from context already loaded or parametric knowledge?" If yes → resolve directly. Track how often the gate fires to measure savings.
