---
generated: 2026-04-04
cluster: general-security-environment
sources: 5
last_updated: 2026-04-04
---

# Security, Environment & Ecosystem

> **TL;DR**: Never put secrets in JSON configs (use env vars). Never add Playwright MCP to Claude Desktop (hijacks downloads). Image changes invalidate prompt cache entirely. STOPA is unique in combining skills + memory + orchestration.

## Overview

Security and environment learnings cluster around two critical rules and several operational patterns. The most severe: Playwright MCP (@playwright/mcp) hijacks Chrome's download profile to a temp folder, silently breaking all browser downloads. It must NEVER be added to Claude Desktop or Claude Code configs (ref: 2026-03-27-playwright-mcp-download-hijack.md). Similarly, API keys and tokens must never be written into JSON config files — always use environment variables or .env files excluded from git (ref: 2026-03-27-secrets-in-config-files.md).

Operationally, adding or removing images anywhere in a Claude API prompt invalidates the entire prompt cache, meaning browse/screenshot workflows consistently miss cache and pay full input price every turn. This makes visual automation significantly more expensive than text-only workflows (ref: 2026-04-01-image-cache-invalidation.md). The fal.ai integration on Windows requires the fal-client package (not fal), proper async handling, FAL_KEY env var, and retry logic for timeouts (ref: environment-falai.md).

STOPA's ecosystem positioning remains unique: it combines skill system + shared memory + orchestration, while competitors typically lack the memory layer (ref: ecosystem-scan.md).

## Key Rules

1. **NEVER add Playwright MCP**: hijacks Chrome downloads to temp folder (ref: 2026-03-27-playwright-mcp-download-hijack.md)
2. **NEVER put secrets in JSON configs**: use env vars or .env (ref: 2026-03-27-secrets-in-config-files.md)
3. **Image changes invalidate prompt cache**: plan visual workflows for cache misses (ref: 2026-04-01-image-cache-invalidation.md)
4. **fal.ai: use fal-client, not fal**: Windows-specific quirks (ref: environment-falai.md)

## Patterns

### Do
- Use `FAL_KEY` env var, never hardcode (ref: environment-falai.md)
- Plan for full cache miss on any turn with screenshot changes (ref: 2026-04-01-image-cache-invalidation.md)
- Position STOPA's memory layer as key differentiator (ref: ecosystem-scan.md)

### Don't
- Add @playwright/mcp to any config (ref: 2026-03-27-playwright-mcp-download-hijack.md)
- Write tokens into claude_desktop_config.json or settings.json (ref: 2026-03-27-secrets-in-config-files.md)
- Assume prompt cache works with changing screenshots (ref: 2026-04-01-image-cache-invalidation.md)

## Related Articles

- See also: [pipeline-engineering](pipeline-engineering.md) — API-level model behavior quirks
- See also: [orchestration-infrastructure](orchestration-infrastructure.md) — session management

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-01-image-cache-invalidation](../learnings/2026-04-01-image-cache-invalidation.md) | 2026-04-01 | medium | Image changes invalidate entire prompt cache |
| [2026-03-27-playwright-mcp-download-hijack](../learnings/2026-03-27-playwright-mcp-download-hijack.md) | 2026-03-27 | critical | Playwright MCP hijacks Chrome downloads |
| [2026-03-27-secrets-in-config-files](../learnings/2026-03-27-secrets-in-config-files.md) | 2026-03-27 | critical | Never put secrets in JSON configs |
| [ecosystem-scan](../learnings/ecosystem-scan.md) | 2026-03-23 | low | STOPA unique in skills+memory+orchestration |
| [environment-falai](../learnings/environment-falai.md) | 2026-03-23 | medium | fal.ai Windows: fal-client, async, FAL_KEY |
