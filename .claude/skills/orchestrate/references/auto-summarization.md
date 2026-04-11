# Auto-Summarization of Agent Results

After an agent completes and writes to `.claude/memory/intermediate/<subtask-id>.json`:

## Step 1 — Read status
Check `status` and `concerns` fields from the JSON (lightweight read).

## Step 2 — Spawn Haiku summarizer (skip if agent output was <20 lines)

```
Agent(model: "haiku", prompt: "
  Summarize this agent's work in 1-2 factual sentences.
  Focus on: what files changed, what was accomplished, any concerns.
  Include specific filenames and numbers.

  Agent: <agent name>
  Status: <status code>
  Files changed: <filesChanged array>
  Details: <first 3000 chars of details field>

  Return ONLY the summary, nothing else.
")
```

## Step 3 — Update the JSON
Write the Haiku summary to a new `compactSummary` field in the intermediate JSON.

## Step 4 — Append to scratchpad

Add a row to `.claude/memory/intermediate/scratchpad.md`:
```
| <next #> | <HH:MM> | <agent name> | <compactSummary> |
```

Create the scratchpad with header if it doesn't exist:
```markdown
# Scratchpad — Accumulated Context

## Wave Summary
| # | Time | Source | Summary |
|---|------|--------|---------|

## Files Modified
| File | Lines Changed | Wave | Agent |
|------|--------------|------|-------|

## Errors Encountered
| Error | File | Wave | Resolution | Status |
|-------|------|------|-----------|--------|

## Key Decisions
| Decision | Rationale | Wave |
|---------|----------|------|

## Routing Log (BIGMAS-inspired, deep tier only)
| Wave | Decision | Reason | Agents So Far | Budget Remaining |
|------|----------|--------|--------------|-----------------|
```

**Populating the new sections** (after each wave):
- **Files Modified**: Extract from agent Status block `filesChanged` array. One row per file.
- **Errors Encountered**: Extract from agent `concerns` field. Mark `resolved` if a subsequent wave addresses it, `open` otherwise.
- **Key Decisions**: Record any non-trivial choice made by an agent (architecture, library selection, approach). Extract from agent output or infer from git diff.

## Step 5 — Context rule

The orchestrator's decision-making uses ONLY `compactSummary` + `status` + `concerns` fields. Never load `details` unless debugging a failure or performing final synthesis (Phase 5).

## When to skip

- Light tier (≤2 agents) — direct return is fine, no need for disk overhead
- Agent output is trivially short (<20 lines)
- Agent returned BLOCKED — read the full output immediately to understand the blocker

## Deep tier token optimization

- When spawning agents in deep tier, use `model: "sonnet"` for implementation agents (save opus for planning/coordination)
- Use extended thinking `display: "omitted"` on API-level agent calls when available — strips thinking blocks from response, saves context tokens while preserving multi-turn signatures
- Prefer returning structured summaries from agents over raw output — reduces context consumption in the orchestrator

## Agent Status Code Protocol

Every spawned agent MUST end its response with a Status block (included in the prompt template).

**Orchestrator handling:**

| Status | Action |
|--------|--------|
| DONE | Accept, proceed to critic (if tier warrants) |
| DONE_WITH_CONCERNS | Accept, pass concerns as extra context to critic |
| NEEDS_CONTEXT | Re-dispatch with requested context (doesn't count as retry) |
| BLOCKED | Attempt resolution. If unresolvable → 3-fix escalation applies |

## After each subtask

1. Parse agent Status block. Handle per the table above.
2. Update `.claude/memory/budget.md` — increment counters for any agents/critics used
3. Update `.claude/memory/state.md` — set subtask to `done` (or `blocked:<dep#>` if BLOCKED). Note concerns if DONE_WITH_CONCERNS
4. **Budget gate**: Check if any counter hit its limit. If yes → stop and report to user
5. **De-sloppify check** (standard/deep tier only, skip for light/farm): Spawn a Haiku agent to scan files changed by the subtask (`git diff --name-only` vs pre-subtask state). Check for:
   - `console.log(` / `print(` debugging leftovers (ignore if inside logging/debug modules)
   - `TODO` / `FIXME` / `HACK` markers introduced in this subtask (not pre-existing)
   - Inconsistent naming: mixed camelCase/snake_case in the same file
   - Commented-out code blocks (3+ consecutive commented lines)
   Report format: list of findings with file:line. **Non-blocking** — log findings but don't fail the subtask. If findings > 0, append to the subtask's concerns for critic review. If 0 findings, skip silently.
6. Invoke `/critic` if tier allows another round. For **light tier**, skip critic on individual subtasks — only run once at the end. If agent reported DONE_WITH_CONCERNS, pass those concerns as extra context to critic. Include de-sloppify findings (step 5) as additional context.
7. If critic returns FAIL → re-execute ONCE. If FAIL again → **circuit breaker** → escalate to user with findings
8. Log decisions to `.claude/memory/decisions.md` via scribe pattern
