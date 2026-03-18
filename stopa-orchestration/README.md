# STOPA Orchestration Plugin

Multi-agent orchestration system for Claude Code. Decomposes complex tasks, delegates to specialized agents, controls costs, and maintains shared memory across sessions.

## Skills included

| Skill | Purpose |
|-------|---------|
| `/stopa-orchestration:orchestrate` | Conductor — decomposes tasks, delegates, coordinates |
| `/stopa-orchestration:scout` | Explorer — maps codebase context before changes |
| `/stopa-orchestration:critic` | Reviewer — evaluates quality of outputs |
| `/stopa-orchestration:scribe` | Recorder — documents decisions, learnings, state |
| `/stopa-orchestration:budget` | Cost controller — tracks agent spawns, enforces limits |
| `/stopa-orchestration:checkpoint` | Session manager — saves/restores session state |
| `/stopa-orchestration:watch` | News scanner — weekly AI/ML ecosystem updates |
| `/stopa-orchestration:skill-generator` | Meta-skill — creates and improves other skills |
| `/stopa-orchestration:dependency-audit` | Auditor — checks outdated dependencies |

## Hooks included

- **SessionStart**: Checks for active checkpoint, warns about memory file sizes
- **Stop**: Reminds to record decisions via `/scribe` when a task is active

## Installation

### From local directory (development)
```bash
claude --plugin-dir ./stopa-orchestration
```

### From GitHub
```
/plugin install github.com/cetej/STOPA/stopa-orchestration
```

## Shared memory

The plugin uses `.claude/memory/` in the project directory for persistent state:

| File | Purpose |
|------|---------|
| `state.md` | Current task status |
| `decisions.md` | Decision log with rationale |
| `learnings.md` | Patterns, anti-patterns, skill gaps |
| `budget.md` | Cost tracking and budget limits |
| `checkpoint.md` | Session snapshot for continuity |
| `news.md` | Results from /watch scans |

## Budget tiers

| Tier | Agents | Critic rounds | When |
|------|--------|---------------|------|
| light | 0-1 | 1 | Single file, quick fix |
| standard | 2-4 | 2 | Multi-file changes |
| deep | 5-8 | 3 | Cross-cutting features |

## Quick start

```
/stopa-orchestration:orchestrate implement user authentication
```

The orchestrator will automatically scout, plan, delegate, review, and record learnings.
