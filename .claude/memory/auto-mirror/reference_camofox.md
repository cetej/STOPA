---
name: reference_camofox
description: Camofox-browser — anti-detection browser MCP for AI agents, integrated as Priority 0 in /browse skill
type: reference
---

Camofox-browser (jo-inc/camofox-browser, 2K stars, MIT, YC W24) wraps Camoufox Firefox fork with C++ fingerprint spoofing.
Bypasses Google, Cloudflare, most bot detection. REST API on localhost:9377.

**Integration**: MCP server at `scripts/camofox-mcp.py` (FastMCP + httpx). Registered in `~/.claude/mcp.json`.
8 tools: camofox_open, camofox_snapshot, camofox_click, camofox_type, camofox_navigate, camofox_screenshot, camofox_close, camofox_press.

**Browse skill**: Priority 0 backend (above agent-browser) for anti-detection scenarios.

**Setup**: `git clone github.com/jo-inc/camofox-browser && npm install && npm start` (port 9377, ~300MB Camoufox download on first run).

**Risks**: bus-factor 1 (single maintainer), /tmp file leak on crashes (issue #58), no native MCP.
**Score**: 7.5/10 ADOPT.
