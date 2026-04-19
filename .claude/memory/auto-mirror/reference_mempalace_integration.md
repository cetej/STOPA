---
name: MemPalace integration
description: MemPalace v3.1.0 — Layer 1 (session archive hook) + Layer 2 (semantic fallback in hybrid-retrieve.py) deployed
type: reference
---

MemPalace (github.com/MemPalace/mempalace) v3.1.0 integrated into STOPA.

## Layer 1 — Session Archive (deployed 2026-04-12)

**Hook**: `.claude/hooks/mempalace-archive.py` runs as Stop hook after session-summary.sh. Reads intermediate/session-summary.json + checkpoint.md, stores as ChromaDB drawer with wing=project, room=sessions.

**Token impact**: 0 at session start (write-only archive).

## Layer 2 — Semantic Retrieval Fallback (deployed 2026-04-12)

**File**: `scripts/hybrid-retrieve.py` — Signal 4 added to RRF fusion.

**Trigger rules**:
- local unique results < 2 AND tier >= standard → fallback triggered
- tier == deep → always-on (maximum recall)
- tier == light → never (fast path preserved)

**How it works**: `mempalace.palace.get_collection()` → ChromaDB query with wing filter → results injected as `mp:*` virtual filenames into RRF fusion. Distance threshold 1.2 filters noise.

**Search**: `from mempalace.searcher import search; search(query, palace_path, wing="stopa")`

## Setup

- `pip install mempalace` (system Python)
- Palace at `~/.mempalace/palace/`, ChromaDB + MiniLM-L6-v2 embeddings

## Layer 3 — Knowledge Graph Sync (deployed 2026-04-12)

**File**: `scripts/kg-sync.py` — bidirectional sync between concept-graph.json and MemPalace SQLite KG.

**Direction A (STOPA → MemPalace)**:
- Typed entities (tool, paper, person, company) → `kg.add_entity()`
- High-weight co-occurrence edges (≥3) → `related_to` triples
- Entity-learning links → `mentioned_in` triples with temporal validity
- Initial sync: 497 entities, 543 triples exported

**Direction B (MemPalace → STOPA)**:
- New triples from MemPalace → concept-graph edges with `mempalace_predicate` field
- Invalidated triples → `invalidated` annotation on existing edges
- Incremental: only processes triples newer than last_sync timestamp

**Hook**: Runs as Stop hook after graph-consolidate.sh and hebbian-consolidate.py.
**State**: `.claude/memory/intermediate/kg-sync-state.json` tracks last_sync and cumulative counters.

**Temporal queries**: `kg.query_entity('camel', as_of='2026-04-09')` — MemPalace KG natively supports time-travel queries that STOPA concept-graph cannot.

## Known issues

- First run downloads 79MB embedding model (one-time, cached)
- ChromaDB on macOS ARM64 may segfault (issue #74)
- Hook timeout 10s may be tight on cold start (model load)
- Windows cp1250 encoding needs sys.stdout.reconfigure workaround
- Palace sparse with 1 session — fallback value grows with accumulated sessions
