---
date: 2026-03-29
type: best_practice
severity: high
component: orchestration
tags: [autoresearch, pipeline, claude-code, agent-loop, research-automation]
summary: "Autoresearch via Claude Code agent loop succeeds when: (1) starting from existing implementations, (2) dense quantitative feedback per iteration, (3) white-box domain (red-teaming). Claudini discovered novel adversarial attacks outperforming 30+ baselines by iterating on GCG."
source: external_research
maturity: draft
uses: 3
harmful_uses: 0
related: [2026-04-23-llm-confirmation-bias.md, 2026-04-08-auto-research-removes-human-bottleneck.md]
verify_check: "manual"
confidence: 1.0
successful_uses: 0
---

## Situace
Claudini (arxiv:2603.24511) demonstrated autonomous adversarial attack discovery via Claude Code agent loop. Starting from existing GCG implementation, the agent iteratively improved attacks to 40% ASR on CBRN queries vs 10% for all baselines. Attacks transferred to held-out models (100% vs 56% baseline).

## Proč to funguje
1. **Existing starting point** — agent didn't invent GCG from scratch, iterating on known good baseline
2. **Dense feedback signal** — each iteration produces quantifiable metric (attack success rate)
3. **White-box domain** — red-teaming allows direct measurement of progress
4. **Explainable search space** — attack parameters are interpretable (token perturbations, etc)

## Vzor pro STOPA /autoresearch
- Initialize from reference implementation or problem formulation (not blank slate)
- Define scalar optimization objective (minimize/maximize something measurable)
- Allow agent to introspect & modify its own search strategy (meta-loop)
- Prefer white-box domains with fast feedback (code, red-teaming, benchmarks) over black-box (user feedback)
- Release findings open-source (credibility + community validation)

## Kdy to selhává
- Black-box objectives without ground truth (subjective creative tasks)
- No reference implementation to build from
- Sparse feedback (evaluation takes hours/days)
- Search space too large to explore efficiently without structure

## Prevence
When designing /autoresearch workflow: always include baseline implementation, scalar metric, and white-box access. If any missing, autoresearch is not the right tool.
