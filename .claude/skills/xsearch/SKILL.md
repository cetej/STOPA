---
name: xsearch
description: "Use when searching for code, patterns, or learnings across all registered projects. Trigger on 'search across projects', 'find in all repos', 'where is this used', 'cross-project search'. Do NOT use for searching within the current project only — use Grep/Glob directly."
user-invocable: true
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Agent"]
---

# Cross-Project Search

Search across all registered projects for code patterns, learnings, and configurations.

## Instructions

1. **Read project registry**: `~/.claude/memory/projects.json`
2. **Parse search query** from user input — extract:
   - Pattern (regex or keyword)
   - Optional filters: project name, file type, component
3. **Execute parallel search** across all active projects:
   - For each project in registry, run Grep with the pattern
   - Use Agent tool with subagent_type=Explore and model=haiku for parallel searches if 4+ projects
   - Skip projects with `status: "archived"`
4. **Aggregate results**:
   - Group by project
   - Show file path, line number, matching line
   - Limit to 5 matches per project (show count if more)
5. **Cross-reference with learnings**:
   - Also search `~/.claude/memory/cross-project-learnings.md`
   - Also search `~/.claude/memory/learnings/` in current project
6. **Output format**:

```
## Results for "{query}"

### PROJECT_NAME (N matches)
- `path/to/file.py:42` — matching line content
- `path/to/other.py:15` — matching line content

### PROJECT_NAME_2 (N matches)
- ...

### Learnings
- [date] relevant learning if found
```

## Edge Cases

- If no matches found: suggest alternative search terms
- If pattern is too broad (100+ matches): ask user to narrow down
- If project path doesn't exist: skip silently, note in summary
