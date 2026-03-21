# Verify — Gotchas

Known failure modes. Add a line each time Claude trips on something.

## Execution
- **Running destructive commands** — verify should be READ-ONLY. Never drop tables, delete files, or modify state during verification
- **Missing venv activation** — Python scripts may fail if run outside the project's virtual environment
- **Hardcoded paths** — test scripts may have paths that work on one machine but not another

## Scope
- **Verifying too much** — focus on what changed, not the entire system. Use git diff to scope
- **Skipping integration** — unit checks pass but end-to-end fails. Always include at least one integration check
- **External dependencies** — API endpoints, databases, or services may be down. Report as SKIP, not FAIL

## Reporting
- **"It works" without evidence** — always show actual output. Screenshot or terminal output
- **Hiding failures** — report ALL failures, even minor ones. Don't cherry-pick passing checks
