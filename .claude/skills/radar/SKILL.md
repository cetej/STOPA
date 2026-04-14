---
name: radar
description: "Use when evaluating a tool, library, or technique from Twitter/X or other source, or running a proactive scan for new tools. Trigger on 'radar', tweet URL, 'evaluate tool', 'posoudit nástroj', 'scan tools'. Do NOT use for ecosystem news (/watch) or deep multi-source research (/deepresearch)."
argument-hint: "<URL or text> | scan | digest"
tags: [research, osint, ai-tools, memory]
phase: meta
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
model: sonnet
effort: medium
maxTurns: 25
---

# Tool Radar — Proactive Tool Discovery & Evaluation

You discover, evaluate, and track new tools, libraries, and techniques relevant to the user's projects. You operate in two modes: **manual** (single URL/text evaluation) and **scan** (proactive multi-source discovery).

## Shared Memory

1. Read `.claude/memory/radar.md` — previous findings, last scan date, known tools
2. Read `.claude/memory/key-facts.md` — current stack and project context
3. Read `.claude/memory/news.md` — last 20 lines only (avoid duplicating /watch findings)

<!-- CACHE_BOUNDARY -->

## Input

Parse `$ARGUMENTS`:
- **URL or text** → Single-item evaluation (manual mode)
- **"scan"** → Proactive scan across all sources
- **"digest"** → Show summary of current radar.md state
- **(empty)** → Show radar.md state (same as digest)

---

## Mode 1: Single-Item Evaluation

When input is a URL or pasted text:

### Step 1: Extract

If URL provided:
- Fetch via Jina Reader: `WebFetch("https://r.jina.ai/{url}", "Extract: tool name, what it does, tech stack, license, pricing, GitHub URL if any")`
- Fallback: direct `WebFetch` if Jina returns < 200 chars
- For Twitter/X URLs: content is often blocked — `WebSearch` for the tool name mentioned in the URL instead

If text provided:
- Parse directly for tool name, description, claims

### Step 2: Enrich

If tool has a GitHub repo or homepage, fetch it for additional context:
- `WebFetch("https://r.jina.ai/{homepage_or_github}", "Extract: stars, last update, documentation quality, dependencies, installation method")`

### Step 3: Score

Apply the 3-Gate Filter + Numeric Score (see Scoring section below).

### Step 4: Store & Act

- Update `.claude/memory/radar.md` with the finding
- If 🔴 (score ≥ 8): Launch `/deepresearch` via Agent tool with prompt focused on tool evaluation
- If 🟡 (score 5-7): Add to Watch List, suggest when to revisit
- If 🟢 (score < 5): Archive with one-line reason
- **Cross-project routing**: For 🔴 and 🟡 tools, invoke `/improve` to route finding to matching projects (creates GitHub issues based on project profiles in `~/.claude/memory/projects/*.yaml`)

### Step 5: Report

Output a concise evaluation to the user:

```
## 🔴/🟡/🟢 [Tool Name] — X/10

**Co to je:** one-line description
**Proč je to zajímavé:** relevance to specific project
**Stack fit:** Python/TS/... | Windows compatible: yes/no
**Maturity:** stars, docs quality, last release
**Akce:** what happens next (deepresearch / watch / archive)
```

---

## Mode 2: Proactive Scan

When input is "scan":

### Source Strategy

These sources complement /watch (which covers news, arXiv, influencer voices). Radar focuses on **concrete new tools and libraries**.

Run searches in parallel batches:

**Batch 1 — Tool launch platforms** (parallel):
1. `site:producthunt.com AI developer tool {current_month} {current_year}`
2. `site:news.ycombinator.com "Show HN" (AI OR LLM OR developer tool) {current_month} {current_year}`
3. `new MCP server "model context protocol" released {current_month} {current_year}`

**Batch 2 — Code repositories** (parallel):
4. `github new release (AI OR LLM OR "developer tool" OR CLI) trending {current_month} {current_year}`
5. `new python library (AI OR ML OR LLM OR automation) released {current_month} {current_year}`
6. `new typescript library (AI OR developer OR CLI) released {current_month} {current_year}`

**Batch 3 — Community signals** (parallel):
7. `site:reddit.com/r/LocalLLaMA new tool OR library OR release {current_month} {current_year}`
8. `(AI OR LLM) new tool launch announcement {current_month} {current_year} -site:arxiv.org`

**Batch 4 — Twitter indirect** (parallel):
9. `twitter (announced OR released OR "check out" OR "just shipped") new (tool OR library) AI {current_month} {current_year}`
10. `(karpathy OR simonw OR swyx OR "riley goodside") recommended OR "must try" tool {current_month} {current_year}`

### Processing

For each search batch:
1. Collect unique tool mentions across all results
2. Deduplicate against radar.md (grep for tool name)
3. Deduplicate against news.md (grep for tool name)
4. For top 3-5 most promising NEW tools: `WebFetch` via Jina Reader for details
5. Score each through the 3-Gate Filter + Numeric Score

### Output

```markdown
## Radar Scan — {date}

**Searches:** N | **Fetches:** N | **New tools found:** N

### 🔴 Immediate Research (score ≥ 8)
| Tool | Score | Category | Why | Action |
|------|-------|----------|-----|--------|

### 🟡 Watch List (score 5-7)
| Tool | Score | Category | Notes |
|------|-------|----------|-------|

### 🟢 Archived (score < 5)
- tool_name — reason for low score

### Skipped (already known)
- tool_name — already in radar.md / news.md
```

After output, update `.claude/memory/radar.md` with all findings.

For 🔴 items: launch `/deepresearch` Agent for each:
```
Agent(prompt="Research tool '{name}': What does it do? How mature is it?
How could we use it in {relevant_project}? Competitors? Installation?
Write findings to outputs/radar-{name}-{date}.md", model="sonnet")
```

---

## Scoring

### 3-Gate Filter (quick pass/fail)

```
GATE 1: RELEVANCE — Does it relate to our projects/stack?

  Projects & areas of interest:
  - STOPA: orchestration, skills, hooks, memory, Claude Code extensions
  - NG-ROBOT: editorial pipeline, NLP, terminology, Czech language
  - MONITOR: OSINT, Czech NLP, intelligence dashboard, web scraping
  - KARTOGRAF: maps, geodata, Copernicus, MapLibre, cartography
  - GRAFIK: image editing, layered generation, fal.ai
  - ZACHVEV: social media analysis, cascade detection, sentiment
  - POLYBOT: prediction markets, trading, forecasting
  - ORAKULUM: time series, causal inference, correlation
  - General: Claude Code, MCP servers, AI/ML tooling, LLM prompting,
             Python libs, TypeScript, developer experience

  ✅ PASS: tool fits any project or general AI/dev tooling
  ❌ FAIL: unrelated domain (iOS, Java, embedded, gaming, crypto-only)
  → FAIL = 🟢 ARCHIVE immediately, score 1-2

GATE 2: ACTIONABILITY — Can we realistically use it?

  ✅ PASS: has docs, API, is open-source or freemium, works on Windows
  ❌ FAIL: concept only, no code, Mac/Linux only, enterprise-only pricing
  → FAIL = 🟢 ARCHIVE, score 2-3

GATE 3: NOVELTY — Is it new to us?

  Check (in order):
  1. Grep radar.md for tool name → already tracked?
  2. Grep news.md for tool name → covered by /watch?
  3. Grep learnings/ for tool name → existing learning?
  → FAIL = SKIP (don't re-score, note "already known" in output)
```

### Numeric Score (1-10) — for items passing all gates

| Signal | Weight | 1 (low) | 5 (mid) | 10 (high) |
|--------|--------|---------|---------|-----------|
| Stack fit | 3x | Vaguely related | Useful in 1 project | Solves active pain point |
| Maturity | 2x | Alpha, no docs | Beta, basic docs | Stable, great docs, active community |
| Uniqueness | 2x | Many alternatives exist | Some alternatives | Nothing like it for our use case |
| Source authority | 1x | Random blog | HN front page | Karpathy/SimonW/core maintainer |
| Urgency | 1x | Evergreen | New release | Breaking change / time-limited |

**Calculation:** weighted average, normalized to 1-10 scale.
- Raw = (stack×3 + maturity×2 + uniqueness×2 + authority×1 + urgency×1) / 9
- Score = round(Raw)

**Thresholds:**
- 🔴 ≥ 8: Auto-trigger /deepresearch
- 🟡 5-7: Add to Watch List
- 🟢 < 5: Archive

---

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "This tool has a lot of GitHub stars so it must be good" | Stars measure hype, not quality; many popular tools have critical issues or are unmaintained | Evaluate against the RADAR matrix dimensions (maturity, maintenance, security, fit) independently |
| "I'll skip the competition analysis since this is clearly the best option" | Without comparing alternatives, you cannot assess relative fit; the 'best' tool may have a better competitor | Always identify at least 2 alternatives and compare on the same criteria |
| "The tool's README says it does X so I'll trust that" | READMEs are marketing; claimed features may be incomplete, broken, or in alpha | Verify claims by checking issues, tests, and actual code; note discrepancies |
| "I'll recommend this tool without checking if it fits the user's stack" | A great tool for Python is useless if the user runs Node.js; fit is as important as quality | Always cross-reference tool requirements against key-facts.md and the user's environment |

## Memory Update Rules

When updating `.claude/memory/radar.md`:
- Add new findings to the appropriate section (🔴/🟡/🟢)
- Update Stats line with new counts and last scan date
- Add entry to Scan Log
- If file exceeds 400 lines: move 🟢 Archive entries older than 60 days to `radar-archive.md`
- Never delete entries — archive only

## Telegram Notification

For 🔴 items found during scan mode, notify via Telegram if MCP is available:
```
Tool: {name} — {score}/10
{one-line description}
Fit: {project}
Spouštím /deepresearch...
```

Use `mcp__plugin_telegram_telegram__reply` with the user's chat_id.

## Handoffs

- 🔴 items → `/deepresearch` (automatic, via Agent)
- Patterns across multiple radar findings → `/scribe` (suggest to user)
- Tool that should be integrated → user decides, then `/orchestrate`
