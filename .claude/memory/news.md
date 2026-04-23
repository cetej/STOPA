# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Archived: `news-archive.md`

## Last Scan: 2026-04-23 (morning-watch) | Next: ~2026-04-30

**Scan log**: `2026-04-21` — full scan | Items: 7 action, 5 watch, 4 info — CC hooks expansion, Google ADK, Agent resume breaking change, context engineering moat
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

**Current (2026-04-21):** 1/8 projects adopted | 11/15 features pass (73.3%)
**Baseline (2026-04-19):** 0/8 projects adopted | **Target:** >=2 projects + >=30% pass rate by 2026-05-17
Formula: `python scripts/passes-rate.py`

**Adopted:**
- NG-ROBOT (2026-04-21, commit 10a8d0e) — 15 features: 11 done / 3 in_progress (F012 Studio Video, F013 TTS unification, F014 INBOX audit) / 1 planned (F015 Phase 7b SEO)

**Next candidates:** ZACHVEV (active social analysis), POLYBOT (prediction markets), MONITOR (OSINT).

## Action Items (Open)

| # | Item | Urgency | Next Step |
|---|------|---------|-----------|
| 111 | **Harness adoption pilot** — NG-ROBOT adopted 2026-04-21 (commit 10a8d0e, 11/15=73.3%). 1/8 projects. | MED | Replicate on ZACHVEV or POLYBOT; reach target 2+ projects by 2026-05-17 |
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
| 112 | **Agent `resume` param removed** — Breaking: Agent() resume param gone, must use SendMessage() | DONE | STOPA skills zkontrolovany (grep cisty) — nulovy dopad |
| 113 | **CC /ultrareview** — cloud parallel multi-agent code review command | MED | Evaluovat jako heavy-tier backend pro /critic skill |
| 114 | **CC 7 novych hook events** — CwdChanged, FileChanged, TaskCreated, PostCompact, StopFailure, PermissionDenied, Elicitation | MED | Aktualizovat event list v behavioral-genome.md; StopFailure handler pro STOPA |
| 115 | **CC PowerShell Tool (Windows preview)** — CLAUDE_CODE_USE_POWERSHELL_TOOL opt-in | MED | Otestovat na Windows — potencialni nahrada Bash pro Windows-native ops |
| 116 | **Google ADK** (google/adk-python) — 8200+ stars, multi-agent Python framework | MED | Evaluovat vs STOPA architektura — overit jestli uz pokryto v ADR 0016 Phase B |
| 117 | **max_tokens 300k Batches API** — Opus 4.6 + Sonnet 4.6, beta header output-300k-2026-03-24 | DEFER | NG-ROBOT potvrzen jako pokracujici (ADR 0016 Phase D: 20% sunset H2 2027). Odlozit AZ po OCR migraci (GLM-OCR, immediate priority #1). |
| 118 | **Context Engineering as AI Moat** (Harrison Chase) — 5 patterns: trace observability, state mgmt, external memory, HITL, sleep-time compute | MED | Chase 5-pattern gap analysis vs STOPA — preverit prekryv s ADR 0016 MemoryBackend |

## Recent Findings (Apr 21)

| Date | Type | Item | Priority | Acted |
|------|------|------|----------|-------|
| 2026-04-21 | ACTION | Agent `resume` param removed (breaking) — SendMessage() jedina cesta | high | Yes (grep 0 matches) |
| 2026-04-21 | ACTION | CC /ultrareview — cloud multi-agent code review | med | No |
| 2026-04-21 | ACTION | CC 7 novych hooks: CwdChanged, FileChanged, TaskCreated, PostCompact, StopFailure, PermissionDenied, Elicitation | med | No |
| 2026-04-21 | ACTION | CC PowerShell Tool — Windows opt-in preview (CLAUDE_CODE_USE_POWERSHELL_TOOL) | med | No |
| 2026-04-21 | ACTION | Google ADK (google/adk-python) — 8200+ stars | med | No (check ADR 0016 Phase B) |
| 2026-04-21 | ACTION | Harrison Chase: Context Engineering as AI Moat — 5 patterns | med | No (check vs ADR 0016) |
| 2026-04-21 | ACTION | max_tokens 300k Batches API (Opus 4.6/Sonnet 4.6) | low | No (check NG-ROBOT obsolescence) |
| 2026-04-21 | WATCH | CC /ultraplan — cloud planning sessions | med | No |
| 2026-04-21 | WATCH | arXiv:2604.04990 Architecture Without Architects | med | No |
| 2026-04-21 | WATCH | arXiv:2604.12843 Growing Pains Benchmarking — 100 anchor questions | med | No |
| 2026-04-21 | WATCH | Simon Willison LLM library: server-side tool execution | med | No |
| 2026-04-21 | WATCH | transformers v5.5.0: TimesFM 2.5, VibeVoice ASR | med | No |
| 2026-04-21 | INFO | Claude Mythos Preview gated (Project Glasswing, invite-only) | low | No |
| 2026-04-21 | INFO | /less-permission-prompts oficialni CC command | low | No |
| 2026-04-21 | INFO | Qwen3.6-35B lepsi nez Opus 4.7 na vizualech | low | No |
| 2026-04-21 | INFO | SWE-Bench-Verified data leakage concern (arXiv:2512.10218) | low | No |

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

## 2026-04-21 Morning Scan

| # | Item | Summary | Action |
|---|------|---------|--------|
| #104 | CC Routines | Saved CC konfigurace (prompt + repos + connectors) spustitelné na Anthropic cloud i bez laptopu | Prozkoumat pro STOPA scheduled tasks |
| #105 | Claude Opus 4.7 GA | Nejsilnější GA model — 1M kontext, 2576px obr., task budgets, $5/$25 (stejné jako 4.6) | Aktualizovat STOPA model tiers |
| #106 | Compaction API + auto-caching | Compaction API beta (server-side summarization), auto prompt caching bez manuálních breakpointů | Zvážit pro dlouhé STOPA sessions |

## 2026-04-22 arXiv Daily Digest

| Date | Type | Item | Urgency | Acted | Source |
|------|------|------|---------|-------|--------|
| 2026-04-22 | [ACTION] | Self-Optimizing Multi-Agent Systems for Deep Research (arXiv:2604.02988) — agents self-play to autonomously explore prompt combinations, eliminating hand-engineered prompts in deep research workflows | high | No | arxiv-daily-digest |
| 2026-04-22 | [WATCH] | Small Model as Master Orchestrator (arXiv:2604.17009) — unifies multi-agent collaboration and tool-use into a single learnable action space with parallel subtask decomposition | medium | No | arxiv-daily-digest |
| 2026-04-22 | [WATCH] | CoCR-RAG: Concept-oriented Context Reconstruction (arXiv:2603.23989) — distills Abstract Meaning Representation concepts to reconstruct unified context for multi-source RAG fusion | medium | No | arxiv-daily-digest |
| 2026-04-22 | [WATCH] | AgentForge: Execution-Grounded Multi-Agent Framework for Software Engineering (arXiv:2604.13120) — Planner/Coder/Tester/Debugger/Critic agents with Docker sandbox achieve 40% SWE-bench Lite | medium | No | arxiv-daily-digest |
| 2026-04-22 | [WATCH] | Adaptive Orchestration: Scalable Self-Evolving Multi-Agent Systems (arXiv:2601.09742) — Dynamic Mixture of Experts (DMoE) for scalable self-evolving orchestration without manual reconfiguration | medium | No | arxiv-daily-digest |

## 2026-04-22 Morning Watch

| # | Item | Summary | Action |
|---|------|---------|--------|
| #107 | CC Ultraplan preview | Cloud plan drafting z CLI, review v web editoru, remote run nebo pull back local — nová hybridní orchestrace | Prozkoumat pro STOPA remote scheduled tasks |
| #108 | CC /resume 67% rychlejší | Velké session (40MB+) se resumují výrazně rychleji; /tui fullscreen, mobile push notifications, session recap | Benefit pro dlouhé STOPA sessions |
| #109 | API data residency (inference_geo) | Nový parametr inference_geo pro US-only inference za 1.1× cenu; dostupný pro modely po 2026-02-01 | Sledovat pro compliance-sensitive projekty |

## 2026-04-23 arXiv Daily Digest

| Date | Type | Item | Urgency | Acted | Source |
|------|------|------|---------|-------|--------|
| 2026-04-23 | [ACTION] | Principled Context Engineering for RAG: Statistical Guarantees via Conformal Prediction (arXiv:2511.17908) — applies conformal prediction post-retrieval to guarantee evidence coverage while reducing context size 2-3×; directly implementable for STOPA hybrid retrieval | high | No | arxiv-daily-digest |
| 2026-04-23 | [WATCH] | Safe and Policy-Compliant Multi-Agent Orchestration for Enterprise AI (arXiv:2604.17240) — CAMCO models multi-agent decision-making as constrained optimization, adding runtime policy compliance layer to orchestration | medium | No | arxiv-daily-digest |
| 2026-04-23 | [WATCH] | The Single-Multi Evolution Loop for Self-Improving Model Collaboration (arXiv:2602.05182) — self-play loop where single-model and multi-model phases alternate to continuously improve collaboration quality | medium | No | arxiv-daily-digest |
| 2026-04-23 | [WATCH] | Scaling Multi-Agent Systems: A Smart Middleware for Improving Agent Interactions (arXiv:2604.03430) — middleware layer that optimizes inter-agent communication patterns and reduces coordination overhead at scale | medium | No | arxiv-daily-digest |
| 2026-04-23 | [WATCH] | Context Kubernetes: Declarative Orchestration of Enterprise Knowledge for Agentic AI (arXiv:2604.11623) — reference architecture treating enterprise knowledge as declaratively managed resources with explicit lifecycle and versioning | medium | No | arxiv-daily-digest |

## 2026-04-23 Morning Watch

| # | Item | Summary | Action |
|---|------|---------|--------|
| #110 | CC odstraněn z Pro (test) | Anthropic testoval odstranění CC z $20/měs Pro pro ~2% nových uživatelů (2026-04-22); existující Pro/Max nejsou ovlivněni; min. tier s CC = Max 5× za $100/měs | Sledovat — může ovlivnit STOPA pricing doporučení |
| #111 | Claude Cowork GA | Cowork obecně dostupný na macOS+Windows v Claude Desktop; nová Analytics API + SCIM správa skupin s vlastními rolemi | Prozkoumat Analytics API pro STOPA usage monitoring |
| #112 | CC prompt caching controls | Nové ovládání cache: 1-hodinový cache + vynucený 5-minutový; Skill tool získal přístup k built-in slash commands | Relevant pro STOPA session optimization |
