---
generated: 2026-04-04
cluster: general-security-environment
sources: 4
last_updated: 2026-04-07
---

# Security, Environment & Ecosystem

> **TL;DR**: Never put secrets in JSON configs (use env vars). Never add Playwright MCP to Claude Desktop (hijacks downloads). Image changes invalidate prompt cache entirely. LlamaFirewall PromptGuard (BERT, 19-92ms) is ADOPT for tool output scanning; CaMeL capability tagging is ADOPT as STOPA convention.

## Overview

Security and environment learnings cluster around two critical rules and several operational patterns. The most severe: Playwright MCP (@playwright/mcp) hijacks Chrome's download profile to a temp folder, silently breaking all browser downloads. It must NEVER be added to Claude Desktop or Claude Code configs (ref: 2026-03-27-playwright-mcp-download-hijack.md). Similarly, API keys and tokens must never be written into JSON config files — always use environment variables or .env files excluded from git (ref: 2026-03-27-secrets-in-config-files.md).

Operationally, adding or removing images anywhere in a Claude API prompt invalidates the entire prompt cache, meaning browse/screenshot workflows consistently miss cache and pay full input price every turn (ref: 2026-04-01-image-cache-invalidation.md).

Defense framework evaluation (2026-04-05) produced clear verdicts: LlamaFirewall PromptGuard 2 (BERT classifier, 19-92ms, pip install, AUC 0.98) is ADOPT for tool output scanning in content-sanitizer.py as ML-based detection for zero-day injection patterns. CodeShield (Semgrep+regex, ~70ms, 50+ CWE patterns) is ADOPT for security scanning. AlignmentCheck (860ms+, Together API) is WATCH — too slow for synchronous hooks, viable as async audit. CaMeL full implementation is SKIP (research artifact), but its capability tagging pattern — marking tool outputs as `[UNTRUSTED]` and blocking direct use in privileged tools — is ADOPT as a STOPA prompt convention (ref: 2026-04-05-agent-defense-frameworks.md).

## Key Rules

1. **NEVER add Playwright MCP**: hijacks Chrome downloads to temp folder (ref: 2026-03-27-playwright-mcp-download-hijack.md)
2. **NEVER put secrets in JSON configs**: use env vars or .env (ref: 2026-03-27-secrets-in-config-files.md)
3. **Image changes invalidate prompt cache**: plan visual workflows for cache misses (ref: 2026-04-01-image-cache-invalidation.md)
4. **PromptGuard ADOPT**: add to content-sanitizer.py as ML injection detector (ref: 2026-04-05-agent-defense-frameworks.md)
5. **[UNTRUSTED] tagging ADOPT**: tag external tool outputs; block in privileged tool contexts (ref: 2026-04-05-agent-defense-frameworks.md)

## Patterns

### Do
- Tag tool outputs from external sources as `[UNTRUSTED]` in state.md (ref: 2026-04-05-agent-defense-frameworks.md)
- Add PromptGuard + CodeShield as layers behind regex patterns in content-sanitizer.py (ref: 2026-04-05-agent-defense-frameworks.md)
- Plan for full cache miss on any turn with screenshot changes (ref: 2026-04-01-image-cache-invalidation.md)

### Don't
- Add @playwright/mcp to any config (ref: 2026-03-27-playwright-mcp-download-hijack.md)
- Write tokens into claude_desktop_config.json or settings.json (ref: 2026-03-27-secrets-in-config-files.md)
- Use AlignmentCheck as synchronous hook — 860ms+ is too slow (ref: 2026-04-05-agent-defense-frameworks.md)

## Related Articles

- See also: [hook-infrastructure](hook-infrastructure.md) — hook-level security patterns
- See also: [pipeline-engineering](pipeline-engineering.md) — API-level model behavior quirks
- See also: [orchestration-infrastructure](orchestration-infrastructure.md) — session management

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-05-agent-defense-frameworks](../learnings/2026-04-05-agent-defense-frameworks.md) | 2026-04-05 | medium | LlamaFirewall PromptGuard ADOPT; CaMeL tagging ADOPT |
| [2026-04-01-image-cache-invalidation](../learnings/2026-04-01-image-cache-invalidation.md) | 2026-04-01 | medium | Image changes invalidate entire prompt cache |
| [2026-03-27-playwright-mcp-download-hijack](../learnings/2026-03-27-playwright-mcp-download-hijack.md) | 2026-03-27 | critical | Playwright MCP hijacks Chrome downloads |
| [2026-03-27-secrets-in-config-files](../learnings/2026-03-27-secrets-in-config-files.md) | 2026-03-27 | critical | Never put secrets in JSON configs |
