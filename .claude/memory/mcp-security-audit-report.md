# MCP Security Audit Report

**Date:** 2026-04-20
**Verdict:** WATCH
**SNYK:** not run (SNYK_TOKEN not set)

## Summary

| Severity | Count | Unique |
|----------|-------|--------|
| Critical | 0 | 0 |
| Warning | 4 | 2 |
| Info | 2 | 1 |

## Findings

### WARN — brave-search: BRAVE_API_KEY plain-text
- **Files:** mcp.json, claude_desktop_config.json
- **Classification:** NEW_WARN
- **Detail:** env var BRAVE_API_KEY contains plain-text secret (31 chars). Use env var reference instead.

### WARN — github: GITHUB_PERSONAL_ACCESS_TOKEN plain-text
- **Files:** mcp.json, claude_desktop_config.json
- **Classification:** NEW_WARN
- **Detail:** env var GITHUB_PERSONAL_ACCESS_TOKEN contains plain-text secret (40 chars). Use env var reference instead.

### INFO — playwright: @latest tag
- **Files:** mcp.json, claude_desktop_config.json
- **Classification:** INFO
- **Detail:** uses @latest tag — vulnerable to supply chain attacks. Consider pinning to specific version.

## Recommended Actions

1. Move BRAVE_API_KEY and GITHUB_PERSONAL_ACCESS_TOKEN to system env vars, reference them as `{"env": "VAR_NAME"}` in config.
2. Pin playwright MCP to a specific version hash instead of @latest.
