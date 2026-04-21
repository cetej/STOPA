---
date: 2026-04-21
status: IMPLEMENTING
component: memory
tags: [memory, abstraction, cmm, adapter-pattern]
supersedes:
---

# 0017 — Memory Backend Abstraction Layer

## Context

ADR 0016 Phase C council (2026-04-21) delivered verdict B for Sub-decision 1:
"Build abstraction layer now + CMM adapter in parallel." The full council
reasoning is in `outputs/adr-0016-phase-c-council.md`.

STOPA currently has ~200 learnings stored as YAML-frontmatter Markdown files
in `.claude/memory/learnings/*.md`. Retrieval is handled by
`scripts/hybrid-retrieve.py` (grep + BM25 + graph walk + RRF fusion).

Claude Managed Memory (CMM) is in Research Preview, targeting GA Q2-Q3 2026.
It offers 6 API methods (list/search/read/write/edit/delete) with cross-session
persistence, versioned audit trail, and workspace scoping.

Without an abstraction layer, migrating to CMM at GA would require editing
every skill and hook that touches the learnings directory — estimated 80+
call sites across 40+ skill files.

## Decision

Implement an **adapter pattern** with a common abstract interface and two
concrete implementations:

1. `MemoryBackend` ABC (`.claude/lib/memory_backend.py`) — 6 methods mirroring
   the CMM API contract: list, search, read, write, edit, delete.

2. `LocalMemoryAdapter` (`.claude/lib/local_memory_adapter.py`) — wraps the
   current file-based system. search() delegates to hybrid-retrieve.py.
   delete() archives to learnings-archive.md (preserves core-invariant #5).

3. `CMMemoryAdapter` (`.claude/lib/cmm_memory_adapter.py`) — mock class showing
   the intended contract shape. Has `TODO(cmm-ga)` comments where real
   `anthropic.beta.memory.*` calls will go. No actual API calls yet.

4. Contract tests (`tests/test_memory_backend.py`) — both adapters pass the
   same pytest suite. write-then-read, list-filter, search, edit-preserves-
   metadata, delete-archives-not-destroys.

Existing callers (skills, hooks, scripts) are NOT refactored in this ADR.
Migration of call sites is a separate ADR when CMM reaches GA.

## Alternatives Considered

**A — Wait for CMM GA, then migrate everything at once.**
Rejected: "big bang" migration is risky; abstraction layer is cheap now
(~300 lines), painful later (80+ call sites under time pressure at GA).

**C — Stay file-based indefinitely, skip abstraction.**
The Skeptic's position. Overruled because STOPA's moat is the semantics above
storage (maturity tiers, confidence, supersedes chains), not the storage
format itself. See council ADR for full reasoning.

**D — Adopt CMM beta now, migrate immediately.**
Would tie STOPA to an unstable Research Preview API. Pragmatist and User
Advocate both argued against this. User confirmed they would not abandon STOPA
even if CMM was perfect ("Neopustil" — answer to Futurist forcing question).

## Consequences

- Migration path to CMM at GA = swap one class reference, not rewrite 80
  skills. Implementation time drops from estimated 2 weeks to ~2 hours.
- No existing callers are modified. The abstraction lives in `.claude/lib/`
  and is available for new code immediately.
- Contract tests run in CI to prevent interface drift between adapters.
- If CMM GA ships without custom metadata fields or skill-scoped namespacing,
  the Skeptic's counter-trigger fires: re-evaluate staying file-based (see
  council ADR §Dissenting View).
- Follow-up work: add `LocalMemoryAdapter` as the default in skills that
  currently call hybrid-retrieve.py directly (tracked in ADR 0016 execution
  plan, Week 5-8).
