---
date: 2026-04-14
type: architecture
severity: medium
component: orchestration
tags: [critic, verification, decomposition, multi-dimensional]
summary: "TraceGuard (arXiv:2604.03968) — 5D CoT monitoring: goal alignment, constraint adherence, reasoning coherence, safety awareness, action-trace consistency. Každá dimenze = oddělený LLM call → odolnost proti kolusi a blind spotům. Alternativa k monolitickému critic callu pro DEEP complexity."
source: external_research
uses: 2
harmful_uses: 0
successful_uses: 0
confidence: 0.8
maturity: draft
skill_scope: [critic]
related: [2026-04-13-judge-panel-size-convergence.md]
verify_check: "Grep('TraceGuard', path='.claude/skills/critic/SKILL.md') → 1+ matches"
---

## TraceGuard — 5D CoT Monitoring

**Paper**: arXiv:2604.03968 (April 2, 2026)

**Problem**: Single-pass critic calls have blind spots and can be colluded by a single model's biases.

**Solution**: Decompose verification into 5 independent dimensions, each evaluated separately:

| Dimension | What it checks |
|-----------|---------------|
| Goal alignment | Does the change achieve the stated objective? |
| Constraint adherence | Are project rules, types, API contracts preserved? |
| Reasoning coherence | Is the logic internally consistent? |
| Safety awareness | Security, error handling, edge cases |
| Action-trace consistency | Do actual edits match the stated plan? |

**Benefit**: 5 parallel Haiku calls (cheap) catch more than 1 expensive monolithic call. Each dimension is independently verifiable → resistant to model collusion.

**STOPA application**: Added to `/critic` SKILL.md as optional decomposition for DEEP complexity reviews only. STANDARD reviews keep the efficient 4-phase pipeline.
