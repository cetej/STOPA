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
| `critic-accuracy.jsonl` | Critic verdict alignment tracking | Per-critic-run |
| `key-facts.md` | Stack, endpoints, env vars (max 200 lines) | On infra change |
| `news.md` | /watch scan results | Weekly |

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
