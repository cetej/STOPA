---
name: MapLibre PBF font format gotcha
description: MapLibre glyph PBF width/height must be WITHOUT SDF buffer — bitmap is (w+6)*(h+6). Broken fonts kill ALL vector layers silently.
type: feedback
---

MapLibre PBF glyph format: `width` and `height` in the protobuf are the RAW glyph dimensions WITHOUT the 3px SDF buffer. The bitmap has `(width + 6) * (height + 6)` bytes. MapLibre adds the buffer internally.

**Why:** Spent hours debugging because a custom Python PBF generator reported padded dimensions. The mismatch caused "mismatched image size" errors that silently broke ALL vector rendering (not just labels).

**How to apply:** When building MapLibre font PBFs (KARTOGRAF, any map project), always validate with `bitmap_length == (width + 2*3) * (height + 2*3)`. Also: SDF edge = 192 (not 128), never serve empty PBF stubs (they break fontstack fallback).
