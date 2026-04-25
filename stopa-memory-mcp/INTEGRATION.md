# Bridge Integration Pattern — Dual-Write for STOPA Skills

How `/scribe`, `/handoff`, `/checkpoint` (and any future memory-writing skill) opt-in to dual-write through the managed memory bridge.

## The pattern

After every successful local memory write, attempt a parallel write to the managed store via the MCP bridge:

```
1. Local write (canonical):  Edit/Write `.claude/memory/<file>`   ← always
2. Bridge detection:         Is mcp__stopa-memory__memstore_write_memory available?
3. If yes — dual-write:      memstore_write_memory(path=<file>, content=<same>)
4. If no — skip silently:    local-only mode is the default
```

Local file is always the source of truth. Managed store is a versioned shadow.

## Detection (graceful degradation)

Skills MUST check availability before calling. Two signals:

1. **Tool list** — is `mcp__stopa-memory__memstore_write_memory` in the available tools? If not, the bridge is not configured. Skip.
2. **Env var** — is `STOPA_MEMSTORE_ID` set? Without it, the bridge raises `ValueError` on every call. Read once at session start; cache the result.

If either check fails, **continue without error**. The skill's job is to write memory — bridge dual-write is a nice-to-have, not a requirement.

## Path mapping

The managed store uses absolute paths (filesystem-style). Map STOPA's relative paths predictably:

| Local file | Memstore path |
|------------|---------------|
| `.claude/memory/decisions.md` | `/decisions.md` |
| `.claude/memory/learnings/<file>.md` | `/learnings/<file>.md` |
| `.claude/memory/state.md` | `/state.md` |
| `.claude/memory/checkpoint.md` | `/checkpoint.md` |
| `.claude/memory/news.md` | `/news.md` |

Strip the `.claude/memory/` prefix; everything else is verbatim. Use forward slashes always (memstore is OS-agnostic).

## Failure handling

If the bridge call fails (network, auth, beta limits, 4xx/5xx), the skill MUST:

1. Log the error to stderr (one line, `[memstore] WARN: <reason>`)
2. Continue — the local write succeeded; that is the canonical state
3. Do NOT retry inside the skill (bridge has its own retry; one attempt per write is enough)
4. Do NOT propagate the error to the user as a failure (the local write worked)

Pattern in pseudo-code:

```
local_write(path, content)              # primary, must succeed
try:
    if bridge_available:
        memstore_write_memory(path=remap(path), content=content)
except Exception as e:
    print(f"[memstore] WARN: {e}", file=stderr)
```

## What this buys

- **Versioned audit trail** — every edit creates an immutable version (30-day retention in beta)
- **Cross-session sync** — multiple CC instances + future Managed Agent runs see the same store
- **Crash safety** — remote copy survives local disk corruption
- **Diff between versions** — `memstore_list_versions(path)` returns full history

## What this does NOT buy (yet)

- **Real-time read consistency** — local writes happen first; reads should still hit local files
- **Concurrent write conflict resolution** — last write wins; no CRDT
- **Free** — pricing not announced for GA; beta currently free but plan accordingly

## When NOT to dual-write

- Memory files exceeding 100 kB per memory (beta limit) — split first or skip
- Files containing secrets (.local.json, secrets.env) — never dual-write secrets, even via bridge
- Ephemeral state (`intermediate/*.json`, post-it files) — these are session-scoped, not worth versioning

Skills should hard-skip dual-write for these categories.

## Reference

- Bridge code: `stopa-memory-mcp/server.py`
- Live test: `stopa-memory-mcp/live_test.py`
- Mock tests: `stopa-memory-mcp/test_server.py`
- Issue: [cetej/STOPA#26](https://github.com/cetej/STOPA/issues/26)
- Live-test result: 7/7 passed against real Anthropic API on 2026-04-25
