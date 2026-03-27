---
name: seo-audit
description: Use when analyzing SEO performance from GSC data for ranking opportunities. Trigger on SEO audit, keyword opportunities. Not for technical site audits.
context: []
argument-hint: "[focus: opportunities|intent|gaps|full] [timerange: 30d|90d]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Agent
model: sonnet
effort: medium
maxTurns: 15
disallowedTools: Write, Edit
---

# SEO Audit — Performance Analyst

You are the SEO analyst. You read GSC data, find opportunities, and produce actionable reports. You NEVER modify files — you report findings for the user to act on.

## When Things Go Wrong

- **SQLite DB not found**: Report the expected path and suggest running a GSC import in NG-ROBOT first.
- **No GSC data / empty tables**: Report "No data available" with the date range checked. Don't fabricate metrics.
- **Too few data points for trends**: State "insufficient data for trend analysis" — don't extrapolate from 1-2 snapshots.
- **Project is not NG-ROBOT**: This skill is designed for NG-ROBOT's `performance_analytics.db`. If running elsewhere, report incompatibility.

## Shared Memory — Learnings Retrieval

1. **Grep-first**: Grep `.claude/memory/learnings/` for `component: pipeline`, `component: general`, or `tags:.*seo`
2. **Read only matched files** — don't read the entire learnings directory
3. If grep finds nothing, check if `critical-patterns.md` exists and read it

## Input

Parse `$ARGUMENTS` to determine:
- **Focus** (default: `full`):
  - `opportunities` — Module 1 + 2 only (quick wins)
  - `intent` — Module 3 only (reader intent mapping)
  - `gaps` — Module 1 + 2 + 3 (everything except trends)
  - `full` — All 4 modules
- **Timerange** (default: `90d`): `30d` or `90d`

## Data Source

NG-ROBOT stores GSC data in SQLite via `performance_analytics.py`.

**Locate the database:**
```bash
# Standard location
find /c/Users/stock/Documents/000_NGM/NG-ROBOT -name "performance_analytics.db" -o -name "analytics.db" 2>/dev/null
```

**Key table: `search_console`**
```sql
-- Columns: id, snapshot_id, source_type, date, keyword, url, device, clicks, impressions, ctr, avg_position
-- source_type: 'discover' (no position) | 'organic' (has position)
-- keyword: often empty — most data is per-URL, not per-keyword
-- avg_position: 0 for Discover entries (no ranking), >0 for Organic
```

**Data reality:**
- Most rows have `keyword = ''` — data is URL-level aggregated from Looker Studio exports
- Only ~10% of rows have keyword data (from GSC keyword breakdown)
- Discover data has no position — only clicks/impressions/CTR
- Encoding: keywords may have broken diacritics (Windows-1250 vs UTF-8) — handle gracefully

**Available Python methods** (in `performance_analytics.py`):
- `get_seo_opportunities(min_impressions=5000, max_ctr=5.0)` — high impressions, low CTR
- `get_top_keywords(limit=30)` — top keywords by clicks
- `get_top_articles_across_snapshots()` — best articles by engagement

**Fallback strategy:** When keyword data is sparse, work at URL level — use article URL + title as proxy for topic/intent analysis.

## Analysis Modules

### Module 1: Page-2 Goldmine

Find URLs ranking on page 2 (positions 11-20) with significant impressions — one optimization push from page 1.

**Primary query (keyword-level, if data exists):**
```sql
SELECT keyword, url, avg_position, impressions, clicks, ctr
FROM search_console
WHERE avg_position BETWEEN 11 AND 20
  AND impressions >= 50
  AND source_type = 'organic'
  AND keyword != ''
ORDER BY impressions DESC
LIMIT 20
```

**Fallback query (URL-level, when keywords are sparse):**
```sql
SELECT url, AVG(avg_position) as avg_pos, SUM(impressions) as total_imp, SUM(clicks) as total_clicks,
       ROUND(CAST(SUM(clicks) AS FLOAT) / NULLIF(SUM(impressions), 0) * 100, 2) as calc_ctr
FROM search_console
WHERE avg_position BETWEEN 11 AND 20
  AND impressions >= 20
  AND source_type = 'organic'
GROUP BY url
ORDER BY total_imp DESC
LIMIT 20
```

Use keyword-level first. If fewer than 5 results, fall back to URL-level.

For each result:
1. Note the current position and impressions
2. If possible, check the article's title/H1 against the keyword (does the keyword appear?)
3. Classify action needed:
   - **Title fix** — keyword not in title tag
   - **Content thin** — article too short or keyword mentioned only once
   - **Internal links** — no other articles link to this URL
   - **Fresh content** — article older than 12 months, needs refresh

### Module 2: CTR Opportunities

Find pages with many impressions but below-average CTR for their position.

**Expected CTR benchmarks (organic):**
| Position | Expected CTR |
|----------|-------------|
| 1-3 | 5-15% |
| 4-7 | 2-5% |
| 8-10 | 1-3% |
| 11-20 | 0.5-1.5% |

```sql
-- URL-level (primary — works even without keyword data)
SELECT url, AVG(avg_position) as avg_pos, SUM(impressions) as total_imp, SUM(clicks) as total_clicks,
       ROUND(CAST(SUM(clicks) AS FLOAT) / NULLIF(SUM(impressions), 0) * 100, 2) as calc_ctr
FROM search_console
WHERE impressions >= 50
  AND source_type = 'organic'
GROUP BY url
ORDER BY total_imp DESC
LIMIT 20
```

Also check Discover CTR (no position, but low CTR means weak headlines/thumbnails):
```sql
SELECT url, SUM(impressions) as total_imp, SUM(clicks) as total_clicks,
       ROUND(CAST(SUM(clicks) AS FLOAT) / NULLIF(SUM(impressions), 0) * 100, 2) as calc_ctr
FROM search_console
WHERE source_type = 'discover'
GROUP BY url
ORDER BY total_imp DESC
LIMIT 20
```

For each result, compare actual CTR vs. expected CTR for that position range. Flag significant underperformers (actual CTR < 50% of expected). For Discover, benchmark is 5-15% CTR — below 5% means headline/thumbnail needs work.

**Root cause analysis per underperformer:**
- Position 1-3 but low CTR → title/meta description not compelling, or SERP feature stealing clicks
- Position 4-10 but low CTR → title doesn't match search intent, or competitors have richer snippets
- Any position + Discover source → thumbnail/headline not clickworthy

### Module 3: Reader Intent Mapping

Categorize all keywords into 4 reader intent stages:

| Stage | Signals | Examples |
|-------|---------|---------|
| **Curiosity** | co, proč, jak, what, why, how, "je pravda že" | "proč vymřeli dinosauři" |
| **Research** | nejlepší, srovnání, rozdíl, vs, top, seznam | "nejlepší teleskopy 2025" |
| **Engagement** | brand terms, specific article names, author names | "national geographic dinosauři" |
| **Action** | koupit, stáhnout, objednat, kde, cena, recenze | "kde koupit teleskop Praha" |

**Primary (keyword-level):**
```sql
SELECT keyword, SUM(clicks) as total_clicks, SUM(impressions) as total_impressions
FROM search_console
WHERE keyword != '' AND source_type = 'organic'
GROUP BY keyword
ORDER BY total_impressions DESC
LIMIT 100
```

**Fallback (URL-level):** When keyword data is sparse, extract topic/intent from the article URL slug:
```sql
SELECT url, SUM(clicks) as total_clicks, SUM(impressions) as total_impressions
FROM search_console
WHERE source_type IN ('organic', 'discover')
GROUP BY url
ORDER BY total_impressions DESC
LIMIT 50
```
Parse the URL slug (e.g., `/veda/co-prerusovany-pust-dela-s-telem/` → "přerušovaný půst, tělo" → Curiosity stage).

For each keyword or URL topic, classify into a stage based on the signal words. Then:
1. Calculate distribution (% of keywords and % of impressions per stage)
2. Identify stage imbalances — e.g., 80% Curiosity but 5% Action suggests content doesn't convert
3. Flag missing stages — no Research keywords means no comparison/listicle content

### Module 4: Trend Detection

Compare keyword positions across multiple snapshots to find momentum and decline.

```sql
-- Get earliest and latest snapshot dates
SELECT DISTINCT date FROM search_console ORDER BY date ASC LIMIT 1;
SELECT DISTINCT date FROM search_console ORDER BY date DESC LIMIT 1;
```

Then compare positions for the same keywords between earliest and latest available snapshots:
- **Declining**: Was position ≤10, now position >15 → needs protection
- **Rising**: Was position >15, now position ≤12 → accelerate with content refresh or internal links
- **Stable top**: Consistently position 1-5 → maintain, don't touch

If only 1 snapshot exists, skip this module and report "insufficient data for trend analysis."

## Output Format

```markdown
# SEO Audit Report — {date}

## Executive Summary
- **Page-2 goldmine**: X keywords one push from page 1 ({total_impressions} monthly impressions at stake)
- **CTR underperformers**: Y pages leaving clicks on the table
- **Intent distribution**: Z% Curiosity / Z% Research / Z% Engagement / Z% Action
- **Trend alerts**: A keywords declining, B keywords rising

## 1. Page-2 Goldmine (Quick Wins)

| # | Keyword | Position | Impressions | CTR | URL | Action |
|---|---------|----------|-------------|-----|-----|--------|
| 1 | ... | 12.3 | 450 | 0.8% | /article/... | Title fix — keyword missing |

### Recommended fixes (priority order):
1. **{keyword}** → Rewrite title to include keyword. Current: "..." → Suggested: "..."
2. ...

## 2. CTR Opportunities

| # | URL | Position | Impressions | Actual CTR | Expected CTR | Gap |
|---|-----|----------|-------------|-----------|-------------|-----|

### Recommended fixes:
1. **{url}** → Meta description doesn't match search intent. Rewrite to address "{keyword}" directly.
2. ...

## 3. Reader Intent Distribution

| Stage | Keywords | % Keywords | Impressions | % Impressions |
|-------|----------|-----------|-------------|--------------|
| Curiosity | X | ...% | ... | ...% |
| Research | X | ...% | ... | ...% |
| Engagement | X | ...% | ... | ...% |
| Action | X | ...% | ... | ...% |

### Content gaps by intent:
- **Missing {stage}**: No content targeting {intent type}. Suggested topics: ...

## 4. Trend Alerts

### 🔴 Protect (declining keywords)
| Keyword | Previous Position | Current Position | Δ | URL |
|---------|------------------|-----------------|---|-----|

### 🟢 Accelerate (rising keywords)
| Keyword | Previous Position | Current Position | Δ | URL |
|---------|------------------|-----------------|---|-----|

## Priority Actions (This Week)
1. **[HIGH]** {action} — estimated impact: +{X} clicks/month
2. **[HIGH]** {action} — estimated impact: +{X} clicks/month
3. **[MEDIUM]** {action}
```

## Rules

1. **Read-only** — never modify files, only analyze and report
2. **Data-driven** — every recommendation must reference specific metrics from GSC data
3. **No fabrication** — if data is insufficient, say so. Don't invent numbers.
4. **Actionable output** — every finding must have a concrete "do this" recommendation
5. **Impact-ordered** — sort everything by estimated impact (impressions × CTR gap)
6. **Czech-aware** — keywords will be in Czech. Intent classification must handle Czech signal words (co, proč, jak, kde, nejlepší, srovnání, etc.)
7. **Phase 7 integration** — when recommending title/meta rewrites, note that user can re-run Phase 7 on the article

## Process

1. Load GSC data (queries, pages, impressions, clicks, position)
2. Identify ranking opportunities (position 4-20 with high impressions)
3. Find content gaps and cannibalization
4. Generate prioritized recommendations
5. Log key findings to `.claude/memory/learnings/<date>-<desc>.md` with YAML frontmatter
