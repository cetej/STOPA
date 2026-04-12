---
name: OpenFreeMap requires TileJSON fetch
description: Vector tiles URL must be fetched from TileJSON endpoint, not hardcoded - URL is versioned
type: feedback
---

OpenFreeMap tile URL is versioned and changes periodically. NEVER hardcode tile URL like `tiles.openfreemap.org/planet/{z}/{x}/{y}.pbf`.

**Why:** The actual URL is `tiles.openfreemap.org/planet/20260401_001001_pt/{z}/{x}/{y}.pbf` (with date-based version). Hardcoding returns 404.

**How to apply:** Always fetch TileJSON first: `fetch('https://tiles.openfreemap.org/planet')` → `json.tiles[0]`, then use that URL for the vector source.
