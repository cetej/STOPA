---
date: 2026-03-23
type: anti_pattern
severity: high
component: skill
tags: [youtube, transcript, yt-dlp, mcp]
summary: "MCP youtube-transcript server broken since 2026-03. Use yt-dlp CLI as primary, MCP only as fallback."
source: auto_pattern
---

# MCP youtube-transcript je broken — vždy použij /youtube-transcript skill (yt-dlp)

MCP server `youtube-transcript` od 2026-03 nefunguje (vrací "Video unavailable" i pro dostupná videa).

**Anti-pattern:** Zkoušet MCP tool → selže → fallback na browser navigaci → teprve pak skill.

**Správný postup:** Při jakémkoli YouTube URL rovnou spustit `/youtube-transcript` skill, který používá `yt-dlp` (lokálně nainstalovaný, funkční).

**Why:** Ztráta času (browser navigace, reklamy, ruční hledání transkriptu) vs. 10 sekund přes yt-dlp.

**How to apply:** Vidíš YouTube URL → `/youtube-transcript`. Žádný MCP tool, žádný browser.
