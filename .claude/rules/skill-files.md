---
globs: "**/skills/*/SKILL.md"
---

# Pravidla pro SKILL.md soubory

- YAML frontmatter musí obsahovat: name, description, user-invocable
- `description` MUST start with "Use when..." — trigger conditions and exclusions ONLY
- `description` MUST NOT summarize the workflow, list steps, or describe internal mechanics
- Why: tested by obra/superpowers — workflow summaries cause Claude to shortcut the description instead of reading full skill body
- Bad: "Multi-persona code review — 6 expert perspectives (Developer, Security, QA...)"
- Good: "Use when reviewing a PR and /critic alone is not thorough enough. Trigger on 'review PR'..."
- `allowed-tools`: least privilege — jen tools které skill skutečně potřebuje
- `deny-tools`: array of tools explicitly DENIED to this skill (overrides allowed-tools). Use for coordinator-pattern skills that must delegate, not execute.
- `permission-tier`: optional, one of `read-only` | `workspace-write` | `full-access` | `coordinator`
  - `read-only`: Read, Glob, Grep, WebFetch, WebSearch only
  - `workspace-write`: read-only + Write, Edit, NotebookEdit, TodoWrite
  - `full-access`: all tools including Bash, Agent (default if omitted)
  - `coordinator`: Read, Glob, Grep, Agent, TodoWrite only — NO Bash/Write/Edit (forces delegation)
- `tags`: array of cross-cutting capability tags for discovery (viz taxonomie níže)
- `requires`: array of runtime dependencies — env vars (UPPER_CASE), CLI tools (lowercase), MCP servers (`mcp:name`)
  - Orchestrátor by měl ověřit dostupnost PŘED spuštěním skillu
  - Vynechej pokud skill nemá žádné externí závislosti
- `supported-os`: array of supported platforms (`windows`, `linux`, `macos`). Vynechej pokud skill funguje všude (default = all)
- Pokud skill zapisuje do memory: musí to být uvedeno v instructions
- Pokud skill spouští sub-agenty: musí specifikovat model (haiku/sonnet/opus) a důvod
- Konvence: anglicky pro technické instrukce, česky pro user-facing texty

## Tag taxonomie (používej konzistentně)

| Tag | Popis |
|-----|-------|
| `code-quality` | Review, linting, refactoring |
| `review` | Explicit review/audit workflow |
| `testing` | Tests, validation, verification |
| `debugging` | Root cause analysis, incident response |
| `research` | Information gathering, analysis |
| `osint` | Open source intelligence, web scraping |
| `web` | Browser automation, web interaction |
| `memory` | Persistent state, learnings, decisions |
| `session` | Checkpoints, handoffs, context management |
| `orchestration` | Multi-step coordination, sub-agents |
| `generation` | AI-generated media (images, video) |
| `media` | Multimedia processing (images, video, audio) |
| `ai-tools` | AI/ML ecosystem tools and prompts |
| `devops` | CI/CD, PRs, issues, deployment |
| `security` | Vulnerability analysis, trust boundaries |
| `dependencies` | Package management, auditing |
| `planning` | Architecture, specs, brainstorming |
| `exploration` | Codebase navigation, search |
| `documentation` | Docs, learnings, knowledge capture |
| `post-edit` | Auto-triggered after code changes |
