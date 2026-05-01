# Radar Proposals — Brain-sourced findings awaiting review

Items here came from `brain-ingest` LLM classification (action_class ∈ {tool, library, mcp-server, cli}).
They are NOT yet in radar.md. Reviewed during `/radar` runs — user accepts/rejects per row.

**Audit invariants (issue #24):**
- Every entry has `source: brain-watch` (or equivalent ingest pipeline)
- Dedup checked against radar.md + this file before append
- Hook never writes to brain/* — no recursion possible

| Date | Tool | Action class | URL | Source | Key idea | Status |
|------|------|--------------|-----|--------|----------|--------|
| 2026-04-27 | [Qwen3.6-27B](https://huggingface.co/Qwen/Qwen3.6-27B) | library | https://huggingface.co/Qwen/Qwen3.6-27B | brain-watch | Anthropic dočasně změnila ceny Claude Code na 100$/měsíc, GitHub Copilot upravil limity kvůli agentním workflowům a Qwen vydal výkonný open-weight model Qwen3.6-27B s 27B parametry. | rejected |
| 2026-04-30 | [honker](https://github.com/russellromney/honker) | library | https://github.com/russellromney/honker | brain-watch | Simon Willison shrnuje zajímavé technologie z 24. dubna 2026: SQLite rozšíření honker pro queues/streams, postmortem bugů v Claude Code, nový model DeepSeek V4 a kritiku AI automatizace od Nilay Patel | accepted |
| 2026-05-01 | [FlashRT](https://github.com/Wang-Yanting/FlashRT) | tool | https://github.com/Wang-Yanting/FlashRT | brain-watch | FlashRT je framework pro optimalizační útoky na long-context LLM (prompt injection, knowledge corruption), který dosahuje 2-7× rychlejšího běhu a 2-4× nižší spotřeby paměti oproti existujícím metodám. | pending |


## Resolved

| Date resolved | Tool | Decision | Notes |
|---------------|------|----------|-------|
| 2026-04-30 | Qwen3.6-27B | rejected (4/10 🟢) | Open-weight model release; STOPA je Claude-native, Gate 1 marginal fail, score 4 |
| 2026-04-30 | honker | accepted (5/10 🟡) | SQLite queues/streams; Simon Willison signal; relevant pro durable queue pattern; added to radar.md Watch List |
