---
name: council
description: Use when making a decision that benefits from multiple competing perspectives — architecture choices, technology selection, strategy dilemmas. Trigger on 'council', 'porada', 'should I', 'which approach'. Do NOT use for code review (/critic) or PR review (/pr-review).
argument-hint: <question or dilemma to deliberate>
tags: [planning, review]
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Agent, WebSearch, WebFetch
model: sonnet
effort: high
maxTurns: 25
---

# Council — Multi-Perspective Decision Deliberation

Inspired by Karpathy's LLM Council (github.com/karpathy/llm-council).
Instead of polling multiple LLM providers, this skill forces **5 distinct advisory personas**
to argue about a question, **anonymously cross-review** each other's reasoning,
then a Chairman synthesizes the final verdict.

The key insight: anonymization prevents self-favoritism and groupthink.

## Shared Memory

Read first:
- `.claude/memory/state.md` — current task context
- `.claude/memory/decisions.md` — past decisions (avoid re-litigating)
- `.claude/memory/key-facts.md` — project constraints

<!-- CACHE_BOUNDARY -->

## Input

Parse `$ARGUMENTS` as the **decision question**.

If the question is vague, reformulate it into a clear decision frame:
- "What exactly is being decided?"
- "What are the constraints?"
- "What are the success criteria?"

State the reformulated question clearly before proceeding.

## Stage 1: Independent Advisory (Parallel)

Spawn **5 sub-agents** (model: haiku) in parallel. Each gets the SAME question but a DIFFERENT persona prompt. They do NOT see each other's work.

### The 5 Advisors

| ID | Persona | System Prompt Core |
|----|---------|-------------------|
| A | **Pragmatist** | You optimize for shipping speed, simplicity, and maintenance cost. You prefer boring technology and proven patterns. You distrust complexity. Ask: "What's the simplest thing that could work?" |
| B | **Architect** | You optimize for long-term scalability, clean abstractions, and extensibility. You think in systems and interfaces. Ask: "How will this look in 2 years?" |
| C | **Skeptic** | You are the devil's advocate. You find failure modes, hidden costs, and unstated assumptions. You distrust optimism. Ask: "What could go wrong that nobody is talking about?" |
| D | **User Advocate** | You optimize for end-user experience, developer ergonomics, and adoption friction. You care about what people actually do, not what they say. Ask: "Who will hate this and why?" |
| E | **Data-Driven** | You demand evidence: benchmarks, case studies, industry data, prior art. You distrust opinions without supporting data. Ask: "What evidence supports this choice?" |

Each advisor receives this prompt:

```
You are advising on this decision:

{QUESTION}

Context:
{relevant context from memory/codebase}

Your advisory persona: {PERSONA_DESCRIPTION}

Provide your analysis in this format:

## Position
State your recommended choice in 1-2 sentences.

## Reasoning
3-5 bullet points supporting your position. Be specific and concrete.

## Risks
2-3 risks of your recommended approach. Be honest about downsides.

## Confidence
Rate 1-5 how confident you are. 5 = slam dunk, 1 = coin flip.
Briefly explain what would change your mind.
```

Collect all 5 responses. Label them **Advisory A through E** — strip persona names.

## Stage 2: Anonymous Cross-Review (Parallel)

Spawn **3 sub-agents** (model: sonnet) in parallel. Each is a **judge** who sees ALL 5 anonymized advisories and ranks them.

Each judge gets:

```
You are evaluating 5 different advisory positions on this decision:

Question: {QUESTION}

Here are the anonymous advisories:

---
Advisory A:
{response_A}

Advisory B:
{response_B}

Advisory C:
{response_C}

Advisory D:
{response_D}

Advisory E:
{response_E}
---

Your task:
1. For each advisory, identify its strongest argument and its biggest weakness.
2. Note where advisories AGREE (consensus signal) and where they DISAGREE (tension points).
3. Rank all 5 from best to worst reasoning quality (not just whether you agree).

IMPORTANT: Your final ranking MUST be formatted EXACTLY as follows:
- Start with the line "FINAL RANKING:" (all caps, with colon)
- Then list from best to worst as a numbered list
- Each line: number, period, space, then ONLY the label (e.g., "1. Advisory A")
- No other text in the ranking section
```

### Parse Rankings

For each judge's response:
1. Split on `"FINAL RANKING:"`
2. Extract ordered list via regex `\d+\.\s*Advisory [A-E]`
3. Fallback: scan for any `Advisory [A-E]` patterns in order

### Compute Aggregate

For each Advisory (A-E):
- Average rank position across all 3 judges
- Count how many judges placed it in top 2

Output the **Council Leaderboard**:

```markdown
### Council Leaderboard

| Rank | Advisory | Persona | Avg Position | Top-2 Votes | Confidence |
|------|----------|---------|-------------|-------------|------------|
| 1 | Advisory C | Skeptic | 1.3 | 3/3 | 4 |
| 2 | Advisory A | Pragmatist | 2.0 | 2/3 | 3 |
| ... | ... | ... | ... | ... | ... |
```

De-anonymize AFTER ranking is computed — the personas are revealed only in the final output.

## Stage 3: Chairman Synthesis

The Chairman (this agent, model: sonnet) reads:
- The original question
- All 5 advisories (now de-anonymized with persona labels)
- All 3 judge evaluations
- The aggregate leaderboard
- Consensus and tension points from judges

Produce the final synthesis:

```markdown
## Council Verdict: {QUESTION_SHORT}

### Decision
{1-3 sentences: the recommended choice}

### Consensus Points
- {things most advisories agreed on — high confidence}

### Key Tensions
- {genuine disagreements that matter — acknowledge trade-offs}

### Risk Mitigation
- {top 2-3 risks and how to address them}

### Confidence: {HIGH / MEDIUM / LOW}
{Why this confidence level. What would warrant revisiting.}

### Dissenting View
{Strongest counter-argument that wasn't adopted. Why it was overruled but deserves noting.}

### Council Leaderboard
{paste leaderboard table}

### Full Advisories (collapsed)
<details>
<summary>Advisory A — Pragmatist (avg rank: X.X)</summary>
{full advisory text}
</details>
{repeat for B-E}
```

## Cost Controls

- Stage 1: 5 × haiku = cheap parallel fan-out
- Stage 2: 3 × sonnet judges (not 5 — diminishing returns)
- Stage 3: 1 × sonnet chairman (this agent)
- Total: ~8-9 sub-agent calls

Check `.claude/memory/budget.md` before starting. If budget is tight, reduce to 3 advisors and 2 judges.

## After Deliberation

1. If the decision is significant, record it in `.claude/memory/decisions.md`
2. Update `.claude/memory/state.md` with the council verdict
3. If the question came from an orchestration task, return verdict to orchestrator

## Rules

1. **Anonymize before cross-review** — judges must NOT know which persona wrote which advisory
2. **De-anonymize only in final output** — transparency for the user
3. **Advisors work independently** — no shared context between them
4. **Judges rank reasoning quality**, not agreement with their own view
5. **Chairman acknowledges dissent** — always include the strongest counter-argument
6. **No unanimous rubber-stamps** — if all 5 agree, Chairman must stress-test the consensus
7. **Concrete over abstract** — advisories must cite specifics, not platitudes
