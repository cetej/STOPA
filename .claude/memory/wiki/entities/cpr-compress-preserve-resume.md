---
name: CPR (Compress-Preserve-Resume)
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mbif-cpr-research, mbif-cpr-implementation-plan]
tags: [memory, session, claude-code]
---

# CPR (Compress-Preserve-Resume)

> 3-command session persistence system: `/preserve` (CLAUDE.md ≤280 lines), `/compress` (structured session log with confidence keywords), `/resume` (grep-based restoration).

## Key Facts

- Created by EliaAlberti (ref: sources/mbif-cpr-research.md)
- 3-layer memory: CLAUDE.md (permanent) → session log summaries (searchable) → raw log (archive) (ref: sources/mbif-cpr-research.md)
- Hard truncation boundary: `## Raw Session Log` heading; `/resume` loads only text above it (ref: sources/mbif-cpr-research.md)
- Confidence keywords in session logs serve as lightweight inverted index for grep retrieval (ref: sources/mbif-cpr-research.md)
- `(PROTECTED)` / `(ARCHIVABLE)` inline section markers in headings (ref: sources/mbif-cpr-research.md)
- Requires `claude config set --global autoCompact false` — critical prerequisite (ref: sources/mbif-cpr-research.md)
- HIGH/LOW SIGNAL filter: rationale + next steps = HIGH; implementation details = LOW (ref: sources/mbif-cpr-research.md)

## Relevance to STOPA

Truncation boundary pattern already adopted in STOPA checkpoint.md. Confidence keywords concept is useful for learnings/ grep retrieval. The 280-line CLAUDE.md limit is more aggressive than STOPA's approach.

## Mentioned In

- [MBIF vs CPR Research](../sources/mbif-cpr-research.md)
- [MBIF/CPR Implementation Plan](../sources/mbif-cpr-implementation-plan.md)
