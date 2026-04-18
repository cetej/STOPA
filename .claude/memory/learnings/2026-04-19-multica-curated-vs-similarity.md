---
date: 2026-04-19
type: architecture
severity: medium
component: memory
tags: [retrieval, memory, skills, architecture, external-validation]
summary: Multica (15.4k★ open-source Claude Managed Agents clone) ships memory with 6 relational tables and ZERO vector embeddings — explicit skill attachment via JOIN, JSONB snapshot at dispatch. Validates STOPA grep-first + curated discovery-keywords approach: "curated relevance beats learned similarity for coding agents — a migration runbook needs the exact runbook, not the statistically-closest one."
source: external_research
confidence: 0.75
maturity: draft
uses: 0
successful_uses: 0
harmful_uses: 0
verify_check: "Grep('discovery-keywords', path='.claude/skills') → 1+ matches AND Grep('hybrid-retrieve', path='.claude/memory') → 1+ matches"
---

## Context

Blog post "How Memory Works in a Multi-Agent System: Inside Multica" (mem0 In Context #6) traces Multica's schema — an open-source alternative to Claude Managed Agents with 15.4k GitHub stars.

## Architecture observed

Six tables, all scoped by `workspace_id UUID NOT NULL REFERENCES workspace(id) ON DELETE CASCADE`:

1. `workspace.context` (TEXT) — workspace-wide prompt inherited by all agents
2. `issue` with `context_refs` + `acceptance_criteria` (JSONB) — task unit
3. `agent_task_queue.context` (JSONB) — point-in-time snapshot the daemon reads ONCE; DB stays cold during inference
4. `skill` + `skill_file` + `agent_skill` — reusable capabilities, attached per agent via join table
5. `comment` — threaded working memory, every row has author_type (member|agent) — never ambiguous
6. `activity_log` — append-only audit trail

Skills retrieval is a plain JOIN, not similarity:
```sql
SELECT * FROM skill s
  JOIN agent_skill a_s ON a_s.skill_id = s.id
 WHERE a_s.agent_id = $1
   AND s.workspace_id = $2
```

## Key thesis (direct quote)

> "For coding agents, curated relevance beats learned similarity. A migration runbook needs the exact runbook, not the statistically-closest one. Curation is cheaper than a retrieval miss."

## STOPA correspondence

| Multica pattern | STOPA equivalent |
|---|---|
| Zero embeddings, relational+JSONB | grep-first learnings, BM25 fallback, no default vector store |
| `agent_skill` explicit JOIN | `discovery-keywords:` frontmatter + tag taxonomy |
| `agent_task_queue.context` JSONB snapshot | `state.md` + PRP context packet at orchestrate dispatch |
| `workspace_id` cascade | per-project `.claude/memory/` isolation |
| `author_type` attribution | learning `source:` field (user_correction, critic_finding, etc.) |

## Limitations Multica has (and how STOPA addresses them)

- **No fuzzy recall** → STOPA: synonym fallback + hybrid retrieval (grep + BM25 + graph walk via RRF)
- **Stale snapshots** → STOPA: `/checkpoint` resume + replay-queue for failure validation
- **No cross-workspace memory** → STOPA: `/improve` cross-project routing + `critical-patterns.md` sync
- **Skills rot without discipline** → STOPA: `/evolve` graduation/pruning with counters (uses, harmful_uses, impact_score, confidence decay)

## Do / Don't

**Do:** Keep trusting grep-first + curated discovery for CODING agents. External 15.4k★ evidence shows this is mainstream, not a STOPA quirk.

**Don't:** Add vector embedding store "just in case" — Multica demonstrates production-grade multi-agent works purely relational. The narrative that embeddings are required is infra-driven, not problem-driven.

**When to reconsider:** chat-assistants, product search, research synthesis over >1000 docs — different workloads where Multica explicitly says their approach doesn't fit.

## Reference

- Article: mem0 In Context blog #6
- Repo: https://github.com/multica-ai/multica (15.4k stars as of 2026-04-19)
- Context: mem0 is the commercial sponsor — they pitch their context layer as complement, not replacement. Treat the limitation list as real but mind the vendor bias.
