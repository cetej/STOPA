---
generated: 2026-04-04
cluster: skill-design
sources: 13
last_updated: 2026-04-08
---

# Skill Design & Architecture

> **TL;DR**: Skills live canonically in STOPA, exist in two synced locations (commands/ and skills/), and their `description` field is the single most important routing mechanism. Compact variants deliver 87-94% word reduction on repeat invocations (measured). Skills with reference files should use 3-layer knowledge routing. Agents voluntarily load only 49% of relevant skills — supplementary discovery-keywords improve selection rate.

## Overview

STOPA's skill system has evolved through competitive analysis (superpowers, Anthropic's official skill-creator) and hard-won bugs into a set of firm architectural rules. The foundational constraint is that skills must be developed in STOPA first and distributed to target projects — never created directly in NG-ROBOT, test1, or ADOBE-AUTOMAT (ref: 2026-03-27-skills-must-live-in-stopa.md). The dual-location structure (`.claude/commands/<name>.md` flat files and `.claude/skills/<name>/SKILL.md` directories) exists for compatibility, but both copies MUST stay identical — desync causes unpredictable behavior (ref: 2026-03-27-commands-vs-skills-structure.md).

The `description` field in SKILL.md frontmatter is the primary routing mechanism: Claude Code matches skills by description text, not by name or body content (ref: 2026-03-25-skill-description-triggers.md). Workflow summaries in descriptions cause Claude to shortcut instead of reading the full skill body. Anthropic's official skill-creator reinforces this with a 3-level progressive disclosure model and a 500-line SKILL.md limit (ref: 2026-04-03-anthropic-skill-creator-patterns.md). A description optimization pipeline with train/test split is planned but not yet implemented (ref: 2026-04-03-description-optimizer-plan.md).

The SKILL0 Dynamic Curriculum pattern introduces compact skill variants (~7% of full size) for repeat invocations within a session, with impact_score tracking for helpfulness-driven learning graduation (ref: 2026-04-04-skill0-dynamic-curriculum.md). Meanwhile, CC v2.1.91 added `disableSkillShellExecution`, but audit revealed 52% of STOPA skills use inline shell — enabling it would break half the system (ref: 2026-04-03-disable-skill-shell-audit.md).

An important operational boundary: deepresearch researcher sub-agents must be capped at max 15 tool calls. A 34-call run took ~4 hours; wide scopes must be split into 2-3 smaller agents of 8-12 calls each (ref: 2026-04-06-deepresearch-agent-scope.md).

Compact variant measurement confirmed 87-94% word reduction across 6 skills — the original ~80% claim was conservative (ref: 2026-04-07-compact-variant-baseline.md). Skill autodiscovery has a retrieval bottleneck: agents voluntarily load only 49% of relevant skills from metadata alone (arXiv:2604.04323). Query-specific refinement and supplementary `discovery-keywords` recover performance; offline refinement doesn't help (ref: 2026-04-07-skill-retrieval-bottleneck.md).

Skills with reference files should use 3-layer knowledge routing: always-on baseline (quality floor), semantic-inference auto-load (from natural language signals), and explicit-override (user-named). The bias should favor loading — cost of extra tokens is lower than cost of low-quality output from missing context (ref: 2026-04-08-progressive-knowledge-routing.md). For output validation, structured numbered rules with explicit error/warning tiers executed by the LLM itself with a hard-stop before delivery outperform advisory self-checks. Python scripts should be decoupled to CI/CD only (ref: 2026-04-08-llm-native-validation-hardstop.md).

## Key Rules

1. **Skills develop in STOPA first**: never create skills directly in target projects (ref: 2026-03-27-skills-must-live-in-stopa.md)
2. **commands/ and skills/ must stay identical**: edit one, sync both (ref: 2026-03-27-commands-vs-skills-structure.md)
3. **description = trigger conditions only**: "Use when..." format, no workflow summaries (ref: 2026-03-25-skill-description-triggers.md)
4. **SKILL.md max 500 lines**: Anthropic recommendation (ref: 2026-04-03-anthropic-skill-creator-patterns.md)
5. **Compact variants for repeat invocations**: SKILL.compact.md at ~7% token size (ref: 2026-04-04-skill0-dynamic-curriculum.md)
6. **Researcher sub-agents: max 15 tool calls**: split wide scope into smaller agents (ref: 2026-04-06-deepresearch-agent-scope.md)
7. **Do NOT enable disableSkillShellExecution**: 52% of skills would break (ref: 2026-04-03-disable-skill-shell-audit.md)
8. **Compact variants: 87-94% reduction** (measured): conservative ~80% claim confirmed (ref: 2026-04-07-compact-variant-baseline.md)
9. **discovery-keywords for autodiscovery**: 49% voluntary load rate without them (ref: 2026-04-07-skill-retrieval-bottleneck.md)
10. **3-layer knowledge routing**: always-on baseline + semantic-inference + explicit-override (ref: 2026-04-08-progressive-knowledge-routing.md)
11. **LLM-native validation with hard-stop**: numbered rules + error/warning tiers before output delivery (ref: 2026-04-08-llm-native-validation-hardstop.md)

## Patterns

### Do
- Start descriptions with "Use when..." and include DO NOT triggers
- Add anti-rationalization tables and verification checklists to Tier 1 skills
- Create SKILL.compact.md for frequently-invoked skills (ref: 2026-04-04-skill0-dynamic-curriculum.md)
- Split researcher agents by topic area when scope exceeds 3-4 methods (ref: 2026-04-06-deepresearch-agent-scope.md)

### Don't
- Put workflow summaries or step lists in the description field (ref: 2026-03-25-skill-description-triggers.md)
- Create or modify skills in target projects (ref: 2026-03-27-skills-must-live-in-stopa.md)
- Edit only one of commands/skills without syncing the other (ref: 2026-03-27-commands-vs-skills-structure.md)
- Give a single researcher agent 6+ methods to explore (ref: 2026-04-06-deepresearch-agent-scope.md)

## Open Questions

- ~~GAP: Compact variant measurement~~ — RESOLVED: 87-94% word reduction measured (ref: 2026-04-07-compact-variant-baseline.md)
- GAP: SKILL.examples.md for positive demonstrations — planned but not yet implemented

## Related Articles

- See also: [skill-evaluation](skill-evaluation.md) — evaluation patterns for skill output quality
- See also: [orchestration-resilience](orchestration-resilience.md) — error handling that skills depend on

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-06-deepresearch-agent-scope](../learnings/2026-04-06-deepresearch-agent-scope.md) | 2026-04-06 | high | Max 15 tool calls per researcher agent |
| [2026-04-04-gap-compact-variant-measurement](../learnings/2026-04-04-gap-compact-variant-measurement.md) | 2026-04-04 | medium | GAP: no measurement data on compact variant effectiveness |
| [2026-04-04-skill0-dynamic-curriculum](../learnings/2026-04-04-skill0-dynamic-curriculum.md) | 2026-04-04 | high | SKILL0 Dynamic Curriculum: compact variants, impact scoring |
| [2026-04-03-anthropic-skill-creator-patterns](../learnings/2026-04-03-anthropic-skill-creator-patterns.md) | 2026-04-03 | high | Anthropic skill-creator: 3-level disclosure, 500-line limit |
| [2026-04-03-description-optimizer-plan](../learnings/2026-04-03-description-optimizer-plan.md) | 2026-04-03 | high | Description optimization pipeline plan |
| [2026-04-03-disable-skill-shell-audit](../learnings/2026-04-03-disable-skill-shell-audit.md) | 2026-04-03 | high | Shell audit: 52% skills use inline shell |
| [2026-03-27-commands-vs-skills-structure](../learnings/2026-03-27-commands-vs-skills-structure.md) | 2026-03-27 | critical | Dual location must stay synced |
| [2026-03-27-skills-must-live-in-stopa](../learnings/2026-03-27-skills-must-live-in-stopa.md) | 2026-03-27 | high | Skills develop in STOPA first |
| [2026-04-08-progressive-knowledge-routing](../learnings/2026-04-08-progressive-knowledge-routing.md) | 2026-04-08 | high | 3-layer knowledge routing for skills with ref files |
| [2026-04-08-llm-native-validation-hardstop](../learnings/2026-04-08-llm-native-validation-hardstop.md) | 2026-04-08 | high | Numbered validation rules with hard-stop |
| [2026-04-07-skill-retrieval-bottleneck](../learnings/2026-04-07-skill-retrieval-bottleneck.md) | 2026-04-07 | high | 49% voluntary skill loading; discovery-keywords fix |
| [2026-04-07-compact-variant-baseline](../learnings/2026-04-07-compact-variant-baseline.md) | 2026-04-07 | medium | 87-94% word reduction measured |
| [2026-03-25-skill-description-triggers](../learnings/2026-03-25-skill-description-triggers.md) | 2026-03-25 | high | Description must contain all trigger words |
