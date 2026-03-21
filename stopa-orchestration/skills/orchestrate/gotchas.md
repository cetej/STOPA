# Orchestrate — Gotchas

Known failure modes. Add a line each time Claude trips on something.

## Agent Spawning
- **Explore agents can't respond to shutdown** — use `subagent_type: "general-purpose"` for audit/research, not Explore (lacks SendMessage)
- **Duplicate work on spawn** — put full instructions in spawn prompt; SendMessage is for follow-up only, not "start working"
- **Unbounded agent spawning** — enforce tier limits (Light=0-1, Standard=2-4, Deep=5-8) or tokens spiral

## Critic Loop
- **Infinite critic→fix→critic cycle** — max 2 FAIL verdicts on same target, then circuit breaker → ask user
- **Critic on trivial changes** — Light tier = 1× critic at end, not after every edit

## Over-Orchestration
- **Trivial edits don't need full pipeline** — single file fix = do it directly, don't spawn scout→plan→execute→critic→scribe
- **Budget tier must be set BEFORE scouting** — start lowest viable, upgrade only if scout reveals complexity

## Memory
- **Memory files > 500 lines** — triggers maintenance, archive old entries before they bloat
- **state.md stale data** — always read state.md at start, don't assume previous session state is current

## Windows
- **Port 8000 occupied** — `taskkill //F //IM python.exe` before restarting API servers
- **File locking by antivirus** — retry with short pause if write fails
