---
date: 2026-04-12
type: best_practice
severity: high
component: skill
tags: [skill-design, harness, mcp, tooling, performance]
summary: "Purpose-built narrow tools are 75× faster than generic MCP wrappers (Playwright CLI 100ms vs Chrome MCP 15s). Keep harness thin — push intelligence up into skills, push execution down into deterministic narrow tools."
source: external_research
uses: 2
successful_uses: 0
harmful_uses: 0
confidence: 1.0
impact_score: 0.0
verify_check: "manual"
---

## Detail

Garry Tan measures: Chrome MCP (screenshot → find → click → wait → read) = ~15 seconds per browser operation. Playwright CLI per operation = ~100ms. Ratio: 75×.

The MCP anti-pattern: 40+ tool definitions eating half the context window. "God-tools" with 2-5 second round-trips per call.

The correct approach: "Build exactly what you need, and nothing else." Domain-specific Python scripts or CLI tools for each specific workflow.

"Speed compounds across every skill invocation."

**STOPA application:**
- Prefer `python scripts/` over MCP calls for automation tasks
- RTK hook (purpose-built token filter) is the right model — narrow scope, fast execution
- When skills are slow: first ask "is there a deterministic tool I could build instead of having the model do this?"
- NEVER justify a new generic MCP server — justify a specific narrow tool

**Related:** behavioral-genome.md anti-pattern: "NEVER add Playwright MCP — hijacks Chrome downloads"
