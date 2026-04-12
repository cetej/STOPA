---
name: reference_meta_harness
description: Meta-Harness paper (arXiv:2603.28052) — full execution traces >> summaries for harness optimization; Pareto frontier framing; practical tips for autonomous optimization loops
type: reference
---

Meta-Harness (Lee, Nair, Zhang, Lee, Khattab, Finn — arXiv:2603.28052, 2026-03)
Source: @neural_avb article thread + paperbreakdown.com/abs/2603.28052

## Core Finding

Agentic proposer with access to full filesystem (code + execution traces + scores)
dramatically outperforms score-only or score+summary feedback for harness optimization.

| Metric | Scores only | Scores+summary | Full traces |
|--------|-------------|----------------|-------------|
| **Best** | 41.3% | 38.7% | **56.7%** |
| **Median** | 34.6% | 34.9% | **50.0%** |

**Median gap = +15 points** (strongest metric — summary makes things slightly *worse* than scores alone).
Token budget: 10M tokens/iter (vs 0.002M for OPRO, 0.015M for TextGrad).
Proposer reads median 82 files/iteration: 41% source code, 40% execution traces.

## What is a Harness

Everything around the LLM that is NOT the LLM itself:
- **Pre/Post Hooks**: input/output transformations
- **Prompt building**: system prompt, user prompt, lazy-loaded skills, mode-specific instructions
- **Tools**: definitions + execution on LLM's behalf
- **Memory**: session, cross-session, organization-level
- **External data sources**: retrieval logic (filesystem, web, databases)

Key insight: harness optimization is a **game theory** problem balancing User (correctness, speed),
Provider (cost efficiency, KV cache), and LLM (in-distribution data, capable tools).

## Pareto Frontier Framing

Two objectives: **accuracy** (task performance) and **token cost** (context tokens used).
Goal: find harnesses on the Pareto frontier — no other harness is both more accurate AND cheaper.
The system tracks ALL candidates and identifies the non-dominated set.

## Filesystem-as-Feedback Pattern

Full experiment history stored as navigable filesystem:
- Full source code of every candidate harness
- Performance scores per candidate
- Execution traces: raw model prompts, tool calls, state updates
- Proposer uses grep/cat/git to search across ALL prior history
- "Unrestricted access to all previous history is essential" — long-horizon dependencies

## Optimization Loop

1. **Inspection**: Proposer searches filesystem for prior results and traces
2. **Diagnosis**: Reasons about failure modes from trace evidence
3. **Proposal**: Writes new harness code version
4. **Evaluation**: Runs harness on task distribution, records reward
5. **Update**: Results added back to filesystem, loop continues

## Practical Tips (from authors)

1. **Write a good skill first** — most important lever. Specify forbidden actions, artifacts, objective. Debug 3-5 iterations to refine skill before full run.
2. **Start with struggling baseline** — simple few-shot prompting. Keep eval set small enough for ~50 full evaluations per run.
3. **Log everything navigable** — machine-readable JSON, hierarchical structure.
4. **Build CLI over logs** — list Pareto frontier, show top-k candidates, diff code/results between runs.
5. **Warm-starts** — convert offline experience into same directory structure.
6. **Automate eval outside proposer** — eval is too simple to delegate to the agentic proposer.

## Case Studies

- **Online Text Classification**: discovered "label primer + coverage block + contrastive block" prompt structure — beat state-of-art context management. +7.7 pts vs best hand-designed harness (ACE), 4× fewer context tokens.
- **TerminalBench-2 (Haiku 4.5)**: 37.6% — #1 among all Haiku 4.5 agents (beats Goose 35.5%, Terminus-KIRA 33.7%)
  - Iterations 1-2: bundled structural + prompt rewrites → both regressed
  - Iteration 3: isolated confound — prompt changes were the failure factor, not structural fixes
  - Iterations 4-6: probed completion-flow fragility, cited specific task+turn counts from prior traces
  - **Iteration 7 pivot**: abandoned control loop changes, added 80-line env snapshot (tool list, language versions, package managers) BEFORE agent starts. → best candidate in the run
  - Key meta-lesson: structural + prompt changes NEVER bundled; confound isolation required
- **TerminalBench-2 (Opus 4.6)**: 76.4% — #2 overall
- **IMO-level Math**: +4.7 pts average; **discovered four-route lexical router** after 40 iterations:
  - Combinatorics: deduplicated BM25 + difficulty reranking
  - Geometry: 1 hard reference + 2 raw BM25 neighbors
  - Number theory: reranked toward solutions stating technique early
  - General: adaptive retrieval based on top-score concentration
  - **Cross-model transfer**: harness transfers unchanged to GPT-5.4-nano, GPT-5.4-mini, Gemini-3.1-Flash-Lite, Gemini-3-Flash, GPT-OSS-20B (5 held-out models)

## STOPA Integration

`.claude/hooks/trace-capture.py` captures tool inputs/outputs during optimization skill runs
(autoloop, autoresearch, self-evolve). Traces stored in `.traces/<run_id>/` with JSONL format.
Skills reference `trace-review.md` context files for selective trace reading.
`/eval --optim` grades optimization traces.

**Alignment (2026-04-02 audit)**:
- Filesystem-as-feedback: YES (all loop skills)
- Pareto frontier: added via `cost_metric:` parameter in autoloop/autoresearch
- CLI over experiments: `/eval --experiments` mode
- Warm-start: explicit in autoloop, implicit in autoresearch (program.md), explicit in self-evolve (meta-param JSON)
- Eval separate from proposer: YES (all skills — locked verify/eval commands)
