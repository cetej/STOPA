# Radar Proposals — Brain-sourced findings awaiting review

Items here came from `brain-ingest` LLM classification (action_class ∈ {tool, library, mcp-server, cli}).
They are NOT yet in radar.md. Reviewed during `/radar` runs — user accepts/rejects per row.

**Audit invariants (issue #24):**
- Every entry has `source: brain-watch` (or equivalent ingest pipeline)
- Dedup checked against radar.md + this file before append
- Hook never writes to brain/* — no recursion possible

| Date | Tool | Action class | URL | Source | Key idea | Status |
|------|------|--------------|-----|--------|----------|--------|

## Resolved

| Date resolved | Tool | Decision | Notes |
|---------------|------|----------|-------|
