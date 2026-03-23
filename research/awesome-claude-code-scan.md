# Awesome Claude Code Scan — 2026-03-23

Source: https://github.com/hesreallyhim/awesome-claude-code
Scanned: 30+ repos, 100+ projects across 9 categories

## Tier 1: Okamžitý dopad, nízký effort

| # | Co | Zdroj | Stars |
|---|---|---|---|
| 1 | Status line (ccstatusline) | sirmalloc/ccstatusline | 3.4k |
| 2 | PostToolUse lint hook (ruff) | disler/claude-code-hooks-mastery | 3.4k |
| 3 | PermissionRequest hook (auto-approve read-only) | disler/hooks-mastery | 3.4k |
| 4 | PreCompact hook (auto-checkpoint) | disler/hooks-mastery | 3.4k |
| 5 | Structured exit token v /autoloop | frankbria/ralph-claude-code | 8.1k |

## Tier 2: Vysoký dopad, střední effort

| # | Co | Zdroj | Stars |
|---|---|---|---|
| 6 | /fix-issue (GitHub issue → fix → testy → commit) | awesome-cc slash-commands | — |
| 7 | /pr-review (6-persona sekvenční review) | awesome-cc slash-commands | — |
| 8 | /brainstorm (Socratic spec refinement) | obra/superpowers | 107k |
| 9 | Circuit breaker by change-detection | frankbria/ralph | 8.1k |
| 10 | Hierarchická context injection pro sub-agenty | spec-workflow | 3.6k |

## Tier 3: Strategické

| # | Co | Zdroj | Stars |
|---|---|---|---|
| 11 | Progressive disclosure pro skills (3-tier loading) | wshobson/agents | 32k |
| 12 | /prp (AI-optimized task context packet) | create-prp command | — |
| 13 | Security review skill (trust boundary) | evaluate-repository | — |
| 14 | Multi-agent observability dashboard | disler/hooks-observability | 1.3k |
| 15 | Token optimization via ccusage MCP server | ryoppippi/ccusage | — |

## Tier 4: Nice-to-have

| # | Co | Zdroj |
|---|---|---|
| 16 | /tdd (RED-GREEN-REFACTOR enforcer) | obra/superpowers |
| 17 | model: field v skill frontmatter | wshobson/agents |
| 18 | Validation output contract v python-files.md | claude-code-mcp-enhanced |
| 19 | Cross-tool sync (symlinks) | EveryInc |
| 20 | claude-esp pro sub-agent visibility | phiat/claude-esp |

## Key Orchestrator Competitors

| Repo | Stars | Klíčová diferenciace |
|---|---|---|
| Claude Code Flow | 23.3k | Byzantine consensus, vector memory, MoE routing |
| Claude Task Master | 26.1k | PRD parsing, multi-model, editor integration |
| Auto-Claude | 13.5k | Kanban UI, AI merge conflict resolution |
| Claude Squad | 6.5k | Multi-model (Claude+Codex+Gemini), tmux sessions |
| Ralph (frankbria) | 8.1k | Dual-condition exit, change-detection circuit breaker |
| superpowers | 107k | Auto-triggered skills, Socratic brainstorm, TDD |
| wshobson/agents | 32k | 72 plugins, progressive disclosure, semantic revert |

## Co STOPA má a konkurence NE

- Goal-backward verification (L1-L4)
- Deviation rules (fix max 3×, STOP na architektuře)
- Budget tiers s approval gates
- Harness engine pro deterministic pipelines
- Plugin marketplace distribuce

## Architektonický insight

Většina konkurence = task scheduling + paralelismus.
STOPA = goal-backward reasoning + verification gates.
Vylepšení by měla posilovat tuto filozofii, ne nahrazovat ji.
