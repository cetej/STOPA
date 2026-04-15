# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Archived: `news-archive.md`

## Last Scan: 2026-04-15 (quick CC-focused) | Next: ~2026-04-22

**Scan log**: `2026-04-15` — scheduled morning-watch | Searches: 2 | Items: 2 action — CC plugin monitors manifest key (#109), fine-grained tool streaming GA (#110)
**Scan log**: `2026-04-15` — CC-focused | Searches: 5 | Fetches: 4 | Items: 4 action, 2 watch — Desktop redesign, v2.1.108 recap+caching, PreCompact hook, skill desc cap 250→1536
**Scan log**: `2026-04-14` — full scan | Searches: 19 | Items: 6 action, 4 watch, 2 info — CC Analytics API GA, Meta Muse Spark (Contemplating mode), DACS paper (3.53× context efficiency), TraceGuard 5D CoT, PwC→HF Trending, Agent SDK additionalDirectories
**Scan log**: `2026-04-14` — scheduled morning-watch | Searches: 2 | Items: 3 action — prompt caching auto, compaction API beta, OpenClaw extra cost
**Scan log**: `2026-04-13` — scheduled morning-watch | Searches: 2 | Items: 1 watch, 2 info — /team-onboarding command, Vertex AI setup wizard, effort param GA
**Scan log**: `2026-04-12` — full scan | Searches: 12 | Fetches: 3 | Items: 3 action, 3 watch, 4 info

## Actionable Rate

**Baseline (2026-04-14):** 5/27 = 18.5% → **Current: 14/27 = 51.9%** | Target: 50% ✅ REACHED
**Resolved items:** 12/12 = 100% (by definition — resolved = acted)

Formula: `actionable_rate = items_with_acted_yes / total_active_items`
Run `python scripts/actionable-rate.py` for current calculation.

## Action Items

<!-- Acted: yes = reálná akce (commit, learning, decision, config change). no = dosud ne. -->

| # | Item | Urgency | Acted | Evidence | Next Step |
|---|------|---------|-------|----------|-----------|
| 109 | **CC Plugin `monitors` manifest key** — Background monitoring v pluginech přes top-level `monitors` klíč v manifestu; auto-arms při startu session nebo invoke skillu | HIGH | no | — | Evaluovat pro stopa-orchestration plugin — background monitoring skills |
| 110 | **Fine-grained tool streaming GA** — Dostupné na všech modelech bez beta headeru; event-level streaming tool calls | MED | no | — | Využít v Claude API integracích, NG-ROBOT pipeline monitoring |
| 105 | **CC Desktop redesign** — sidebar pro multi-session, built-in terminal+editor, HTML/PDF preview, drag&drop panes, routines | HIGH | no | — | Otestovat nový workspace; routines = /loop GUI ekvivalent |
| 106 | **CC v2.1.108 — `/recap` + 1h prompt cache** — `/recap` obnoví kontext session; `ENABLE_PROMPT_CACHING_1H` env var pro 1h TTL; model invokuje slash commands přes Skill tool | HIGH | **yes** | settings.json: ENABLE_PROMPT_CACHING_1H=1, CLAUDE_CODE_ENABLE_AWAY_SUMMARY=1 | /recap = krátkodobé přerušení, /checkpoint = mezisession |
| 107 | **CC v2.1.105 — Skill description cap 250→1536 znaků** — STOPA skill descriptions mohou být 6× delší | HIGH | **yes** | 13 commands expanded (verify, scribe, budget, brainstorm, fix-issue, harness, skill-generator, nano, klip, youtube-transcript, autofix, autoharness, project-sweep) | — |
| 108 | **CC v2.1.105 — PreCompact hook** — pluginy mohou blokovat /compact přes exit code 2 | MED | **yes** | pre-compact.sh hook created + registered in settings.json (PreCompact event) | — |
| 99 | **CC Analytics API (GA)** — programmatický přístup k denním metrikám CC | HIGH | **yes** | budget SKILL.md:34 — tertiary source documented | Full impl when ccusage unavailable |
| 100 | **Meta Muse Spark** — Meta's first proprietary frontier model, "Contemplating mode" | MED | no | — | Přidat do `/eval` tier srovnání |
| 101 | **PwC sunset → HF Trending Papers** | MED | **yes** | watch SKILL.md:61 — Tier 2b note updated | — |
| 102 | **DACS (arXiv:2604.07911)** — Registry↔Focus context switching, 3.53× efficiency | HIGH | **yes** | learning `dacs-context-scoping`, commit `ad97748` | Implementovat v orchestrate pro >3 agentů |
| 103 | **TraceGuard (arXiv:2604.03968)** — 5D CoT monitoring | MED | **yes** | learning `traceguard-5d-critic`, commit `ad97748` | Upgrade `/critic` na 5D dekompozici |
| 104 | **Claude Agent SDK** — `additionalDirectories`, `ENABLE_TASKS` | MED | **yes** | evaluated: additionalDirs for future KODER multi-project, ENABLE_TASKS is Agent SDK only | Adopt at KODER multi-project |
| 81 | **CC MCP 500K tool result limit** | MED | **yes** | auto-applied by CC, no config needed | SAFE |
| 82 | **CC PreToolUse "defer" decision** | MED | **yes** | evaluated: not needed for interactive STOPA, PARKED for headless KODER | Adopt when KODER headless |
| 77 | **Model Capabilities API** — `GET /v1/models` | MED | **yes** | evaluated: orchestrate has per-subtask routing, hardcoded tiers sufficient | Adopt at Mythos/Capybara GA |
| 78 | **AGENTS.md efficiency study** (arXiv:2601.20404) | MED | **yes** | learning `agents-md-efficiency-validated` | Přidat do onboarding checklistu |
| 74 | **Claude Sonnet 5** — postupný rollout | MED | no | waiting for account access | Přepnout model tiers až dostupný |
| 83 | **CC effort=high default** | MED | **yes** | CLAUDE.md note updated | Sledovat náklady |
| 96 | **Prompt caching auto-placement** | MED | no | — | Zjednodušit NG-ROBOT caching |
| 97 | **Compaction API (beta)** | MED | no | — | Evaluovat pro /compact backend |
| 98 | **OpenClaw extra cost** | LOW | no | — | Sledovat pricing |
| 84 | **Claude Managed Agents (Public Beta)** | MED | no | — | Evaluovat jako alternativu |
| 85 | **`thinking: {type: enabled}` deprecated** | MED | **yes** | audit: NG-ROBOT+ADOBE both use adaptive, no deprecated code | SAFE |
| 86 | **`ant` CLI** | LOW | no | — | Sledovat až GA |
| 93 | **Advisor Tool public beta** | HIGH | **yes** | learning `advisor-tool-public-beta`, commit `2c600e5` | Integrace do orchestrate tiers |
| 94 | **CC v2.1.101 security fix** — Bash permission bypass | HIGH | **yes** | audit: all hooks use list args, no shell=True, no backslash flags | SAFE — no action needed |
| 95 | **CC Monitor tool** — realtime background streaming | MED | **yes** | evaluated: useful for KODER headless, current notifyOnCompletion sufficient | Adopt when KODER headless |
| 65 | CC `forceRemoteSettingsRefresh` | LOW | no | — | Sledovat při distribuci |
| 42 | CC Voice Mode — Czech included | MED | no | — | Otestovat až dostupný |
| 44 | CC HTTP hooks | PARKED | no | — | Adopt při remote agents |
| 29t | Bootleg SSL (arXiv:2603.15553) | LOW | no | — | Sledovat pro ORAKULUM |
| 29s | Attention innovations | INFO | no | — | Sledovat DiffAttn, TransMLA, Multiscreen |
| 29r | `hf papers` CLI | LOW | no | — | Kandidát pro /watch upgrade |

## Resolved (2026-04-04)
| # | Item | Resolution |
|---|------|------------|
| 59 | CC v2.1.91 `disableSkillShellExecution` | SAFE — STOPA skills používají Bash přes tool calls, ne přímé skill-framework shell. 29 skills neovlivněno. |
| 60 | Sonnet 4.6 GA | DONE — CLAUDE.md:114 má note, tier-definitions.yaml generický "sonnet", žádné staré model IDs. |
| 64 | CC v2.1.92 Stop hook fix | SAFE — 7 Stop hooks nejsou závislé na fixnuté sémantice. |
| 68 | CC v2.1.92 `/cost` per-model breakdown | DONE — /budget skill už má ccusage s per-model granularitou (npx ccusage daily). |
| 36 | Haiku 3 deprecation | DONE — NG-ROBOT na `claude-haiku-4-5-20251001`, ADOBE aktuální, STOPA bez aktivního kódu. |
| 48 | 1M context window retiring 2026-04-30 | SAFE — žádné aktivní `context-1m-2025-08-07` headers. |
| 49 | CC v2.1.89+90 hook upgrades | DONE — settings.json aktualizován (if: guards, PermissionDenied, TaskCreated). |
| 51 | CC v2.1.90 `thinking.display: "omitted"` | DONE — orchestrate SKILL.md:1064, Rule #12+#13. |
| 52 | Anthropic API web search/fetch GA | DONE — NG-ROBOT používá GA endpoint. |
| 53 | CC v2.1.90 `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE` | DONE — dokumentováno. |

## Resolved (2026-03-31)
| # | Item | Resolution |
|---|------|------------|
| 43 | CC `/effort` command | DONE — integrováno do orchestrate tier selection (light→Low, standard→Med, deep→High) |
| 41 | LiteLLM supply chain attack | DONE — audit: žádný z našich projektů nepoužívá LiteLLM |

## Watch List

### Models & Releases
| Item | Detail | Trigger |
|------|--------|---------|
| 83. CC v2.1.89 Named subagents via @mention | Subagenti jsou nyní adresovatelní @mention syntaxí. Potenciálně zjednodušuje STOPA multi-agent koordinaci. | Prozkoumat při příštím orchestrate refactoru |
| 75. Gemini CLI (Google) | Apache 2.0, ReAct loop, MCP support, 1M context. Direct competitor to Claude Code. FastMCP integration v dubnu 2026. [github](https://github.com/google-gemini/gemini-cli) | Sledovat adopci; patterns pro STOPA |
| 76. Google Colab MCP Server | Open-source MCP server pro Colab runtimes s GPU přístupem z libovolného AI agenta. [blog](https://developers.googleblog.com/announcing-the-colab-mcp-server-connect-any-ai-agent-to-google-colab/) | Kandidát pro POLYBOT/test1 inference |
| 40. Mythos/Capybara | **Training dokončen, piloting s early customers** (2026-04-03). "Nejschopnější model ever." Step change coding+reasoning. | GA datum → přeplánovat STOPA model tiers |
| 61. Gemma 4 | Google DeepMind, 2026-04-02. 4 modely (2B, 4B, 26B MoE, 31B), Apache 2.0, vision+reasoning. Simon Willison covered. | Open-weight alternativa — zvážit pro levné lokální inference tiery |
| 58. Mistral Small 4 | 119B, Apache 2.0, reasoning+multimodal+agentic coding unifikovaný model | Open-weight alternativa k Claude pro lokální nasazení |
| 35. CC v2.1.85 | /compact fix, deniedMcpServers fix, timestamp markery, MCP OAuth | Informativní |
| 5. Haiku 3 retire | 2026-04-19 deadline | Audit před deadline |
| 18. Gemini 3.1 Pro | 77.1% ARC-AGI-2, $2/$12 | Multi-provider srovnání |
| 29g. Gemini 3.1 Flash-Lite | $0.25/M — 1/8 ceny Pro | Cost tier reference |

### Video & Diffusion (test1/NG-ROBOT relevance)
| Item | Detail |
|------|--------|
| 57. Consistency-Preserving Video Gen (arXiv:2602.15287) | Joint-sampling FM: batch diversity + temporal consistency — relevantní pro test1 |
| 29p. PyTorch 2.11 | FlexAttention + FA4 — test1 dependency |
| 29q. Modular Diffusers 0.37.1 | Patch release Mar 25. Composable pipeline — test1 refactor |
| 29b. Foveated Diffusion | Spatially adaptive token alloc — video efficiency |
| 29c. FSVideo | 14B DIT, "order of magnitude faster" — Pyramid Flow alt |
| 26. 3× flow matching papers | FastLightGen, Warm-Start FM, Transition FM |
| 21. Wan2.1 + LTX 0.9.5 | Diffusers 0.37.0 video models |
| 29k. Luma Uni-1 | Decoder-only image gen, ~$0.09/img — /nano kandidát |

### Agent/Tool Research
| Item | Detail |
| 105. Meta Muse Spark "Contemplating mode" | Paralelní interní agenti v Meta's frontier model — architektonický vzor pro STOPA farm tier. [meta.com](https://ai.meta.com/blog/introducing-muse-spark-msl/) Trigger: GA pricing |
| 106. DACS — Registry↔Focus context switching | arXiv:2604.07911 (Apr 9) — pro orchestrátory s >3 agenty: 200-token summaries pro idle agenty, full context pro aktivního. Bez kódu. Sledovat implementaci. |
| 107. TraceGuard 5D CoT monitor | arXiv:2604.03968 (Apr 2) — 5 independent critic calls > 1 monolithic. Bez kódu. |
| 108. LangGraph 1.1.7a1 | Apr 10. Async subagent nodes, content moderation middleware, multi-modal read_file. [github](https://github.com/langchain-ai/deepagents) |
| 96. Hermes Agent v0.8.0 (NousResearch) | 40K+ GitHub stars. "Agent that grows with you" — persistent memory, auto-generated skills, learns projects. Cross-platform (Telegram, Discord, Slack, WhatsApp, Signal, Email). 5 backends. v0.8.0 Apr 8: background task auto-notifications, live model switching, MCP OAuth 2.1. [github](https://github.com/nousresearch/hermes-agent) — Inspirace pro STOPA persistent skill learning + cross-platform reach |
| 97. Memory Intelligence Agent (arXiv:2604.04503) | Comprehensive memory framework pro agenty — Apr 2026. Cache layers (immediate reasoning) + memory layers (retrieval + persistence). Framing blízký STOPA MemPalace. Bez kódu. Sledovat. |
| 79. Context Engineering (Goodside) | "Context engineering = co model čte, prompt engineering = co user píše." Terminologická divergence. Relevantní pro skill design filozofii. [interconnects.ai](https://www.interconnects.ai/p/riley-goodside-on-science-of-prompting) |
| 80. AI defers architecture decisions (Willison) | "AI udělalo refactoring levným → design se odkládal → zmatený kód → rewrite." Design musí přijít od člověka PŘED agentem. [simonwillison.net](https://simonwillison.net/2026/Apr/5/building-with-ai/) |
|------|--------|
| 73. Meta-Harness median gap | **[ACTION]** arXiv:2603.28052 — MEDIAN full traces: 50.0 vs scores-only: 34.6 (+15 pts). Best numbers (56.7 vs 41.3) zakrývají sílu nálezu. Iteration 7: 80-line env snapshot → #1 Haiku 4.5 TerminalBench-2 (37.6%). Cross-model transfer na 5 held-out modelů. STOPA: `/eval` musí reportovat median; `/orchestrate` přidat tool inventory jako P1 krok. |
| 71. MCP Toolbox for Databases (Google) | Production MCP server, 30+ DB (PostgreSQL, MongoDB, Redis, Snowflake, Neo4j…), one config, NL2SQL, connection pooling, IAM auth, OpenTelemetry. Pre-datuje MCP — není trend-chasing. [github](https://github.com/googleapis/genai-toolbox) — Trigger [ACTION] až POLYBOT/MONITOR implementuje DB layer |
| 70. agent-browser (Vercel Labs) | **[ACTION]** CLI pro agenty: snapshot→refs→act pattern, Rust daemon (nízká latence, žádný Node.js), CDP pro Electron (Discord, VSCode, Slack), 80+ příkazů, named sessions, domain allowlists. Nižší tokenová zátěž než Playwright. Instalace: `npm install -g agent-browser`. [github](https://github.com/vercel-labs/agent-browser) — **browser tools matice aktualizována** |
| 69. open-multi-agent | TypeScript: DAG task decomp + auto-unblocking, AgentPool semaphore, message bus. 3.5k★, 1.7k forks. Vzory: explicitní dependency graph (→ /orchestrate), paralelismus limit (→ circuit breaker upgrade). [github](https://github.com/JackChen-me/open-multi-agent) |
| 56. SMART (arXiv:2502.11435) | Tool Overuse Mitigation — agent self-awareness redukuje zbytečné tool calls. Inspirace pro STOPA light tier. |
| 58. Tool Use Survey (arXiv:2603.22862) | Single→multi-tool orchestration, 6 dimenzí: planning, training, safety, efficiency, capability, benchmarks |
| 49w. Message Batches 300k | Opus 4.6/Sonnet 4.6 — beta header `output-300k-2026-03-24`. Kandidát: /farm tier |
| 50. EFlow (arXiv:2603.27086) | Fast few-step video DiT, Gated Local-Global Attention — test1 alternativa k Pyramid Flow. Čekat na code release |
| 45. LangChain Deep Agents | Agent harness: planning (write_todos), filesystem offload, subagent spawning, persistent memory. GitHub: langchain-ai/deepagents |
| 29l. AgentScope | Alibaba, Apache 2.0, MsgHub orchestration, ReMe memory |
| 29m. MCP Elicitation | MCP servers → structured user input mid-task (confirmed released CC feature) |
| 29f. Agent SDK repos | claude-agent-sdk-python + typescript |
| 29e. Mem0 | Graph-based memory architecture — STOPA inspirace |
| 9. OpenClaw/NemoClaw | Messaging-first agent runtime, 210k★ (updated) |

### Papers (metodologie)
| Item | Relevance |
|------|-----------|
| 72. Multiscreen (arXiv:2604.01178) | Screening attention: absolutní relevance místo softmax kompetice, 40% méně parametrů, 3.2× rychlejší inference na 100K. Bez kódu. Sledovat adopci. |
| 62. Hi-CoT (arXiv:2604.00130) | Hierarchical CoT: planning → execution v substepech. Inspirace pro orchestrate hierarchické decomposition. |
| 63. Agentic Tool Use (arXiv:2604.00835) | 3 paradigmata: prompting plug-and-play, supervised, reward-driven. Taxonomie pro STOPA tool strategy. |
| 46. Bootstrapping Coding Agents (arXiv:2603.17399) | "Specification is the program" — agent re-impl sám sebe z 926-slov spec. IEEE Software. |
| 47. Flowception (arXiv:2512.11438 v2, 2026-03-22) | Video gen: frame insertion + denoising interleave, 3× FLOPs vs full-seq. Pro test1. |
| 29n. SWAP | Stepwise CoT penalization → cost reduction pro Opus calls |
| 29o. FinMCP-Bench | MCP tool-use benchmark, 613 vzorků |
| 29d. Beyond the Prompt | ICL/CoT mechanismy — validuje skill trigger design |
| 22. BOULDER | Multi-turn degrades reasoning → prefer single-shot evals |
| 23. MCPAgentBench | MCP tool discrimination benchmark |
| 24. CARE | Confounder-aware LLM-as-judge, −26.8% bias |
| 25. ToolTree | MCTS tool planning, ~10% gain |
| 27. SWE-CI | CI-loop benchmark, long-term maintenance |
| 28. ClarEval | Agent ambiguity detection benchmark |
| 8. Czech ABSA | ufal/robeczech-base — ZACHVEV sentiment |

### CC Hooks (v2.1.92, kandidáti pro implementaci)
| Item | Detail |
|------|--------|
| 66. InstructionsLoaded hook | Fires when CLAUDE.md nebo .claude/rules/*.md jsou načteny. Pro STOPA: redundantní (SessionStart hooks checkpoint-check.sh + memory-brief.sh to pokrývají). Přeskočit. |
| 67. agent_id/agent_type v hook contextu | DONE 2026-04-04 — guard přidán do všech 7 Stop hooks. Subagent Stop events (agent_type přítomen v stdin JSON) jsou skipnuty. |

### Ecosystem
| Item | Detail |
|------|--------|
| 1. Channels | Telegram/Discord integration. CRITICAL: no message queue |
| 2. /context suggestions | Memory bloat detection |
| 3. Memory timestamps | CC freshness awareness |
| 4. autoMemoryDirectory | Custom memory path |
| 5. /remote-control | CC ↔ claude.ai/code ↔ VS Code bridge |
| 6. GitHub Spec Kit | Competitor analysis done: `competitive-spec-kit.md` |
| 19. Papers with Code → HF | huggingface.co/papers/trending |
| 20. MCP lazy loading | Up to 95% context reduction |

## Scan History

### 2026-04-07 #2 — full | Searches: 15 | Fetches: 3 | Items: 2 action, 2 watch, 3 info — Model Capabilities API, AGENTS.md study (+28.64% runtime), Context Engineering framing, AI+architecture anti-pattern
### 2026-04-07 — quick (scheduled) | Searches: 3 | Fetches: 3 | Items: 0 action, 0 watch, 0 info — No new releases since 2026-04-04 (v2.1.92). API notes unchanged since 2026-03-30.
### 2026-04-06 #2 — quick (scheduled) | Searches: 3 | Fetches: 2 | Items: 0 action, 0 watch, 4 info — API bugfixes: Extended Thinking whitespace fix, Tool Streaming fix, Write Tool +60% perf, Message Batches 300k confirmed official (item 49w status update)
### 2026-04-06 — full | Searches: 16 | Fetches: 3 | Items: 1 action, 2 watch, 3 info
### 2026-04-05 — quick (scheduled) | Searches: 3 | Fetches: 1 | Items: 0 action, 0 watch, 0 info — No new releases since 2026-04-04
### 2026-04-04 #6 — targeted content (Meta-Harness thread) | Fetches: 0 | Items: 1 action, 0 watch, 0 info
### 2026-04-04 #5 — targeted URL (Multiscreen arXiv:2604.01178) | Fetches: 2 | Items: 0 action, 1 watch, 0 info
### 2026-04-04 #4 — targeted URL (MCP Toolbox for Databases) | Fetches: 0 | Items: 0 action, 1 watch, 0 info
### 2026-04-04 #3 — targeted URL (agent-browser) | Fetches: 1 | Items: 1 action, 0 watch, 0 info
### 2026-04-04 #2 — targeted URL | Fetches: 2 | Items: 0 action, 1 watch, 0 info
### 2026-04-04 — quick | Searches: 3 | Fetches: 1 | Items: 2 action, 3 watch, 1 info
### 2026-04-03 #2 — full | Searches: 9 | Fetches: 2 | Items: 2 action, 2 watch, 3 info
### 2026-04-03 — full | Searches: 13 | Fetches: 2 | Items: 5 action, 4 watch, 3 info
### 2026-04-01 — full | Searches: 10 | Fetches: 2 | Items: 5 action, 4 watch, 4 info
### 2026-03-31 — full | Searches: 14 | Fetches: 3 | Items: 3 action, 4 watch, 4 info
### 2026-03-29 — full (PyTorch 2.11, Modular Diffusers, hf papers CLI)
### 2026-03-28 — full (Mythos leak, LiteLLM, MCP Elicitation, papers)
### 2026-03-27 — targeted (CC v2.1.85)

Older: see `news-archive.md`

## Weekly Digest 2026-04-13

**Aktivita projektů:** STOPA 10 commitů (deterministic gates 65 kroků, workspace contract validator, semantic hygiene, design DB). NG-ROBOT 10 commitů (pipeline truncation fix, SEO cleanup, Python-first term verifier). ADOBE-AUTOMAT 10 commitů (IDML Track Changes, DOCX/MD export, AI korektury fixes). ZACHVEV/POLYBOT/MONITOR/GRAFIK idle.

**Novinky:** 17+ ACTION items otevřeno (2 HIGH: CC v2.1.101 security fix, Advisor Tool beta). 15+ WATCH položek. Trend: CC v2.1.94→v2.1.101 za týden, Advisor Tool public beta (executor+advisor model pair), Mythos/Capybara piloting u zákazníků.

**Poučení:** 34 nových learnings (Apr 5–8) — deception pod tlakem, auto-research bez human bottleneck, iterative refinement > long CoT, living memory > static retrieval.

**Údržba:** ⚠️ news.md přes limit → archivovat. decisions.md (27) a budget.md (39) OK.

**Doporučení:** 1) CC v2.1.101 security fix — zkontrolovat hooks na backslash-escaped bash, 2) Evaluovat Advisor Tool beta pro STOPA orchestrate tier, 3) Archivovat news.md.

## Weekly Digest 2026-04-06

**Aktivita projektů:** STOPA 50 commitů (prompt-evolve GEPA, HERA failure-learning fáze 1-5, PromptGuard+CodeShield, BM25 memory search, permission hook v3.0, Command Center+/design, deepresearch fix, /clean-writing). NG-ROBOT aktivní (SEO phase 7b, Preview Hub). Ostatní projekty bez commitů.

**Novinky:** 5 ACTION items — #73 Meta-Harness (/eval median + /orchestrate tool inventory), #70 agent-browser, #74 Sonnet 5 (čeká na rollout), #42 Voice Mode CZ. ~20 WATCH položek. Trend: agent defense + self-improvement smyčky.

**Poučení:** 27 nových learnings v dubnu — SKILL0 dynamic curriculum, OSFT self-sharpening, agent defense frameworks, BM25 memory retrieval.

**Údržba:** news.md 139 řádků (PŘES LIMIT 120) → archivovat. decisions.md OK (27). budget.md OK (36).

**Doporučení:** 1) Archivovat news.md, 2) Implementovat #73 Meta-Harness, 3) Otestovat agent-browser (#70).

## Last Scan: 2026-04-09 (scheduled morning-watch) | Next: ~2026-04-14

### Action Items

| # | Item | Urgency | Next Step |
|---|------|---------|----------|
| 75 | Haiku 3 retirement April 19 | ~~DONE~~ | Ověřeno: NG-ROBOT i ADOBE na haiku-4-5, STOPA bez aktivního kódu |
| 83 | CC v2.1.94 default effort=high | 🟡 MEDIUM | Agentic běhy dražší. STOPA orchestrate už má effort:high — aligned. Sledovat náklady. |
| 84 | Claude Managed Agents (Public Beta) | 🟡 WATCH | Beta header `managed-agents-2026-04-01`. Managed harness s sandboxingem. Potenciální alternativa k části STOPA orchestration. |
| 85 | `thinking: {type: enabled}` deprecated | 🟡 MEDIUM | Migrovat na `thinking: {type: adaptive}` + effort. STOPA clean — žádný skill/hook to nepoužívá. Target projekty ověřit. |
| 86 | `ant` CLI (Anthropic) | 🟢 INFO | Nový Anthropic CLI, YAML-based API resources. Sledovat až bude GA. |
| 76 | CLAUDE.md HTML comments skryty | 🟡 HIGH | Auditovat CLAUDE.md + rules/*.md, přesunout instrukce z HTML komentářů |
| 77 | TaskCreated hook — nový event | 🟡 MEDIUM | Evaluovat přidání do STOPA hook systému |
| 78 | PermissionDenied hook + retry | 🟡 WATCH | Zvážit pro permission hook v3.0 recovery flow |
| 79 | 1M context beta retirement April 30 | 🟡 WATCH | Ověřit model usage, migrovat pokud potřeba |
| 80 | --bare flag pro headless -p | 🟢 INFO | Evaluovat pro STOPA headless subagenty |
| 81 | MCP 500K result size | 🟢 INFO | Dostupné pro STOPA MCP servery s velkými výstupy |
| 82 | SessionStart hook deferred 500ms | 🟢 INFO | Záměrné zpoždění — není bug |

| 90 | **Sonnet 3.7 + Haiku 3.5 retired** — requesty vrací chyby. Upgrade na Sonnet 4.6 resp. Haiku 4.5. | 🔴 HIGH | Zkontrolovat target projekty (NG-ROBOT, ADOBE, test1) zda nepoužívají claude-sonnet-3-7 nebo claude-haiku-3-5 |
| 91 | **Messages API na Amazon Bedrock (research preview)** — stejný request shape jako první-party API, AWS-managed infrastruktura, nulový operator access, us-east-1. | 🟢 INFO | Sledovat pro enterprise deployment scénáře |
| 92 | **CC Focus view (Ctrl+O)** — nový UI mód: prompt + jednořádkový tool summary s edit diffstats + finální odpověď. NO_FLICKER mode. | 🟢 INFO | Otestovat při práci s velkými diff outputy |
| 87 | Compaction API beta (Opus 4.6) | 🟡 MEDIUM | Server-side context summarization pro infinite conversations. Potenciální alternativa k /compact skill. Evaluovat integraci. |
| 88 | Claude Mythos Preview (Project Glasswing) | 🟡 WATCH | Preview s 11 partnery, cybersecurity focus. Confirmed live — sledovat GA datum a pricing. |
| 89 | Data residency controls (inference_geo) | 🟢 INFO | US-only inference za 1.1× cenu pro modely po 2026-02-01. Enterprise feature. |
| 93 | **CC `/team-onboarding` command** — generuje ramp-up guide pro nové členy týmu z lokálního CC usage. Auto-detekuje stack, konvence, časté příkazy. | 🟢 INFO | Otestovat při onboardingu nových spolupracovníků |
| 94 | **CC Vertex AI interactive setup wizard** — interaktivní průvodce nastavením Google Vertex AI přístupný z login screen. Alternativa k manuální .env konfiguraci. | 🟢 INFO | Sledovat pokud STOPA bude potřebovat Vertex AI backend |
| 95 | **`effort` parameter GA** — bez beta headeru, nativně podporuje Opus 4.6. Nahrazuje `budget_tokens` na nových modelech. | 🟡 MEDIUM | STOPA orchestrate tier selection — ověřit, zda skills posílají `effort` bez beta headeru |

| 2026-04-15 | [ACTION] | Self-Optimizing Multi-Agent Systems for Deep Research (arXiv:2604.02988) — orchestrátor + paralelní worker agenti se self-play optimalizací promptů; přímo aplikovatelné na STOPA self-evolve/autoloop | high | Yes | arxiv-daily-digest |
| 2026-04-15 | [WATCH] | CLEAR: Context Augmentation from Contrastive Learning via Agentic Reflection (arXiv:2604.07487) — kontrastivní porovnání rolloutů extrahuje znovupoužitelný strategy-level kontext pro agenty | medium | No | arxiv-daily-digest |
| 2026-04-15 | [WATCH] | Verified Multi-Agent Orchestration: Plan-Execute-Verify-Replan Framework (arXiv:2603.11445) — DAG dekompozice dotazů s verification-driven koordinací specializovaných agentů | medium | No | arxiv-daily-digest |
| 2026-04-15 | [WATCH] | SiriuS: Self-improving Multi-agent Systems via Bootstrapped Reasoning (arXiv:2502.04780) — buduje knihovnu zkušeností z úspěšných reasoning trajektorií pro bootstrapped self-improvement | medium | No | arxiv-daily-digest |
| 2026-04-15 | [WATCH] | CoCR-RAG: Concept-oriented Context Reconstruction for RAG (arXiv:2603.23989) — concept-level fúze více zdrojů pro koherentnější retrieval augmentaci | medium | No | arxiv-daily-digest |

### Scan History

### 2026-04-15 — arxiv-daily-digest | Searches: 4 | Items: 1 action, 4 watch — Self-Optimizing MAS (arXiv:2604.02988), CLEAR context augmentation (arXiv:2604.07487), Verified Orchestration (arXiv:2603.11445), SiriuS (arXiv:2502.04780), CoCR-RAG (arXiv:2603.23989)
### 2026-04-14 — full scan | Searches: 19 | Items: 6 action, 4 watch, 2 info — CC Analytics API GA (#99), Meta Muse Spark (#100), PwC→HF Trending (#101), DACS arXiv:2604.07911 (#102), TraceGuard arXiv:2604.03968 (#103), Agent SDK additionalDirectories (#104)
### 2026-04-12 — full scan | Searches: 12 | Fetches: 3 | Items: 3 action, 3 watch, 4 info — Advisor Tool public beta, CC v2.1.101 security fixes + Monitor tool, Hermes Agent v0.8.0, Memory Intelligence Agent paper, Qwen3.6-Plus, BEHELM benchmark
### 2026-04-10 — scheduled morning-watch | Searches: 2 | Items: 1 action, 2 watch — Sonnet 3.7+Haiku 3.5 retired (errors), Bedrock Messages API preview, CC Focus view
### 2026-04-09 — scheduled morning-watch | Searches: 2 | Items: 2 watch, 1 info — Compaction API beta, Mythos Preview live (Project Glasswing), data residency controls
### 2026-04-08 — quick+update | Searches: 3+3 | Fetches: 2+1 | Items: 4 action, 3 watch — Managed Agents beta, effort=high default, thinking deprecation, ant CLI, Haiku 3 verified safe
### 2026-04-13 — scheduled morning-watch | Searches: 2 | Items: 1 watch, 2 info — /team-onboarding command (#93), Vertex AI wizard (#94), effort param GA (#95)
### 2026-04-08 — quick (scheduled) | Searches: 3 | Fetches: 2 | Items: 3 action, 3 watch, 2 info — Haiku 3 deadline April 19, CLAUDE.md HTML comments skryty, TaskCreated hook, PermissionDenied hook+retry, 1M context retirement April 30, --bare flag