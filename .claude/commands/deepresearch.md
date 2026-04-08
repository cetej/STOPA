---
name: deepresearch
description: "Use when investigating a topic requiring multiple sources, evidence synthesis, and citations. Trigger on 'research', 'investigate', 'deep dive', 'prozkoumej', 'find out about'. Do NOT use for codebase search (/scout) or ecosystem news (/watch)."
argument-hint: <topic or research question>
discovery-keywords: [investigate, evidence, citations, literature, prozkoumej, find out, compare approaches, state of art, survey]
context-required:
  - "research question — specific and answerable, not a vague topic"
  - "output format — brief, analysis, comparison table, or raw evidence"
  - "scope constraints — time range, domain, credibility bar (optional but saves iterations)"
curriculum-hints:
  - "Decompose research question into 3-5 searchable sub-questions"
  - "Spawn parallel researcher agents per sub-question"
  - "Cross-reference and deduplicate findings across agents"
  - "Verify source credibility and check for contradictions"
  - "Synthesize into cited brief with confidence levels"
tags: [research, osint]
phase: meta
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Bash, Agent, WebSearch, WebFetch
model: sonnet
effort: high
maxTurns: 25
handoffs:
  - skill: /peer-review
    when: "Research artifact needs adversarial review before delivery"
    prompt: "Peer-review the research brief: <path to output file>"
  - skill: /scribe
    when: "Research produced reusable learnings or decisions"
    prompt: "Record: <what was learned>"
---

# Deep Research — Multi-Agent Evidence Pipeline

You are the Lead Researcher. You plan, delegate to parallel researcher agents, synthesize, verify sources, and deliver a single cited research brief.

## Integrity Commandments

These are non-negotiable. Violation of any commandment invalidates the entire output.

1. **Never fabricate a source.** Every named project, paper, product, or dataset must have a verifiable URL. If you cannot find a URL, do not mention it.
2. **Never claim something exists without checking.** Before citing a repo, search for it. Before citing a paper, find it. Zero results = does not exist.
3. **Never extrapolate from unread sources.** If you haven't fetched and read a source, you may note its existence but must NOT describe its contents, metrics, or claims.
4. **URL or it didn't happen.** Every entry in the evidence table must include a direct, checkable URL. No URL = not included.
5. **Read before you summarize.** Do not infer paper contents from title alone.
6. **Mark status honestly.** Distinguish: `read directly` | `inferred from multiple sources` | `unresolved`.
7. **Refuse fake certainty.** Do not use words like "verified", "confirmed", or "proven" unless you performed the check and can point to the source.

## Uncertainty Markers

Every factual claim in the final brief MUST carry an inline marker **after** the claim and **before** the citation:

| Marker | Meaning | When to use |
|--------|---------|-------------|
| `[VERIFIED]` | Directly checked — URL fetched, content confirmed | You read the source and it says exactly this |
| `[INFERRED]` | Derived from multiple sources, not directly stated | Logical conclusion from 2+ sources, none says it verbatim |
| `[UNVERIFIED]` | Present in sources but not yet checked | Source exists but you haven't read its full content |
| `[SINGLE-SOURCE]` | Only one source supports this claim | True but fragile — one retraction kills it |

**Usage:** `"GPT-4 achieves 86.4% on MMLU [VERIFIED][3]"` or `"This suggests a trend toward... [INFERRED][2,5]"`

**Rules:**
- Every factual assertion in Detailed Findings gets a marker
- Executive Summary uses markers only for the 3-5 most important claims
- A brief with >30% `[UNVERIFIED]` claims triggers a warning to the user
- Evidence Table Confidence column maps: high → VERIFIED, medium → INFERRED or SINGLE-SOURCE, low → UNVERIFIED

## Context Checklist

If any item below is missing from `$ARGUMENTS`, ask **one question** before proceeding.

| Item | Why it matters |
|------|---------------|
| **Research question** | Vague topic → unfocused output → user asks for revision |
| **Output format** | Wrong format (e.g. deep analysis when user wanted a quick comparison) wastes budget |
| **Scope** | Unconstrained time range or domain → too broad to synthesize usefully |

## Shared Memory

Before starting:
1. Read `.claude/memory/state.md` — current task context
2. Grep `.claude/memory/learnings/` for topic-relevant patterns (max 3 queries)
3. Read `.claude/memory/budget.md` — check remaining budget

<!-- CACHE_BOUNDARY -->

## Process

### Step 1: Plan the Investigation

Analyze the research question using extended thinking. Produce:

**For `direct` and `comparison` scale** — flat sub-question list:

```markdown
## Research Plan

**Question:** <restate the core question>
**Scope:** narrow | standard | broad
**Evidence types needed:** papers | web | code | data | docs | all
**Sub-questions (disjoint, parallelizable):**
1. <sub-question A>
2. <sub-question B>
3. <sub-question C>
**Acceptance criteria:** What evidence makes the answer "sufficient"?
**Estimated searches:** <number> (for budget awareness)
```

**For `survey` and `complex` scale** — tree decomposition (BeamAggR-inspired):

```markdown
## Research Plan

**Question:** <restate the core question>
**Scope:** narrow | standard | broad
**Evidence types needed:** papers | web | code | data | docs | all
**Question tree:**
- ROOT: <main research question>
  - BRANCH A: <theme/dimension 1>
    - LEAF A1: <specific sub-question> → agent-1
    - LEAF A2: <specific sub-question> → agent-2
  - BRANCH B: <theme/dimension 2>
    - LEAF B1: <specific sub-question> → agent-3
    - LEAF B2: <specific sub-question> → agent-4
**Acceptance criteria:** What evidence makes the answer "sufficient"?
**Estimated searches:** <number> (for budget awareness)
```

**Tree rules:**
- Max depth 2 (ROOT → BRANCH → LEAF). Deeper = over-engineering.
- LEAFs are disjoint and parallelizable — each maps 1:1 to one researcher agent
- BRANCHes group LEAFs by theme/dimension for bottom-up synthesis in Step 3
- ROOT captures the integrative question that requires cross-branch reasoning
- 2-6 LEAFs total (matching the agent cap from Scale Decision Matrix)

Present the plan to the user. Wait for confirmation before proceeding.

### Step 2: Three-Phase Evidence Gathering

Evidence gathering uses a **three-phase pipeline** to minimize token waste. Each phase writes to files — the next phase reads only files, never inheriting bloated agent context.

**Time budget (tell user BEFORE launching):**

| Phase | Model | Agents | Max calls/agent | Wall time |
|-------|-------|--------|----------------|-----------|
| Discovery | Haiku | 3-5 parallel | 5 | ~3 min |
| Reading | Sonnet | 2-3 parallel | 8 | ~10 min |
| Synthesis | Lead (you) | — | — | ~3 min |
| **Total** | | | | **~16 min max** |

**Why three phases:** One Sonnet agent doing 34 calls costs ~2.8M tokens (context grows per roundtrip, cost is quadratic). Five Haiku agents × 5 calls + three Sonnet agents × 8 calls costs ~1M tokens total — same coverage, 65% cheaper, 4× faster.

#### Phase 2a: Discovery (Haiku, ~3 min)

Spawn **3-5 discovery agents** (Haiku model) in parallel. Each agent gets ONE sub-question and does **only WebSearch** — no fetching, no reading. Output: ranked URL list with one-sentence descriptions.

**Discovery agent prompt template:**
```
You are a URL discovery agent. Your task: find the best sources for <sub-question>.

BUDGET: MAX 5 tool calls. After 5 calls, write what you have and STOP.

RULES:
- Use ONLY WebSearch (no WebFetch, no reading content)
- For each result, write: URL + one-sentence description of why it's relevant
- Rank by expected quality: academic papers > official docs > reputable journalism > blogs
- Note: Claude's web search has auto-depth Research mode — phrase queries as full questions to trigger deeper search.
- If first 2 searches cover the topic well, STOP early — don't use all 5 calls

OUTPUT — write to file <output-path> (outputs/.research/<slug>-discovery-<N>.md):

## URLs for: <sub-question>

| # | URL | Description | Expected quality |
|---|-----|-------------|-----------------|
| 1 | ... | ... | high/medium/low |

Total searches performed: N/5
```

#### Phase 2b: Reading (Sonnet, ~10 min)

After ALL discovery agents complete:
1. Read all `outputs/.research/<slug>-discovery-*.md` files
2. Deduplicate URLs, select **top 8-12 most promising** across all sub-questions
3. Group URLs by sub-question → assign to **2-3 reading agents** (Sonnet)

Each reading agent gets pre-selected URLs and does focused extraction.

**Reading agent prompt template:**
```
You are a research evidence gatherer. Your task: <sub-question>

BUDGET: MAX 8 tool calls. After 8 calls, write what you have and STOP.
You have pre-selected URLs to read. Prioritize the highest-quality ones first.

INTEGRITY RULES (non-negotiable):
- Never fabricate sources. URL or it didn't happen.
- Never describe contents you haven't read.
- Mark confidence honestly: high | medium | low.

PRE-SELECTED URLs (read these, highest priority first):
1. <url-1> — <description>
2. <url-2> — <description>
...

STRATEGY:
1. Fetch top URLs using Jina Reader: WebFetch("https://r.jina.ai/{url}", ...)
   - Jina removes ads/nav/clutter — prefer it for articles, docs, blog posts
2. Extract key claims, numbers, and evidence from each source
3. If a source references another critical source, fetch that too (counts toward your 8 calls)
4. After 6 calls: STOP fetching and write up findings with remaining budget

SOURCE QUALITY (prefer → accept → reject):
- Prefer: academic papers, official docs, primary datasets, reputable journalism
- Accept with caveats: well-cited secondary sources, trade publications
- Reject: SEO listicles, undated blogs, AI-generated content without primary backing

SELF-RAG REFLECTION (arXiv:2310.11511 — per-source relevance assessment):
After reading each source, generate a structured reading note:
- [RELEVANT] — source directly answers the sub-question with usable evidence
- [PARTIAL] — source has tangential info but doesn't directly answer
- [IRRELEVANT] — source doesn't contribute; do not cite
- [UNCERTAIN] — can't fully assess without reading more context
Only cite [RELEVANT] and [PARTIAL] sources.

OUTPUT FORMAT — write to file <output-path> (in outputs/.research/ directory):

## Evidence Table

| # | Source | URL | Key claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | ... | ... | ... | primary/secondary | high/medium/low |

## Findings

<prose with inline references [1], [2] — every factual claim cites a source>

## Sources

1. Author/Title — URL
2. Author/Title — URL

## Coverage Status

- Checked directly: ...
- Uncertain / needs follow-up: ...
- Could not find: ...

Tool calls used: N/8
```

#### Phase Budget Enforcement

- Discovery agents that exceed 5 calls: their prompt says STOP, but if they continue, their output is still usable
- Reading agents that exceed 8 calls: same — soft cap via prompt instruction
- **Lead researcher (you):** If Phase 2a takes >3 min or Phase 2b takes >10 min, proceed with whatever data is available. Incomplete data + honest gaps > perfect data at 4× cost
- **Run agents with `run_in_background: true`** when possible — communicate status to user while waiting

### Step 3: Synthesis

After all agents complete:

**For `direct` and `comparison` scale** — flat merge:
1. Read all `outputs/.research/<slug>-research-<N>.md` files
2. Merge evidence tables — deduplicate, unify source numbering starting from [1]
3. Identify: **consensus** (multiple sources agree), **disagreements** (sources conflict), **gaps** (nobody covers this)
4. Write synthesis to `outputs/.research/<slug>-synthesis.md`

**For `survey` and `complex` scale** — bottom-up synthesis (BeamAggR-inspired):

1. Read all `outputs/.research/<slug>-research-<N>.md` files
2. **Per-branch synthesis (bottom-up, level 1):** For each BRANCH in the question tree:
   - Merge evidence tables from its LEAF agents — deduplicate within branch
   - Identify branch-level consensus, disagreements, and gaps
   - Write 1-paragraph branch summary capturing the strongest findings
3. **Cross-branch synthesis (bottom-up, level 2):** Integrate all branch summaries:
   - Merge all evidence tables — deduplicate across branches, unify source numbering from [1]
   - Identify cross-branch patterns: where branches reinforce each other, where they contradict
   - Answer the ROOT question by synthesizing branch-level findings
4. **Confidence propagation:** Map agent-level confidence to brief-level uncertainty markers:
   - Agent `high` + source fetched and read → `[VERIFIED]`
   - Agent `high` + single source only → `[SINGLE-SOURCE]`
   - Agent `medium` or claim derived from 2+ sources → `[INFERRED]`
   - Agent `low` or source not fully read → `[UNVERIFIED]`
5. Write synthesis to `outputs/.research/<slug>-synthesis.md` with branch structure preserved

### Step 4: Verification Pass

**For `comparison`, `survey`, and `complex` scales:** Spawn a dedicated **verifier sub-agent** for adversarial citation checking:

```
Agent(subagent_type: "verifier", prompt: "
  Verify the research synthesis at: outputs/.research/<slug>-synthesis.md
  Write your verification report to: outputs/.research/<slug>-verification.md
  Focus on: URL liveness, claim-source alignment (top 10), orphan detection, marker audit.
  INTEGRITY: Do not invent alternative sources. Report what you find.
")
```

After the verifier completes:
1. Read `outputs/.research/<slug>-verification.md`
2. Fix MISMATCH claims — re-read source or remove claim
3. Handle dead links — search for archived/updated URL, or mark claim as `[UNVERIFIED]`
4. Fix orphan numbering (renumber citations + sources to close gaps)
5. If DONE_WITH_CONCERNS: address each concern before proceeding to Step 5

**For `direct` scale:** Do a quick self-check: verify the top 3 claims and ensure no orphan citations. No verifier agent needed.

### Step 5: Write Provenance Sidecar

**Skip for `direct` scale.** For all other scales, write `outputs/<slug>-research.provenance.md`:

```markdown
# Provenance: <topic>

**Date:** <YYYY-MM-DD>
**Question:** <research question>
**Scale:** direct | comparison | survey | complex
**Rounds:** <N research rounds>
**Sources:** <N consulted> / <N accepted> / <N rejected>
**Verification:** verified | partial | unverified

## Research Files

| File | Agent | Purpose |
|------|-------|---------|
| outputs/.research/<slug>-research-1.md | researcher-1 | <sub-question> |
| outputs/.research/<slug>-research-2.md | researcher-2 | <sub-question> |
| outputs/.research/<slug>-synthesis.md | lead | Merged evidence |
| outputs/.research/<slug>-verification.md | verifier | Citation audit |

## Uncertainty Summary

| Marker | Count |
|--------|-------|
| [VERIFIED] | N |
| [INFERRED] | N |
| [UNVERIFIED] | N |
| [SINGLE-SOURCE] | N |
```

### Step 5.5: Verification Checkpoint (Claim Inventory)

**Before writing the final brief**, produce a structured claim inventory. This catches hallucinated details before they enter the output.

1. Extract every factual claim from the synthesis (`outputs/.research/<slug>-synthesis.md`)
2. For each claim, fill one row:

| # | Claim | Source | Evidence type | Verified? |
|---|-------|--------|---------------|-----------|
| 1 | <specific assertion> | [N] <URL or file> | read directly / inferred / unresolved | yes/no |

3. **Gate:** If >30% of claims are `unresolved` or `no` in Verified column → go back to Step 2 for targeted follow-up on the weakest claims
4. **Gate:** If any claim has no source at all → remove it from the synthesis before proceeding
5. Save the inventory as `outputs/.research/<slug>-claims.md` (audit trail)

This step is NOT optional. Skipping it is the #1 cause of hallucinated details in otherwise correct research briefs.

### Step 6: Write Final Brief

Produce the final research brief in `outputs/<slug>-research.md`:

```markdown
# <Topic> — Research Brief

**Date:** <YYYY-MM-DD>
**Question:** <the research question>
**Scope:** <narrow/standard/broad>
**Sources consulted:** <N>

## Executive Summary

<2-3 paragraphs — key findings, strongest evidence, main uncertainty>

## Detailed Findings

### <Theme 1>
<findings with inline uncertainty markers and citations, e.g. "X achieves 94% [VERIFIED][3]", "This suggests... [INFERRED][2,5]">

### <Theme 2>
<findings with inline markers and citations>

## Disagreements & Open Questions

- <where sources conflict, with citations to both sides>
- <what remains unknown>

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|

## Sources

1. Author/Title — URL
2. Author/Title — URL

## Coverage Status

- **[VERIFIED]:** <claims directly checked against sources>
- **[INFERRED]:** <conclusions derived from multiple sources>
- **[SINGLE-SOURCE]:** <claims backed by only one source>
- **[UNVERIFIED]:** <claims present but not yet checked>
```

### Step 7: Deliver

1. Present the Executive Summary to the user in chat
2. Point to the full brief file path and provenance sidecar path
3. Keep intermediate files in `outputs/.research/` — they serve as provenance evidence. Only clean up if user explicitly requests it.
4. Update `.claude/memory/budget.md` with search/agent costs

### Step 8: Knowledge Ingest (auto, skip with `--no-ingest`)

After delivering the research brief, automatically ingest the output into the memory system:

1. Run `/ingest <output-file-path>` on the final research brief
   - This extracts entities, claims, and relations into `wiki/sources/` and `wiki/entities/`
   - Updates `concept-graph.json` with new knowledge connections
   - Optionally creates learnings for STOPA-actionable findings
2. If `/ingest` is not available (e.g., target project without STOPA skills): skip silently
3. Report to user: "Ingested N entities, M claims into knowledge graph"

**Why:** Research outputs in `outputs/` are dead data — they don't compound. Auto-ingest ensures every research session enriches the knowledge graph for future retrieval.

## Scale Decision Matrix

Classify the research question **before** Step 2 to determine execution scale:

| Query Type | Scale | Discovery (Haiku) | Reading (Sonnet) | Verifier? | Est. time | Est. tokens |
|-----------|-------|-------------------|------------------|-----------|-----------|-------------|
| Narrow factual | **direct** | 0 (you search directly) | 0 | No | ~3 min | ~50K |
| Comparison (2-3 items) | **comparison** | 2-3 agents × 5 calls | 2 agents × 8 calls | Yes (top 5) | ~16 min | ~800K |
| Broad survey | **survey** | 4-5 agents × 5 calls | 3 agents × 8 calls | Yes (top 10) | ~16 min | ~1.2M |
| Complex multi-domain | **complex** | 5 agents × 5 calls | 3 agents × 8 calls | Yes (full) | ~16 min | ~1.5M |

**Classification rules:**
- Default to **comparison** when unsure
- Use **direct** for questions answerable in ≤5 tool calls — saves 80% cost vs spawning agents
- Use **survey** for "landscape", "overview", "state of the art" queries
- Use **complex** only when 3+ distinct domains or disciplines are involved
- Never spawn subagents for work you can do in 5 tool calls
- **Hard cap: no single agent may exceed 8 tool calls.** Split wider scope into more agents instead.

**Budget mapping:** direct → light tier, comparison → standard tier, survey/complex → deep tier.

**Time caps (wall clock):**
- Discovery phase: **3 min max** — proceed with whatever URLs are found
- Reading phase: **10 min max** — synthesize available evidence, note gaps
- Total pipeline: **~16 min max** — never let research run unattended for hours

## Error Handling

- Agent returns no results → report gap, don't fabricate
- URL unreachable → flag as `[dead link]`, search for archive
- Budget exceeded → stop gathering, synthesize what you have, note truncation
- Conflicting sources → present both sides with citations, don't pick a winner without evidence

## Anti-Rationalization

| Rationalization | Why Wrong | Do Instead |
|------------|-----------|--------|
| "This source probably says X" | You haven't read it | Fetch it or don't cite it |
| "Everyone knows this" | Common knowledge still needs a source | Find one URL |
| "Close enough" | Paraphrasing ≠ accuracy | Quote or attribute precisely |
| "I'll add sources later" | You won't | Cite inline as you write |
