---
name: Preview tool cannot render MapLibre/WebGL
description: Claude Preview MCP has 0x0 viewport - cannot verify MapLibre GL maps visually
type: feedback
---

The Claude Preview MCP tool has a headless viewport of 0x0 pixels. MapLibre GL requires a real viewport for WebGL rendering. `onLoad` never fires, screenshots timeout.

**Why:** Headless browser has no GPU/viewport.

**How to apply:** For MapLibre changes, verify via: build check (tsc + vite build), console error check, network request check, API endpoint tests. Don't waste time trying screenshot/snapshot. Tell user to test in real browser.
