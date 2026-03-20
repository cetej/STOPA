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
| `/stopa-orchestration:autoloop` | Optimizer — Karpathy Loop pattern for iterative file improvement |
| `/stopa-orchestration:project-init` | Initializer — sets up new project with .claude/ structure |

## Hooks included

- **SessionStart**: Checks for active checkpoint, warns about memory file sizes
- **PostCompact**: Reminds to checkpoint after context compaction
- **Stop**: Reminds to record decisions via `/scribe` when a task is active

## Installation

### Method 1: Marketplace via settings.json (recommended)

Add this to `.claude/settings.json` in your project — plugin auto-installs from GitHub:

```json
{
  "extraKnownMarketplaces": {
    "stopa-tools": {
      "source": {
        "source": "github",
        "repo": "cetej/STOPA"
      }
    }
  },
  "enabledPlugins": {
    "stopa-orchestration@stopa-tools": true
  }
}
```

Merge with your existing settings.json (add the two keys alongside existing `hooks`, `env`, etc.). Skills become available after CC restart.

### Method 2: Plugin install (CLI)
```
/plugin install github.com/cetej/STOPA --subdir stopa-orchestration
```

### Method 3: Local directory (development)
```bash
claude --plugin-dir ./stopa-orchestration
```

> **Note**: Since v2.1.76, `--plugin-dir` accepts only one path per flag. Use repeated flags for multiple plugins.

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
