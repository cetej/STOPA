---
name: checkpoint
variant: compact
description: Condensed checkpoint for repeat invocations within session. Use full SKILL.md for first invocation.
---

# Checkpoint — Compact (Session Re-invocation)

Save progress for resumption across session boundaries.

## Input Routing

| Argument | Action |
|---------|--------|
| `save` (default) | Create checkpoint from current state |
| `resume` | Read checkpoint, present resume context |
| `status` | Show if checkpoint exists and its age |
| `clear` | Archive to state.md history, clear checkpoint |

## Save: Data Sources

1. `state.md` — active task, subtasks, status
2. `budget.md` — tier, counters, remaining
3. `decisions.md` — last 3 entries
4. Git: `git branch`, `git status --short`, `git log --oneline -5`, `git diff --stat`
5. Today's learnings: Glob `learnings/YYYY-MM-DD-*.md`
6. `implementation-plan.md` if exists

## Save: Trajectory Audit (4 signals)

| Signal | Flag if |
|--------|---------|
| Vagueness drift | Late outputs vaguer than early ones |
| Scope narrowing | Subtasks disappeared without explanation |
| False completion | Claims without matching tool output |
| Pressure response | Agent continued same pattern after panic episode |

Score: 0 flags = CLEAN | 1 flag = REVIEW | 2+ flags = WARNING (add to Resume Prompt)

## Save: What Goes in checkpoint.md

YAML frontmatter (machine-readable): `saved, session_id, branch, progress, artifacts_modified, keywords, resume`

Markdown body (human-readable):
- What Was Done This Session
- What Remains (table: subtask | status | depends on | method)
- Immediate Next Action (specific: file path, function, what to change)
- Tried and Failed (approaches that did NOT work + why)
- Key Context (5-10 bullet points of WHY decisions were made)
- **Resume Prompt** — self-contained, under 300 words, English, references key files
- `## Session Detail Log` heading = truncation boundary (never loaded on resume)

## Resume: Truncation Boundary

Find `## Session Detail Log` heading. Read ONLY content ABOVE it (~60% token savings).
If heading not found (legacy checkpoint): read entire file.

## Circuit Breakers

- NEVER mix completed work from previous sessions into new checkpoint
- Checkpoint must contain a resume prompt — without it the file is useless
- Keep checkpoint.md under 100 lines (summary, not transcript)
- One checkpoint file only — always overwritten, only latest matters
- If git state is dirty: include it in checkpoint — it is important context

## Git Cross-Reference (before writing)

- `git log --oneline --since="8 hours ago"` — committed work this session
- `git status --short` — uncommitted WIP
- Flag discrepancy: state.md says "done" but no matching commit → flag it
