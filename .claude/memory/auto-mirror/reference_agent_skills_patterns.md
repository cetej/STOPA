---
name: agent-skills patterns adoption
description: Patterns adopted from addyosmani/agent-skills into STOPA — anti-rationalization, red flags, verification checklists, lifecycle phases
type: reference
---

## addyosmani/agent-skills — Adopted Patterns (2026-04-04)

Source: https://github.com/addyosmani/agent-skills (Addy Osmani, Google)

### What was adopted into STOPA

1. **Anti-Rationalization Defense** — standardized 3-column table (`Rationalization | Why Wrong | Do Instead`) in every Tier 1/2/4 skill. Addresses agent shortcutting.
2. **Red Flags** — bullet list of observable symptoms of skill misapplication. Tier 1 required, others optional.
3. **Verification Checklist** — checkbox exit criteria with evidence requirements. Tier 1 required.
4. **Lifecycle Phase Tagging** — `phase:` field in frontmatter (define/plan/build/verify/review/ship/meta). All 48 skills tagged.

### What STOPA already had that agent-skills doesn't
- Permission tiers + tool-gate.py runtime enforcement
- Orchestration with budget tiers and circuit breakers
- Shared persistent memory between skills
- Learnings system with confidence/decay/graduation
- Panic detector + calm steering hooks

### Spec locations
- Section format: `.claude/rules/skill-files.md` ("Skill Body Sections")
- Phase mapping: `.claude/rules/skill-tiers.md` ("Lifecycle Phase Mapping")
- Required sections by tier: both files contain the table
