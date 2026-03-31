# Meta Self-Modification Mode — Self-Evolve Extension

When `meta:true` is specified, self-evolve can modify its own co-evolution parameters and
generate new curriculum strategies during the run. Inspired by HyperAgents (Meta, arXiv:2603.19461):
metacognitive self-modification — improving not just the skill, but the mechanism that generates improvements.

**Default:** `meta:false` — standard v1 behavior, no meta-modification.

## Safety Boundaries

### 1. Sandbox Isolation
All meta-changes happen in `.claude/memory/intermediate/meta-sandbox/self-evolve-<target>.json`.
Original parameters are NEVER modified during the run. Changes apply only after user approval.

### 2. Whitelist — What CAN Be Modified

| Parameter | Type | Default | Bounds | Example |
|-----------|------|---------|--------|---------|
| `curriculum_strategy_weights` | object | edge:0.25, adversarial:0.25, scale:0.25, composition:0.25 | values sum to 1.0 | adversarial:0.4, edge:0.3, scale:0.1, composition:0.2 |
| `escalation_threshold` | float | 1.0 | [0.95, 1.0] | 0.95 (escalate at 95% instead of 100%) |
| `critic_frequency` | int | 2 | [1, 4] | 3 (critic every 3 rounds instead of 2) |
| `circuit_breaker_revert_limit` | int | 3 | [2, 5] | 4 (allow more attempts before stopping) |
| `max_cases` | int | 20 | [10, 30] | 15 (tighter case budget) |
| `custom_strategies` | array | [] | max 2 entries | see Custom Strategy Format below |

### 3. Blacklist — What CANNOT Be Modified

- Loop structure (Phase 0-3 sequence, step ordering)
- Git operations (commit, revert, branch, merge)
- Eval case format (input.md / expected.md / eval.md)
- Meta-mode rules themselves (no meta-meta)
- Eval case immutability ("cases are sacred" rule)
- User approval requirements (merge, persistence)
- Sub-agent model assignments (Curriculum=haiku, Curriculum Critic=sonnet, Executor=sonnet)

### 4. Explicit Tracking

Initialize `meta-log.tsv` at setup:
```
round	parameter	old_value	new_value	rationale	score_before	score_after	meta_status
```

Every meta-change is logged BEFORE application. Valid meta_status: `meta-keep`, `meta-revert`.

### 5. Circuit Breaker

If 3 consecutive meta-changes result in pass_rate drops: auto-disable meta-mode for the rest of the run.
Revert all meta-changes to original parameters. Log: `⚠ META CIRCUIT BREAKER: 3 consecutive drops, reverting to original parameters.`

## Custom Strategy Format

Meta-agent can propose up to 2 new curriculum strategies per run. Each strategy is a JSON template:

```json
{
  "name": "regression",
  "description": "Test that new edits don't break previously passing cases",
  "focus": "backward compatibility",
  "difficulty_axis": "interaction between features",
  "example_pattern": "Modify case-003 input slightly and verify same expected output"
}
```

**Required fields:** name, description, focus, difficulty_axis, example_pattern
**Validation:** Every new strategy's first generated case MUST pass Curriculum Critic (score ≥3).
If first case fails Critic: strategy is rejected, does not count toward the 2-strategy limit.

## Setup (Phase 0 additions)

1. Check for persisted meta-params: `.claude/memory/intermediate/self-evolve-meta/<target>.json`
   - If exists: load as defaults instead of hardcoded values. Print: `♻ Loaded evolved parameters from previous run (v{version}).`
   - If not: use hardcoded defaults
2. Create sandbox: `.claude/memory/intermediate/meta-sandbox/self-evolve-<target>.json`
3. Copy current parameters to sandbox
4. Initialize `meta-log.tsv`
5. Print: `⚠ EXPERIMENTAL: Meta self-modification enabled. Changes sandboxed until user approval.`

## During Loop

Every **3 rounds**, meta-agent analyzes and MAY propose ONE change:

### Analysis Phase (read-only)
1. **Strategy effectiveness**: Which curriculum strategies produce cases that Executor fails on? (= useful hard cases). Which produce cases that pass immediately? (= too easy)
2. **Critic efficiency**: Is critic catching real issues or generating false positives?
3. **Convergence rate**: How fast is pass_rate improving? Stalling?
4. **Revert ratio**: How many Executor edits are reverted? High ratio = Executor struggling, maybe relax critic or adjust strategy weights.

### Propose Phase
1. Name the parameter and proposed value
2. Explain rationale based on analysis
3. Log to `meta-log.tsv` BEFORE applying
4. Apply in sandbox only

### Evaluate Phase
1. Next round uses sandbox parameters
2. If pass_rate improves or holds: `meta-keep`
3. If pass_rate drops: `meta-revert` (restore previous value)

### Custom Strategy Proposal
If meta-agent identifies that none of the existing strategies (edge/adversarial/scale/composition) are effective for the target skill's domain:

1. Propose new strategy in JSON template format
2. Curriculum agent generates 1 case using the new strategy
3. Case goes through Curriculum Critic (score ≥3 required)
4. If accepted: strategy is added to available strategies with initial weight 0.2 (weights rebalanced)
5. If rejected: strategy is discarded, agent may propose a different one (max 1 retry)

## After Loop — User Approval Gate

Present meta-changes summary:

```markdown
### Meta-Modifications

| Round | Parameter | Original | Modified | Effect | Status |
|-------|-----------|----------|----------|--------|--------|
| 3 | adversarial weight | 0.25 | 0.40 | pass_rate +5% | meta-keep |
| 6 | critic_frequency | 2 | 3 | fewer false reverts | meta-keep |
| 9 | NEW strategy "regression" | — | added | caught 2 regressions | meta-keep |

Meta-keeps: 3 | Meta-reverts: 0 | Circuit breaker: no
```

### Persistence Decision
Ask user: "Persist evolved parameters for future `/self-evolve <target>` runs?"
- **Yes**: Write to `.claude/memory/intermediate/self-evolve-meta/<target>.json`
- **No**: Parameters are discarded, next run starts from defaults

Persistence format:
```json
{
  "target": "<target>",
  "version": N,
  "evolved_at": "YYYY-MM-DD",
  "params": {
    "curriculum_strategy_weights": {"edge": 0.3, "adversarial": 0.4, "scale": 0.1, "composition": 0.2},
    "escalation_threshold": 1.0,
    "critic_frequency": 3,
    "circuit_breaker_revert_limit": 3,
    "max_cases": 20,
    "custom_strategies": [
      {"name": "regression", "description": "...", "focus": "...", "difficulty_axis": "...", "example_pattern": "..."}
    ]
  },
  "history": [
    {"version": 1, "date": "YYYY-MM-DD", "change": "initial defaults", "reason": "baseline"},
    {"version": 2, "date": "YYYY-MM-DD", "change": "adversarial weight 0.25→0.4", "reason": "edge cases too easy for critic skill"}
  ]
}
```
