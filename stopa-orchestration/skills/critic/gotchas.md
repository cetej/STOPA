# Critic — Gotchas

Known failure modes. Add a line each time Claude trips on something.

## Scope Creep
- **Critic tries to fix code** — critic REPORTS issues, never implements. If it starts editing, it's broken
- **Reviewing unchanged code** — focus only on diff/changed files, not entire codebase
- **Style nitpicking** — don't flag style issues unless they break conventions defined in CLAUDE.md

## False Positives
- **Flagging valid patterns as bugs** — check project conventions before reporting. What looks wrong in general may be correct here
- **Import order complaints** — project may have specific import conventions, read CLAUDE.md first

## Loop Risks
- **Same issue reported twice** — if critic already flagged it, don't flag again. Check previous critic output
- **Circular feedback** — critic says "add error handling" → implementer adds → critic says "too much error handling" → STOP, ask user

## Context
- **Missing project context** — always read state.md and learnings.md before reviewing. Without context, reviews are generic and useless
- **Reviewing generated code** — auto-generated files (migrations, lockfiles) should be skipped
