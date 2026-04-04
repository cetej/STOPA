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
- `constrained-tools`: optional dict mapping tool name → array of allowed invocation patterns (glob syntax). When a tool is both in `allowed-tools` AND in `constrained-tools`, it's allowed but ONLY with matching patterns. Inspired by Google MCP Toolbox "structured queries" pattern — agents access tools only through approved operation shapes.
  - Example: `constrained-tools: {Bash: ["python *", "git diff*", "ruff *"]}`
  - Semantics: Bash is allowed, but only commands matching the glob patterns
  - Enforced at runtime by `tool-gate.py` PreToolUse hook (STOPA_TOOL_GATE=enforce)
  - Currently supported: Bash command matching. Future: Write/Edit path matching
- `tags`: array of cross-cutting capability tags for discovery (viz taxonomie níže)
- `phase`: lifecycle phase — one of `define` | `plan` | `build` | `verify` | `review` | `ship` | `meta`
  - `define` — routing, klasifikace, porozumění požadavkům (triage, brainstorm, council)
  - `plan` — dekompozice, explorace, architektura (orchestrate, scout, scenario)
  - `build` — implementace, generace, exekuce (tdd, fix-issue, nano, klip)
  - `verify` — testování, důkaz, validace (verify, critic, harness, eval)
  - `review` — retrospektivní kvalita, peer audit (peer-review, pr-review, autoreason)
  - `ship` — deployment, handoff, cleanup (checkpoint, handoff, sweep)
  - `meta` — introspekce, evoluce, budget (status, budget, scribe, watch)
  - Skill s více fázemi použije PRIMARY fázi. Sekundární fáze vyjádří přes `tags:`
- `requires`: array of runtime dependencies — env vars (UPPER_CASE), CLI tools (lowercase), MCP servers (`mcp:name`)
  - Orchestrátor by měl ověřit dostupnost PŘED spuštěním skillu
  - Vynechej pokud skill nemá žádné externí závislosti
- `supported-os`: array of supported platforms (`windows`, `linux`, `macos`). Vynechej pokud skill funguje všude (default = all)
- `effort`: `low` | `high` | `auto`. When `auto`: orchestrator uses progressive skill withdrawal (SKILL0-inspired Dynamic Curriculum). First invocation in session loads full `SKILL.md`, subsequent invocations load `SKILL.compact.md` if it exists. This reduces token overhead by ~80% on repeat invocations within a session.

## Compact Skill Variants (SKILL0-inspired Dynamic Curriculum)

Skills MAY have a `SKILL.compact.md` alongside `SKILL.md`. The compact variant contains:
- Core purpose and role (1-2 sentences)
- Decision points and critical rules (condensed tables)
- Circuit breakers and anti-patterns (abbreviated)
- Output format expectations

The compact variant does NOT contain:
- Full phase descriptions or step-by-step workflows
- Detailed examples or reference file reads
- Extended tables, scoring rubrics, or templates
- Anti-Rationalization Defense (covered in first invocation)

### Progressive Withdrawal Protocol (per session)

| Invocation | What loads | Token estimate |
|-----------|-----------|---------------|
| 1st | Full `SKILL.md` | ~5-7K tokens |
| 2nd+ | `SKILL.compact.md` (if exists) | ~500-800 tokens |
| Explicit `--full` | Always full `SKILL.md` | ~5-7K tokens |

**Rules:**
- Compact variant MUST preserve all circuit breakers and hard stops
- If compact variant doesn't exist, always load full SKILL.md
- User can force full version with `--full` flag
- Session-scoped: new session resets to full version
- The `variant: compact` field in frontmatter identifies compact files
- Compact files are NOT synced to commands/ (they're skill-internal optimization)
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

## Skill Body Sections (za workflow, před Rules)

Tři sekce pro obranu proti shortcuttování a ověření kvality. Pořadí: Anti-Rationalization → Red Flags → Verification Checklist → Rules.

### Anti-Rationalization Defense

Heading: `## Anti-Rationalization Defense`

Standardizovaný formát tabulky (VŠECHNY skills MUSÍ použít tyto sloupce):

```markdown
| Rationalization | Why Wrong | Do Instead |
|---|---|---|
| "I'll skip X because..." | Faktická odpověď proč je to špatně | Imperativní akce co dělat místo toho |
```

Pravidla:
- Min 3, max 10 řádků
- Sloupec 1: vždy citovaná first-person fráze (co agent říká sám sobě)
- Sloupec 2: jedna věta, faktická — proč je to špatně
- Sloupec 3: imperativní akce — co dělat místo toho
- Umístění: za hlavní workflow, před Red Flags
- Existující skills s variant headers (`Temptation`, `Reality`, `Required Action`) migrují na standard při příštím editu
- Odlišné od Red Flags: rationalizations = interní reasoning traps, red flags = externí pozorovatelné symptomy

### Red Flags

Heading: `## Red Flags`

Pozorovatelné symptomy špatného použití skillu:

```markdown
STOP and re-evaluate if any of these occur:
- Observable symptom phrased as gerund or "Doing X without Y"
- Another observable symptom
```

Pravidla:
- Min 3, max 7 flagů
- Každý flag = pozorovatelný vzor chování, ne teoretický problém
- Formulace: gerund ("Skipping tests") nebo "Doing X without Y"
- Umístění: za Anti-Rationalization, před Verification Checklist

### Verification Checklist

Heading: `## Verification Checklist`

Exit criteria před prohlášením "hotovo" — odlišné od Output Format (template výstupu ≠ exit criteria):

```markdown
- [ ] Specific verifiable criterion with evidence requirement
- [ ] Another criterion referencing concrete output (test results, tool output)
```

Pravidla:
- Min 3, max 8 položek
- Každá objektivně ověřitelná — ne "seems right", ale "these tests pass"
- Položky referencují konkrétní výstupy (test results, build output, grep results)
- Umístění: za Red Flags, před Rules

### Required Sections by Tier

| Sekce | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|-------|--------|--------|--------|--------|
| Anti-Rationalization Defense | REQUIRED | REQUIRED | RECOMMENDED | REQUIRED |
| Red Flags | REQUIRED | OPTIONAL | OPTIONAL | OPTIONAL |
| Verification Checklist | REQUIRED | OPTIONAL | OPTIONAL | OPTIONAL |
| `phase:` frontmatter | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
