---
name: mcp-scan security scanner
description: Invariant Labs tool for detecting MCP tool poisoning attacks via hidden docstring instructions — run on all MCP configs
type: reference
---

**mcp-scan** (Invariant Labs, 2026-04-01): lokalni scanner detekujici tool poisoning utoky pres MCP docstrings.

**Utok**: Kompromitovany MCP server skryje instrukce do neviditelnych casti tool definice (description, parameter hints). Model je poslecha jako systemove instrukce. Jeden server muze ovladnout cely agent kontext vcetne exfiltrace env vars.

**Kde**: https://github.com/invariantlabs-ai/mcp-scan (npx mcp-scan)

**How to apply:** Spustit `npx mcp-scan` na kazdem stroji kde bezi Claude Code/Desktop s MCP servery. Zvlast po pridani noveho MCP serveru. Prioritne zkontrolovat community/third-party servery (brave-search, context7, filesystem) — officalni Anthropic servery maji nizsi riziko.
