# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Archived: `news-archive.md`

## Last Scan: 2026-04-04 (quick) | Next: ~2026-04-10

## Action Items

| # | Item | Urgency | Next Step |
|---|------|---------|-----------|
| 65 | CC v2.1.92 — `forceRemoteSettingsRefresh` policy | LOW | Fail-closed při nenačtení remote managed settings. Sledovat při distribuci do target projektů. |
| 42 | CC Voice Mode (`/voice`) — Czech included | MED | Otestovat až se rolling out dostane k účtu; 20 jazyků vč. češtiny |
| 44 | CC HTTP hooks (POST JSON → URL) | PARKED | Adopt při remote agents; pro teď nepotřebujeme |
| 29t | Bootleg SSL (arXiv:2603.15553) | LOW | Sledovat pro ORAKULUM/ZACHVEV pokud Chronos-2 nestačí |
| 29s | Attention innovations status | INFO | Produkce: MLA, GQA, iRoPE. Sledovat DiffAttn DEX adapter + TransMLA + **Multiscreen** (arXiv:2604.01178) |
| 29r | `hf papers` CLI (AK) | LOW | Kandidát pro upgrade /watch Tier 2b strategy |

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
|------|--------|
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
