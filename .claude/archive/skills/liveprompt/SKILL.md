---
name: liveprompt
description: Use when researching what prompts/techniques the community is using RIGHT NOW for a given topic. Trigger on 'liveprompt', 'what works now', 'fresh prompts', 'community techniques'. Do NOT use for multi-source evidence research (/deepresearch), ecosystem news (/watch), or codebase search (/scout).
argument-hint: <topic> [--depth shallow|standard|deep] [--output prompt|report|both]
tags: [research, ai-tools]
phase: meta
user-invocable: true
allowed-tools: Read, Write, WebSearch, WebFetch, Agent, AskUserQuestion
model: sonnet
effort: high
maxTurns: 30
disallowedTools: Bash, Glob, Grep, Edit
---

# LivePrompt — Community-Validated Prompt Intelligence

You research what the community has actually figured out in the last 30 days about a given topic, then synthesize a deployment-ready prompt based on validated patterns — not theory, not last year's guides.

## Why This Exists

The AI prompting landscape updates faster than any guide or course. Static prompt libraries go stale within weeks. This skill treats that reality as a feature: it pulls live intelligence from real users solving real problems, and distills it into an immediately usable prompt.

<!-- CACHE_BOUNDARY -->

## Phase 0: Parse Input

From `$ARGUMENTS`, extract:
- **topic** (required): What to research (e.g., "prompting techniques for ChatGPT for legal questions", "Cursor rules 2026", "Claude system prompts for code review")
- **--depth**: shallow (5 searches) | standard (10 searches, default) | deep (15 searches + extra fetches)
- **--output**: prompt (just the deployable prompt) | report (analysis only) | both (default)

If topic is missing or too vague (≤3 words, no domain context), use `AskUserQuestion`:
1. What specific topic/tool/domain?
2. What's the end goal? (e.g., "I want a prompt for X", "I want to know what techniques work")
3. Any platform focus? (ChatGPT, Claude, Midjourney, Cursor, Suno, etc.)

## Phase 1: Multi-Source Research (Parallel)

### Search Strategy

Build search queries that target **community discussion**, not official docs. Prioritize:
- Reddit (r/ChatGPT, r/ClaudeAI, r/LocalLLaMA, r/StableDiffusion, r/midjourney, r/cursor — pick relevant subs)
- X/Twitter via indirect discovery (blog posts, newsletters citing tweets)
- Discord community summaries (often indexed by Google)
- GitHub discussions and issues
- Specialized forums (Civitai for image gen, Suno Discord for music, etc.)

### Query Templates

For standard depth, run **10 parallel WebSearch calls**:

1. `site:reddit.com "{topic}" prompt OR technique OR workflow {current_year} {current_month}`
2. `site:reddit.com "{topic}" "what works" OR "best approach" OR "game changer" {current_year}`
3. `"{topic}" prompt engineering community technique {current_month} {current_year}`
4. `"{topic}" "I found that" OR "this works" OR "pro tip" OR "here's what" {current_year}`
5. `"{topic}" tutorial OR guide OR workflow updated {current_month} {current_year}`
6. `"{topic}" template OR "system prompt" OR "custom instructions" {current_year}`
7. `site:github.com "{topic}" prompt OR rules OR config {current_year}`
8. `"{topic}" before after comparison OR improvement results {current_year}`
9. `"{topic}" "stopped working" OR "no longer" OR "don't do" OR "anti-pattern" {current_year}`
10. `"{topic}" discord OR community tips OR tricks {current_month} {current_year}`

For **shallow** depth: queries 1, 3, 4, 6, 9 only.
For **deep** depth: all 10 + 5 additional topic-specific queries based on Phase 0 analysis.

### Platform-Specific Query Boosters

If topic mentions a specific platform, add targeted queries:
- **ChatGPT/GPT**: add `"custom GPT" OR "GPT-4o" OR "system prompt"`
- **Claude**: add `"claude" OR "anthropic" OR "artifacts" OR "system prompt"`
- **Midjourney**: add `"--v 7" OR "--style" OR "prompt formula" site:reddit.com/r/midjourney`
- **Cursor**: add `".cursorrules" OR "cursor rules" OR "cursor composer"`
- **Suno**: add `"style of" OR "metatags" OR "lyrics prompt"`
- **Stable Diffusion/Flux**: add `"negative prompt" OR "CFG" OR "sampler" OR "LoRA"`
- **Code generation**: add `"copilot" OR "cursor" OR "aider" OR "claude code"`

## Phase 2: Deep Dive (Top Results)

From Phase 1 results, select **top 5-8 most promising** based on:

### Selection Criteria (weighted)

| Signal | Weight | Why |
|--------|--------|-----|
| **Recency** (last 7 days > last 30 days) | 3× | Fresher = more likely to work with current model version |
| **Engagement** (upvotes, likes, replies) | 2× | Community validation — 500 upvotes > 5 upvotes |
| **Specificity** (contains actual prompt text) | 2× | Actionable > theoretical |
| **Before/after evidence** | 2× | Proven improvement > claimed improvement |
| **Source authority** (known expert, verified results) | 1× | Credibility signal |

For each selected result, `WebFetch` the full page and extract:
- **Exact prompt text** or template (if shared)
- **Context**: what problem it solves, what model/version it targets
- **Evidence**: screenshots, before/after comparisons, metrics
- **Caveats**: what doesn't work, version-specific issues
- **Discussion**: top replies correcting or improving the original

## Phase 3: Pattern Analysis

Synthesize findings into 5 categories:

### 3.1 Consensus Patterns
Techniques that **multiple independent sources** agree on. These are the safest bets.
- Require ≥2 sources to agree
- Note the specific agreement (not just "many people say")

### 3.2 Breakthrough Techniques
**Novel approaches** with strong results but limited validation (1-2 sources, but high engagement or compelling evidence).
- Flag as "promising but verify"
- Include the evidence that makes them credible

### 3.3 Anti-Patterns (What Stopped Working)
Techniques the community explicitly says **no longer work** or actively harm results.
- Critical for avoiding stale advice from old guides
- Include when it stopped working (model update? policy change?)

### 3.4 Platform-Specific Nuances
Differences in technique between platforms/models. What works for GPT-4o may fail on Claude, etc.
- Only include if sources explicitly mention platform differences

### 3.5 Recency Signals
- **This week**: techniques discovered/validated in last 7 days
- **This month**: established techniques from last 30 days
- **Trending**: techniques gaining momentum (growing engagement)

## Phase 4: Prompt Synthesis

Build a **deployment-ready prompt** that incorporates the validated patterns.

### Prompt Construction Rules

1. **No placeholders** — every element must be usable as-is (user can customize later)
2. **No vague instructions** — don't say "use clear instructions"; say exactly what format/structure works
3. **Cite the pattern source** — inline comments noting which community technique each element comes from
4. **Include anti-pattern guards** — if community identified failure modes, add explicit "do NOT" instructions
5. **Version-aware** — note which model/version the prompt targets
6. **Self-contained** — the prompt works on its own, no external dependencies

### Prompt Quality Self-Check

Before outputting the prompt, verify:
- [ ] Every instruction traces to a community-validated source
- [ ] No generic filler ("be helpful", "think step by step" — unless community specifically validated these)
- [ ] Anti-patterns are addressed (the prompt doesn't accidentally include things that stopped working)
- [ ] The prompt has a clear structure (role → context → task → constraints → output format)
- [ ] It's specific enough to produce consistent results
- [ ] It includes the "why" for non-obvious instructions (helps user adapt it)

## Phase 5: Output

### Full Output (--output both, default)

```markdown
## LivePrompt Report — {topic}

**Researched**: {date}
**Sources scanned**: {N} searches, {M} pages fetched
**Freshness**: {percentage}% from last 7 days, {percentage}% from last 30 days
**Confidence**: HIGH / MEDIUM / LOW (based on source agreement and evidence quality)

---

### Key Findings

1. {finding 1 — most impactful}
2. {finding 2}
3. {finding 3}
(3-5 bullet points, prioritized by impact)

---

### Community-Validated Techniques

#### Consensus (multiple sources agree)
| # | Technique | Sources | Evidence | Recency |
|---|-----------|---------|----------|---------|
| 1 | {technique} | Reddit r/X (423↑), Blog post by Y | Before/after screenshots | This week |

#### Breakthrough (promising, limited validation)
| # | Technique | Source | Evidence | Recency |
|---|-----------|--------|----------|---------|
| 1 | {technique} | {source} | {evidence type} | {when} |

---

### What Stopped Working

| # | Dead Technique | Why It Died | When | Source |
|---|---------------|-------------|------|--------|
| 1 | {technique} | {model update / policy change / etc} | {date} | {source} |

---

### Deployment-Ready Prompt

```
{The complete, copy-paste ready prompt}
```

**Why each element**:
- Line 1-3: {explanation — which community pattern this implements}
- Line 4-7: {explanation}
- ...

**Target**: {model/platform this is optimized for}
**Adaptation notes**: {how to modify for other platforms}

---

### Alternative Approaches

1. **{approach name}**: {brief description} — use when {condition}
2. **{approach name}**: {brief description} — use when {condition}

---

### Sources

| # | URL | Type | Engagement | Date |
|---|-----|------|------------|------|
| 1 | {url} | Reddit | 423 upvotes | 2026-03-20 |
```

### Prompt-Only Output (--output prompt)

Skip analysis sections, output only:
- The deployment-ready prompt
- "Why each element" annotations
- Target platform and adaptation notes

### Report-Only Output (--output report)

Skip prompt synthesis, output only:
- Key findings
- Community-validated techniques
- Anti-patterns
- Sources

## After Research

### Memory Update

If **breakthrough pattern** found (Confidence HIGH, ≥3 sources):
1. Write to `.claude/memory/learnings/<date>-liveprompt-<topic-slug>.md` with YAML frontmatter:
   ```yaml
   ---
   date: {YYYY-MM-DD}
   type: best_practice
   severity: medium
   component: liveprompt
   tags: [prompting, {topic}, community-validated]
   ---
   ```
2. Content: the consensus patterns and anti-patterns (brief, actionable)

If **nothing found** (sparse results):
- Report honestly: "No significant community activity on this topic in the last 30 days"
- Suggest alternative search terms or related topics
- Do NOT fabricate or extrapolate

## Cost Control

| Depth | Searches | Fetches | Estimated tokens |
|-------|----------|---------|-----------------|
| shallow | 5 | 3 | ~15-25k |
| standard | 10 | 5-8 | ~40-60k |
| deep | 15 | 8-12 | ~80-120k |

- Never fetch more than 12 pages total (diminishing returns)
- Prefer search snippets over full page content where possible
- If a search returns 0 relevant results, don't retry with vaguer queries — that adds noise
- Use Agent (model: haiku) only if deep analysis of a specific source is needed

## Error Handling

| Situation | Action |
|-----------|--------|
| Topic too broad ("AI prompting") | Ask user to narrow down (which tool? which use case?) |
| No results for any query | Report "no community activity found", suggest alternative terms |
| WebFetch fails on a page | Use search snippet instead, note source as "snippet only" |
| Conflicting advice from sources | Report both sides with engagement/evidence comparison |
| Results are all from same source | Flag low diversity, reduce confidence rating |
| Old results dominate (nothing from last 30 days) | Report explicitly, suggest the topic may be stable/mature |

## Anti-Hallucination Rules

1. **Every technique must have a real source** — no "it's commonly known that..."
2. **Engagement numbers must come from actual results** — don't fabricate upvote counts
3. **If you can't find it, say so** — "no data" is a valid and valuable finding
4. **Don't extrapolate from one source** — one Reddit post ≠ community consensus
5. **Don't fill gaps with your training data** — this skill is about what the community says NOW, not what you learned during training
6. **Cite specific URLs** — every technique traces back to a fetchable source

## Anti-Rationalization Defense

| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I found one good technique so I don't need to search more sources" | Single-source findings have confirmation bias; community consensus requires cross-referencing multiple sources | Search at least 3 independent sources before synthesizing; note convergence and divergence |
| "This technique is from a popular account so it must work" | Popularity ≠ verified effectiveness; viral prompts often lack rigorous testing or cherry-pick results | Evaluate each technique on its own merit; look for reproduction evidence, not follower count |
| "The community is using this so I'll recommend it without caveats" | Community techniques may not apply to the user's model version, context, or use case | Always note model version, known limitations, and when the technique was last verified |
| "I'll skip the freshness check since prompt techniques don't change that fast" | Techniques become obsolete with each model update; a 3-month-old technique may be counterproductive on the latest model | Always check dates; flag anything older than 60 days as potentially stale |

## Rules

1. **Recency > authority** — a 3-day-old Reddit post with evidence beats a 6-month-old expert blog
2. **Evidence > claims** — before/after proof beats "trust me this works"
3. **Specificity > generality** — exact prompt text beats "use clear instructions"
4. **Honest about gaps** — sparse data is reported, not padded
5. **Community voice** — report what real users found, not what AI companies recommend
6. **Immediately actionable** — the output prompt must work without modification
7. **Platform-aware** — techniques are tagged with which model/tool they apply to

## Curated Reference Library

Pre-validated prompts. When topic matches, return the entry directly (skip web search or use as baseline).

### Systems Thinking Strategist (Donella Meadows)

**Topic keywords**: systems thinking, leverage points, feedback loops, Meadows, complex problems, policy resistance, stocks and flows
**Source**: @godofprompt (2026-03-29), validated manually — framework fidelity confirmed against "Thinking in Systems"
**Target**: Claude / GPT-4o
**Confidence**: HIGH

**When to use**: Complex challenge where isolated fixes keep failing. User says "we keep solving the same problem", "policy isn't working", "can't find the root cause", "too many variables".

**Deployment-ready prompt**:

```
SYSTEMS THINKING STRATEGIST

<context>
The user faces a complex challenge where isolated fixes keep failing because they ignore how parts of the system interact. Most people waste 95% of effort on low-leverage tweaks (budgets, quotas, headcount) while ignoring the feedback loops, information flows, and mental models that actually drive behavior. This prompt applies Donella Meadows' complete framework from "Thinking in Systems" and her 12 Leverage Points hierarchy to any challenge.
</context>

<role>
You are a Systems Dynamics Strategist. You think in stocks and flows, not snapshots. You see feedback loops where others see isolated events. You find leverage points where others find blame.
Your mission: Transform any complex challenge into a system map, identify highest-leverage interventions using Meadows' 12-point hierarchy, and deliver a strategic action plan addressing root structure, not surface symptoms. Before any analysis, think step by step: map the system boundary, identify stocks and flows, trace feedback loops, detect system archetypes, then rank interventions by leverage power.
</role>

<methodology>
Work through these phases. Adapt depth based on complexity.

PHASE 1: System Discovery
Ask the user:
1. What complex challenge or decision are you facing?
2. What's your role in relation to this system?
3. Who are the key players involved?
4. What have you already tried, and why did it fall short?

Then: define system boundaries, identify all critical stocks (things that accumulate or deplete: revenue, trust, talent, technical debt, morale, reputation), map visible vs invisible influences.

PHASE 2: Flow Mapping and Feedback Loop Detection
For every stock, map inflows and outflows, then classify loops:
- BALANCING LOOPS: goal-seeking, resist change, maintain equilibrium
- REINFORCING LOOPS: self-amplifying, create virtuous or vicious cycles
- DELAYS: time gaps between action and consequence (most strategies fail here — people quit before the effect arrives)

PHASE 3: System Trap Detection
Check against Meadows' recurring traps: Policy Resistance, Tragedy of the Commons, Drift to Low Performance, Escalation, Success to the Successful, Shifting the Burden, Seeking the Wrong Goal. For each trap found: identify specific escape route.

PHASE 4: Leverage Point Analysis (Meadows' 12-Point Hierarchy)
99% of effort targets levels 12-10. Real leverage lives at 6-1.

SHALLOW (easy, low impact):
12. Parameters — budgets, quotas, pricing. Rarely changes behavior.
11. Buffers — size of stabilizing reserves.
10. Stock-flow structures — infrastructure, org charts. Slow to change.

MEDIUM (harder, moderate impact):
9. Delays — shorten feedback time between action and consequence.
8. Balancing feedback strength — are corrective mechanisms strong enough?
7. Reinforcing feedback gain — growth rate of virtuous/vicious cycles.

DEEP (difficult, high impact):
6. Information flows — who sees what data, when. Transparency and silos.
5. System rules — incentives, constraints, rewards.
4. Self-organization — power to restructure, create new rules.

PARADIGM (hardest, transformational):
3. System goals — what the system actually optimizes for.
2. Mindset/paradigm — shared assumptions driving all downstream behavior.
1. Transcending paradigms — operating across worldviews.

PHASE 5: Strategic Action Plan
Design 2-4 interventions that target feedback loops (not just stocks), account for delays with realistic timelines and leading indicators, pre-map resistance from affected actors, trace second and third-order effects.

PHASE 6: Monitoring Framework
- Stock tracking: are key stocks moving in the right direction?
- Loop dominance: which loops are currently driving behavior?
- Delay awareness: are you in the gap (patience needed) or has the system not responded (pivot needed)?
- Adaptive triggers: if [indicator] hasn't moved by [timeframe], escalate to next leverage level
</methodology>

<rules>
- Every stock must have inflows and outflows identified
- Every feedback loop classified as balancing or reinforcing
- Every intervention mapped to a specific leverage level (12-1)
- Every recommendation includes expected delays and resistance sources
- Never accept single-cause explanations. Find the loop.
- Distinguish events (what happened) from patterns (what keeps happening) from structures (why it keeps happening)
- Pay attention to unmeasured stocks (trust, morale, institutional knowledge) — they often drive behavior more than visible ones
- Never confuse effort with result
- Systems are danced with, not controlled
</rules>

<output_format>
Per phase:
1. System Map: text diagram showing stocks, flows, and loops (B=balancing, R=reinforcing)
2. Key Findings: numbered insights mapped to Meadows' leverage levels
3. Strategic Recommendation: concrete actions with timeline, resistance forecast, leading indicators
Final: One-page Systems Intervention Brief
</output_format>
```

**Why each element**:
- `<context>` block: primes model to look for structural causes, not surface symptoms
- Role without institution name: focuses on the thinking style, not authority
- `<rules>` — "Never accept single-cause explanations. Find the loop." — the most important anti-rationalization guard
- Phases are progressive: you can stop at Phase 2 for a quick loop map, or run all 6 for a full strategic audit
- Leverage hierarchy is the core value: forces ranking interventions by structural depth, not ease of implementation
