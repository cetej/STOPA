---
date: 2026-03-27
type: architecture
severity: critical
component: skill
tags: [commands, skills, structure, source-of-truth, destructive-error]
summary: "STOPA has TWO skill locations: commands/ (flat) and skills/ (dirs). They MUST stay identical. Edit commands/ as source, sync to skills/."
---

# STOPA has TWO skill locations — commands/ AND skills/

## Structure

```
.claude/
├── commands/       ← CANONICAL versions (flat files: watch.md, autoloop.md...)
├── skills/         ← SKILL.md copies (directories: watch/SKILL.md, autoloop/SKILL.md...)
```

Both must exist and be IDENTICAL. The commands/ versions are the ones that were iteratively improved (autoresearch, RLM, Tier 4 voices, guard mode, semi-formal reasoning etc.).

## History

Commit `801f80a` — "commands-over-skills split" moved canonical versions to commands/.
Skills/ copies exist for compatibility with the plugin distribution system.

## Rule

1. ALWAYS check `ls .claude/` at session start — know the full structure
2. NEVER create a new skill in skills/ without checking if it exists in commands/
3. When editing a skill: edit commands/ first, then sync to skills/
4. Before ANY file overwrite: diff against ALL existing versions (commands/, skills/, target projects, git history)

## Incident (2026-03-27)

Agent created new inferior versions in skills/ without knowing commands/ existed.
Lost: autoresearch pattern, guard mode, Tier 4 voices, semi-formal reasoning, anti-rationalization tables, crash recovery protocol.
All recovered from commands/ (which were untouched).
