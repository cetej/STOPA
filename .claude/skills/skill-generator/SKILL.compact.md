---
name: skill-generator
variant: compact
description: Condensed skill-generator for repeat invocations within session. Use full SKILL.md for first invocation.
---

# Skill Generator — Compact (Session Re-invocation)

Create, update, improve, or audit Claude Code skills.

## Actions

| Action | Steps |
|--------|-------|
| `create` | Design → Write SKILL.md → Validate-and-Repair (max 3 iterations) → Sync to commands/ |
| `update` | Read existing → Edit targeted changes → Validate |
| `improve` | Analyze for vague descriptions, broad permissions, missing error handling → Edit |
| `list` | Glob skills/*/SKILL.md, read frontmatter, present table |
| `improve-all` / `audit` | M5 score all skills, propose fixes for <12/15 |

## Required SKILL.md Frontmatter

`name, description, user-invocable, tags, phase, allowed-tools, effort`

## description field rules

- MUST start with "Use when..."
- Trigger conditions and exclusions ONLY
- MUST NOT contain workflow summaries, step lists, or internal mechanics

## Validate-and-Repair Loop (after writing)

Run up to 3 iterations. Check in order:
1. YAML frontmatter — all required fields present
2. description — starts with "Use when...", no workflow summary
3. Required sections by tier (Anti-Rationalization REQUIRED for Tier 1/2/4, Red Flags + Verification Checklist REQUIRED for Tier 1/4)
4. allowed-tools — minimal; flag if Bash granted unnecessarily
5. Line count — must be under 500 lines

If any check fails: fix with Edit, re-validate. After 3 failures: report to user, STOP.

## M5 Structural Score (audit mode)

Max 15 points. Key positive checks: description has trigger words (+2), argument-hint present (+1), process section exists (+1), references .claude/memory/ (+2), shared memory read instruction (+2). Negative: vague description words (-2), missing description (-3). Threshold: <12/15 → flag for improvement.

## Circuit Breakers

- NEVER create skills for trivial one-off tasks
- NEVER grant Bash access unless skill genuinely needs shell commands
- NEVER write skills longer than 500 lines
- NEVER skip commands/ sync — commands/ and skills/ must stay identical (core-invariant #2)
- Use Edit (not Write) for updates to existing skills

## After Completion

Update `skill-generator/LEARNINGS.md` + log decision to `decisions.md` via scribe pattern.
