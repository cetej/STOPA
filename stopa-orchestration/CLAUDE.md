# stopa-orchestration Plugin

Distribution package for the STOPA orchestration system.
This directory is what gets installed into target projects.

## Structure
- `skills/` — orchestration skills (subset of .claude/skills/)
- `commands/` — command copies (subset of .claude/commands/)
- `hooks/` — hook scripts + hooks.json
- `.claude-plugin/plugin.json` — plugin manifest

## Sync rules
- Source of truth: `.claude/commands/` and `.claude/skills/` in STOPA root
- This directory contains COPIES for distribution
- After editing skills in STOPA, sync here before publishing
- Use `scripts/sync-orchestration.sh` for automated sync

## Target projects
Full list in `~/.claude/memory/projects/`. Primary targets:
- NG-ROBOT (github.com/cetej/NG-ROBOT) — high priority
- ADOBE-AUTOMAT (github.com/cetej/ADOBE-AUTOMAT) — medium
- ZACHVEV, POLYBOT, MONITOR — medium

## Installation methods
1. Marketplace via `settings.json` (recommended)
2. `claude --plugin-dir ./stopa-orchestration` (local dev)
3. `/plugin install` CLI command

## Namespace
Skills installed via plugin use namespace: `/stopa-orchestration:<skill-name>`
Skills synced directly use no namespace: `/<skill-name>`
