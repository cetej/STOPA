---
id: scout-003
skill: scout
title: Explores the memory system and reports key files
eval-tags: [codebase_search, file_operations, memory_write]
ideal_steps: 5
ideal_tool_calls: 4
max_acceptable_steps: 9
fixture: live-repo
---

# Eval Case: Explores the memory system and reports key files

Tests that `/scout` understands the memory hierarchy — top-level files, learnings subdirectory, archive files.

## Fixture

`live-repo` — STOPA repository. Known structure in `.claude/memory/`:
- `state.md`, `budget.md`, `checkpoint.md`, `decisions.md`, `news.md`
- `learnings/` subdirectory with per-file YAML learnings
- `*-archive.md` files for old entries
- `eval-baseline.tsv` (may or may not exist)

## Invocation

```
/scout .claude/memory/
```

## Assertions

| # | Type | Check | Expected |
|---|------|-------|----------|
| A1 | contains | Output mentions `budget.md` | true |
| A2 | contains | Output mentions `state.md` or `checkpoint.md` | true |
| A3 | contains | Output mentions `learnings/` directory | true |
| A4 | contains | Output describes the memory system's purpose or architecture | true |

## Scoring

- 4 assertions pass: PASS
- 2-3 assertions pass: PARTIAL
- 0-1 assertions pass: FAIL

## Why This Matters

The memory system is central to STOPA's session continuity. Scout must understand hierarchical structures (files + subdirectories) and report them coherently.
