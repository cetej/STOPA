# Orchestrate — Gotchas

Known failure modes. Add a line each time Claude trips on something.

## Agent Spawning
- **Explore agents can't respond to shutdown** — use `subagent_type: "general-purpose"` for audit/research, not Explore (lacks SendMessage)
- **Duplicate work on spawn** — put full instructions in spawn prompt; SendMessage is for follow-up only, not "start working"
- **Unbounded agent spawning** — enforce tier limits (Light=0-1, Standard=2-4, Deep=5-8) or tokens spiral
- **Agents sharing files → overwrite conflicts** — assign file ownership per agent in spawn template; each agent edits ONLY its owned files
- **Agent idle without work → wasted tokens** — always assign explicit tasks in spawn prompt; vague roles ("help out") lead to agents doing nothing

## Critic Loop
- **Infinite critic→fix→critic cycle** — max 2 FAIL verdicts on same target, then circuit breaker → ask user
- **Critic on trivial changes** — Light tier = 1× critic at end, not after every edit

## Over-Orchestration
- **Trivial edits don't need full pipeline** — single file fix = do it directly, don't spawn scout→plan→execute→critic→scribe
- **Budget tier must be set BEFORE scouting** — start lowest viable, upgrade only if scout reveals complexity

## Memory
- **Memory files > 500 lines** — triggers maintenance, archive old entries before they bloat
- **state.md stale data** — always read state.md at start, don't assume previous session state is current

## Context Compaction
- **Haiku summarizer can lose nuance** — if agent reported DONE_WITH_CONCERNS, always read the full `concerns` array directly from JSON, don't rely on `compactSummary` alone
- **Scratchpad ≠ state.md** — scratchpad tracks intermediate work products, state.md tracks task/subtask status. Don't conflate them.
- **Don't compact small results** — if agent output is <20 lines, skipping summarization is cheaper. Only compact when `details` field is substantial.

## Windows
- **Port 8000 occupied** — `taskkill //F //IM python.exe` before restarting API servers
- **File locking by antivirus** — retry with short pause if write fails
