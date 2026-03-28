# Meta Self-Modification Mode — AutoLoop Extension

When `meta:true` is specified, autoloop can modify its own scoring parameters and exploration strategy during the optimization loop. This is the Hyperagents "metacognitive self-modification" pattern.

**Constraint:** `meta:true` requires `mode:linear`. Tree + meta combination is rejected.

## Safety Boundaries

### 1. Sandbox Isolation
All meta-changes happen in `.claude/memory/intermediate/meta-sandbox/`.
Original scoring parameters are NEVER modified during the run.

### 2. Whitelist — What CAN Be Modified

| Parameter | Type | Example |
|-----------|------|---------|
| Scoring weights (S1-S12) | point values | S1: +2 → +3 |
| Penalty weights (N1-N4) | point values | N1: -2 → -1 |
| LOC creep threshold | percentage | 30% → 40% |
| Metric spike multiplier | float | 3× → 4× |
| Plateau discard count | integer | 7 → 5 |
| Exploration weight ramp | float[] | [1.4, 1.7, 2.0] → [1.2, 1.5, 2.5] |

### 3. Blacklist — What CANNOT Be Modified

- Loop structure (phases, steps, ordering)
- Git operations (commit, revert, branch)
- Guard/verify command logic
- Meta-mode rules themselves (no meta-meta)
- TSV log format
- File mode vs metric mode detection
- Crash recovery protocol

### 4. Explicit Tracking

Initialize `meta-log.tsv` at setup:
```
iteration	parameter	old_value	new_value	score_before	score_after	meta_status
```

Every meta-change is logged BEFORE application. Valid meta_status: `meta-keep`, `meta-revert`.

### 5. Circuit Breaker

If 3 consecutive meta-changes result in score drops: auto-disable meta-mode for the rest of the run. Revert all meta-changes to original parameters. Log: `⚠ META CIRCUIT BREAKER: 3 consecutive drops, reverting to original parameters.`

## Setup

1. Create `.claude/memory/intermediate/meta-sandbox/`
2. Copy current scoring parameters to `meta-sandbox/scorer-params.json`:
   ```json
   {
     "weights": {"S1": 2, "S2": 1, ..., "N1": -2, ...},
     "thresholds": {"loc_creep": 0.30, "spike_multiplier": 3.0},
     "exploration": {"ramp": [1.4, 1.7, 2.0], "plateau_limit": 7}
   }
   ```
3. Initialize `meta-log.tsv`
4. Print: `⚠ EXPERIMENTAL: Meta self-modification enabled. Changes sandboxed until user approval.`

## During Loop

Every **3 iterations**, the agent MAY propose ONE meta-change:

1. **Analyze**: Review last 3 iterations' results. Is the scoring too lenient? Too strict? Is exploration weight helping?
2. **Propose**: Name the parameter and new value. Explain rationale.
3. **Log**: Write to `meta-log.tsv` before applying.
4. **Apply**: Update `scorer-params.json` in sandbox. Use sandbox params for next iteration's scoring.
5. **Evaluate**: If next iteration's score improves → `meta-keep`. If drops → `meta-revert` (restore previous param value).

## After Loop — User Approval Gate

Present all meta-changes in a summary table:

```markdown
### Meta-Modifications

| Parameter | Original | Modified | Effect | Status |
|-----------|----------|----------|--------|--------|
| S1 weight | +2 | +3 | Score +0.8 | meta-keep |
| LOC threshold | 30% | 40% | No change | meta-revert |
| Exploration ramp[0] | 1.4 | 1.2 | Score +0.3 | meta-keep |

Meta-keeps: 2 | Meta-reverts: 1 | Circuit breaker: no
```

Ask user for EACH `meta-keep` change individually:
> "Apply `S1 weight: +2 → +3` to the real scorer? (yes/no)"

Only explicit "yes" applies the change. All others are discarded.
