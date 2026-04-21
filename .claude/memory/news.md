# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Archived: `news-archive.md`

## Last Scan: 2026-04-20 (arxiv-daily-digest) | Next: ~2026-04-27

**Scan log**: `2026-04-20` — arxiv-daily-digest | Items: 1 action, 4 watch — Context Awareness Gate (arXiv:2411.16133)
**Scan log**: `2026-04-19` — arxiv-daily-digest | Items: 1 action, 4 watch — RL for RAG (arXiv:2510.24652), TEA Protocol, Orchestral AI
**Scan log**: `2026-04-18` — arxiv-daily-digest | Items: 1 action, 4 watch — AgentForge (arXiv:2604.13120), CoMAS
**Scan log**: `2026-04-17` — morning-watch | Items: 3 action — CC Routines, CC Desktop Redesign, Opus 4.7 GA
**Scan log**: `2026-04-17` — arxiv-daily-digest | Items: 1 action, 4 watch — RL Skill Library, Context Kubernetes, MAE
**Scan log**: `2026-04-16` — arxiv-daily-digest | Items: 2 action, 3 watch — Context Engineering Multi-Agent, Smart MAS Middleware
**Scan log**: `2026-04-15` — arxiv-daily-digest | Items: 1 action, 4 watch — Self-Optimizing MAS, CLEAR, Verified Orchestration
**Scan log**: `2026-04-15` — CC-focused | Items: 4 action, 2 watch — Desktop redesign, v2.1.108, PreCompact hook, skill desc 1536
**Scan log**: `2026-04-14` — full scan | Searches: 19 | Items: 6 action, 4 watch, 2 info — CC Analytics GA, DACS, TraceGuard
**Scan log**: `2026-04-13` — morning-watch | Items: 1 watch, 2 info — /team-onboarding, Vertex AI wizard, effort param GA
**Scan log**: `2026-04-12` — full scan | Fetches: 3 | Items: 3 action, 3 watch, 4 info — Advisor Tool beta, CC Monitor, Hermes v0.8.0

## Actionable Rate

**Current: 14/27 = 51.9%** | Target: 50% REACHED | Baseline (2026-04-14): 5/27 = 18.5%
Formula: `python scripts/actionable-rate.py`

## Passes Rate (Harness Adoption)

**Baseline (2026-04-19):** 0/8 projects adopted | **Target:** >=2 projects + >=30% pass rate by 2026-05-17
Formula: `python scripts/passes-rate.py`

## Action Items (Open)

| # | Item | Urgency | Next Step |
|---|------|---------|-----------|
| 117 | **Batches API 300k max_tokens cap** (beta `output-300k-2026-03-24`, Opus/Sonnet 4.6) | MED | NG-ROBOT: acted, decision NE migrovat (viz ng-robot-batches-migration.md) |
| 111 | **Harness adoption pilot** — multi-session harness resurrected (commit 8fafe19). 0/8 projects. | MED | Run `/project-init <target> --harness` on NG-ROBOT or ZACHVEV |
| 109 | **CC Plugin monitors manifest key** — background monitoring v pluginech | HIGH | Evaluovat pro stopa-orchestration plugin |
| 110 | **Fine-grained tool streaming GA** — event-level streaming | MED | Vyuzit v Claude API integracich, NG-ROBOT |
| 105 | **CC Desktop redesign** — sidebar, terminal+editor, HTML/PDF preview, routines | HIGH | Otestovat novy workspace |
| 100 | **Meta Muse Spark** — Meta frontier model, Contemplating mode | MED | Pridat do /eval tier srovnani |
| 74 | **Claude Sonnet 5** — postupny rollout | MED | Prepnout model tiers az dostupny |
| 96 | **Prompt caching auto-placement** | MED | Zjednodusit NG-ROBOT caching |
| 97 | **Compaction API (beta)** | MED | Evaluovat pro /compact backend |
| 84 | **Claude Managed Agents (Public Beta)** | MED | Evaluovat jako alternativu |
| 86 | ant CLI | LOW | Sledovat az GA |
| 98 | **OpenClaw extra cost** | LOW | Sledovat pricing |
| 65 | CC forceRemoteSettingsRefresh | LOW | Sledovat pri distribuci |
| 42 | CC Voice Mode — Czech included | MED | Otestovat az dostupny |
| 44 | CC HTTP hooks | PARKED | Adopt pri remote agents |

## Recent Findings (Apr 15-20)

| Date | Type | Item | Priority | Acted |
|------|------|------|----------|-------|
| 2026-04-20 | ACTION | Context Awareness Gate (arXiv:2411.16133) — gate pro podminene spousteni RAG; hybridretrieve.py | high | No |
| 2026-04-19 | ACTION | RL for RAG (arXiv:2510.24652) — RL retrieval optimization; hybrid-retrieve.py | high | No |
| 2026-04-18 | ACTION | AgentForge (arXiv:2604.13120) — Planner/Coder/Tester/Debugger/Critic + Docker, 40% SWE-bench | high | No |
| 2026-04-17 | ACTION | CC Routines — cloud-side automations; alternativa k STOPA scheduled-tasks | high | No |
| 2026-04-17 | ACTION | CC Desktop Redesign — parallel sessions, drag-drop layout, terminal, diff viewer | high | No |
| 2026-04-17 | ACTION | Claude Opus 4.7 GA — 3x visual resolution, xhigh reasoning, Task Budgets, $5/$25 | high | No |
| 2026-04-17 | ACTION | RL Skill Library (arXiv:2512.17102) — RL agent buduje skill library bez supervisora | high | No |
| 2026-04-16 | ACTION | Context Engineering Multi-Agent (arXiv:2603.09619) — taxonomie pro STOPA skills | high | No |
| 2026-04-16 | ACTION | Smart MAS Middleware (arXiv:2604.03430) — middleware pro koordinaci agentu paralelne | high | No |
| 2026-04-15 | ACTION | Self-Optimizing MAS (arXiv:2604.02988) — self-play prompt optimization pro STOPA self-evolve | high | Yes |
| 2026-04-20 | WATCH | SE Benchmarks Survey (arXiv:2510.09721) | medium | No |
| 2026-04-20 | WATCH | Context Matters ADR (arXiv:2604.03826) — context engineering > model scaling (validated) | medium | No |
| 2026-04-19 | WATCH | TEA Protocol (arXiv:2506.12508) — Tool-Environment-Agent s explicitnim lifecyclem | medium | No |
| 2026-04-19 | WATCH | Orchestral AI (arXiv:2601.02577) — modularni orchestrace vyvazujici debuggability | medium | No |
| 2026-04-19 | WATCH | Hierarchical RAG (arXiv:2604.14166) — hierarchicke vrstveni RAG | medium | No |
| 2026-04-18 | WATCH | CoMAS (arXiv:2510.08529) — agenti se zlepsují RL z meziagenturnich interakci | medium | No |
| 2026-04-17 | WATCH | Context Kubernetes (arXiv:2604.11623) — deklarativni sprava kontextu cross-platform | medium | No |
| 2026-04-17 | WATCH | MAE Self-Improve (arXiv:2510.23595) — Proposer-Solver-Judge loop | medium | No |
| 2026-04-16 | WATCH | Adaptive Orchestration MoE (arXiv:2601.09742) | medium | No |
| 2026-04-16 | WATCH | MCP Planner-Executor (arXiv:2604.07681) | medium | No |
| 2026-04-15 | WATCH | CLEAR (arXiv:2604.07487) — kontrastivni porovnani rolloutu | medium | No |
| 2026-04-15 | WATCH | Verified Orchestration (arXiv:2603.11445) — DAG s verification-driven koordinaci | medium | No |

## Watch List (Ongoing)

### Models & Releases
| Item | Detail | Trigger |
|------|--------|---------|
| Mythos/Capybara | Training dokoncen, piloting (2026-04-03). Step change coding+reasoning. | GA datum — preplanovat STOPA model tiers |
| Claude Sonnet 5 #74 | Postupny rollout — ceka na account access | Prepnout tiers az dostupny |
| Gemini CLI #75 | Apache 2.0, ReAct loop, MCP support, 1M context. Direct competitor. | Sledovat adopci |
| Gemma 4 #61 | 4 modely (2B-31B), Apache 2.0, vision+reasoning | Open-weight alternativa |

### Agent/Tool Research (active)
| Item | Detail |
|------|--------|
| Meta-Harness #73 | MEDIAN traces: 50.0 vs scores-only: 34.6 (+15 pts). /eval musi reportovat median; /orchestrate pridat tool inventory P1 |
| agent-browser #70 | CLI pro agenty: snapshot-refs-act, Rust daemon, CDP. npm install -g agent-browser |
| Hermes Agent v0.8.0 #96 | 40K+ stars, persistent memory, auto-generated skills, cross-platform, MCP OAuth 2.1 |
| Memory Intelligence Agent arXiv:2604.04503 | Cache + memory layers blizke STOPA MemPalace |
| DACS #102 acted | Registry-Focus context switching, 3.53x efficiency — implementovat v orchestrate pro >3 agenty |
| TraceGuard #103 acted | 5D CoT monitoring — upgrade /critic na 5D |
| MCP Toolbox for DBs #71 | 30+ DB (PostgreSQL, MongoDB, Redis), NL2SQL. Trigger: POLYBOT/MONITOR DB layer |
| Colab MCP Server #76 | Google Colab runtime s GPU pro agenty. Kandidat: POLYBOT inference |

## Weekly Digest 2026-04-13

**Aktivita:** STOPA 10 commitu (deterministic gates, workspace validator). NG-ROBOT 10 commitu (pipeline fix, SEO). ADOBE 10 commitu (IDML Track Changes, DOCX export).
**Novinky:** Advisor Tool beta, Mythos/Capybara piloting. CC v2.1.94->v2.1.101 za tyden.
**Pouceni:** 34 novych learnings (Apr 5-8) — deception pod tlakem, auto-research, iterative refinement.

Older digests: see news-archive.md
