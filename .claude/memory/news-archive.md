# News Archive

Archived items from `news.md`. Read-only reference — not actively loaded into context.

## Archived Action Items

<!-- Archived 2026-03-30 — CALM-inspired compression maintenance -->

- **Cloud Auto-Fix PRs + Scheduled Tasks** (#34, CC Web, 2026-03-27) — Status: DONE 2026-03-29
  - `/autofix` skill implemented, `/fix-issue` Phase 7 added
  - Scheduled cloud tasks: PLANNED (needs Claude GitHub App)

- **AutoDream / `/dream`** (#32, CC v2.1.81+) — Status: EVALUATED 2026-03-26
  - Verdict: KOEXISTENCE — dream=janitor, scribe=architekt. PR #39299 stále open.

- **CC v2.1.86** (#37, 2026-03-27) — Windows settings.json corruption fix
  - Akce: update CLI — Status: PENDING (low priority)

- **CC v2.1.84 PowerShell** (#38) — Status: NOTED (opt-in preview)

- **Claude Desktop Windows** (#39, 2026-03-28) — v1.1.1931, Computer Use Mac only

- **CC 2.1.84** (#30) — TaskCreated + WorktreeCreate hooks — Status: NOTED

- **CC 2.1.83** (#31) — FileChanged hook, managed-settings.d/ — Status: NOTED

- **Auto Mode** (#0, 2026-03-24) — `claude --enable-auto-mode` research preview
  - Relevance: nahradí manuální permission approvals. Team plan only.

- **Computer Use Mac** (#0b) — macOS only, Windows pending

- **Claude Dispatch** (#0c) — QR párování iPhone→Mac, Max/Pro subscribers

- **Claude Mobile Interactive Apps** (#33) — live charts v mobile konverzaci

- **Codified Context** (#29, arXiv 2602.20478) — Context Bootstrap do /orchestrate — PENDING

- **`${CLAUDE_PLUGIN_DATA}`** (#1) — plugin persistent state — deferred

- **1M context GA** (#2) — Opus+Sonnet 4.6, no beta header — NOTED

- **`thinking.display: "omitted"`** (#3) — omit thinking blocks, 2.5× faster streaming — NOTED

- **Models API capabilities** (#4) — dynamic model selection — NOTED

- **Opus 4.6 max output 128k** (#6) — default 64k, upper 128k — NOTED

- **HTTP hooks** (#7) — GA od v2.1.63, TLS SNI bug workaround — NOTED

<!-- Archived 2026-03-29 routine maintenance — DONE items -->

- **Claude web search — light Research auto-depth mode** (Alex Albert, Mar 2026) — Status: DONE 2026-03-29
  - Web search automaticky nastavuje hloubku vyhledávání dle query complexity
  - Implementováno: přidáno do `/deepresearch` SEARCH STRATEGY + `/watch` Tier 2b intro

- **`${CLAUDE_SKILL_DIR}` proměnná** (CC, Mar 2026) — Status: DONE 2026-03-29
  - Implementováno: přidán `${CLAUDE_SKILL_DIR}/tier-heuristics.md` do plugin orchestrate + zkopírován tier-heuristics.md

- **CC v2.1.85 hook conditions** (2026-03-26) — `if` podmínky — Status: DONE 2026-03-29
  - Přidáno `if: "Edit(*.py)|Write(*.py)"` na ruff-lint hook, `if: "Bash(git commit*)"` na post-commit-analyzer

- **CC 2.1.83 `initialPrompt` v agent frontmatter** (2026-03-25) — Status: DONE 2026-03-29
  - stopa-worker již měl, přidáno do watchdog agenta

<!-- Archived 2026-03-24 Phase 1 hygiene cleanup -->

- **Modular Diffusers v0.37.0** (2026-03-05) — EVALUATED 2026-03-24: SKIP. Pyramid Flow incompatible (no DiffusionPipeline, PyTorch ≥2.3 conflict). Build on 0.37 paralelně s novým modelem.
- **HTTP hooks v CC** — EVALUATED 2026-03-24: GA od v2.1.63. Merged with ACTION #6 in news.md.

<!-- Archived 2026-03-24 quick scan cleanup -->

- **`effort` frontmatter pro skills** (v2.1.80) — DONE: verify→high, scout→low (critic/orchestrate/scribe set)
- **PreToolUse security fix** (v2.1.77) — DONE: Dippy funguje, fix se týká `deny` rules, STOPA nepoužívá
- **GitHub Spec Kit** (81k★) — ARCHIVED: analýza hotova v competitive-spec-kit.md, vzory adoptovány

<!-- Archived 2026-03-23 batch 2 — all remaining action items processed -->

7. ~~**Diffusers 0.37.0** (Mar 5)~~ — Modular Diffusers, FIBO Edit, Cosmos Predict2.5
   - Status: **DEFERRED** — relevantní pro NG-ROBOT, ne STOPA. Evaluovat při práci na NG-ROBOT.

8. ~~**Claude Code v2.1.79**~~ — `/remote-control` VSCode bridge, PreToolUse `deny` bug fix
   - Status: **DONE** — informativní, žádná akce potřeba

10. ~~**API code execution zdarma**~~ — s web search nebo web fetch
    - Status: **DEFERRED** — low priority, update budget kalkulace až bude relevantní

16. ~~**Claude Code v2.1.81**~~ (Mar 20) — `--bare` flag, `--channels` relay, Windows streaming off
    - Status: **NOTED** — `--bare` nepotřebujeme (STOPA nevolá claude CLI jako subprocess). Windows streaming info = informativní.

17. ~~**`source: 'settings'` existuje**~~ (v2.1.80) — inline plugin deklarace
    - Status: **DONE** — informativní, stávající implementace OK. Zaznamenáno v learnings.md.

18. ~~**CC v2.1.77 — Agent `resume` odstraněn**~~ — použij `SendMessage({to: agentId})`
    - Status: **SAFE** — STOPA už používá SendMessage od 2026-03-19

19. ~~**API: Automatic caching**~~ (Feb 19) — `cache_control` v request body
    - Status: **DEFERRED** — relevantní pro NG-ROBOT pipeline, ne STOPA

<!-- Archived 2026-03-23 by manual maintenance -->

1. ~~**Plugin `git-subdir` source type** (v2.1.69)~~ — **DONE** (plugin.json + README updated, v1.3.0)

2. ~~**`${CLAUDE_PLUGIN_DATA}` persistent state**~~ (v2.1.78) — plugin-specific storage surviving updates
   - Impact: medium — evaluated: all 6 memory files stay in `.claude/memory/` (project-shared). `${CLAUDE_PLUGIN_DATA}` reserved for future cache (autoloop M5, watch deduplikace).
   - Status: **DONE** — design decision made, no migration needed now

3. ~~**New hook events** (v2.1.69-76)~~ — PostCompact, StopFailure, TaskCompleted implemented. InstructionsLoaded: SKIP (audit only, no use case). TeammateIdle: deferred to Agent Teams implementation. Elicitation: SKIP (no MCP auth needs yet).
   - Impact: high — 3/6 events active, 3 evaluated and deferred/skipped
   - Status: **DONE** — all 6 evaluated, 3 implemented, 3 consciously skipped

4. ~~**Skills frontmatter fields** (v2.1.69)~~ — `model:`, `effort:`, `maxTurns`, `disallowedTools` now on all 11 skills. Only `${CLAUDE_SKILL_DIR}` still unused.
   - Impact: high — per-skill model selection + resource limits active
   - Status: **DONE** — model: + effort: + maxTurns + disallowedTools all set

5. ~~**`--plugin-dir` breaking change** (v2.1.76)~~ — **DONE** (README updated with repeated flags note)

6. ~~**Agent Teams**~~ — native parallel agent coordination (experimental but stable)
   - Impact: high for /orchestrate deep tier
   - Status: **DONE** — env var enabled in settings.json, /orchestrate deep tier updated with Teams workflow.

9. ~~**Extended thinking `display: "omitted"`**~~ (API) — vynechání thinking bloků z odpovědi pro rychlejší streaming, signatura zachována pro multi-turn
   - Impact: medium — ušetří tokeny v /orchestrate deep tier
   - Status: **DONE** — added to /orchestrate deep tier optimization section

12. **Claude Code v2.1.80** — `effort` frontmatter GA, `rate_limits` statusline, `--channels` MCP preview, --resume bug fix, -80MB paměti
    - Status: **DONE** — marketplace implementován přes `github` source v settings.json

20. **API: Sonnet 3.7 + Haiku 3.5 retired** (Feb 19) — STOPA safe (aliases).
    - Status: SAFE

14. **Claude Haiku 3 odchod** (April 19, 2026) — STOPA safe (aliases)
    - Status: SAFE

## Archived Watch List (2026-03-27 maintenance)

<!-- Archived 2026-03-27 — evaluated/stale watch items -->

- **PyTorch 2.11** — EVALUATED 2026-03-24: WAIT do PyTorch 2.12 (~květen 2026). FA4 backend nestabilní.
- **PostCompact hook** (v2.1.76) — NOTED, no immediate use case
- **Elicitation hooks** (v2.1.76) — NOTED, no MCP auth needs yet
- **MagCache + TaylorSeer** (Diffusers 0.37.0) — inference caching, relevant for test1 only
- **Seedance 2.0** (ByteDance) — video gen model, no API
- **Mistral Small 4** (119B, Apache 2.0) — potenciální open-weights alternative, no action
- **Flowception + DMD** (ICLR 2026) — video gen speedup, relevant for test1
- **Veo 3.1** (Google) — video gen, ComfyUI + fal.ai

## Archived Watch List

<!-- Archived 2026-03-23 batch 2 — informational items, no action needed -->

9. ~~**Google Flow**~~ (Feb/Mar 2026) — unified AI video workspace. Žádné veřejné API — nelze integrovat.
10. ~~**Models API capability fields**~~ (March 18) — `GET /v1/models` — informativní, žádná akce
11. ~~**1M kontext GA pro Sonnet 4.6**~~ (March 13) — informativní, bez nutné akce

<!-- Archived 2026-03-23 — deduplicated entries (short versions removed, full versions kept) -->

1. **MCP elicitation** (v2.1.76) — servers request structured input mid-task via interactive dialog
2. **FlashAttention-4 + KernelAgent** (PyTorch blog, Mar 2026)
3. **Direction-Magnitude Decoupling** (ICLR 2026)
4. **ViFeEdit** (Mar 16, 2026) — video generation + editing trénovaný jen na 2D obrázcích
5. **Flowception** — non-autoregressive variable-length video gen
6. **Hook-enforced orchestration** — `barkain/claude-code-workflow-orchestration`
7. **MCP Memory Servers** — persistent memory via MCP instead of file-based
8. **PyTorch 2.10.0** (Jan 21, 2026)

## Archived Scan History (2026-03-29 maintenance)

### 2026-03-26 — targeted + full scans (AutoDream eval, CC 2.1.83-84, papers)
### 2026-03-25 — papers scan + full scan (Auto Mode, Opus 128k output, 7 papers)
### 2026-03-24 — hands-on research + full scan (Diffusers SKIP, PyTorch WAIT, HTTP hooks GA)
### 2026-03-23 — 2× full scan (CHANGELOG deep-dive, batch cleanup of 7 items)

### 2026-03-27 — targeted scan (CC v2.1.85 hooks conditions)
### 2026-03-26 — targeted (AutoDream eval) + evening full (CC 2.1.83-84, papers) + morning full (Agent SDK repos, Codified Context)
- Key: initialPrompt + FileChanged hooks = significant STOPA upgrade potential
- Key: Codified Context paper validates STOPA architecture, identifies missing retrieval hooks
### 2026-03-25 — papers (BOULDER, MCPAgentBench, CARE, 3× flow matching) + full (Auto Mode, Computer Use Mac, Dispatch)
- Key: BOULDER shows multi-turn degrades reasoning → single-shot for reasoning-heavy evals
### 2026-03-24 — hands-on (3 items: Diffusers SKIP, PyTorch WAIT, HTTP hooks GA) + full + quick desktop
- Key: Harness Design blog → anti-leniency protocol implemented in /critic

## Archived Scan History

<!-- Archived 2026-03-23 batch 2 — scans older than 2 days -->

### 2026-03-22 — quick scan (Tier 1)
- CC: stále v2.1.81 — žádná nová verze
- API: žádné nové release notes od March 18

### 2026-03-21 (2) — full scan
- CC v2.1.77: Agent tool `resume` param odstraněn (STOPA safe), SendMessage auto-resume, plugin validate vylepšen
- API: Automatic caching GA (Feb 19), Sonnet 3.7 + Haiku 3.5 retired (safe — aliases)
- LTX-2.3, Google Flow redesign, Czech ABSA benchmarks

<!-- Archived 2026-03-23 — scans older than 14 days -->

### 2026-03-19 — topic:openclaw (večerní scan)
- OpenClaw: personal AI agent runtime, 250k+ stars, messaging-first paradigma, bridge pluginy s CC
- Security: CVE-2026-25253 CVSS 8.8, 12 % malicious community skills
- Governance: creator odešel do OpenAI, přechod na foundation
- Verdict: WATCH — nestabilní nyní, potenciálně zajímavé jako distribution channel/mobile layer

### 2026-03-19 — full (odpolední scan)
- v2.1.79: /remote-control VSCode bridge, PreToolUse deny fix, streaming po řádcích
- Extended thinking display:omitted, API code execution zdarma s web search
- FlashAttention-4 + KernelAgent (PyTorch), Direction-Magnitude Decoupling (ICLR 2026), ViFeEdit
- AI píše 41 % kódu, ale produktivita +10 % — adoption vs. output gap

### 2026-03-19 — full (ranní scan)
- Plugin git-subdir, ${CLAUDE_PLUGIN_DATA}, new hook events, skills frontmatter fields
- 4 previously open items resolved (plugin GA, /loop, HTTP hooks, token limits)
- Diffusers 0.37.0 Modular Diffusers, Flowception paper
- Voice mode supports Czech, 1M context for Opus 4.6
- 340 plugins + 1367 skills in ecosystem

### 2026-03-18 — full — STOPA-focused scan
- Plugin System GA — highest priority finding
- Agent Teams GA, /loop command, HTTP hooks
- Competing orchestration patterns (hook-enforced vs convention-based)
- 14k+ MCP servers in ecosystem

### 2026-03-18 — full — initial scan (in test1 context)
- First scan focused on Pyramid Flow dependencies
- Orchestration-relevant items extracted to STOPA

### Resolved Items (archived)

1. ~~Plugin System GA~~ — **DONE** (implemented in STOPA, v2.1.69+)
2. ~~`/loop` command~~ — **GA** (v2.1.71) — available now
3. ~~HTTP hooks~~ — **GA** (v2.1.63) — available now
4. ~~Token limit increase~~ — **CONFIRMED** (Opus 4.6: 64k default, 128k max output)


## Archived 2026-04-20 (maintenance)

### Resolved Items (2026-04-04)
| # | Item | Resolution |
|---|------|------------|
| 59 | CC v2.1.91 disableSkillShellExecution | SAFE — STOPA skills pouzivaji Bash pres tool calls. 29 skills neovlivneno. |
| 60 | Sonnet 4.6 GA | DONE — CLAUDE.md:114 note, tier-definitions.yaml genericky "sonnet". |
| 64 | CC v2.1.92 Stop hook fix | SAFE — 7 Stop hooks nezavisle na fixnute semantice. |
| 68 | CC v2.1.92 /cost per-model breakdown | DONE — /budget skill ma ccusage s per-model granularitou. |
| 36 | Haiku 3 deprecation | DONE — NG-ROBOT na haiku-4-5-20251001, ADOBE aktualni. |
| 48 | 1M context window retiring 2026-04-30 | SAFE — zadne context-1m headers. |
| 49 | CC v2.1.89+90 hook upgrades | DONE — settings.json aktualizovan. |
| 51 | CC v2.1.90 thinking.display omitted | DONE — orchestrate SKILL.md. |
| 52 | Anthropic API web search/fetch GA | DONE — NG-ROBOT pouziva GA endpoint. |
| 53 | CC v2.1.90 CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE | DONE — dokumentovano. |

### Resolved Items (2026-03-31)
| # | Item | Resolution |
|---|------|------------|
| 43 | CC /effort command | DONE — integrovano do orchestrate tier selection |
| 41 | LiteLLM supply chain attack | DONE — zadny projekt nepouziva LiteLLM |

### Acted Action Items (archived)
| # | Item | Evidence |
|---|------|----------|
| 106 | CC v2.1.108 — /recap + 1h prompt cache | settings.json: ENABLE_PROMPT_CACHING_1H=1 |
| 107 | CC v2.1.105 — Skill description cap 250->1536 | 13 commands expanded |
| 108 | CC v2.1.105 — PreCompact hook | pre-compact.sh + settings.json |
| 99 | CC Analytics API (GA) | budget SKILL.md:34 documented |
| 101 | PwC sunset -> HF Trending Papers | watch SKILL.md:61 updated |
| 102 | DACS (arXiv:2604.07911) | learning dacs-context-scoping, commit ad97748 |
| 103 | TraceGuard (arXiv:2604.03968) | learning traceguard-5d-critic, commit ad97748 |
| 104 | Claude Agent SDK additionalDirectories | evaluated: additionalDirs for future KODER |
| 81 | CC MCP 500K tool result limit | auto-applied by CC, no config needed |
| 82 | CC PreToolUse "defer" decision | PARKED for headless KODER |
| 77 | Model Capabilities API | evaluated: hardcoded tiers sufficient |
| 78 | AGENTS.md efficiency study | learning agents-md-efficiency-validated |
| 83 | CC effort=high default | CLAUDE.md note updated |
| 85 | thinking.type.enabled deprecated | audit: NG-ROBOT+ADOBE both use adaptive |
| 93 | Advisor Tool public beta | learning advisor-tool-public-beta, commit 2c600e5 |
| 94 | CC v2.1.101 security fix | audit: all hooks use list args, no shell=True |
| 95 | CC Monitor tool | evaluated: current notifyOnCompletion sufficient |
| 67 | agent_id/agent_type v hook contextu | DONE 2026-04-04 — guard pridan do 7 Stop hooks |

### Watch List Archive — Video & Diffusion (test1 relevance)
| Item | Detail |
|------|--------|
| 57 | Consistency-Preserving Video Gen (arXiv:2602.15287) |
| 29p | PyTorch 2.11 — FlexAttention + FA4 |
| 29q | Modular Diffusers 0.37.1 — composable pipeline |
| 29b | Foveated Diffusion — spatially adaptive token alloc |
| 29c | FSVideo — 14B DIT |
| 26 | 3x flow matching papers — FastLightGen, Warm-Start FM, Transition FM |
| 21 | Wan2.1 + LTX 0.9.5 — Diffusers 0.37.0 video models |
| 29k | Luma Uni-1 — Decoder-only image gen ~$0.09/img |
| 50 | EFlow (arXiv:2603.27086) — Fast few-step video DiT |
| 47 | Flowception (arXiv:2512.11438 v2) — video gen frame insertion |

### Watch List Archive — Papers (methodology, March 2026)
| Item | Detail |
|------|--------|
| 72 | Multiscreen (arXiv:2604.01178) — screening attention, 40% fewer params |
| 62 | Hi-CoT (arXiv:2604.00130) — hierarchical CoT |
| 63 | Agentic Tool Use (arXiv:2604.00835) — 3 paradigmata |
| 46 | Bootstrapping Coding Agents (arXiv:2603.17399) |
| 29n | SWAP — stepwise CoT penalization |
| 29o | FinMCP-Bench — MCP tool-use benchmark |
| 22 | BOULDER — multi-turn degrades reasoning |
| 23 | MCPAgentBench — MCP tool discrimination |
| 24 | CARE — confounder-aware LLM-as-judge |
| 25 | ToolTree — MCTS tool planning |
| 27 | SWE-CI — CI-loop benchmark |
| 28 | ClarEval — agent ambiguity detection |
| 8 | Czech ABSA — ufal/robeczech-base (ZACHVEV sentiment) |

### Watch List Archive — CC Hooks (v2.1.92)
| Item | Status |
|------|--------|
| 66 | InstructionsLoaded hook — redundantni, SessionStart hooks pokryvaji. Skip. |
| 35 | CC v2.1.85 — /compact fix, deniedMcpServers fix, timestamp markery |

### Watch List Archive — Ecosystem (old items)
| Item | Detail |
|------|--------|
| 1 | Channels — Telegram/Discord integration |
| 2 | /context suggestions — memory bloat detection |
| 3 | Memory timestamps — CC freshness awareness |
| 4 | autoMemoryDirectory — custom memory path |
| 5 | /remote-control — CC + claude.ai/code + VS Code bridge |
| 6 | GitHub Spec Kit — competitor analysis done |
| 19 | Papers with Code -> HF — huggingface.co/papers/trending |
| 20 | MCP lazy loading — up to 95% context reduction |

### Watch List Archive — Agent/Tool (old items, March 2026)
| Item | Detail |
|------|--------|
| 56 | SMART (arXiv:2502.11435) — tool overuse mitigation |
| 58 | Tool Use Survey (arXiv:2603.22862) |
| 49w | Message Batches 300k — kandidat: /farm tier |
| 45 | LangChain Deep Agents — planning, filesystem offload |
| 29l | AgentScope — Alibaba, MsgHub orchestration |
| 29m | MCP Elicitation — MCP servers -> structured user input |
| 29f | Agent SDK repos — claude-agent-sdk-python + typescript |
| 29e | Mem0 — graph-based memory architecture |
| 9 | OpenClaw/NemoClaw — 210k* messaging-first agent runtime |
| 69 | open-multi-agent — TypeScript DAG, AgentPool semaphore |
| 79 | Context Engineering (Goodside) — terminologicka divergence |
| 80 | AI defers architecture decisions (Willison) |

### Weekly Digest 2026-04-06
**Aktivita projektov:** STOPA 50 commitu (prompt-evolve GEPA, HERA, BM25 memory search). NG-ROBOT aktivni (SEO phase 7b).
**Novinky:** #73 Meta-Harness, #70 agent-browser, #74 Sonnet 5. Trend: agent defense + self-improvement.
**Pouceni:** 27 novych learnings — SKILL0 dynamic curriculum, OSFT self-sharpening, agent defense, BM25 retrieval.

### Scan History Archive (before 2026-04-12)
- 2026-04-10 — morning-watch | Sonnet 3.7+Haiku 3.5 retired, Bedrock Messages API preview
- 2026-04-09 — morning-watch | Compaction API beta, Mythos Preview live, data residency controls
- 2026-04-08 — quick+update | Managed Agents beta, effort=high, thinking deprecation, ant CLI
- 2026-04-07 #2 — full | Model Capabilities API, AGENTS.md study, Context Engineering
- 2026-04-07 — quick | No new releases since 2026-04-04
- 2026-04-06 #2 — quick | Extended Thinking whitespace fix, Tool Streaming fix, Write Tool +60%
- 2026-04-06 — full | Items: 1 action, 2 watch, 3 info
- 2026-04-05 — quick | No new releases
- 2026-04-04 — multiple targeted (Meta-Harness, Multiscreen, MCP Toolbox, agent-browser)
- 2026-04-03 — full x2 | Items: 7 action, 6 watch, 6 info
- 2026-04-01 — full | Items: 5 action, 4 watch, 4 info
- 2026-03-31 — full | Items: 3 action, 4 watch, 4 info
- 2026-03-29 — full (PyTorch 2.11, Modular Diffusers, hf papers CLI)
- 2026-03-28 — full (Mythos leak, LiteLLM, MCP Elicitation)
- 2026-03-27 — targeted (CC v2.1.85)


<!-- Archived 2026-04-27 — memory-maintenance scheduled task -->

## Archived Scan Logs (Apr 12-18, 2026)

- **2026-04-18** — arxiv-daily-digest | Items: 1 action, 4 watch — AgentForge (arXiv:2604.13120), CoMAS
- **2026-04-17** — morning-watch | Items: 3 action — CC Routines, CC Desktop Redesign, Opus 4.7 GA
- **2026-04-17** — arxiv-daily-digest | Items: 1 action, 4 watch — RL Skill Library, Context Kubernetes, MAE
- **2026-04-16** — arxiv-daily-digest | Items: 2 action, 3 watch — Context Engineering Multi-Agent, Smart MAS Middleware
- **2026-04-15** — arxiv-daily-digest | Items: 1 action, 4 watch — Self-Optimizing MAS, CLEAR, Verified Orchestration
- **2026-04-15** — CC-focused | Items: 4 action, 2 watch — Desktop redesign, v2.1.108, PreCompact hook, skill desc 1536
- **2026-04-14** — full scan | Searches: 19 | Items: 6 action, 4 watch, 2 info — CC Analytics GA, DACS, TraceGuard
- **2026-04-13** — morning-watch | Items: 1 watch, 2 info — /team-onboarding, Vertex AI wizard, effort param GA
- **2026-04-12** — full scan | Fetches: 3 | Items: 3 action, 3 watch, 4 info — Advisor Tool beta, CC Monitor, Hermes v0.8.0

## Archived DONE Action Items

- **#112 Agent `resume` param removed** (2026-04-21) — Breaking: Agent() resume param gone, must use SendMessage(). STOPA skills checked (grep clean) — zero impact. Status: DONE.

## Archived Recent Findings (Apr 15-20, 2026)

| Date | Type | Item | Priority | Acted |
|------|------|------|----------|-------|
| 2026-04-20 | ACTION | Context Awareness Gate (arXiv:2411.16133) | high | No |
| 2026-04-19 | ACTION | RL for RAG (arXiv:2510.24652) | high | No |
| 2026-04-18 | ACTION | AgentForge (arXiv:2604.13120) — 40% SWE-bench | high | No |
| 2026-04-17 | ACTION | CC Routines — cloud-side automations | high | No |
| 2026-04-17 | ACTION | CC Desktop Redesign — parallel sessions, drag-drop | high | No |
| 2026-04-17 | ACTION | Claude Opus 4.7 GA — 3x visual resolution, $5/$25 | high | No |
| 2026-04-17 | ACTION | RL Skill Library (arXiv:2512.17102) | high | No |
| 2026-04-16 | ACTION | Context Engineering Multi-Agent (arXiv:2603.09619) | high | No |
| 2026-04-16 | ACTION | Smart MAS Middleware (arXiv:2604.03430) | high | No |
| 2026-04-15 | ACTION | Self-Optimizing MAS (arXiv:2604.02988) | high | Yes |
| 2026-04-20 | WATCH | SE Benchmarks Survey (arXiv:2510.09721) | medium | No |
| 2026-04-20 | WATCH | Context Matters ADR (arXiv:2604.03826) | medium | No |
| 2026-04-19 | WATCH | TEA Protocol (arXiv:2506.12508) | medium | No |
| 2026-04-19 | WATCH | Orchestral AI (arXiv:2601.02577) | medium | No |
| 2026-04-19 | WATCH | Hierarchical RAG (arXiv:2604.14166) | medium | No |
| 2026-04-18 | WATCH | CoMAS (arXiv:2510.08529) | medium | No |
| 2026-04-17 | WATCH | Context Kubernetes (arXiv:2604.11623) | medium | No |
| 2026-04-17 | WATCH | MAE Self-Improve (arXiv:2510.23595) | medium | No |
| 2026-04-16 | WATCH | Adaptive Orchestration MoE (arXiv:2601.09742) | medium | No |
| 2026-04-16 | WATCH | MCP Planner-Executor (arXiv:2604.07681) | medium | No |
| 2026-04-15 | WATCH | CLEAR (arXiv:2604.07487) | medium | No |
| 2026-04-15 | WATCH | Verified Orchestration (arXiv:2603.11445) | medium | No |

## Archived Daily Scans (Apr 21-23, 2026)

### 2026-04-21 Morning Scan
- #104 CC Routines — cloud automations
- #105 Claude Opus 4.7 GA — 1M context, $5/$25
- #106 Compaction API + auto-caching beta

### 2026-04-22 arXiv Daily Digest
- [ACTION] Self-Optimizing Multi-Agent Systems (arXiv:2604.02988) — high
- [WATCH] Small Model as Master Orchestrator (arXiv:2604.17009) — medium
- [WATCH] CoCR-RAG (arXiv:2603.23989) — medium
- [WATCH] AgentForge (arXiv:2604.13120) — medium
- [WATCH] Adaptive Orchestration DMoE (arXiv:2601.09742) — medium

### 2026-04-22 Morning Watch
- #107 CC Ultraplan preview — cloud plan drafting
- #108 CC /resume 67% faster, /tui fullscreen, mobile push
- #109 API data residency (inference_geo) — US-only inference 1.1×

### 2026-04-23 arXiv Daily Digest
- [ACTION] Principled Context Engineering for RAG (arXiv:2511.17908) — high, conformal prediction
- [WATCH] CAMCO Safe MAS Orchestration (arXiv:2604.17240) — medium
- [WATCH] Single-Multi Evolution Loop (arXiv:2602.05182) — medium
- [WATCH] Smart Middleware (arXiv:2604.03430) — medium
- [WATCH] Context Kubernetes (arXiv:2604.11623) — medium

### 2026-04-23 Morning Watch
- #110 CC removed from Pro (test, ~2% users) — STOPA pricing impact
- #111 Claude Cowork GA — Analytics API + SCIM
- #112 CC prompt caching controls — 1h cache + Skill tool slash commands

## Archived Weekly Digest 2026-04-13

**Aktivita:** STOPA 10 commitů (deterministic gates, workspace validator). NG-ROBOT 10 commitů (pipeline fix, SEO). ADOBE 10 commitů (IDML Track Changes, DOCX export).
**Novinky:** Advisor Tool beta, Mythos/Capybara piloting. CC v2.1.94->v2.1.101 za týden.
**Poučení:** 34 nových learnings (Apr 5-8) — deception pod tlakem, auto-research, iterative refinement.
