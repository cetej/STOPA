---
name: seo-audit
variant: compact
description: Condensed seo-audit for repeat invocations within session. Use full SKILL.md for first invocation.
---

# SEO Audit — Compact (Session Re-invocation)

Read GSC data from NG-ROBOT SQLite, find opportunities, produce actionable report. Read-only — never modify files.

## Focus Modes

| Focus | Modules run |
|-------|-------------|
| `opportunities` | Module 1 + 2 only |
| `intent` | Module 3 only |
| `gaps` | Module 1 + 2 + 3 |
| `full` (default) | All 4 modules |

Timerange: `30d` or `90d` (default: `90d`)

## Data Source

SQLite DB at NG-ROBOT project: `performance_analytics.db`. Table: `search_console`.
Key columns: `source_type` (organic/discover), `keyword`, `url`, `clicks`, `impressions`, `ctr`, `avg_position`
Note: ~90% of rows have empty keyword — use URL-level fallback queries when keyword data is sparse.

## 4 Analysis Modules

1. **Page-2 Goldmine** — positions 11-20 with significant impressions. For each: classify action needed (Title fix / Content thin / Internal links / Fresh content).
2. **CTR Opportunities** — compare actual CTR vs benchmark by position range. Flag underperformers (actual < 50% of expected). Discover CTR < 5% = headline/thumbnail fix.
3. **Reader Intent Mapping** — classify keywords/URL slugs into: Curiosity | Research | Engagement | Action. Calculate distribution, flag missing stages.
4. **Trend Detection** — compare earliest vs latest snapshots. Declining (was <=10, now >15) | Rising (was >15, now <=12). If only 1 snapshot: "insufficient data — skip module."

## CTR Benchmarks

| Position | Expected CTR |
|----------|-------------|
| 1-3 | 5-15% |
| 4-7 | 2-5% |
| 8-10 | 1-3% |
| 11-20 | 0.5-1.5% |

## Circuit Breakers

- NEVER fabricate metrics — if data insufficient, say so
- NEVER suggest >3 Priority Actions (causes none to get actioned)
- For every title issue: provide current text AND specific suggested replacement
- If DB not found: report expected path, suggest running GSC import in NG-ROBOT first
- Trend module: if 1 snapshot only → skip, do not extrapolate

## Output

Report with Executive Summary + 4 module tables + Priority Actions (top 3, by impressions x CTR gap, labeled HIGH/MEDIUM).
