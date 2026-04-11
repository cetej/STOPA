# Workspace Schema (BIGMAS-aligned, arXiv:2603.15371)

Formalized workspace model for STOPA orchestration. Maps existing infrastructure to 4 typed zones inspired by Global Workspace Theory. All zones use existing STOPA files — no new infrastructure needed.

## Zone Definitions

| Zone | Purpose | STOPA Path | Readers | Writers | Validation |
|------|---------|-----------|---------|---------|------------|
| **B_ctx** | Read-only task context | `grounding_refs` + `context_scope` files | All agents | Orchestrator only (Phase 0/2) | Immutable during execution |
| **B_work** | Read-write intermediate results | `intermediate/{task-id}/*.json` + `scratchpad.md` | Orchestrator, downstream agents | Owning agent only | Non-empty status field, valid JSON |
| **B_sys** | System metadata & routing | `state.md` frontmatter + `budget.md` | All (via injection) | Orchestrator only | Schema per state.md YAML spec |
| **B_ans** | Final answer / artifacts | `state.md` artifacts + completion contract | Phase 5 auditor | Phase 4 agents (via artifacts) | All CC assertions evaluable |

## Per-Subtask Workspace Contract

Each subtask in state.md YAML gains two fields defining its workspace interaction:

```yaml
subtasks:
  - id: "st-1"
    # ... existing fields ...
    reads_from: []                    # no upstream dependencies
    writes_to: ["src/auth.py", "intermediate/{task-id}/st-1.json"]
  - id: "st-2"
    # ... existing fields ...
    reads_from: ["st-1/output"]       # depends on st-1's artifacts
    writes_to: ["src/middleware.py", "intermediate/{task-id}/st-2.json"]
```

**`reads_from` format:**
- `"st-N/output"` — artifacts from upstream subtask N (resolved from state.md `subtasks[N].artifacts`)
- `"grounding/<filename>"` — file from grounding_refs (B_ctx zone, immutable)
- `"shared/notes.md"` — cross-agent shared findings

**`writes_to` format:**
- Absolute or relative file paths the subtask will create/modify
- Always includes the agent's own `intermediate/{task-id}/{subtask-id}.json`

## Validation Rules

### At subtask launch (Phase 4)
1. **Readability**: every `reads_from` entry must be resolvable:
   - `st-N/output` → subtask N must have status `done` with non-empty `artifacts`
   - `grounding/*` → file must exist on disk
   - `shared/*` → directory must exist (file may not exist yet — that's OK)
2. **Write disjointness**: `writes_to` must not overlap with any parallel (same-wave) subtask's `writes_to`
   - This extends the existing File Access Manifest disjointness check

### At wave boundary (Phase 4, inter-wave)
3. **Write completion**: for each completed subtask, verify its `writes_to` files exist and are non-empty
   - Missing file → subtask produced incomplete output → flag for review
4. **Downstream readiness**: for each next-wave subtask, verify all `reads_from` entries are now resolvable
   - Unresolvable → blocked dependency → do not launch, flag as `blocked:st-N`

### At task completion (Phase 5)
5. **B_ans completeness**: all completion contract assertions reference files that exist in B_ans
6. **No orphan writes**: every file in any `writes_to` was actually created (git diff cross-check)

## Workspace State Machine

```
INIT (Phase 0-2)
  ├── B_ctx loaded: grounding_refs + context_scope populated
  ├── B_sys initialized: state.md created with subtask YAML, budget.md updated
  └── B_work created: intermediate/{task-id}/ directory + manifest.json

PER_WAVE (Phase 4, repeats)
  ├── B_work grows: agent outputs written to intermediate/*.json
  ├── B_sys updated: subtask statuses transition in state.md
  ├── Scratchpad updated: new rows in scratchpad.md
  └── Routing decision: reads ALL zones, decides next action
      → CONTINUE | EARLY_TERMINATE | REPLAN | PRUNE | COMPLEXITY_ESCALATE

TERMINAL (Phase 5-6)
  ├── B_ans populated: artifacts + completion contract evaluated
  ├── Phase 5 validates B_ans against B_ctx requirements
  └── Phase 6 archives B_work (intermediate/ cleanup), updates B_sys (state.md → done)
```

## Backward Compatibility

- `reads_from` and `writes_to` are optional fields in subtask YAML
- If omitted: orchestrator infers from `context_scope` (reads) and `method` + `description` (writes)
- Existing orchestrations without these fields continue to work unchanged
- Deep tier: these fields are generated automatically in Phase 3.3 (Topology Selection)
- Light/standard/farm: omit — the overhead of explicit contracts is not worth it for simple tasks
