---
name: SkillReducer
type: paper
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [vertical-scaling-research, vertical-scaling-report]
tags: [skill-design, token-efficiency, context-engineering]
---

# SkillReducer

> Paper demonstrating that 60%+ of skill/prompt content is non-actionable; 75% token reduction via compression produces BETTER quality outputs (less-is-more effect).

## Key Facts

- Paper: arXiv:2603.29919 (ref: sources/vertical-scaling-research.md)
- 60%+ of skill content is non-actionable (ref: sources/vertical-scaling-research.md)
- 75% token reduction: 359K → 84K tokens across 100 skills (ref: sources/vertical-scaling-research.md)
- Quality after compression: HIGHER — 0.742 vs 0.722 (p=0.002) (ref: sources/vertical-scaling-research.md)
- Reference files: 1.67M tokens per 100 skills (505 files); cross-file deduplication = 29% savings (ref: sources/vertical-scaling-research.md)

## Relevance to STOPA

Direct justification for SKILL.compact.md variants and progressive skill withdrawal (SKILL0 pattern). The less-is-more effect validates that condensed skill versions are not just cheaper but actually better. Apply to all Tier 1 STOPA skills.

## Mentioned In

- [Vertikální škálování Research](../sources/vertical-scaling-research.md)
- [Vertikální škálování STOPA orchestrace — Technická zpráva](../sources/vertical-scaling-report.md)
