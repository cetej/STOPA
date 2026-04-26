# Opus Skills Audit (Sonnet Execute POC)

## Skills with model: opus

| Skill name | Path | Recommendation |
|-----------|------|----------------|
| build-project | .claude/skills/build-project/SKILL.md | Keep opus — end-to-end autonomous project builder requires deep multi-step planning and architectural decisions across many files |
| orchestrate | .claude/skills/orchestrate/SKILL.md | Keep opus — core orchestrator for complex task decomposition, multi-agent coordination, and tier/budget decisions |

## Methodology

Used `grep -rl "^model: opus"` across all SKILL.md files in `.claude/skills/` to find exact frontmatter matches.

## Verification

Ground truth check: `grep -rl "^model: opus" .claude/skills/*/SKILL.md`
Match: yes
