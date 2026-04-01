# Quality Gates — Per-Project Criteria

Gates are concrete, testable pass/fail checks that /critic applies automatically.
They compound: when /critic repeatedly catches the same issue type, it proposes a new gate.

## Active Gates

| # | Gate | Check | Source | Added |
|---|------|-------|--------|-------|
| G1 | Python files set UTF-8 encoding | Grep for `reconfigure(encoding=` in new/changed .py files with I/O | rules/python-files.md | 2026-04-01 |
| G2 | No bare print() in production code | Grep for `print(` in changed .py files (exclude tests/, scripts/) | rules/python-files.md | 2026-04-01 |
| G3 | Skill description starts with "Use when" | Read YAML frontmatter of changed SKILL.md files | core-invariants #3 | 2026-04-01 |
| G4 | No secrets in JSON config files | Grep for API key patterns in changed .json files | core-invariants #4 | 2026-04-01 |
| G5 | commands/ and skills/ copies are identical | Diff changed command against its skills/ copy | core-invariants #2 | 2026-04-01 |

## Gate Lifecycle

- **Proposal**: /critic finds same issue type 2+ times across reviews -> proposes new gate in "Gate Proposals" output section
- **Activation**: User approves -> gate added to Active Gates table with next # and date
- **Tightening**: Gate triggers frequently (5+ times) -> candidate for promotion to core-invariants.md or a linter hook
- **Pruning**: Gate never triggers in 10+ consecutive reviews -> candidate for removal (flag in /evolve)

## Gate Proposal Log

Track proposed gates and their status. /critic appends here, user approves/rejects.

| Date | Proposed Gate | Trigger Count | Status |
|------|---------------|---------------|--------|
| _(none yet)_ | | | |
