# Skill Tiers — Progressive Disclosure

Skills are organized into 4 tiers by frequency of use. This helps Claude prioritize which skills to suggest.

## Tier 1 — Core (always suggest when relevant)
Daily-use skills that should be triggered proactively:
- `/triage` — task routing: STOPA vs project vs both (run before orchestrate when unsure)
- `/orchestrate` — multi-step task decomposition
- `/scout` — codebase exploration before changes
- `/critic` — quality review after edits
- `/checkpoint` — session state management
- `/scribe` — decision and learning capture
- `/status` — system state dashboard (task, budget, checkpoint, health)

## Tier 2 — Extended (suggest when task matches)
Specialized skills for specific workflows:
- `/fix-issue` — GitHub issue resolution
- `/autofix` — PR CI failure & review comment fixer (cloud or local)
- `/deepresearch` — multi-agent evidence-based research with citations
- `/peer-review` — adversarial review of research artifacts and documents
- `/brainstorm` — spec refinement from vague ideas
- `/prp` — context packet for handoffs
- `/handoff` — capture findings from completed/remote sessions into persistent memory
- `/verify` — end-to-end proof of correctness
- `/harness` — deterministic pipelines
- `/security-review` — vulnerability analysis
- `/dependency-audit` — outdated/risky packages
- `/incident-runbook` — failure diagnosis
- `/scenario` — edge case & failure mode explorer (pre-implementation)
- `/liveprompt` — live community prompt intelligence (what works RIGHT NOW for a topic)
- `/autoreason` — adversarial debate loop for subjective text improvement (SHL0MS-inspired)
- `/autoresearch` — experimental code iteration with measurable outcomes (Claudini-inspired)
- `/autoharness` — auto-generate validators from observed failure patterns (AutoHarness-inspired)
- `/eval` — grade and replay harness JSONL traces, detect regressions, compare harness configurations
- `/build-project` — end-to-end autonomous project builder from requirements
- `/fetch` — clean URL reader via Jina Reader (no API key, no browser needed)
- `/radar` — proactive tool discovery & evaluation (auto-scan 2x/day + manual URL input)

## Tier 3 — Advanced (only on explicit request)
Generative/creative tools and meta-skills:
- `/nano` — image generation (requires FAL_KEY)
- `/klip` — video generation (requires FAL_KEY)
- `/skill-generator` — create/modify skills
- `/autoloop` — iterative optimization
- `/project-init` — new project setup
- `/watch` — ecosystem news scan
- `/sweep` — post-session entropy cleanup (stale docs, dead code, contradictions)
- `/compact` — context compaction (save results to disk, auto-summarize with Haiku)
- `/budget` — cost tracking
- `/browse` — Chrome automation
- `/youtube-transcript` — video transcripts
- `/self-evolve` — adversarial co-evolution loop for skill improvement (Agent0-inspired)

## Tier 4 — Methodology (suggest when development discipline matters)
Engineering methodology skills inspired by superpowers patterns:
- `/tdd` — RED-GREEN-REFACTOR enforcer for test-driven development
- `/systematic-debugging` — 4-phase root cause methodology (no guessing)

## Lifecycle Phase Mapping (alternative to tier browsing)

Skills mapped to SDLC phases. Use `phase:` in frontmatter for each skill.

| Phase | Popis | Skills |
|-------|-------|--------|
| `define` | Routing, klasifikace, porozumění | triage, brainstorm, council |
| `plan` | Dekompozice, explorace, architektura | orchestrate, scout, scenario, prp, project-init, build-project |
| `build` | Implementace, generace, exekuce | tdd, fix-issue, autofix, autoloop, autoresearch, nano, klip, browse, fetch |
| `verify` | Testování, důkaz, validace | verify, critic, harness, eval, security-review, dependency-audit, autoharness |
| `review` | Retrospektivní kvalita, peer audit | peer-review, pr-review, autoreason, self-evolve, sweep |
| `ship` | Deployment, handoff, cleanup | checkpoint, handoff, compact |
| `meta` | Introspekce, evoluce, budget | status, budget, scribe, evolve, skill-generator, radar, watch, liveprompt, xsearch, deepresearch, seo-audit, youtube-transcript, incident-runbook, systematic-debugging, project-sweep |

### Using phases for skill selection
1. Identifikuj fázi uživatelova úkolu (define → ship)
2. Filtruj skills v dané fázi
3. Cross-referencuj s tier (Tier 1 first)
4. Upřesni přes tags

## Tag-Based Discovery (alternative to tier browsing)

Every skill has `tags:` in frontmatter. Use tags to find skills by capability instead of tier:

| Need | Tags to search | Top matches |
|------|---------------|-------------|
| Code quality | `code-quality`, `review` | critic, verify, tdd, self-evolve, autoreason, sweep |
| Research | `research`, `osint` | deepresearch, scout, liveprompt, watch, radar |
| Testing | `testing` | verify, harness, eval, tdd, scenario |
| Debugging | `debugging` | systematic-debugging, incident-runbook |
| Session mgmt | `session`, `memory` | checkpoint, handoff, compact, scribe |
| DevOps/PRs | `devops` | fix-issue, autofix, pr-review, harness |
| Planning | `planning` | orchestrate, brainstorm, scenario, build-project |
| Security | `security` | security-review, dependency-audit |
| Media gen | `generation`, `media` | nano, klip |
| Web/OSINT | `web`, `osint` | fetch, browse, seo-audit, deepresearch, watch |

### Pre-flight: `requires` check
Skills with `requires:` in frontmatter need external dependencies:
- `FAL_KEY` → nano, klip
- `gh` CLI → fix-issue, autofix, pr-review
- `mcp:claude-in-chrome` → browse

Orchestrátor by měl ověřit dostupnost PŘED spuštěním skillu.

## How to Apply

When the user describes a task:
1. Check Tier 1 skills first — these cover 80% of workflows
2. If task is specialized, suggest the matching Tier 2 skill
3. Only mention Tier 3 skills when user explicitly asks or when the specific capability is clearly needed
4. Suggest Tier 4 skills when user is debugging (→ /systematic-debugging) or implementing with tests (→ /tdd)
5. **Tag search**: if no tier match, grep `tags:` across skills for the user's need
6. Never list all skills unprompted — suggest 1-2 most relevant ones
