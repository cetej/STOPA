---
name: scribe
variant: compact
description: Condensed scribe for repeat invocations within session. Use full SKILL.md for first invocation.
---

# Scribe — Compact (Session Re-invocation)

Maintain shared memory. Record facts neutrally. Do NOT judge or execute.

## Input to Target Mapping

| Argument | Target |
|---------|--------|
| `decision` | ADR file in `docs/decisions/` + entry in `decisions.md` index |
| `learning` | New file in `learnings/` with YAML frontmatter |
| `state` | Update active task section in `state.md` |
| `complete` | Move task to history, clear Active Task section |
| free text | Determine best target file |

## Write-Time Salience Gate (mandatory)

```
SALIENCE = source_reputation x novelty x reliability
```

| Factor | Values |
|--------|--------|
| source_reputation | user_correction=1.0, critic_finding=0.8, auto_pattern=0.6, external_research=0.5, agent_generated=0.4 |
| novelty | unique=1.0, related but distinct=0.5, near-duplicate (same component + 2+ tags + >60% overlap)=0.1 |
| reliability | verify_check passes=1.0, defined=0.7, manual rule=0.5, unverifiable=0.3 |

Thresholds: >=0.4 WRITE | 0.2-0.4 write as severity:low | <0.2 DO NOT WRITE (log to activity-log.md)

**Mandatory dedup before writing:** Grep component + tags, compare summary. Near-duplicate → update existing, don't create new file.

## Learning File Required Frontmatter Fields

`date, type, severity, component, tags, summary, source, uses: 0, successful_uses: 0, harmful_uses: 0, confidence`

Optional: `supersedes, related, failure_class, failure_agent, task_context, model_gate, verify_check`

Initial confidence by source: user_correction=0.9, critic_finding=0.8, auto_pattern=0.7, external_research=0.6, agent_generated=0.5

## Contradiction Check

Before writing: grep same component + 2+ shared tags → compare summaries. If contradicts existing:
- Better solution → `supersedes: <old-file>` in new frontmatter
- Context-dependent → add `## Context Boundary` + `related: [<old-file>]`
- Unclear → WARNING to user

## Circuit Breakers

- NEVER write a learning without component and tags (grep-unfindable)
- NEVER skip dedup gate — it is mandatory, not optional
- NEVER delete history — archive only
- critical-patterns.md max 10 entries — bump weakest before adding
- Memory files max 500 lines → maintenance required

## Maintenance

Auto-triggered at >500 lines. Steps: dedup learnings → staleness check (90 days) → counter health → archive budget/performance → rebuild L2 indexes.
