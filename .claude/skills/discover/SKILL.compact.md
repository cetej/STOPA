---
name: discover
variant: compact
description: Condensed discover for repeat invocations within session. Use full SKILL.md for first invocation.
---

# /discover — Compact (Session Re-invocation)

Behavioral n-gram analysis of session traces: surface emergent patterns, get human verdicts, persist results.

## Input Flags

| Flag | Effect |
|------|--------|
| `--days N` | Analyze last N days (default: 7) |
| `--focus <keyword>` | Filter traces by tool name or path |
| `--compare` | Show week-over-week delta |

## 5-Phase Pipeline

1. **AGGREGATE** — Glob `.traces/sessions/*.jsonl`, filter by date, parse records. Build per-session data: tool_sequence, error_count, files_touched, skills_used. If >50 files: sample 20 recent + 10 random.

2. **SEQUENCE** — Extract behavioral n-grams:
   - Bigrams: top 15 (tool→tool transition frequencies)
   - Trigrams: top 10 (3-tool micro-workflows)
   - Failure sequences: what tool failed, what came before, what came after
   - Session signatures: top-3 tools per session → behavioral clusters
   - Primitive action sequences: reusable 2-4 tool chains that appear in 5+ sessions with exit==0

3. **DISCOVER** — Classify patterns into: `healthy` | `desperation` (Edit→Bash→Edit loops 3+) | `delegation_cascade` | `blind_editing` | `recovery_success` | `novel`. Compute entropy per session (low <1.5 = potential desperation). Surface only patterns in 3+ sessions (exception: 3+ failures in one session).

4. **PRESENT** — Decision table: pattern | category | frequency | sessions | verdict(?). For novel/confidence <0.6: ask user for (a) reinforce / (b) suppress / (c) neutral / (d) need more data.

5. **PERSIST** — Write classified patterns to `discovered-patterns.md` with verdict: reinforce | suppress | pending.

## Circuit Breakers

- NEVER modify trace files — read-only analysis only
- NEVER classify novel patterns without human input
- Limit output to max 15 most significant patterns (filter by frequency x impact)
- discovered-patterns.md max 300 lines — archive old entries when approaching limit
- If no session traces found: report and EXIT (no invented analysis)

## Output feeds /evolve

Discovered patterns with human verdicts → /evolve Phase 7b artifact synthesis.
