# Improvement Queue

Updated: 2026-04-10

## Active Violations

| Priority | Type | Pattern | Count | Action |
|----------|------|---------|-------|--------|
| 3 | violation | NEVER write API keys/tokens into JSON config files. Use environment variables or | 1 | fix rule or code |
| 3 | violation | 6. Analysis-Paralysis Guard | 1 | fix rule or code |

## RLM Improvements — Tier 2-3 (arXiv:2512.24601)

Quick wins (#1-3) done 2026-04-10. Remaining items ranked by impact x feasibility.

| # | Improvement | Skills | Effort | Impact | Source |
|---|-------------|--------|--------|--------|--------|
| 4 | **Structured output contracts** — JSON schema pro agent outputy, programaticka agregace misto NL | output-contract enforcement, orchestrate | 4h | high | RLM: REPL data structures |
| 5 | **Lazy context loading** — paths misto content v agent promptech | orchestrate subtask format | 3h | medium | Google ADK reimpl. |
| 6 | **"Never summarize" rule** — partitionovat misto komprimovat pri velkem kontextu | compact redesign | 4h | medium | RLM core principle |
| 7 | **Contradiction detection** — post-merge check pri kombinaci vysledku z vice agentu | deepresearch, critic | 5h | medium | Gap analysis |
| 8 | **Strategy pre-enumeration** — enumerate strategie pred iteraci, odhadnout success probability | autoloop, autoresearch (Phase 0.5) | 4h | medium | RLM PLAN principle |
