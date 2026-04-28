---
date: 2026-04-08
type: architecture
severity: medium
component: orchestration
tags: [multi-agent, state-sharing, farm-tier, coordination, isolation]
summary: "CORAL pattern: agents share knowledge via symlinked `.coral/public/` dir instead of message passing — zero sync overhead, każdy agent v vlastním git worktree branchi. Knowledge reuse je primární driver multi-agent gainů, ne parallelismus samotný."
source: external_research
uses: 17
harmful_uses: 0
successful_uses: 1
confidence: 1.00
maturity: core
graduated_to: ""
verify_check: "Glob('.claude/memory/intermediate/shared/notes.md') → 1+ matches"
related: [2026-03-29-claudini-autoresearch-loop.md]
failure_class: ""
task_context: {task_class: research, complexity: medium, tier: standard}
---

## Shared Public State — Agent Coordination bez Message Passing

CORAL (arXiv:2604.01658) ukazuje efektivnější koordinaci multi-agent systémů:

**Pattern:**
- Každý agent = vlastní git worktree branch (filesystem isolation, ne sandbox)
- Shared state = jeden symlinked adresář `.coral/public/` readable/writable všemi agenty
- Žádný explicit message passing, žádný orchestrátor jako dispatcher

**Proč to funguje:**
- Symlink reads = filesystem-level, ne network/IPC → zero sync overhead
- Agenti publikují partial results průběžně bez blokování svého local loop
- Knowledge reuse (sdílené attempts, notes, skills) je primární driver gainů — ne pouhý paralelismus

**Relevance pro STOPA:**
STOPA farm tier aktuálně předává state přes `checkpoint.md` + `state.md` sekvenčně. Pro true async parallel agents v `--group N` by shared public dir pattern eliminoval polling a merge konflikty.

**Jak aplikovat:**
Pro farm tier orchestration: zvažit `.claude/shared/` dir (symlinked nebo přímý) místo checkpoint-based handoff. Agenti zapisují do per-slot souborů (`agent-1.md`, `agent-2.md`), orchestrátor čte.
