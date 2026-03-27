---
name: watch
description: Use when scanning for AI/ML ecosystem news, Claude Code updates, or arXiv research papers. Trigger on 'watch', 'news', "what's new", 'novinky', 'papers', 'arXiv'. Do NOT use for web browsing (/browse).
argument-hint: [full / quick / papers / topic:specific-topic]
user-invocable: true
allowed-tools: Read, Write, Edit, WebSearch, WebFetch, Agent
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: ""
---

# Watch — News & Updates Scanner

You scan external sources for news, updates, and changes relevant to this project and its orchestration system. You report findings and suggest actionable improvements.

## Decision Tree — /watch vs alternatives

Use this tree when you're unsure whether to invoke `/watch` or do something simpler:

```
Do I need broad situational awareness about the AI ecosystem?
├── YES → /watch (full or quick)
│
└── NO — Is it a specific, targeted question?
    ├── "What's the latest version of library X?" → WebSearch directly (1 call, no overhead)
    ├── "Is there a breaking change in diffusers 0.33?" → WebFetch the changelog directly
    ├── "Check if Claude Code has new hooks" → /watch quick (Tier 1 only)
    └── "What changed since last Monday?" → /watch full (checks news.md last-scan date)
```

**Concrete examples:**

| Situation | Right choice | Reason |
|-----------|-------------|--------|
| Start of week, no recent scan | `/watch` or `/watch full` | Broad sweep needed |
| Investigating a specific import error | Direct `WebSearch` | Targeted — `/watch` overhead not worth it |
| `/watch` just ran 2 days ago but you want Claude API news only | `/watch quick` | Narrow scope, cheap |
| Planning a major dependency upgrade | `/watch topic:pytorch` then `/dependency-audit` | Focused research + deep audit |
| User asks "anything new?" with no context | `/watch quick` first, upgrade to `full` if Tier 1 returns nothing | Progressive cost escalation |
| Already have recent news.md with relevant findings | Re-read `news.md` directly | Don't re-scan what's already cached |
| Need latest research papers only | `/watch papers` | Tier 2b only, ~10k tokens |

## Shared Memory

1. Read `.claude/memory/news.md` — previous findings and last scan date
2. Grep `.claude/memory/learnings/` for keywords related to current scan topics — spot relevant existing patterns
3. Read `CLAUDE.md` — project dependencies and tech stack (to know what to watch)

## Input

Parse `$ARGUMENTS` using the following logic:

```
raw = strip($ARGUMENTS)

if raw is empty or raw == "full":
    mode = "full"
    topic = null

elif raw == "quick":
    mode = "quick"
    topic = null

elif raw == "papers":
    mode = "papers"
    topic = null

elif raw starts with "topic:":
    mode = "topic"
    topic = raw.split("topic:")[1].strip()
    if topic is empty → default to "full" mode, warn user

else:
    # Treat unrecognized input as a free-form topic
    mode = "topic"
    topic = raw
```

**Edge cases:**
- `$ARGUMENTS` not provided → treat as `full`
- `topic:` with no value → fall back to `full` and note the missing topic
- Multiple arguments (e.g., `full topic:pytorch`) → ignore second token, use first recognized mode; note ambiguity in report header
- Numeric or invalid input → treat as `full`, add note to report

**Mode summary:**

| Argument | Mode | Tiers scanned | Approx. cost |
|----------|------|---------------|-------------|
| _(empty)_ or `full` | full | 1 + 2 + 2b + 3 | ~50–75k tokens |
| `quick` | quick | 1 only | ~5–8k tokens |
| `papers` | papers | 2b only | ~10–15k tokens |
| `topic:X` | topic | 1 + filtered 2/3 | ~10–20k tokens |

## Source Tiers

### Tier 1: Claude Code & Anthropic (always scan)

Use `WebSearch` for each:
1. **Claude Code releases** — search: `"claude code" changelog OR release notes site:docs.anthropic.com OR site:github.com/anthropics {current_year}`
2. **Claude API updates** — search: `anthropic claude API new features OR models {current_year}`
3. **Claude skills/hooks** — search: `"claude code" skills OR hooks OR MCP new {current_year}`

For each result, `WebFetch` the most relevant 1-2 pages.

### Tier 2: AI/ML Ecosystem (scan on "full")

Use `WebSearch` for each:
4. **PyTorch** — search: `pytorch release OR blog {current_year} {current_month}`
5. **HuggingFace + diffusers** — search: `huggingface diffusers release OR update {current_year}`
6. **Flow matching / video generation** — search: `"flow matching" OR "video generation" model paper {current_year}`
7. **timm / einops** — search: `timm OR einops release {current_year}` (skip if no results)

### Tier 2b: Research Papers (scan on "full" or "papers")

Use `WebSearch` for arXiv papers from last 30 days:
8. **Agent/orchestration papers** — search: `site:arxiv.org "LLM agent" OR "tool use" OR "multi-agent" {current_year} {current_month}`
9. **Code generation / SWE papers** — search: `site:arxiv.org "code generation" OR "software engineering" LLM benchmark {current_year}`
10. **Prompt engineering papers** — search: `site:arxiv.org "prompt engineering" OR "chain of thought" OR "in-context learning" {current_year} {current_month}`

Also check: `WebFetch` on `https://huggingface.co/papers` for trending papers.

For each paper: note title, arxiv ID, key finding, relevance to STOPA, and whether code is available.

### Tier 3: Community (scan on "full")

Use `WebSearch` for each:
11. **GitHub trending** — search: `github trending python machine learning video generation {current_month} {current_year}`
12. **Reddit** — search: `site:reddit.com (r/LocalLLaMA OR r/StableDiffusion) "flow matching" OR "video generation" OR "pyramid" {current_year}`
13. **General AI news** — search: `AI tools developer productivity {current_month} {current_year}`

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
- If "full" or "papers" mode, launch Tier 2b (items 8-10) in parallel
- If "full" mode, launch Tier 3 (items 11-13) in parallel
- Fetch detailed pages only for promising results

## Output Format

```markdown
## Watch Report — <date>

**Mode**: full / quick / papers / topic:X
**Sources scanned**: N
**Items found**: N (X action, Y watch, Z info)

### Action Items

| # | Source | Finding | Suggested Action |
|---|--------|---------|-----------------|
| 1 | Claude Code v1.X | New skill hooks API | Update orchestration to use new hooks |
| 2 | diffusers 0.32 | Breaking change in scheduler API | Check compatibility with our schedulers |

### Watch List

| # | Source | Finding | Why It Matters |
|---|--------|---------|---------------|
| 1 | arxiv | New flow matching technique | Could improve generation quality |

### Info

- <brief bullet points for [INFO] items>

### Recommendations for Orchestration System

<If any findings suggest improvements to the skill system, list them here>

### Recommendations for Active Projects

<If any findings affect project dependencies or techniques, list them here>
```

## After Scanning

1. **Update `.claude/memory/news.md`**:
   - Record scan date and mode
   - Append ACTION and WATCH items (not INFO — too noisy)
   - If an ACTION item from a previous scan is now resolved, mark it done

2. **If ACTION items found for orchestration system**:
   - Add to `.claude/memory/learnings/` as a new file with YAML frontmatter (date, type, component, tags)
   - If a new skill is suggested, add to Skill Gaps

3. **If ACTION items found for project dependencies**:
   - Note in `.claude/memory/state.md` as a potential future task

## Cost Control

- **Quick mode**: ~5-8k tokens (3 searches, 1-2 fetches)
- **Papers mode**: ~10-15k tokens (3 searches, 1-2 fetches)
- **Full mode**: ~50-75k tokens (13 searches, 5-10 fetches)
- Use `haiku` model for agent spawns if deeper analysis needed
- Never spawn more than 1 agent — do the search/fetch work directly
- If a source consistently returns nothing useful, skip it in future scans (note in news.md)

## When NOT to Use /watch

Skip `/watch` in these situations — use a more targeted tool instead:

| Situation | Better alternative |
|-----------|-------------------|
| Need to check a **specific library version** right now | `WebSearch` or `WebFetch` directly |
| Running a **quick bug-fix session** (no time for news) | Skip — run `/watch` at the next natural pause |
| Last scan was **< 3 days ago** | Nothing meaningful will have changed; skip |
| Working **offline or with limited tokens** | Use `/watch quick` only, or defer to next session |
| Need news **outside the project's tech stack** | Manual search — `/watch` is filtered to CLAUDE.md dependencies |
| The task is urgent and news context isn't needed | Start the task, run `/watch` afterwards |

**Don't invoke `/watch` just to fill context** — it costs 5–75k tokens and adds noise if the task is already well-defined.

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

## Related Skills

| Skill | When to chain with /watch |
|-------|--------------------------|
| `/budget` | Run `/budget check` **before** a full scan to confirm you have token headroom — full mode costs up to 75k tokens. If budget is tight, downgrade to `quick` mode. |
| `/orchestrate` | If `/watch` surfaces multiple [ACTION] items that require coordinated changes across files or services, hand off to `/orchestrate` with a summary of the action items. `/watch` finds; `/orchestrate` acts. |
| `/dependency-audit` | When `/watch` flags a version bump for a library in the stack, follow up with `/dependency-audit` for a deep compatibility check before upgrading. |
| `/checkpoint` | After a `/watch full` scan that produces multiple action items, run `/checkpoint save` to preserve the findings across session boundaries. |
| `/scribe` | After acting on a `/watch` [ACTION] item, use `/scribe` to record the decision in `decisions.md` and the learning in `learnings.md`. |

## Rules

1. **Signal over noise** — skip irrelevant results ruthlessly. Better to report 3 useful items than 20 tangential ones.
2. **Actionable over informational** — prioritize things the user can act on
3. **Cost-aware** — use parallel searches, minimal fetches, haiku for analysis
4. **No false urgency** — don't mark things [ACTION] unless they genuinely need attention
5. **Cumulative knowledge** — always check previous news.md to avoid reporting the same thing twice
6. **Respect project context** — filter through the lens of CLAUDE.md dependencies and tech stack
