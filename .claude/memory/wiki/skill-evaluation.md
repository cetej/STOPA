---
generated: 2026-04-04
cluster: skill-evaluation
sources: 6
last_updated: 2026-04-04
---

# Skill Evaluation & Optimization

> **TL;DR**: Decomposed per-dimension scoring catches 3x more issues than holistic review. Optimization loops (Karpathy, AutoReason) work when feedback is dense and quantitative. Isolate reasoning from output to reduce bias.

## Overview

Evaluation of skill outputs has converged on decomposed scoring: breaking review into independent dimensions rather than assigning a single holistic grade. OS-Themis and APM research shows this catches 3x more issues (ref: 2026-03-25-decomposed-evaluation.md). This applies directly to /critic and /verify phases.

For iterative skill improvement, the Karpathy optimization loop (edit → measure → score → iterate) provides the structural backbone, combining structural heuristics with LLM-as-judge scoring (ref: karpathy-loop-autoloop.md). For subjective domains (prompts, arguments, copy), the AutoReason adversarial debate pattern extends this with cold-start agent isolation to prevent confirmation bias and randomized judge labels to prevent position bias (ref: 2026-04-01-autoreason-adversarial-debate.md).

Reasoning quality improves when reasoning and output generation are isolated — BOULDER/CARE patterns show this reduces bias in multi-turn conversations (ref: 2026-03-25-reasoning-isolation.md). Tool-specific learnings round out the picture: solo dev projects should skip branch/PR workflow in /fix-issue (ref: 2026-03-24-fix-issue-solo-workflow.md), and MCP youtube-transcript has been broken since 2026-03, requiring yt-dlp CLI as primary tool (ref: 2026-03-23-youtube-transcript-yt-dlp.md).

## Key Rules

1. **Decomposed evaluation over holistic**: score each dimension independently (ref: 2026-03-25-decomposed-evaluation.md)
2. **Isolate reasoning from output**: prevents bias in multi-turn prompts (ref: 2026-03-25-reasoning-isolation.md)
3. **Cold-start isolation for debate**: adversarial agents must not see each other's prior output (ref: 2026-04-01-autoreason-adversarial-debate.md)
4. **Dense quantitative feedback**: optimization loops need measurable signals, not vibes (ref: karpathy-loop-autoloop.md)
5. **yt-dlp over MCP for YouTube**: MCP server broken since 2026-03 (ref: 2026-03-23-youtube-transcript-yt-dlp.md)
6. **Solo dev: commit to main**: skip branch/PR in solo projects (ref: 2026-03-24-fix-issue-solo-workflow.md)

## Patterns

### Do
- Score each review dimension separately before aggregating (ref: 2026-03-25-decomposed-evaluation.md)
- Use structural heuristics + LLM-as-judge together (ref: karpathy-loop-autoloop.md)
- Randomize judge labels in adversarial debate (ref: 2026-04-01-autoreason-adversarial-debate.md)

### Don't
- Assign a single holistic score when per-dimension is feasible (ref: 2026-03-25-decomposed-evaluation.md)
- Let adversarial agents see each other's reasoning (ref: 2026-04-01-autoreason-adversarial-debate.md)
- Rely on MCP youtube-transcript as primary (ref: 2026-03-23-youtube-transcript-yt-dlp.md)

## Open Questions

- GAP: No data on how decomposed evaluation compares across model tiers (Haiku vs Sonnet vs Opus)

## Related Articles

- See also: [skill-design](skill-design.md) — structural rules for SKILL.md files
- See also: [orchestration-multi-agent](orchestration-multi-agent.md) — multi-agent debate patterns

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-01-autoreason-adversarial-debate](../learnings/2026-04-01-autoreason-adversarial-debate.md) | 2026-04-01 | medium | Adversarial debate loop for subjective optimization |
| [2026-03-25-decomposed-evaluation](../learnings/2026-03-25-decomposed-evaluation.md) | 2026-03-25 | high | Per-dimension scoring catches 3x more issues |
| [2026-03-25-reasoning-isolation](../learnings/2026-03-25-reasoning-isolation.md) | 2026-03-25 | high | BOULDER/CARE: isolate reasoning from output |
| [2026-03-24-fix-issue-solo-workflow](../learnings/2026-03-24-fix-issue-solo-workflow.md) | 2026-03-24 | medium | Solo dev: commit to main, skip PR workflow |
| [2026-03-23-youtube-transcript-yt-dlp](../learnings/2026-03-23-youtube-transcript-yt-dlp.md) | 2026-03-23 | high | MCP broken, use yt-dlp CLI |
| [karpathy-loop-autoloop](../learnings/karpathy-loop-autoloop.md) | 2026-03-23 | medium | Karpathy loop: edit-measure-score-iterate |
