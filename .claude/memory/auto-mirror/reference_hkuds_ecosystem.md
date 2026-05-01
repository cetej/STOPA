---
name: HKUDS — STOPA architectural mirror lab
description: Hong Kong University Data Intelligence Lab (Chao Huang) independently converged on STOPA-style architecture across 9 repos (>150k stars). External validation signal — when conflicting evidence arises about STOPA architecture choices, this lab is a reference comparator.
type: reference
originSessionId: 00f5b39f-e83c-4c07-956d-3a247f6e63d5
---
## Lab identity

- **Name**: Data Intelligence Lab @ HKU (HKUDS)
- **PI**: Chao Huang, Assistant Professor, HKU CS + Institute of Data Science
- **Lab site**: https://sites.google.com/view/chaoh
- **GitHub org**: https://github.com/HKUDS (10.4k followers)
- **Focus**: LLMs, autonomous agents, graph learning, RAG

## 9-repo ecosystem (totaling >150k stars, all 2026-04-30 active)

| Repo | Stars | Role | STOPA equivalent |
|------|-------|------|------------------|
| nanobot | 41.3k | Agent engine | Claude Code |
| LightRAG | 34.6k | RAG (EMNLP 2025) | grep+BM25+graph |
| CLI-Anything | 33k | Agent-native CLI | (none) |
| DeepTutor | 22.6k | Learning product (Jan 2026) | (none — domain product) |
| RAG-Anything | 19.4k | All-in-one RAG | grep+BM25+graph |
| DeepCode | 15.3k | Agentic coding | /orchestrate + /tdd |
| OpenHarness | 11.6k | **10-subsystem STOPA mirror** (Apr 2026) | `.claude/` structure |
| ClawTeam | 5k | Agent swarm | farm tier + Teams |
| Vibe-Trading | 3.7k | Finance — 72 skills, 29 swarm presets (Apr 2026) | NG-ROBOT/POLYBOT |

## HKUDS-authored papers on agents

- **AutoAgent: Fully-Automated Zero-Code Framework for LLM Agents** (ACL 2026) — academic basis for runtime skill authoring
- **AI-Researcher: Autonomous Scientific Innovation** (NeurIPS 2025) — possibly seed for multi-agent + skills + memory triad
- **OpenPhone: Mobile Agentic Foundation Models** (ACL 2026) — same template, mobile domain

## Convergent architectural choices (= STOPA validation)

skills as `.md` files, persistent cross-session memory, hooks (PreTool/PostTool), multi-provider routing (13+ providers in Vibe-Trading), permissions/safety modes, MCP integration, multi-agent coordination (DAG swarm), skill CRUD (agents author skills at runtime), session resume + auto-compact, commands subsystem.

## STOPA's distinct choices (NOT in HKUDS — STOPA is more advanced here)

- Per-file YAML learnings with empirical counters (uses, harmful_uses, confidence, maturity, impact_score, valid_until, model_gate, skill_scope)
- Reflexion + replay queue + outcomes for credit assignment
- Cross-project routing (`/improve` + project profiles + GitHub issues)
- RLM operator algebra (ρσιεκ) + commit-invariants safety gates
- Drift discipline (`auto-commit-drift.sh`)
- Scheduled tasks + auto-memory
- Per-skill optstate JSON

## When to consult this memory

- Architectural decision about adding/removing a STOPA subsystem → check if HKUDS has equivalent first
- "Should we replace grep+BM25 with FTS5?" → Vibe-Trading uses FTS5 (simpler, look at their impl)
- "Should we add Default/Auto/Plan permission modes?" → OpenHarness has them, study UX
- "Is the skill-as-`.md`-file approach correct?" → independent convergence answers yes
- New STOPA evolution candidate → check if it would diverge further from HKUDS or converge

Detailed analysis with all 7 divergence points: `.claude/memory/learnings/2026-04-30-hkuds-stopa-architecture-clone-pattern.md` in STOPA repo.
