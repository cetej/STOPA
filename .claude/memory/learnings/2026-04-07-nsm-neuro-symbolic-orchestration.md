---
date: 2026-04-07
type: architecture
severity: high
component: orchestration
tags: [orchestration, planning, agent-execution, context-management]
summary: "Neuro-symbolic architecture (PDDL planner + learned policies) outperforms end-to-end VLA by 3x on structured tasks. 5 patterns adopted: operator-scoped context, input/output contracts with plan chain validation, done-when completion criteria, mid-execution replanning, and primitive action sequence extraction."
source: external_research
maturity: draft
confidence: 1.0
uses: 1
successful_uses: 0
harmful_uses: 0
impact_score: 0.0
verify_check: "Grep('context_scope', path='.claude/skills/orchestrate/SKILL.md') → 1+ matches"
---

## NSM Neuro-Symbolic Patterns for Orchestration

Ref: Duggan et al., "The Price Is Not Right" (arXiv:2602.19260, ICRA 2026).
Neuro-symbolic (PDDL + diffusion policies) achieved 95% vs VLA 34% on 3-block Hanoi, 78% vs 0% on unseen 4-block.

### Adopted patterns (implemented 2026-04-07):

1. **Operator-Scoped Context (Feature Selector φ)**: Each agent receives only files/context relevant to its subtask via `context_scope` field. Reduces noise, improves focus. → orchestrate Phase 4.

2. **Input/Output Contracts + Plan Chain Validation**: Skills now support `input-contract`, `preconditions`, `effects` in frontmatter. Orchestrator validates chain compatibility BEFORE agent execution. → skill-files.md rules + orchestrate Phase 3.

3. **Done-When Completion Criteria**: Each subtask has machine-verifiable `done_when` condition. Agent self-checks before reporting DONE. → orchestrate subtask format.

4. **Mid-Execution Replanning**: On subtask failure that invalidates downstream plan, orchestrator re-decomposes affected branch (not full restart). Max 1 replan per task. → orchestrate inter-wave check.

5. **Primitive Action Sequence Extraction**: /discover extracts reusable micro-operations (informed-edit, test-loop) that compose into workflows. Analogous to NSM learning stack primitives from 50 demos. → discover Phase 2e.

### Key insight
50 primitive demos > 300 full-task demos. Composable operators with explicit interfaces > monolithic end-to-end. Same principle validates STOPA's skill-based architecture over prompt-only approaches.
