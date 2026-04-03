# Context Health Check

Score the session context load after each subtask. Each signal adds points:

| Signal | Points | How to detect |
|--------|--------|---------------|
| Subtask progress >70% | +2 | Count done/total in state.md |
| Agent spawns ≥3 | +2 | Check budget.md agent counter |
| Agent spawns ≥5 | +3 | Check budget.md agent counter |
| Critic rounds ≥2 | +1 | Check budget.md critic counter |
| User back-and-forth ≥5 exchanges | +1 | Estimate from conversation |
| Large tool outputs received | +1 | If any agent returned very long results |
| Tier is deep | +1 | Check budget.md tier |

## Thresholds

- **Score 0-2**: Healthy. Continue normally.
- **Score 3-4**: **Yellow**. Save checkpoint silently. Continue working.
- **Score 5-6**: **Orange**. Auto-trigger `/compact` to offload completed subtask results to disk, then continue. Log: "Auto-compact triggered (context score N)."
- **Score 7+**: **Red**. Save checkpoint + notify user: "Kontext session je velký. Checkpoint uložen. Pokud zaznamenáš pokles kvality, začni novou session s resume promptem z `/checkpoint status`."

## Auto-Compact Trigger (Deep Agents adoption)

When context health score reaches **5+** (Orange threshold), automatically invoke `/compact` BEFORE continuing to the next wave/subtask:

1. **What to compact**: All completed subtask intermediate files that have already been summarized (have `compactSummary` field)
2. **How**: Invoke `/compact save-and-summarize` targeting `.claude/memory/intermediate/` — this saves full results to disk and replaces in-context references with compact summaries
3. **When NOT to compact**: If the next subtask explicitly depends on detailed output from a just-completed subtask (check `Depends on` column) — keep that specific result in context
4. **Log**: Write to budget.md: `"Auto-compact at score N — freed ~X intermediate results"`
5. **Frequency**: Max 1 auto-compact per wave (don't compact between every subtask)

This replaces the previous "Red = notify user" approach with proactive context management. The orchestrator self-heals before quality degrades.

**Rules**:
- Only notify user at score **7+** (after auto-compact has already fired)
- Never stop work — only compact and optionally notify
- If user explicitly says "continue", respect that even at score 7+
- At score 7+, suggest (don't force) starting a new session
