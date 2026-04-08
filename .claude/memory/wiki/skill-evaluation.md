---
generated: 2026-04-04
cluster: skill-evaluation
sources: 9
last_updated: 2026-04-08
---

# Skill Evaluation & Optimization

> **TL;DR**: Decomposed per-dimension scoring catches 3x more issues than holistic review. Schema compliance ≠ downstream utility (Schema-F1 0.964, SR 0.472) — always test on downstream data. Zero-shot CoT for critic, Reflexion verbal notes in 3-fix, SPP model gating in council.

## Overview

Evaluation of skill outputs has converged on decomposed scoring: breaking review into independent dimensions rather than assigning a single holistic grade. OS-Themis and APM research shows this catches 3x more issues (ref: 2026-03-25-decomposed-evaluation.md). This applies directly to /critic and /verify phases.

Tool-Genesis cascade evaluation (arXiv:2603.05578) revealed that minor L1 errors amplify through L2→L3→L4 into catastrophic downstream failures (Qwen3-8B: L1 68.6% → L4 1.2%). More critically, schema compliance decouples from downstream utility: Claude-Haiku-3.5 achieved Schema-F1 0.964 but SR only 0.472. The fix: always test format-compliant outputs against downstream data, never declare done from schema match alone. Iterative repair with execution feedback gives 2-5x SR improvement over one-shot (ref: 2026-04-04-toolgenesis-cascade-evaluation.md).

EgoAlpha prompt pattern analysis mapped 38 research techniques to STOPA: Zero-shot CoT reasoning primer in critic/debugging ("Let me trace through this step by step"), Reflexion verbal notes in 3-fix escalation (explicit "what to do differently next time" after each FAIL), SPP model gating in council (high-stakes decisions require sonnet advisors, not haiku), and ICL order sensitivity (strongest examples at END for recency effect). STOPA implements 25/38 analyzed techniques, several before formal publication (ref: 2026-04-05-egoalpha-prompt-patterns.md).

For generative media prompts (image/video), only describe observable outputs — what the renderer can see — never internal states like emotions or intentions. "Tears streaming down her cheeks" instead of "she feels sad." Rhythm words outperform technical parameters because models parse semantics, not numbers (ref: 2026-04-08-descriptive-over-narrative-generative.md).

For iterative skill improvement, the AutoReason adversarial debate pattern uses cold-start agent isolation to prevent confirmation bias and randomized judge labels to prevent position bias (ref: 2026-04-01-autoreason-adversarial-debate.md). Reasoning quality improves when reasoning and output generation are isolated — BOULDER/CARE patterns reduce bias in multi-turn conversations (ref: 2026-03-25-reasoning-isolation.md).

## Key Rules

1. **Decomposed evaluation over holistic**: score each dimension independently (ref: 2026-03-25-decomposed-evaluation.md)
2. **Schema compliance ≠ utility**: after format check, ALWAYS test on downstream data (ref: 2026-04-04-toolgenesis-cascade-evaluation.md)
3. **Cascade order**: verify L1 before jumping to L3 — early failures amplify (ref: 2026-04-04-toolgenesis-cascade-evaluation.md)
4. **Zero-shot CoT in critic**: "Let me trace through this step by step" before verdict (ref: 2026-04-05-egoalpha-prompt-patterns.md)
5. **Reflexion nota after FAIL**: generate explicit "what to do differently" before next attempt (ref: 2026-04-05-egoalpha-prompt-patterns.md)
6. **SPP model gating**: council uses sonnet+ advisors; cognitive synergy requires GPT-4/Opus tier (ref: 2026-04-05-egoalpha-prompt-patterns.md)
7. **Cold-start isolation for debate**: adversarial agents must not see each other's prior output (ref: 2026-04-01-autoreason-adversarial-debate.md)
8. **Descriptive over narrative in generative prompts**: observable outputs only, no internal states (ref: 2026-04-08-descriptive-over-narrative-generative.md)

## Patterns

### Do
- Score each review dimension separately before aggregating (ref: 2026-03-25-decomposed-evaluation.md)
- Run repair loop (max 3 iterations) with execution feedback for tool/skill generation (ref: 2026-04-04-toolgenesis-cascade-evaluation.md)
- Use structural heuristics + LLM-as-judge together
- Randomize judge labels in adversarial debate (ref: 2026-04-01-autoreason-adversarial-debate.md)

### Don't
- Declare success from schema or format match alone (ref: 2026-04-04-toolgenesis-cascade-evaluation.md)
- Assign a single holistic score when per-dimension is feasible (ref: 2026-03-25-decomposed-evaluation.md)
- Use haiku for high-stakes council decisions — cognitive synergy only at stronger models (ref: 2026-04-05-egoalpha-prompt-patterns.md)
- Let adversarial agents see each other's reasoning (ref: 2026-04-01-autoreason-adversarial-debate.md)

## Open Questions

- GAP: No data on how decomposed evaluation compares across model tiers (Haiku vs Sonnet vs Opus)
- STOPA has zero positive demonstrations in skill bodies — Min et al. shows format matters more than label correctness; SKILL.examples.md for critic and orchestrate planned (ref: 2026-04-05-egoalpha-prompt-patterns.md)

## Related Articles

- See also: [skill-design](skill-design.md) — structural rules for SKILL.md files
- See also: [orchestration-multi-agent](orchestration-multi-agent.md) — multi-agent debate patterns

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-05-egoalpha-prompt-patterns](../learnings/2026-04-05-egoalpha-prompt-patterns.md) | 2026-04-05 | high | Zero-shot CoT, Reflexion, SPP gating, ICL order sensitivity |
| [2026-04-04-toolgenesis-cascade-evaluation](../learnings/2026-04-04-toolgenesis-cascade-evaluation.md) | 2026-04-04 | high | Schema compliance ≠ utility; L1→L4 cascade amplification |
| [2026-04-01-autoreason-adversarial-debate](../learnings/2026-04-01-autoreason-adversarial-debate.md) | 2026-04-01 | medium | Adversarial debate loop for subjective optimization |
| [2026-03-25-decomposed-evaluation](../learnings/2026-03-25-decomposed-evaluation.md) | 2026-03-25 | high | Per-dimension scoring catches 3x more issues |
| [2026-03-25-reasoning-isolation](../learnings/2026-03-25-reasoning-isolation.md) | 2026-03-25 | high | BOULDER/CARE: isolate reasoning from output |
| [2026-03-24-fix-issue-solo-workflow](../learnings/2026-03-24-fix-issue-solo-workflow.md) | 2026-03-24 | medium | Solo dev: commit to main, skip PR workflow |
| [2026-03-23-youtube-transcript-yt-dlp](../learnings/2026-03-23-youtube-transcript-yt-dlp.md) | 2026-03-23 | high | MCP broken, use yt-dlp CLI |
| [2026-04-08-descriptive-over-narrative-generative](../learnings/2026-04-08-descriptive-over-narrative-generative.md) | 2026-04-08 | medium | Observable descriptions only for generative prompts |
| [2026-04-03-anthropic-skill-creator-patterns](../learnings/2026-04-03-anthropic-skill-creator-patterns.md) | 2026-04-03 | high | Anthropic skill-creator validation of STOPA patterns |
