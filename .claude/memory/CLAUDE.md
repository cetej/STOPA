# Memory System Rules

## General
- Max 500 lines per file — archive overflow to `*-archive.md`, never delete
- Format: markdown with clear structure (headings, tables, lists)
- Dates: YYYY-MM-DD (absolute, never relative)

## File types
| File | Purpose | Update frequency |
|------|---------|-----------------|
| `state.md` | Current task state (YAML frontmatter + markdown) | Per-task |
| `budget.md` | Cost ledger + tier | Per-agent-call |
| `decisions.md` | Index pointing to `docs/decisions/` | Per-decision |
| `checkpoint.md` | Session snapshot (YAML frontmatter + markdown) | Per-session |
| `key-facts.md` | Stack, endpoints, env vars (max 200 lines) | On infra change |
| `news.md` | /watch scan results | Weekly |
| `radar.md` | /radar tool evaluations | Per-scan |
| `improvement-log.md` | Cross-project routing audit trail | Per-routing |
| `replay-queue.md` | HERA failure-sourced learning validation queue | Per-failure |
| `outcomes/` | Per-run RCL credit records (success/failure) | Per-skill-run |
| `failures/` | HERA failure trajectory records | Per-failure |
| `optstate/` | Per-skill optimization state (JSON) | Per-skill-run |
| `intermediate/` | Skill post-it state (max 30 lines, 24h TTL) | Per-skill-run |

## Global memory (outside STOPA)
| File | Purpose |
|------|---------|
| `~/.claude/memory/projects/*.yaml` | Project profiles for cross-project improvement routing |
| `~/.claude/memory/projects.json` | Project registry (paths, repos, stack) |

## Learnings (`learnings/` subdirectory)
- One file per learning, YAML frontmatter: date, type, severity, component, tags, summary, source, uses, harmful_uses, confidence
- Filename: `YYYY-MM-DD-short-description.md`
- Retrieval: grep-first by component/tags, then read matched files
- Graduation: `uses >= 10` AND `confidence >= 0.8` -> promote to `critical-patterns.md`
- `critical-patterns.md`: always-read, max 10 entries

## Archive policy
- When file exceeds 500 lines: move old entries to `*-archive.md`
- Never delete history — archive only
- Stale entries (90+ days): verify during maintenance
