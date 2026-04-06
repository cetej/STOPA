---
name: compile
description: "Use when synthesizing learnings into thematic wiki articles for better retrieval and onboarding. Trigger on 'compile', 'build wiki', 'synthesize memory', 'knowledge base'. Do NOT use for recording individual learnings (/scribe), pruning rules (/evolve), or file optimization (/autoloop)."
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash
tags: [memory, documentation, meta, synthesis]
phase: meta
---

# /compile — Wiki Synthesis Engine

You are the knowledge synthesizer. You read all atomic learnings, decisions, and key facts,
then produce thematic wiki articles that make the full knowledge base discoverable.

**Core principle**: Atomic learnings are write-optimized (easy to create). Wiki articles are
read-optimized (easy to find and apply). Compile bridges the gap.

---

## Shared Memory

Read first:
- `.claude/memory/learnings/critical-patterns.md` — current top patterns
- `.claude/memory/key-facts.md` — project reference data
- `.claude/memory/decisions.md` — decision log index

## Input

Parse `$ARGUMENTS`:
- `--full` (default on first run): Read all learnings, rebuild all wiki articles from scratch
- `--incremental` (default on subsequent runs): Only process learnings changed since last compile
- `--dry-run`: Show clustering plan and predicted articles without writing files

---

## Phase 1: Refresh Manifest & Load Sources

### Step 1.1: Refresh block manifest
Run: `python scripts/build-component-indexes.py`
This regenerates `index-*.md` files and `block-manifest.json` from current YAML frontmatter.
If script doesn't exist or fails, proceed manually — Glob all learnings and parse YAML frontmatter.

### Step 1.2: Load all sources
Read silently:
- `.claude/memory/learnings/block-manifest.json` — structured metadata for all learnings (if exists)
- `.claude/memory/learnings/critical-patterns.md` — current top 10
- `.claude/memory/decisions.md` — decision index
- `.claude/memory/key-facts.md` — project constants
- All individual learning files: Glob `.claude/memory/learnings/2*.md` (date-prefixed files)
- **Raw agent outputs**: Glob `.claude/memory/raw/*.md` — auto-captured agent outputs (if any exist). These are unstructured staging data from sub-agents. Extract key facts and patterns, then move processed files to `.claude/memory/raw/processed/` after compile.

### Step 1.3: Check incremental eligibility
Read `.claude/memory/wiki/.compile-state.json` (if exists).

If `--incremental` AND compile-state exists:
- Compare each learning file's list against stored list in compile-state
- Identify new/deleted learnings by filename comparison
- If >50% of learnings are new/changed since last compile, fall back to `--full`
- Otherwise, only re-synthesize articles whose source learnings changed

If `--full` OR no compile-state exists → process everything.

---

## Phase 2: Cluster Learnings

### Step 2.1: Group by component
From YAML frontmatter, group all active (non-superseded) learnings by `component` field.
Expected components: orchestration, skill, memory, general, pipeline, workflow.

### Step 2.2: Sub-cluster large components
For components with **8+ learnings**, compute tag Jaccard similarity between all pairs:

```
jaccard(A, B) = |tags_A ∩ tags_B| / |tags_A ∪ tags_B|
```

Group learnings where jaccard > 0.2 with at least one other member.
Use single-linkage clustering (merge groups if ANY cross-pair exceeds threshold).
Name each sub-cluster by its 2-3 most common tags.

### Step 2.3: Merge small groups
Components with **< 3 learnings** merge into the nearest cluster by shared tag count.
If no cluster shares tags, create an "Infrastructure & General" catch-all article.

### Step 2.4: Assign article slugs
Each cluster becomes a wiki article. Slug format: `<component>-<theme>.md`

**Output clustering plan BEFORE proceeding** (even in non-dry-run mode):

```
CLUSTERING PLAN:
  1. orchestration-multi-agent (7 learnings): [filenames...]
  2. orchestration-resilience (5 learnings): [filenames...]
  3. skill-design (8 learnings): [filenames...]
  4. memory-architecture (4 learnings): [filenames...]
  5. infrastructure-general (5 learnings): [filenames...]

Total: 5 articles from 44 learnings. 0 uncovered.
```

**Verify**: every active learning appears in exactly one cluster. If any is uncovered, assign it to the nearest cluster.

If `--dry-run`: output clustering plan and STOP. Do not generate articles.

---

## Phase 3: Detect Contradictions & Gaps

### Step 3.1: Intra-cluster contradiction scan
Within each cluster, compare learning summaries pairwise. Flag pairs recommending opposing actions.

```
CONTRADICTIONS FOUND: N
  1. [file-a.md] says "X" BUT [file-b.md] says "Y"
     Resolution: context-dependent | supersedes | unclear
```

### Step 3.2: Cross-cluster gap detection
For each component, check whether the cluster covers core concerns:
- **orchestration**: cost, parallelism, error handling, agent patterns, delegation
- **skill**: design, triggers, evaluation, lifecycle, frontmatter
- **memory**: retrieval, write patterns, maintenance, cross-project
- **general**: security, environment, tools, browser

Missing coverage = knowledge gap:

```
KNOWLEDGE GAPS: N
  1. memory: no learnings about "cross-project memory sharing"
  2. skill: no learnings about "compact variant effectiveness"
```

### Step 3.3: Cross-project scan (optional, only on --full)
Glob `~/.claude/projects/*/memory/MEMORY.md`. Scan each for keyword overlap with local learnings.
Note reinforcing or contradicting patterns. **NEVER write to cross-project files.**

---

## Phase 4: Generate Wiki Articles

For each cluster, generate a wiki article at `.claude/memory/wiki/<slug>.md`.

### Article Template

```markdown
---
generated: YYYY-MM-DD
cluster: <component>-<theme>
sources: N
last_updated: YYYY-MM-DD
---

# <Theme Title>

> **TL;DR**: <2-3 sentence executive summary of this knowledge area>

## Overview

<1-2 paragraphs synthesizing what we know about this theme. Narrative form,
not a bullet list. References source learnings with (ref: filename.md) citations.>

## Key Rules

1. **<Rule name>**: <actionable statement> (ref: <source.md>)
2. **<Rule name>**: <actionable statement> (ref: <source.md>)

## Patterns

### Do
- <Pattern to follow> (ref: <source>)

### Don't
- <Anti-pattern to avoid> (ref: <source>)

## Open Questions

- WARNING: <Contradiction description> — needs resolution
- GAP: <Missing knowledge area> — suggest creating learning about this

## Related Articles

- See also: [<article>](<article>.md)

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [filename](../learnings/filename) | YYYY-MM-DD | high | summary |
```

### Generation Rules

1. **SYNTHESIZE, don't list** — write coherent narrative, not bullet dump of learnings
2. **Every claim cites source**: `(ref: <filename.md>)`
3. **Key Rules section**: grep-friendly actionable statements (imperative form)
4. **Cross-reference**: link related articles with `See also: [name](name.md)`
5. **Source Learnings table**: mandatory, for traceability
6. **Mark contradictions**: `WARNING:` prefix with context boundary explanation
7. **Mark gaps**: `GAP:` prefix with suggestion what learning to create
8. **Max 150 lines per article** — if theme is larger, sub-cluster it

---

## Phase 4.5: Quality Gate (Hermes Pattern)

Before promoting articles, run an independent review. This prevents hallucinated connections from entering the permanent wiki brain.

### For each generated article:

1. **Spawn reviewer sub-agent** (Haiku model, fresh context — no compile history):

```
Agent(model: haiku, prompt: "
  You are an independent knowledge reviewer. You have NO context about how this article was produced.
  Review this wiki article for accuracy and usefulness.

  <article_content>
  {article content here}
  </article_content>

  <source_learnings>
  {source learning summaries — only the summaries, not full files}
  </source_learnings>

  Evaluate:
  1. Does each Key Rule in the article trace to a source learning?
  2. Are there claims not supported by any source?
  3. Are there contradictions between rules?
  4. Is the synthesis coherent or just a list dressed as prose?

  Output EXACTLY this JSON (nothing else):
  {\"approved\": true/false, \"accuracy_concerns\": [...], \"unsupported_claims\": [...], \"quality_score\": 0.0-1.0}
")
```

2. **Fail-closed rule**: If `accuracy_concerns` is non-empty → article is NOT promoted. Move to `.claude/memory/wiki/rejected/` with the reviewer's concerns appended.

3. **Approved articles** → write to `.claude/memory/wiki/<slug>.md` (as in Phase 4).

### When to skip gate (budget optimization):
- `--incremental` with ≤2 articles changed: skip gate, trust contradiction detection from Phase 3
- `--no-gate` flag: explicit user opt-out
- First-ever compile (`--full` with no prior state): run gate on all articles

### Gate metrics (append to compile report):
```
QUALITY GATE: N articles reviewed, M approved, K rejected
  Rejected: <slug> — <primary concern>
```

---

## Phase 5: Generate INDEX.md

Write `.claude/memory/wiki/INDEX.md`:

```markdown
# Knowledge Base — STOPA

> Auto-generated by /compile. Last built: YYYY-MM-DD.
> Health score: X/10 | N learnings → M articles | Run `/recipe knowledge-health` for full audit.

## Start Here

New to this knowledge base? Read these first:
1. **[Top article by source count]** — highest concentration of validated knowledge
2. **[Most recent article]** — latest additions
3. **critical-patterns.md** — the N rules that matter most

Recent additions (last 14 days):
- `learning-filename.md` — one-line summary
- `learning-filename.md` — one-line summary

## Articles

| # | Article | Theme | Sources | Key Insight | Updated |
|---|---------|-------|---------|-------------|---------|
| 1 | [slug](slug.md) | Theme | N | One-line insight | YYYY-MM-DD |

## Health

- **Coverage**: N/M learnings compiled (X%)
- **Contradictions**: N open
- **Gaps**: N identified (topics worth researching next)
- **Stalest article**: <slug> (N days since last update)
- **Unused learnings**: N (uses=0, older than 60 days)
- **Next action**: most urgent recommendation (e.g., "compile stale", "prune decaying")

## By Component

- **orchestration**: [article1](article1.md), [article2](article2.md)
- **skill**: [article3](article3.md)

## By Tag (top 10)

- `multi-agent`: [orchestration-multi-agent](orchestration-multi-agent.md)
- `evaluation`: [skill-evaluation](skill-evaluation.md)
```

Health score formula: `10 - (stale_articles × 0.5) - (contradictions × 1.5) - (gaps × 0.5) - (unused_learnings × 0.3)`, clamped to 1-10.

**Max 90 lines.** INDEX.md is the entry point for session onboarding — keep it scannable.
"Start Here" section is the key UX improvement: tells Claude AND user what to read first.

---

## Phase 6: Write Compile State

Write `.claude/memory/wiki/.compile-state.json`:

```json
{
  "last_compile": "2026-04-04T12:00:00Z",
  "compile_mode": "full",
  "total_learnings": 52,
  "total_articles": 7,
  "contradictions": 2,
  "gaps": 3,
  "articles": {
    "orchestration-multi-agent.md": {
      "source_learnings": ["2026-03-29-bigmas.md", "2026-04-02-distributed.md"],
      "generated": "2026-04-04"
    }
  },
  "learnings_compiled": ["2026-03-23-youtube.md", "2026-03-24-fix-issue.md"]
}
```

---

## Phase 7.5: Generate Per-Skill Briefings

After wiki articles are finalized, generate role-filtered briefings for skills.

### Briefing generation:

For each role category, read wiki articles matching that role's tags and produce a condensed briefing:

| Role | Wiki tags to include | Output file |
|------|---------------------|-------------|
| orchestration | orchestration, planning, multi-agent, resilience | `.claude/memory/briefings/orchestration.md` |
| research | research, osint, exploration | `.claude/memory/briefings/research.md` |
| code-quality | code-quality, review, testing, debugging | `.claude/memory/briefings/code-quality.md` |
| memory | memory, session, documentation | `.claude/memory/briefings/memory.md` |

### Briefing format:
```markdown
# Briefing: <Role> — Auto-generated by /compile
> Last updated: YYYY-MM-DD | Source: N wiki articles

## Key Rules (actionable, grep-friendly)
- <rule from wiki article> (ref: <wiki-slug>)

## Anti-Patterns
- <don't do this> (ref: <wiki-slug>)

## Recent Insights
- <newest patterns from most recent wiki articles>
```

### Rules:
- **Max 2000 words per briefing** (OpenClaw bootstrap cap reference)
- Prioritize Key Rules from wiki articles — skip verbose narratives
- Most recent articles first (by `last_updated` date)
- If a wiki article matches multiple roles, include in all matching briefings
- Briefings are READ-ONLY for skills — /compile owns them

---

## Phase 7.7: News→Learning Bridge

Scan `.claude/memory/news.md` for ACTION items not yet reflected in learnings.

### Step 7.7.1: Extract actionable signals
Read `news.md`. Extract entries tagged `ACTION` that have a date within last 60 days.

### Step 7.7.2: Cross-reference with existing learnings
For each ACTION item, grep learnings/ for keywords (tool name, concept, version).
If a matching learning already exists → skip.

### Step 7.7.3: Propose new learnings
For unmatched ACTION items, output proposals:

```
NEWS→LEARNING BRIDGE: N unmatched action items found
  1. [news] "Sonnet 4.6 GA with 1M context" → No learning about model tier update
     → Propose: learning about orchestration model-tier adjustment
  2. [news] "mcp-scan tool poisoning detector" → Already covered by 2026-04-03-mcp-scan.md
     → Skip
```

**Rules:**
- Read-only on news.md — never modify it
- Only propose, never auto-create learnings (that's /scribe's job)
- Max 5 proposals per compile run (focus on highest-impact)
- Skip WATCH and INFO items — only ACTION items matter

---

## Phase 8: Report

Output final report:

```
COMPILE COMPLETE
  Mode: full | incremental
  Learnings processed: N (M new since last compile)
  Articles generated: N (K updated, J unchanged)
  Contradictions: N (M resolved in-article, K need /evolve)
  Knowledge gaps: N
  Cross-project patterns: N reinforcing, M contradicting (if --full)

  Wiki location: .claude/memory/wiki/
  Entry point: .claude/memory/wiki/INDEX.md

  Recommended follow-ups:
  - [if contradictions] Run /evolve to resolve contradicting learnings
  - [if gaps] Run /scribe to create learnings for identified gaps
  - [if stale learnings] Run /evolve for pruning audit
```

---

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll just update the index files, no need for full wiki articles" | Index files list but don't synthesize. The retrieval gap exists because listing ≠ understanding. | Generate proper wiki articles with narrative synthesis, key rules, and cross-references. |
| "Learnings are short, I'll concatenate them into one big file" | Concatenation is not synthesis. A pile of atomic facts is no more discoverable than scattered files. | Write each article as coherent narrative connecting insights and extracting actionable rules. |
| "I'll skip contradiction detection to save time" | Contradictions are the highest-value output. Two learnings recommending opposite actions silently degrade every skill that retrieves them. | Always run contradiction scan. In incremental mode, scan only changed clusters. |
| "The clustering looks wrong but I'll proceed" | Bad clustering → bad articles. An article mixing unrelated learnings wastes context tokens on irrelevant content. | Show clustering plan. Adjust if any cluster mixes unrelated themes. |
| "I don't need to cite source learnings" | Without citations, articles are untraceable. When a source learning is updated or pruned, no way to know which articles need regeneration. | Every factual claim cites `(ref: filename.md)`. Source Learnings table is mandatory. |
| "Cross-project scan found useful patterns, I'll import them" | Cross-project memory is owned by other contexts. Auto-importing can introduce irrelevant or conflicting knowledge. | Report cross-project patterns. Never auto-write to cross-project files or auto-import. |

## Red Flags

STOP and re-evaluate if any of these occur:

- Generating a wiki article that exceeds 150 lines (reproducing, not synthesizing)
- Any active learning not covered by any wiki article after Phase 4
- An article has 0 citations to source learnings
- Overwriting articles without checking incremental state first
- Running `--full` when `--incremental` was appropriate and <50% changed
- Skipping contradiction detection entirely
- Wiki articles containing verbatim copy-paste from learning files
- INDEX.md and compile report disagreeing on counts

## Verification Checklist

- [ ] block-manifest.json regenerated or learnings parsed manually (Phase 1)
- [ ] Every active learning appears in exactly one wiki article cluster
- [ ] Each wiki article has YAML frontmatter (generated, cluster, sources, last_updated)
- [ ] Each wiki article has narrative Overview section (not just bullet lists)
- [ ] Each wiki article has Key Rules section with grep-friendly statements
- [ ] Each factual claim cites source with `(ref: filename.md)`
- [ ] Each article has Source Learnings table at bottom
- [ ] Contradictions marked with `WARNING:` in relevant articles
- [ ] Knowledge gaps marked with `GAP:` in relevant articles
- [ ] INDEX.md generated with articles table, health summary, and quick reference
- [ ] INDEX.md is under 80 lines
- [ ] .compile-state.json written with full article→learnings mapping
- [ ] Compile report outputs counts matching INDEX.md

## Rules

1. **Synthesis, not reproduction** — wiki articles must be narratives, not concatenated learnings
2. **100% coverage** — every active, non-superseded learning in exactly one article
3. **Citation mandatory** — every claim cites `(ref: filename.md)`
4. **150-line article cap** — if a theme is larger, sub-cluster it
5. **80-line INDEX cap** — must be cheap to read for /status and /checkpoint
6. **Incremental default** — full rebuild only on first run or >50% changed
7. **Source files read-only** — compile never modifies learnings, decisions, or key-facts
8. **No sub-agents** — single-pass synthesis in main context (corpus fits)
9. **Manifest-first** — always refresh or parse manifest before compilation
10. **Cross-project read-only** — scan but never write to `~/.claude/projects/*/memory/`
11. **Clustering transparency** — always show plan before generating articles
