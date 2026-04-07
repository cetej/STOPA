---
name: My-Brain-Is-Full-Crew
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [mbif-cpr-research, mbif-cpr-implementation-plan]
tags: [orchestration, memory, session, claude-code]
---

# My-Brain-Is-Full-Crew

> Multi-agent orchestration system for Obsidian vault: 8 specialized agents + 13 skills, CLAUDE.md as pure dispatcher ("NEVER RESPOND DIRECTLY"), pull-based chaining, post-it state.

## Key Facts

- Created by gnekt; targets Obsidian vault management (ref: sources/mbif-cpr-research.md)
- CLAUDE.md is a pure router — never answers directly, always routes to skill or agent (ref: sources/mbif-cpr-research.md)
- Pull-based chaining: agent writes `### Suggested next agent`; max depth 3, no agent repeated (ref: sources/mbif-cpr-research.md)
- Post-it state: `Meta/states/{name}.md`, max 30 lines, overwritten each run (ref: sources/mbif-cpr-research.md)
- Least-privilege tools: Seeker = Read/Glob/Grep only; Connector = Read+Edit; Architect = full Bash (ref: sources/mbif-cpr-research.md)
- Architect + Librarian = opus; others = sonnet (ref: sources/mbif-cpr-research.md)
- Agent instructions always in English; description field in user's language (trigger matching) (ref: sources/mbif-cpr-research.md)

## Relevance to STOPA

Pull-based chaining and post-it state are directly adoptable in STOPA. Post-it pattern is already partially adopted (memory/intermediate/). Pure-dispatcher CLAUDE.md is a design philosophy divergent from STOPA's approach — useful reference but not a direct port.

## Mentioned In

- [MBIF vs CPR Research](../sources/mbif-cpr-research.md)
- [MBIF/CPR Implementation Plan](../sources/mbif-cpr-implementation-plan.md)
