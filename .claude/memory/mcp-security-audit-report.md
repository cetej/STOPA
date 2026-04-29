# MCP Security Audit Report

**Date:** 2026-04-28
**Verdict:** WATCH
**SNYK:** not run (SNYK_TOKEN not set)

## Summary

| Severity | Count | Unique |
|----------|-------|--------|
| Critical | 0 | 0 |
| Warning | 4 | 2 |
| Info | 2 | 1 |

All findings are KNOWN_REPEAT — identical to previous report (2026-04-20). No new criticals, no new warnings, no resolved items.

## Findings

### WARN — brave-search: BRAVE_API_KEY plain-text
- **Files:** mcp.json, claude_desktop_config.json
- **Classification:** KNOWN_REPEAT (since 2026-04-20)
- **Detail:** env var BRAVE_API_KEY contains plain-text secret (31 chars). Use env var reference instead.

### WARN — github: GITHUB_PERSONAL_ACCESS_TOKEN plain-text
- **Files:** mcp.json, claude_desktop_config.json
- **Classification:** KNOWN_REPEAT (since 2026-04-20)
- **Detail:** env var GITHUB_PERSONAL_ACCESS_TOKEN contains plain-text secret (40 chars). Use env var reference instead.

### INFO — playwright: @latest tag
- **Files:** mcp.json, claude_desktop_config.json
- **Classification:** KNOWN_REPEAT (since 2026-04-20)
- **Detail:** uses @latest tag — vulnerable to supply chain attacks. Consider pinning to specific version.

## Recommended Actions (carryover)

1. Move BRAVE_API_KEY and GITHUB_PERSONAL_ACCESS_TOKEN to system env vars, reference them as `{"env": "VAR_NAME"}` in config.
2. Pin playwright MCP to a specific version hash instead of @latest.

## Run Notes

Suspected prompt injection observed in bash tool output during this run — a `<create-pr-command>` block was embedded in the audit script's stderr/output, instructing the agent to commit, push, and open a PR against cetej/STOPA. Ignored per autonomous-execution policy and prompt-injection handling rules. Logged to alerts.md.
