---
name: watch
description: Use when scanning for AI/ML ecosystem news, Claude Code updates, or arXiv research papers. Trigger on 'watch', 'news', "what's new", 'novinky', 'papers', 'arXiv'. Do NOT use for web browsing (/browse).
argument-hint: [full / quick / papers / voices / topic:specific-topic]
discovery-keywords: [news, updates, novinky, what changed, ecosystem, new release, papers, arXiv]
tags: [research, osint]
phase: meta
user-invocable: true
allowed-tools: Read, Write, Edit, WebSearch, WebFetch, Agent
model: sonnet
effort: medium
maxTurns: 25
disallowedTools: Bash, Glob, Grep
---

# Watch — News & Updates Scanner

You scan external sources for news, updates, and changes relevant to this project and its orchestration system. You report findings and suggest actionable improvements.

## Shared Memory

1. Read `.claude/memory/news.md` — previous findings and last scan date
2. Read `.claude/memory/learnings.md` — current patterns (to spot relevant updates)
3. Read `CLAUDE.md` — project dependencies and tech stack (to know what to watch)

<!-- CACHE_BOUNDARY -->

## Input

Parse `$ARGUMENTS`:
- **"full"** (default) → Scan all source tiers (1-4)
- **"quick"** → Tier 1 only (Claude Code + API). Cheapest option.
- **"papers"** → Tier 1 + Tier 2b only (Claude updates + arXiv research). Good for "co je nového ve výzkumu".
- **"voices"** → Tier 1 + Tier 4 only (Claude updates + Influencer Pulse). Good for "co je nového ve světě".
- **"topic:X"** → Focus scan on specific topic (e.g., "topic:pytorch", "topic:flow-matching")

## Source Tiers

### Tier 1: Claude Code & Anthropic (always scan)

Use `WebSearch` for each:
1. **Claude Code releases** — search: `"claude code" changelog OR release notes site:docs.anthropic.com OR site:github.com/anthropics {current_year}`
2. **Claude API updates** — search: `anthropic claude API new features OR models {current_year}`
3. **Claude skills/hooks** — search: `"claude code" skills OR hooks OR MCP new {current_year}`

For each result, `WebFetch` the most relevant 1-2 pages.
- Prefer Jina Reader for cleaner text: `WebFetch("https://r.jina.ai/{url}", ...)` — removes nav/ads, better for LLM parsing. Fall back to direct URL if Jina returns < 200 chars.

### Tier 2: AI/ML Ecosystem (scan on "full")

Use `WebSearch` for each:
4. **PyTorch** — search: `pytorch release OR blog {current_year} {current_month}`
5. **HuggingFace + diffusers** — search: `huggingface diffusers release OR update {current_year}`
6. **Flow matching / video generation** — search: `"flow matching" OR "video generation" model paper {current_year}`
7. **timm / einops** — search: `timm OR einops release {current_year}` (skip if no results)

### Tier 2b: Research Papers — arXiv & Academic (scan on "full" or "papers")

Fresh research papers are the earliest signal — new models, techniques, and benchmarks appear on arXiv days to weeks before they hit Reddit or blogs. Focus on papers with practical impact, not pure theory.

> **Alternative: `hf papers` CLI** (2026-03+) — HuggingFace Trending Papers is the official Papers with Code successor (**PwC sunsetted April 2026** — papers-with-code.com is dead; use `huggingface.co/papers/trending`). If `hf papers` CLI is available as a tool/MCP, prefer it over `site:arxiv.org` WebSearch queries for better recall. Fallback: use WebSearch as below.

Use `WebSearch` for each:
8. **LLM & agents** — search: `site:arxiv.org "large language model" OR "LLM agent" OR "tool use" {current_month} {current_year}`
9. **Prompting & reasoning** — search: `site:arxiv.org "chain of thought" OR "prompt engineering" OR "in-context learning" OR reasoning {current_month} {current_year}`
10. **Code generation** — search: `site:arxiv.org "code generation" OR "program synthesis" OR "coding agent" {current_month} {current_year}`
11. **Video & image generation** — search: `site:arxiv.org "flow matching" OR "video generation" OR "diffusion" OR "image generation" new model {current_month} {current_year}`
12. **Benchmarks & evaluations** — search: `site:arxiv.org benchmark evaluation LLM OR "foundation model" {current_month} {current_year}`

For promising results (high relevance to our stack), `WebFetch` the arXiv abstract page (max 2 fetches). Read abstract + introduction only — don't attempt full paper.

#### Paper Relevance Filter

| Include | Exclude |
|---------|---------|
| New model architectures we could use | Pure math/theory with no practical application |
| Training techniques applicable to our models | Hardware-specific optimizations (TPU clusters) |
| Agent/tool-use patterns | Papers about models we don't use and can't switch to |
| Prompting/reasoning improvements | Marginal benchmark improvements (<2%) |
| New benchmarks relevant to our use cases | Domain-specific papers (medical, legal) unless user's domain |
| Open-source model releases with weights | Papers without code or reproducibility |

#### Paper Signal Strength

Prioritize papers by practical impact:
- **Code available** (GitHub link in paper) → higher priority
- **HuggingFace model/dataset** released → higher priority
- **Cited by Papers With Code** trending → higher priority
- **Multiple citations within first week** → emerging consensus
- **Author is known (from Voice Registry or major lab)** → credibility boost

### Tier 3: Community (scan on "full")

Use `WebSearch` for each:
13. **GitHub trending** — search: `github trending python machine learning video generation {current_month} {current_year}`
14. **Reddit** — search: `site:reddit.com (r/LocalLLaMA OR r/StableDiffusion) "flow matching" OR "video generation" OR "pyramid" {current_year}`
15. **General AI news** — search: `AI tools developer productivity {current_month} {current_year}`

### Tier 4: Influencer Pulse (scan on "full" or "voices")

Curated voices who consistently signal what's coming next. The goal is NOT to follow their daily chatter — it's to catch **announcements, demos, and directional shifts** that affect our stack.

#### Voice Registry

| # | Person | Handle | Watch For | Relevance |
|---|--------|--------|-----------|-----------|
| 1 | Andrej Karpathy | @karpathy | New training techniques, model architecture insights, educational content on LLMs/transformers | ML fundamentals, model understanding |
| 2 | Simon Willison | @simonw | Claude Code tips, LLM tooling patterns, prompt engineering, new AI dev tools | Direct — Claude Code + orchestration |
| 3 | Andrej Karpathy / Jim Fan | @DrJimFan | Embodied AI, foundation models, agent architectures | Agent patterns for orchestration |
| 4 | AK (@_akhaliq) | @_akhaliq | Daily paper roundups — new models, techniques, benchmarks | Early signal on breakthroughs |
| 5 | Swyx (Shawn Wang) | @swyx | AI engineering patterns, "AI Engineer" movement, tooling trends | Orchestration + dev workflow |
| 6 | Riley Goodside | @goodaboreside | Prompt engineering techniques, jailbreaks, capability discoveries | Prompt craft for skills |
| 7 | Yann LeCun | @ylecun | Architecture debates, meta-learning directions, contrarian takes on AGI | Strategic — where the field is heading |
| 8 | Alex Albert | @alexalbert__ | Anthropic insider — Claude capabilities, system prompt tips, feature previews | Direct — Claude features |
| 9 | Jeremy Howard | @jeremyphoward | Fast.ai, practical ML, new training recipes | Practical ML patterns |
| 10 | Harrison Chase | @hwchase17 | LangChain/LangGraph, agent frameworks, RAG patterns | Agent orchestration patterns |

#### Search Strategy

WebSearch cannot reliably scrape X/Twitter directly. Use **indirect discovery** — search for their insights as they propagate to blogs, newsletters, and aggregators:

For each voice group, run ONE combined search (not per-person — too expensive):

16. **AI Leaders — announcements** — search: `(karpathy OR "simon willison" OR "jim fan" OR "alex albert") (announced OR released OR "new model" OR "new tool") {current_month} {current_year}`
17. **AI Practitioners — techniques** — search: `(swyx OR "riley goodside" OR "jeremy howard" OR "harrison chase") (technique OR pattern OR framework OR "prompt engineering") {current_month} {current_year}`
18. **Paper scouts** — search: `akhaliq OR "papers with code" trending AI model {current_month} {current_year}`
19. **Aggregator catch-all** — search: `site:simonwillison.net OR site:swyx.io OR site:karpathy.ai {current_year} {current_month}`

If a search returns a promising blog post or newsletter, `WebFetch` it via Jina Reader (`https://r.jina.ai/{url}`) for clean text (max 2 fetches for this tier).

#### Filtering Sieve (CRITICAL — prevents noise)

For EACH result from Tier 4, apply this 3-gate filter before including in report:

```
GATE 1: Relevance — Does it affect our stack?
  ✅ Claude/Anthropic features, agent patterns, prompt techniques,
     ML training, video generation, Python tooling, MCP
  ❌ General AI philosophy, AGI debates, hiring news, company drama,
     hardware announcements, unrelated frameworks (Rust ML, iOS ML)

GATE 2: Actionability — Can we do something with it?
  ✅ New tool we could adopt, technique to try, pattern to apply,
     breaking change to prepare for, capability we didn't know about
  ❌ "Interesting" but no clear next step, pure opinion/commentary,
     announcements of things not yet available

GATE 3: Freshness — Is it new since last scan?
  ✅ Published after last scan date (check news.md)
  ❌ Already covered in previous scans, old news resurfacing
```

Only items that pass ALL 3 gates get included. Items passing Gate 1+3 but failing Gate 2 → classify as [WATCH] (monitor, don't act).

## Processing

For each source that returns results:

1. **Filter**: Is this relevant to our project or orchestration system?
2. **Classify**:
   - `[ACTION]` — Directly useful, should act on it (new version of dependency, breaking change, new Claude feature)
   - `[WATCH]` — Interesting, monitor further (emerging technique, upcoming release)
   - `[INFO]` — Good to know, no action needed (industry trend, tangential news)
3. **Summarize**: 1-2 sentences per item
4. **Suggest**: For `[ACTION]` items, propose a concrete next step

## Parallel Execution

To minimize cost, use parallel WebSearch calls:
- Launch Tier 1 searches (items 1-3) in parallel
- If "full" mode, launch Tier 2 (items 4-7) in parallel
- If "full" or "papers" mode, launch Tier 2b (items 8-12) in parallel
- If "full" mode, launch Tier 3 (items 13-15) in parallel
- If "full" or "voices" mode, launch Tier 4 (items 16-19) in parallel
- Fetch detailed pages only for promising results

## Output Format

```markdown
## Watch Report — <date>

**Mode**: full / quick / topic:X
**Sources scanned**: N
**Items found**: N (X action, Y watch, Z info)

### Action Items

| # | Source | Finding | URL | Suggested Action |
|---|--------|---------|-----------------|
| 1 | Claude Code v1.X | New skill hooks API | Update orchestration to use new hooks |
| 2 | diffusers 0.32 | Breaking change in scheduler API | Check compatibility with our schedulers |

### Watch List

| # | Source | Finding | URL | Why It Matters |
|---|--------|---------|---------------|
| 1 | HuggingFace | New scheduler API | Could improve generation quality |

### Research Papers (arXiv)

| # | Paper | Area | Key Insight | Code? | Impact |
|---|-------|------|-------------|-------|--------|
| 1 | "Title" (arxiv:XXXX.XXXXX) | LLM agents | New tool-use architecture outperforms ReAct by 15% | GitHub ✅ | [ACTION] |
| 2 | "Title" (arxiv:XXXX.XXXXX) | Prompting | Chain-of-draft reduces tokens 80% vs CoT | No code | [WATCH] |

### Influencer Pulse

| # | Voice | Signal | URL | Gate | Classification |
|---|-------|--------|------|---------------|
| 1 | Simon Willison | New Claude Code workflow pattern for X | 1+2+3 ✅ | [ACTION] |
| 2 | Karpathy | Blog post on efficient fine-tuning | 1+3 ✅, 2 ❌ | [WATCH] |

### Info

- <brief bullet points for [INFO] items>

### Recommendations for Orchestration System

<If any findings suggest improvements to the skill system, list them here>

### Recommendations for Active Projects

<If any findings affect project dependencies or techniques, list them here>

### Harness Adoption Health

<Auto-populated from `python scripts/passes-rate.py --json`. Shows feature-list.json completion across registered projects. Include global rate + any project with stale_days > 30.>

Example row format:
| Project | Harness | Passed/Total | Rate | Stale |
|---------|---------|--------------|------|-------|
| NG-ROBOT | yes | 12/18 | 66.7% | 3d |
| ZACHVEV | no | — | — | — |

Flag HIGH urgency if: (a) global rate dropped >10pp vs last scan, or (b) any harness-adopted project has stale_days > 30.
```

## After Scanning

1. **Update `.claude/memory/news.md`** (with provenance):
   - Record scan date, mode, and throughput in Scan log
   - Append ACTION items to the **Action Items table** with this format:
     `| <next#> | **Title** — short description | HIGH/MED/LOW | no | — | Concrete next step |`
     The table has columns: `# | Item | Urgency | Acted | Evidence | Next Step`
   - New items always start with `Acted: no` — tracking happens retroactively
   - **Retroactive acted update**: Before adding new items, scan existing items and mark `Acted: **yes**` if evidence exists (commit, learning, decision, config change). Add evidence reference.
   - If an ACTION item from a previous scan is now resolved, move to Resolved section
   - **Clean up DONE items**: Move resolved items from Active to Resolved with date
   - **Deduplicate**: If a Watch List item already exists (same topic), update existing entry

2. **If ACTION items found for orchestration system**:
   - Add to `.claude/memory/learnings.md` under appropriate section
   - If a new skill is suggested, add to Skill Gaps

3. **If ACTION items found for project dependencies**:
   - Note in `.claude/memory/state.md` as a potential future task

4. **Harness adoption health check**:
   - Run `python scripts/passes-rate.py --json` and parse the output
   - Extract `global.rate`, `global.harness_adopted_projects`, and any project with `stale_days > 30`
   - Populate the `### Harness Adoption Health` section of the report
   - Compare `global.rate` against the previous scan's rate (stored in `news.md` scan log):
     - Drop > 10pp → add HIGH urgency ACTION item: "passes-rate regression — investigate"
     - Any project stale_days > 30 → add MED urgency ACTION item: "harness project X idle, check status"
   - Persist current rate in news.md Scan log for next delta

5. **Cross-project improvement routing**:
   - For each HIGH/MED action item: invoke `/improve` to route finding to matching projects
   - `/improve` reads project profiles from `~/.claude/memory/projects/*.yaml`, scores relevance, and creates GitHub issues
   - This ensures findings don't stay STOPA-local but reach the projects where they're actionable
   - Skip routing for STOPA-internal items (skill improvements, memory system changes)

## Cost Control

- **Quick mode**: ~5-8k tokens (3 searches, 1-2 fetches)
- **Papers mode**: ~20-35k tokens (3+5 searches, 2-4 fetches)
- **Voices mode**: ~15-25k tokens (3+4 searches, 2-4 fetches)
- **Full mode**: ~80-120k tokens (19 searches, 7-14 fetches)
- Use `haiku` model for agent spawns if deeper analysis needed
- Never spawn more than 1 agent — do the search/fetch work directly
- If a source consistently returns nothing useful, skip it in future scans (note in news.md)
- Tier 4 blog fetches: max 2 pages — prefer search snippets over full articles

## Scheduling Guidance

Recommended cadence: **weekly** (every Monday or at first session of the week).

How to trigger:
- User runs `/watch` or `/watch full` manually
- Orchestrator checks `.claude/memory/news.md` last scan date — if >7 days, suggest running `/watch`
- User can set up a hook or reminder externally

## When Things Go Wrong

- **WebSearch returns no results for a tier**: Skip that tier, note it in the report. Don't retry with vaguer queries — that adds noise.
- **WebFetch fails on a page**: Use the search snippet summary instead. Don't block the whole scan for one broken URL.
- **All sources return nothing new**: Report "No significant updates since last scan" — this is a valid result, not a failure.
- **news.md is missing or empty**: Create it with the standard template (see Output Format). First scan initializes the file.
- **Tier 4 returns only noise (opinions, drama, no substance)**: This is expected — most influencer output fails the 3-gate filter. Report "Tier 4: No actionable signals this week" and move on. Don't loosen the gates.
- **A voice consistently returns nothing**: After 3 consecutive empty scans, move them to a "dormant" note in news.md. Re-check quarterly or when user mentions them.

## Rules

1. **Signal over noise** — skip irrelevant results ruthlessly. Better to report 3 useful items than 20 tangential ones.
2. **Actionable over informational** — prioritize things the user can act on
3. **Cost-aware** — use parallel searches, minimal fetches, haiku for analysis
4. **No false urgency** — don't mark things [ACTION] unless they genuinely need attention
5. **Cumulative knowledge** — always check previous news.md to avoid reporting the same thing twice
6. **Respect project context** — filter through the lens of CLAUDE.md dependencies and tech stack
