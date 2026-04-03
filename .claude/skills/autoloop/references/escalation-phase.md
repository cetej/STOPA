# Escalation Phase (Agent0-inspired, optional)

**Trigger:** `escalate:true` flag AND 3 consecutive discards (plateau detected).
**Concept:** Instead of just ramping exploration weight, raise the bar -- add harder constraints or tighter metrics. Inspired by Agent0's co-evolutionary curriculum: when the optimizer plateaus, the challenge must escalate.

## How it works

1. **Analyze current state**: Read all "keep" iterations from TSV -- what has already been optimized?

2. **Generate escalation** based on mode:

   | Mode | Escalation method |
   |------|-------------------|
   | **Metric mode** | Tighten target: if metric plateaued at 92%, set new floor at 90% and add a SECOND metric as guard (e.g., complexity, coverage, latency) |
   | **File mode (SKILL.md)** | Add 2-3 NEW scoring checks beyond the original 15-point heuristic, derived from what's NOT yet covered (e.g., "has examples section", "has edge case handling") |
   | **File mode (other)** | Switch from current scorer to a stricter one: add new constraints derived from the goal (e.g., "under 100 LOC" + "no nested loops") |

3. **Reset plateau counter** to 0, keep budget running
4. **Log escalation** in TSV as special row:
   ```
   E1	-	92.0	0.0	-	escalation	added guard: complexity < 150 LOC
   ```
5. **Resume loop** with new constraints -- the bar is now higher
6. **Max 2 escalations** per run -- after 2nd escalation plateaus -> HARD STOP

## Escalation status in status block
```
AUTOLOOP_STATUS:
  escalation_level: <0|1|2>
  escalation_desc: "<what was added>"
```
