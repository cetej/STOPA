---
generated: 2026-04-04
cluster: skill-design
sources: 8
last_updated: 2026-04-04
---

# Skill Design & Architecture

> **TL;DR**: Skills live canonically in STOPA, exist in two synced locations (commands/ and skills/), and their `description` field is the single most important routing mechanism. Progressive disclosure via compact variants reduces token overhead by ~80% on repeat invocations.

## Overview

STOPA's skill system has evolved through competitive analysis (superpowers, Anthropic's official skill-creator) and hard-won bugs into a set of firm architectural rules. The foundational constraint is that skills must be developed in STOPA first and distributed to target projects — never created directly in NG-ROBOT, test1, or ADOBE-AUTOMAT (ref: 2026-03-27-skills-must-live-in-stopa.md). The dual-location structure (`.claude/commands/<name>.md` flat files and `.claude/skills/<name>/SKILL.md` directories) exists for compatibility, but both copies MUST stay identical — desync causes unpredictable behavior (ref: 2026-03-27-commands-vs-skills-structure.md).

The `description` field in SKILL.md frontmatter is the primary routing mechanism: Claude Code matches skills by description text, not by name or body content (ref: 2026-03-25-skill-description-triggers.md). Tested by obra/superpowers, workflow summaries in descriptions cause Claude to shortcut instead of reading the full skill body (ref: superpowers-adoption.md). Anthropic's official skill-creator reinforces this with a 3-level progressive disclosure model and a 500-line SKILL.md limit (ref: 2026-04-03-anthropic-skill-creator-patterns.md). A description optimization pipeline with train/test split is planned but not yet implemented (ref: 2026-04-03-description-optimizer-plan.md).

The SKILL0 Dynamic Curriculum pattern introduces compact skill variants (~7% of full size) for repeat invocations within a session, with impact_score tracking for helpfulness-driven learning graduation (ref: 2026-04-04-skill0-dynamic-curriculum.md). Meanwhile, CC v2.1.91 added `disableSkillShellExecution`, but audit revealed 52% of STOPA skills use inline shell — enabling it would break half the system (ref: 2026-04-03-disable-skill-shell-audit.md).

## Key Rules

1. **Skills develop in STOPA first**: never create skills directly in target projects (ref: 2026-03-27-skills-must-live-in-stopa.md)
2. **commands/ and skills/ must stay identical**: edit one, sync both (ref: 2026-03-27-commands-vs-skills-structure.md)
3. **description = trigger conditions only**: "Use when..." format, no workflow summaries (ref: 2026-03-25-skill-description-triggers.md)
4. **Include all trigger words in description**: CC matches by description text (ref: superpowers-adoption.md)
5. **SKILL.md max 500 lines**: Anthropic recommendation (ref: 2026-04-03-anthropic-skill-creator-patterns.md)
6. **Compact variants for repeat invocations**: SKILL.compact.md at ~7% token size (ref: 2026-04-04-skill0-dynamic-curriculum.md)
7. **Do NOT enable disableSkillShellExecution**: 52% of skills would break (ref: 2026-04-03-disable-skill-shell-audit.md)

## Patterns

### Do
- Start descriptions with "Use when..." and include DO NOT triggers (ref: superpowers-adoption.md)
- Add anti-rationalization tables and verification checklists to Tier 1 skills (ref: superpowers-adoption.md)
- Create SKILL.compact.md for frequently-invoked skills (ref: 2026-04-04-skill0-dynamic-curriculum.md)
- Plan description optimization with train/test eval split (ref: 2026-04-03-description-optimizer-plan.md)

### Don't
- Put workflow summaries or step lists in the description field (ref: 2026-03-25-skill-description-triggers.md)
- Create or modify skills in target projects (ref: 2026-03-27-skills-must-live-in-stopa.md)
- Edit only one of commands/skills without syncing the other (ref: 2026-03-27-commands-vs-skills-structure.md)

## Open Questions

- GAP: No measurement data on compact variant effectiveness — how much context is actually saved in practice?

## Related Articles

- See also: [skill-evaluation](skill-evaluation.md) — evaluation patterns for skill output quality
- See also: [orchestration-resilience](orchestration-resilience.md) — error handling that skills depend on

## Source Learnings

| File | Date | Severity | Summary |
|------|------|----------|---------|
| [2026-04-04-skill0-dynamic-curriculum](../learnings/2026-04-04-skill0-dynamic-curriculum.md) | 2026-04-04 | high | SKILL0 Dynamic Curriculum: compact variants, impact scoring |
| [2026-04-03-anthropic-skill-creator-patterns](../learnings/2026-04-03-anthropic-skill-creator-patterns.md) | 2026-04-03 | high | Anthropic skill-creator: 3-level disclosure, 500-line limit |
| [2026-04-03-description-optimizer-plan](../learnings/2026-04-03-description-optimizer-plan.md) | 2026-04-03 | high | Description optimization pipeline plan |
| [2026-04-03-disable-skill-shell-audit](../learnings/2026-04-03-disable-skill-shell-audit.md) | 2026-04-03 | high | Shell audit: 52% skills use inline shell |
| [2026-03-27-commands-vs-skills-structure](../learnings/2026-03-27-commands-vs-skills-structure.md) | 2026-03-27 | critical | Dual location must stay synced |
| [2026-03-27-skills-must-live-in-stopa](../learnings/2026-03-27-skills-must-live-in-stopa.md) | 2026-03-27 | high | Skills develop in STOPA first |
| [2026-03-25-skill-description-triggers](../learnings/2026-03-25-skill-description-triggers.md) | 2026-03-25 | high | Description must contain all trigger words |
| [superpowers-adoption](../learnings/superpowers-adoption.md) | 2026-03-23 | high | Anti-rationalization, trigger matching from superpowers |
