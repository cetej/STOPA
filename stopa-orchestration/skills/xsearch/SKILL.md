---
name: xsearch
description: Use when searching for code or patterns across all registered projects. Trigger on search across projects, cross-project search. Do NOT use for single-project searches.
argument-hint: <search pattern> [--type py|ts|md] [--project name]
tags: [exploration, orchestration]
phase: meta
effort: low
user-invocable: true
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Agent"]
---

# Cross-Project Search

Search across all registered projects for code patterns, learnings, and configurations.

## Instructions

1. **Read project registry**: Check if `~/.claude/memory/projects.json` exists. If not, fall back to known project paths from CLAUDE.md (Cílové projekty section).
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
   - Grep `.claude/memory/learnings/` in current project for the search pattern
6. **Output format**:

```
<!-- CACHE_BOUNDARY -->

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

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "The pattern returned 100+ matches, but I'll show them all since the user might want everything" | Dumping 100+ matches overwhelms the user and buries the useful signal | Enforce the 5-match-per-project cap; if total exceeds 100, stop and ask the user to narrow the query before continuing |
| "Project X path doesn't exist locally so I'll just silently skip it" | Silently skipping a project means the user thinks it was searched when it wasn't — a false negative | Note every skipped project explicitly in the summary with the reason (path missing, archived, etc.) |
| "I'll skip the learnings cross-reference since the main results look complete" | Learnings contain captured patterns and known pitfalls that won't appear in code search — they are a separate and complementary signal | Always run the learnings Grep as Step 5, even when code search found matches |
| "The registry file doesn't exist, so I'll only search the current project" | Falling back to CLAUDE.md's Cílové projekty section is explicitly defined — single-project search defeats the purpose of this skill | Read CLAUDE.md fallback paths and search all listed projects, noting that the registry is missing |

## Rules

1. Never modify files in other projects — read-only
2. Skip projects not cloned locally (note in summary)
3. Report which projects were searched vs skipped
4. If 100+ matches: ask user to narrow the query before showing results
