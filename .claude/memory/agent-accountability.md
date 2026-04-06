# Agent Accountability (HERA-inspired)

Rolling 30-day agent performance tracking. Updated by orchestrator in Phase 6.
HERA source: arXiv:2604.00901 — per-agent failure attribution enables targeted improvement.

## How to use

- Orchestrator reads before agent assignment (Phase 3)
- Agent with >20% failure rate on a failure_class → assign stronger model or different agent
- Agent with 0% failures → preferred for critical subtasks
- After 2+ failures same agent+class → trigger `/learn-from-failure`

## Performance Table

| Date | Agent/Skill | Task | Failure Class | Result | Notes |
|------|-------------|------|---------------|--------|-------|
| — | — | — | — | — | (no data yet) |

## Summary (auto-generated after 10+ entries)

| Agent/Skill | Total Tasks | Failures | Failure Rate | Top Failure Class |
|---|---|---|---|---|
| — | — | — | — | — |

## Maintenance

- Entries older than 30 days → archive to `agent-accountability-archive.md`
- Summary table regenerated when new entries added
- Max 100 entries before archive
