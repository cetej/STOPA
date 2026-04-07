---
date: 2026-03-30
type: architecture
severity: medium
component: memory
tags: [memory, orchestration, research]
summary: >
  CALM paper (Shao et al., Tencent/Tsinghua) validates "semantic bandwidth per step" as design axis.
  Applied to STOPA: table format 2-3x denser than prose for memory files. decisions.md compressed
  135→25 lines, news.md 351→105 lines with zero information loss (archived, not deleted).
source: external_research
uses: 1
harmful_uses: 0
verify_check: "Glob('.claude/memory/decisions.md') → 1+ matches"
related:
  - 2026-03-29-claudini-autoresearch-loop.md
confidence: 0.85
successful_uses: 0
---

## CALM Semantic Bandwidth Principle for Memory

**Paper**: Continuous Autoregressive Language Models (arXiv, March 2026, Shao et al.)
**Core insight**: Increasing semantic bandwidth per generative step improves efficiency.
**STOPA application**: Same principle applies to prompt/memory token density.

### Proven compression results
- `decisions.md`: 135 → 25 lines (table format, 5 archived to decisions-archive.md)
- `news.md`: 351 → ~105 lines (table format, 17 items archived to news-archive.md)
- Zero information loss — all content preserved in archive files

### Convention established
- New decision entries: table row format (date | decision | status | key detail)
- New news entries: table row within category section
- Detail sections only when context > 1 sentence

### Parked idea: Instruction Tiering for sub-agents
- Full skill body on first invocation, condensed (1/3 length) on repeat
- Blocked by: CC sub-agents have no shared state between spawns
- Revisit when token budget tracking shows sub-agent prompt cost is significant
