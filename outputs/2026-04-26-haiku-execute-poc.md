# Opus Skills Audit (Haiku Execute POC)

## Skills with model: opus

| Skill name | Path | Recommendation |
|-----------|------|----------------|
| build-project | `.claude/skills/build-project/SKILL.md` | KEEP opus. Orchestrates end-to-end project scaffolding, multi-feature implementation, and integration verification. Requires sustained reasoning across sessions with feature-list.json ground truth tracking and complex dependency management. Multi-session harness justifies model strength. |
| orchestrate | `.claude/skills/orchestrate/SKILL.md` | KEEP opus. Routes and decomposes complex multi-step tasks with explicit budget tiers, parallel agent coordination, and architectural decision-making. Coordinator tier (deny-tools: [Bash, Write, Edit]) means delegation intelligence is critical — no direct execution safety net. Requires strong reasoning for subtask decomposition and input/output contract validation. |

## Methodology

Used `grep -l "^model: opus" .claude/skills/*/SKILL.md` to search all 50+ SKILL.md files in the skills directory. This pattern matches only YAML frontmatter declarations at the line start, filtering out commented or indented references. Found 2 matches.

## Verification

Ground truth check: `grep -l "^model: opus" .claude/skills/*/SKILL.md`

```
.claude/skills/build-project/SKILL.md
.claude/skills/orchestrate/SKILL.md
```

Match: **yes**

Both skills justified to retain opus:
1. **build-project** — full project lifecycle with multi-session state, feature harness ground truth, per-feature E2E verification
2. **orchestrate** — complex decomposition + parallel coordination + architectural routing (no direct execution means routing decisions must be sound)

Neither should downgrade to sonnet without loss of capability.

## Status
- code: DONE
- found_count: 2
- verified: yes
