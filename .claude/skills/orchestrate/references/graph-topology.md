# Graph Topology Selection (BIGMAS-aligned, arXiv:2603.15371)

**Deep tier only.** Light/standard/farm skip this step — the overhead is not worth it for simpler tasks.

After decomposing subtasks (Phase 3, steps 1-9) and before wave assignment (step 5), classify the graph shape and generate workspace contracts.

## Step 1: Classify Graph Shape

Analyze the dependency structure of the decomposed subtasks:

| Dependency Signal | Shape | Wave Strategy | Workspace Rules |
|-------------------|-------|---------------|-----------------|
| All subtasks independent (p >= 0.8) | **Flat parallel** | All in Wave 1 | Each agent writes independently, no cross-reads needed |
| Linear chain (each depends on previous) | **Pipeline** | Sequential waves, 1 subtask per wave | Strict handoff: downstream reads_from = upstream writes_to |
| Fan-out then merge (A→B,C→D) | **DAG with merge** | Standard topological waves | Extra validation at merge point: verify all upstream artifacts consistent |
| Iterative refinement (implement→review→fix cycle) | **Pipeline + feedback** | Wave re-open protocol (max 2 iterations) | Each iteration reads previous iteration's output + critic feedback |
| Scout uncertain about structure | **Conservative pipeline** | Add verification subtask after each stage | Extra validation subtasks increase wave count but catch errors early |

**Rules:**
- If all shapes look equally plausible → pick the simplest (flat parallel > DAG > pipeline)
- If subtask count is 2 or fewer → skip topology selection entirely (trivial graph)
- Mixed shapes are valid: a DAG with one pipeline branch and one parallel branch

## Step 2: Infer Agent Roles

For each subtask, derive a descriptive role label from its description and context_scope:

```
Role label format: <domain>-<action>
Examples: "auth-implementer", "schema-migrator", "test-generator", "api-reviewer"
```

**Role deduplication check:**
- If 2 subtasks share the same role label → likely duplicated work → consider merging
- If 3+ subtasks share a role label → either it's a farm-style batch (correct) or the decomposition is too fine-grained (merge)
- Exception: same role with different context_scope is valid (e.g., "test-generator" for auth module vs. API module)

**Role diversity check (deep tier only):**
- Count unique role labels. If unique_roles < total_subtasks × 0.5 → warn: low role diversity may mean over-decomposition
- Diversity framing (from agent-execution.md) already varies reasoning approach — roles are orthogonal to that

## Step 3: Generate Workspace Contracts

For each subtask, define explicit `reads_from` and `writes_to` fields:

```yaml
subtasks:
  - id: "st-1"
    role: "auth-implementer"
    reads_from: []                              # root node, no upstream
    writes_to: ["src/auth.py", "intermediate/{task-id}/st-1.json"]
  - id: "st-2"
    role: "test-generator"
    reads_from: ["st-1/output"]                 # needs st-1's implementation
    writes_to: ["tests/test_auth.py", "intermediate/{task-id}/st-2.json"]
  - id: "st-3"
    role: "integration-reviewer"
    reads_from: ["st-1/output", "st-2/output"]  # needs both
    writes_to: ["intermediate/{task-id}/st-3.json"]
```

**Validation (run before committing plan to state.md):**
1. **Completeness**: every subtask has both fields defined
2. **Consistency**: for each `reads_from: ["st-N/output"]`, st-N must exist and have matching `writes_to`
3. **Disjointness**: no two same-wave subtasks share a `writes_to` entry (except intermediate/ JSON which is always unique)
4. **Reachability**: every subtask is either a root (reads_from = []) or all its reads_from entries are produced by upstream subtasks

Validation here is **LLM-driven** — perform the 4 checks above mentally while decomposing. A Python `workspace_validator` was prototyped (2026-04-12) but never wired: the orchestrator has no Bash access and the runtime integration was never designed. See `.claude/hooks/archive/workspace_validator.py` if the feature is revived.

## Step 4: Routing Estimate (difficulty proxy)

Calculate a pre-execution difficulty estimate based on topology:

```
dependency_density = total_edges / total_subtasks
routing_estimate = total_waves × avg_subtasks_per_wave × (1 + dependency_density)
```

| routing_estimate | Interpretation |
|-----------------|----------------|
| < 3 | Simple — typical deep tier, no special handling |
| 3-8 | Standard — normal deep tier complexity |
| 8-15 | Complex — consider budget reallocation, warn user about potential cost |
| > 15 | Very complex — likely needs scope reduction or tier=farm decomposition |

**Threshold warning:** If `routing_estimate > 2× median` for past deep-tier tasks (from topology-evolution.md), log: `"Warning: routing_estimate {N} exceeds 2x median ({M}) — expect higher cost and potential escalations."`

If no historical data yet (topology-evolution.md empty): use absolute threshold of 10.

## Step 5: Log Topology

Write topology metadata to state.md YAML frontmatter:

```yaml
topology:
  graph_shape: "dag_with_merge"      # from Step 1
  routing_estimate: 6.4              # from Step 4
  roles: ["auth-implementer", "test-generator", "integration-reviewer"]
  unique_role_count: 3
  dependency_density: 0.67
```

This metadata feeds into:
- Phase 4 Full-State Routing (routing_estimate vs actual comparison)
- Phase 6 topology-evolution.md (data collection for future calibration)
- N-Plan Selection scoring (topology fitness dimension)

## Integration with N-Plan Selection

When N-Plan Selection is active (deep tier, from `references/n-plan-selection.md`), add **Topology fitness** as a 6th scoring dimension:

| Dimension | Score 1 (worst) | Score 5 (best) |
|-----------|----------------|----------------|
| Topology fitness | Complex cyclic graph, high routing_estimate, many merge points | Clean DAG or flat parallel, low routing_estimate, minimal merge |

Simpler topologies are preferred when all else is equal — they have fewer failure points and lower coordination cost.

## Anti-Patterns

- **Over-decomposition**: 8+ subtasks for a task that could be 3-4 → merging subtasks is cheaper than coordinating them
- **False parallelism**: marking subtasks as independent when they actually share write targets → catch via disjointness check
- **Topology speculation**: spending 500+ tokens analyzing shape for a 3-subtask task → skip, the benefit is near zero
- **Ignoring scout uncertainty**: scout reported gaps → using flat parallel shape → use conservative pipeline instead
