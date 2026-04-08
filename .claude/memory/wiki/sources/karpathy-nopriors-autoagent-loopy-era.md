---
title: "No Priors: Andrej Karpathy on Code Agents, AutoResearch, and the Loopy Era of AI"
slug: karpathy-nopriors-autoagent-loopy-era
source_type: transcript
url: ""
date_ingested: 2026-04-08
date_published: "2026-03-20"
entities_extracted: 6
claims_extracted: 7
---

# No Priors: Andrej Karpathy on Code Agents, AutoResearch, and the Loopy Era of AI

> **TL;DR**: Karpathy describes December 2025 as the inflection from manual to agent-dominated coding (2% / 98%). Core thesis: the human is always the bottleneck; auto-research removes them from optimization loops. Research orgs are just program.md files and can be meta-optimized. Digital AI will massively outpace physical/robotics. Education shifts from teaching humans to teaching agents.

## Key Claims

1. December 2025: shift from 80% manual / 20% agent to inverse ratio; "haven't typed a line of code since December" — `asserted`
2. Auto-research found untuned hyperparams (value embedding weight decay, adam betas) in a repo Karpathy already considered well-tuned — `argued`
3. Open source models ~8 months behind frontier as of March 2026; healthy power balance — `asserted`
4. Jevons paradox: cheaper code → more software demand → more engineering jobs (ATM / bank teller analogy) — `argued`
5. Research orgs are markdown files (program.md); auto-research on the org → better methodology — `argued`
6. "Joke test": models stuck on 5-year-old jokes despite massive gains elsewhere; RL only improves verifiable domains — `argued`
7. Physical world lags digital by significant margin; atom manipulation ~1M× harder than bit manipulation — `argued`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Andrej Karpathy](../entities/andrej-karpathy.md) | person | new |
| [Auto-Research Loop](../entities/auto-research-loop.md) | concept | new |
| [Agent Psychosis](../entities/agent-psychosis.md) | concept | new |
| [Program.md Research Org](../entities/program-md-research-org.md) | concept | new |
| [Jevons Paradox Applied to Coding](../entities/jevons-paradox-coding.md) | concept | new |
| [OpenClaw](../entities/openclaw.md) | tool | updated (creator + Dobby deployment) |

## Relations

- Andrej Karpathy `created_by` microGPT (200-line minimal GPT training)
- Auto-Research Loop `created_by` Andrej Karpathy
- Program.md Research Org `extends` Auto-Research Loop
- OpenClaw `created_by` Peter Steinberg
- Jevons Paradox Applied to Coding `contradicts` AI-job-displacement narrative
- Auto-Research Loop `inspired_by` AutoResearchClaw (parallel independent development)

## Cross-References

- Related entities: `karpathy-wiki-pattern.md` (same author, different contribution), `autoresearchclaw.md` (independent implementation of same concept)
- Related learnings: none found (new territory)
- Contradictions: none with existing learnings
