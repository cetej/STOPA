---
task_id: bigmas-workspace-validation
goal: "Add workspace contract validation to orchestrate — validate reads_from/writes_to at subtask launch, wave boundary, and task completion"
type: feature
status: planned
branch: main
tier: deep
task_style: structured
verifiability: METRIC
topology:
  graph_shape: "dag_with_merge"
  routing_estimate: 6.0
  roles: ["schema-validator-implementer", "launch-gate-implementer", "wave-boundary-implementer", "completion-checker-implementer", "integration-tester", "hook-wirer"]
  unique_role_count: 6
  dependency_density: 0.5
routing_decisions: 0
subtasks:
  - {id: "st-1", description: "Implement reads_from resolution logic — resolve st-N/output refs, grounding/ paths, shared/ paths", criterion: "All 3 ref types resolve correctly; unresolvable refs raise clear error", done_when: "python -c 'from workspace_validator import resolve_reads; print(resolve_reads([\"st-1/output\", \"grounding/x.md\", \"shared/notes.md\"], mock_state))' succeeds", context_scope: ["references/workspace-schema.md"], grounding_refs: [], depends_on: [], wave: 1, method: "Agent:general", status: "pending", artifacts: [], reads_from: ["grounding/workspace-schema.md"], writes_to: [".claude/hooks/workspace-validator.py", "intermediate/bigmas-workspace-validation/st-1.json"]}
  - {id: "st-2", description: "Implement writes_to disjointness check — verify no two same-wave subtasks share write targets", criterion: "Overlapping writes detected and reported; non-overlapping passes silently", done_when: "python -c 'from workspace_validator import check_disjointness; assert check_disjointness(mock_plan)' passes", context_scope: ["references/workspace-schema.md", "references/agent-execution.md"], grounding_refs: [], depends_on: [], wave: 1, method: "Agent:general", status: "pending", artifacts: [], reads_from: ["grounding/workspace-schema.md", "grounding/agent-execution.md"], writes_to: [".claude/hooks/workspace-validator.py", "intermediate/bigmas-workspace-validation/st-2.json"]}
  - {id: "st-3", description: "Implement wave boundary validation — verify writes_to files exist and are non-empty after each wave", criterion: "Missing/empty files flagged; complete files pass", done_when: "python -c 'from workspace_validator import validate_wave_completion; validate_wave_completion(mock_completed_wave)' passes", context_scope: ["references/workspace-schema.md", "references/wave-recovery.md"], grounding_refs: [], depends_on: ["st-1"], wave: 2, method: "Agent:general", status: "pending", artifacts: [], reads_from: ["st-1/output", "grounding/wave-recovery.md"], writes_to: [".claude/hooks/workspace-validator.py", "intermediate/bigmas-workspace-validation/st-3.json"]}
  - {id: "st-4", description: "Implement completion validation — B_ans completeness check + orphan writes detection via git diff", criterion: "Orphan writes detected; all CC assertions reference existing files", done_when: "python -c 'from workspace_validator import validate_completion; validate_completion(mock_state)' passes", context_scope: ["references/workspace-schema.md", "references/completion-contract.md"], grounding_refs: [], depends_on: ["st-1"], wave: 2, method: "Agent:general", status: "pending", artifacts: [], reads_from: ["st-1/output", "grounding/completion-contract.md"], writes_to: [".claude/hooks/workspace-validator.py", "intermediate/bigmas-workspace-validation/st-4.json"]}
  - {id: "st-5", description: "Wire validator into orchestrate — add PreToolUse hook or inline checks at Phase 4 launch, wave boundary, Phase 5 completion", criterion: "Validator runs automatically during orchestration; errors logged to scratchpad", done_when: "Grep('workspace.validator', path='.claude/skills/orchestrate/SKILL.md') returns 1+ matches AND hook registered in settings.json", context_scope: ["SKILL.md", "references/agent-execution.md", "references/wave-recovery.md"], grounding_refs: [], depends_on: ["st-1", "st-2", "st-3", "st-4"], wave: 3, method: "Agent:general", status: "pending", artifacts: [], reads_from: ["st-1/output", "st-2/output", "st-3/output", "st-4/output"], writes_to: ["SKILL.md", ".claude/settings.json", "intermediate/bigmas-workspace-validation/st-5.json"]}
  - {id: "st-6", description: "Integration test — run validator against 2 past orchestration traces (from topology-evolution.md) + 1 synthetic invalid plan", criterion: "Valid traces pass; invalid trace caught with correct error message", done_when: "python tests/test_workspace_validator.py passes all 3 cases", context_scope: [".claude/hooks/workspace-validator.py", "tests/"], grounding_refs: [], depends_on: ["st-5"], wave: 4, method: "Agent:general", status: "pending", artifacts: [], reads_from: ["st-5/output"], writes_to: ["tests/test_workspace_validator.py", "intermediate/bigmas-workspace-validation/st-6.json"]}
---

# Shared Memory — Task State

Current task state shared across all agents and skills.

## Active Task

**Goal**: Add workspace contract validation to orchestrate — validate reads_from/writes_to at subtask launch, wave boundary, and task completion
**Type**: feature
**Status**: planned (dry-run verification of Phase 3.3 BIGMAS topology)
**Tier**: deep (6 subtasks, 4 waves, cross-cutting)

### Subtasks

| # | Subtask | Criterion | Depends on | Wave | Method | Status |
|---|---------|-----------|-----------|------|--------|--------|
| 1 | reads_from resolution logic | 3 ref types resolve | — | 1 | Agent:general | pending |
| 2 | writes_to disjointness check | Overlapping detected | — | 1 | Agent:general | pending |
| 3 | Wave boundary validation | Missing/empty flagged | 1 | 2 | Agent:general | pending |
| 4 | Completion validation (B_ans) | Orphan writes detected | 1 | 2 | Agent:general | pending |
| 5 | Wire into orchestrate | Hook runs automatically | 1,2,3,4 | 3 | Agent:general | pending |
| 6 | Integration test | 3 cases pass | 5 | 4 | Agent:general | pending |

### Dependency Graph

```
1 ──→ 3 (output: resolve logic)
1 ──→ 4 (output: resolve logic)
1,2,3,4 → 5 (all validators merged)
5 ──→ 6 (wired hook → test it)

Wave 1: [1, 2]    ← independent (reads_from + writes_to logic)
Wave 2: [3, 4]    ← both need st-1 resolve logic
Wave 3: [5]       ← merge all validators + wire hook
Wave 4: [6]       ← integration test
```

### Topology Analysis (Phase 3.3 — BIGMAS)

- **Graph shape**: DAG with merge (fan-out Wave 1→2, merge at Wave 3)
- **Routing estimate**: 6.0 (4 waves × 1.5 avg subtasks × 1.0 density factor)
- **Role diversity**: 6 unique roles / 6 subtasks = 1.0 (no duplication)
- **Workspace contracts**: `reads_from`/`writes_to` defined per subtask in YAML
- **Disjointness check**: st-1 and st-2 both write to `workspace-validator.py` but are in same wave → CONFLICT → must sequentialize or merge

### Disjointness Resolution

st-1 and st-2 both write to `.claude/hooks/workspace-validator.py`. Options:
1. **Merge st-1 + st-2 into one subtask** (reduces wave count, simplifies)
2. **Sequentialize** (st-1 first, st-2 second, same wave but sequential)

→ **Decision**: Merge st-1 + st-2 (both are validation logic for the same file). This reduces total subtasks to 5 and routing_estimate to ~5.0.
