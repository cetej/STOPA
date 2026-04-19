---
name: Cross-Project Improvement System
description: System for discovering, routing, and delivering improvement tips to all projects via /improve skill, project profiles, and GitHub issues
type: project
originSessionId: b9fd8a0a-b959-4137-8dd4-133c5f271625
---
Cross-project improvement system implemented 2026-04-14.

**Architecture:** Discovery sources (watch, radar, manual, cross-pollinate) → central routing in STOPA → delivery via GitHub issues (projects with repos) or improvement-backlog.md (projects without repos).

**Components:**
- Project profiles: `~/.claude/memory/projects/*.yaml` (13 projects: STOPA, NG-ROBOT, ADOBE-AUTOMAT, ZACHVEV, POLYBOT, MONITOR, GRAFIK, KARTOGRAF, DANE, BONANZA, ORAKULUM, terminology-db, ADVISORS)
- `/improve` skill: router + GitHub issue delivery (`.claude/commands/improve.md`)
- `/watch` extended: Phase 4 routes HIGH/MED findings via /improve
- `/radar` extended: ADOPT/TRIAL tools routed via /improve
- `/scribe` extended: cross-project routing section for manual "tohle by se hodilo do X"
- SessionStart hook: `improvement-notify.sh` (global, shows open improvement issues)
- Scheduled task: `cross-project-improve-sweep` (Wed+Sat 10am, scans unrouted findings)

**Priority thresholds:**
- high priority projects: relevance_score >= 3
- medium priority projects: relevance_score >= 5
- low priority projects: relevance_score >= 7

**Why:** Previously all findings stayed STOPA-local. This system routes them to where they're actionable.
**How to apply:** When discovering something useful for another project, either invoke `/improve` directly or let /watch and /radar handle routing automatically.
