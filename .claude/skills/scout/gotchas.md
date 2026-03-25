# Scout — Gotchas

Known failure modes. Add a line each time Claude trips on something.

## Search Strategy
- **Too broad search** — start with specific file patterns (Glob), fall back to Grep only if needed. Don't read entire directories
- **Missing naming conventions** — project may use Czech names, camelCase, snake_case, or mixed. Search for all variants
- **Greenfield confusion** — if directory doesn't exist yet, report that cleanly instead of searching endlessly

## Reporting
- **Too much detail** — scout report should be actionable summary, not a dump of every file found. Key files + patterns + scope estimate
- **Missing scope estimate** — always include: how many files affected, complexity tier suggestion, dependencies

## Context
- **Not reading learnings/critical-patterns.md first** — previous sessions may have already explored this area. Check before re-exploring
- **Ignoring git history** — `git log --oneline -20` reveals recent changes and intent. Use it

## Performance
- **Agent spawning for simple searches** — if it's 1-2 Glob/Grep calls, do it directly. Don't spawn sub-agents for trivial lookups
- **Large binary files** — skip .npy, .parquet, images. They appear in Glob results but can't be meaningfully read
