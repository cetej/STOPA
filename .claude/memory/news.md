# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Only ACTION and WATCH items are recorded here.
Archived items: `.claude/memory/news-archive.md`

## Last Scan

**2026-03-28** — quick scan (Claude Desktop v1.1.1931 Windows, CC v2.1.86)

## Active Items

### Action Items

37. **CC v2.1.86 (2026-03-27)** — Windows config corruption fix
    - Windows settings.json corruption fix (zbytečné disk writes)
    - `X-Claude-Code-Session-Id` header pro proxy agregaci
    - Fix: `--resume` s tool_use blocks; Write/Edit mimo project root
    - **Akce:** Spustit `npm update -g @anthropic-ai/claude-code` pro update na v2.1.86

38. **CC v2.1.84 — PowerShell tool (Windows opt-in preview)**
    - Claude Code umí spouštět PowerShell na Windows (vedle Bash)
    - Enable: `"powershellEnabled": true` v settings.json
    - **Akce:** Vyzkoušet pro Windows STOPA workflow

39. **Claude Desktop Windows — aktuální stav** (2026-03-28)
    - User má v1.1.1931 — relativně aktuální (Chocolatey má 1.1.1520, Mac je 1.1.8629 ale oddělená větev)
    - Computer Use v Cowork zatím **Mac only** — Windows pending
    - **Sledovat:** Computer Use na Windows → STOPA remote control potenciál

35. **CC v2.1.85** (2026-03-26 večer) — hooks podmínky + MCP vylepšení
    - **`if` podmínky v hooks** — `permission rule` syntax pro podmíněné spouštění (`if: "branch == 'main'"` apod.)
    - **`/compact` fix** — opraven crash "context exceeded" → přímý dopad na náš `/compact` skill
    - **`deniedMcpServers` fix** — správně blokuje claude.ai MCP servery
    - Timestamp markery v transkriptech pro scheduled tasks (`/loop`, `CronCreate`)
    - Deep link queries rozšířeny na 5 000 znaků
    - MCP OAuth: RFC 9728 Protected Resource Metadata discovery
    - Org policy blokuje zakázané pluginy
    - Memory leak fix v remote sessions
    - **Akce:** Prozkoumat `if` podmínky v hooks — mohlo by zjednodušit STOPA hook logiku (např. `FileChanged` jen pro `.py` soubory)

36. **⚠️ Haiku 3 deprecace** (deadline: 2026-04-19)
    - `claude-3-haiku-20240307` → retirement April 19, 2026
    - Migrovat na Haiku 4.5 (`claude-haiku-4-5-20251001`)
    - **Akce:** Zkontrolovat STOPA skills/hooks, kde je Haiku 3 hardcoded → nahradit Haiku 4.5

34. **🔥 Cloud Auto-Fix PRs + Scheduled Tasks** (CC Web, 2026-03-27) — Claude Code on the web auto-fix
    - Claude subscribes to GitHub events on a PR (CI failures, review comments), pushes fixes autonomously
    - Requires Claude GitHub App installed on repo
    - Trigger: web UI "Auto-fix" button, mobile command, or paste any PR URL
    - Behavior: clear fixes → auto-push; ambiguous → asks user; duplicates → skip
    - Replies to review comments under user's GitHub account (labeled "Claude Code")
    - **Scheduled Tasks** (cloud): recurring prompts on cron (hourly/daily/weekly), runs in isolated VM
      - Repos cloned fresh, pushes only to `claude/` branches by default
      - MCP connectors (Slack, Linear, Drive) available per-task
      - CLI: `/schedule`, web: claude.ai/code/scheduled
    - **`--remote` flag**: `claude --remote "prompt"` → creates cloud session, monitor via `/tasks`
    - **`/teleport`**: pull cloud session back to local terminal
    - **Akce:** Implementovat `/autofix` skill wrapper + přidat do `/fix-issue` flow

32. **🔥 AutoDream / `/dream`** (CC, v2.1.81+, PR #39299 stále open) — **EVALUATED 2026-03-26**
    - 4-phase background subagent (Orient, Gather Signal, Consolidate, Prune+Index), trigger: 24h + 5 sessions
    - Feature flag `tengu_onyx_plover` (rolling out), manuální `/dream` stále broken (PR #39299 not merged)
    - Known bugs: nepravdivé sumarizace (#38493), žádný log změn, identity confusion
    - **Verdict: KOEXISTENCE** — dream jako "janitor", STOPA `/scribe` jako "architekt" (YAML frontmatter, grep-first, archivace)
    - Ochranný HTML komentář přidán do MEMORY.md; eskalace: `autoDreamEnabled: false` pokud rozbíjí STOPA formát
    - Sledovat: PR #39299 merge → otestovat manuální `/dream` s STOPA strukturou

33. **Claude Mobile — Interactive Apps** (2026-03-25) — live charts, diagramy, shareable assets v konverzaci
    - Claude mobile teď renderuje interaktivní vizualizace přímo v chatu
    - Relevance: UI upgrade pro mobilní přístup k STOPA výstupům (watch reporty, scans)

30. **CC 2.1.84** (2026-03-26, dnes) — `TaskCreated` hook, `WorktreeCreate` hook (HTTP), PowerShell tool (Windows opt-in preview), MCP tool descriptions capped 2KB
    - `TaskCreated` hook: automatický trigger při vytvoření tasku → budget tracking
    - `WorktreeCreate` hook: HTTP type s `worktreePath` → orchestrace worktree agentů
    - **Akce:** Přidat nové hooks do STOPA hook registru; implementovat TaskCreated → budget auto-tracking

31. **CC 2.1.83** (2026-03-25) — `managed-settings.d/` drop-in, `CwdChanged`+`FileChanged` hooks, `initialPrompt` v agent frontmatter
    - `initialPrompt`: agenti mohou deklarovat bootstrap kontext v YAML frontmatter → zásadní zjednodušení sub-agent spawning
    - `FileChanged` hook: auto-trigger po editaci souboru → potenciální auto-critic
    - `managed-settings.d/`: drop-in directory pro enterprise managed settings
    - **Akce:** Experimentovat s `initialPrompt` pro STOPA sub-agenty; implementovat FileChanged → auto-critic hook

29. **Codified Context** (arXiv 2602.20478, Feb 2026) — infrastructure pro AI agenty v komplexním codebase
    - 3 komponenty: Hot-Memory Constitution (konvence + retrieval hooks), 19 domain agentů, Cold-Memory KB (34 on-demand docs)
    - Testováno 283 sessions, 108k řádků C#; open-source
    - STOPA analogy: `critical-patterns.md` = Hot-Memory, `learnings/` = Cold-Memory, ale chybí "retrieval hooks" vrstva
    - **Akce:** Přidat "Context Bootstrap" do `/orchestrate` skill — explicitní instrukce co číst pro daný task type

0. **🔥 Auto Mode** (CC, 2026-03-24, research preview) — nový permission mode `auto`
   - Claude sám rozhoduje o povolení tool calls, safeguard classifier kontroluje každou akci
   - Střední cesta mezi `default` (vše schvalovat) a `bypassPermissions` (vše přeskočit)
   - Enable: `claude --enable-auto-mode`, pak Shift+Tab pro přepnutí
   - Config: `autoMode.environment` (trusted infra), `autoMode.allow/soft_deny` (pravidla)
   - CLI: `claude auto-mode defaults`, `claude auto-mode config`, `claude auto-mode critique`
   - Dostupné na Team plan (research preview), Enterprise + API brzy
   - **Akce pro STOPA:**
     - Vyzkoušet auto mode v session — potenciálně nahradí manuální permission approvals
     - Nastavit `autoMode.environment` pro naše projekty (GitHub cetej/*, lokální cesty)
     - Scheduled tasks (morning-watch, daily-rebalancer) by mohly běžet bez pre-approve
     - Zvážit doporučení auto mode jako default pro STOPA orchestraci

0b. **Claude Computer Use on Mac** (2026-03-24, research preview) — Claude ovládá Mac (klik, psaní, scroll, apps)
   - Funguje v Claude Code i Cowork; nejdřív zkusí konektory (Gmail, Drive, Slack), pak screen control
   - Dostupné Pro/Max subscribers, jen macOS
   - ⚠️ My jsme Windows — zatím nepoužitelné, sledovat Windows podporu
   - Relevance: potenciální alternativa k MCP pro ovládání desktop aplikací (Adobe, browser)

0c. **Claude Dispatch** (~2026-03-17, research preview) — remote task assignment z iPhonu na Mac
   - QR párování, textuješ instrukce z telefonu → Claude vykonává na desktopu
   - Mac musí běžet s Claude app, Max/Pro subscribers
   - Relevance: alternativa k Telegram kanálu pro STOPA remote control (ale Mac only)

1. **`${CLAUDE_PLUGIN_DATA}` proměnná** (2026-03-23, v2.1.78) — plugin persistent state
   - stopa-orchestration plugin může ukládat state (budget, session data) bez souborů
   - Akce: zvážit při Plugin sync v2.0.0

2. **1M context window GA** (API, 2026-03-13) — Opus 4.6 + Sonnet 4.6, no beta header needed
   - Media limit raised 100→600 images per request
   - Akce: audit STOPA skills pro lingering `1m-context-beta` header references

3. **`thinking.display: "omitted"`** (API, 2026-03-16) — omit thinking blocks from streaming
   - Signature preserved for multi-turn, billing unchanged; up to 2.5× faster streaming
   - Akce: přidat do `/budget` skill jako cost-reduction lever pro thinking-heavy tasks

4. **Models API `capabilities` object** (API, 2026-03-18) — `GET /v1/models` vrací max_input_tokens, max_tokens, capabilities
   - Akce: zvážit v `/orchestrate` pro dynamic model selection

5. **⚠️ Haiku 3 retires April 19, 2026** — `claude-3-haiku-20240307` vrátí chybu za 3 týdny
   - Migrate to: `claude-haiku-4-5-20251001`
   - Akce: zkontrolovat NG-ROBOT, ADOBE-AUTOMAT, test1 pro hardcoded Haiku 3 model ID

6. **Opus 4.6 max output zvýšen** (CC, 2026-03-25) — default 64k tokens, upper bound 128k
   - Opus + Sonnet 4.6 obě na 128k upper bound
   - Akce: přezkoumat `/budget` skill — výchozí max_tokens pro Opus může být vyšší než předpoklad
   - Akce: zkontrolovat, zda STOPA skills explicitně limitují output (mohly by využít vyšší limit)

7. **HTTP hooks implementace** (CC v2.1.63+, GA) — webhook notifikace pro STOPA
   - Config: `"type": "http"` v hooks settings, POST s custom headers
   - ⚠️ TLS SNI bug (#30613) — HTTPS selhává, workaround: localhost proxy
   - ⚠️ URL nepodporuje env vars (#31653) — hardcode v `settings.local.json`
   - Akce: implementovat TaskCompleted → Slack webhook (localhost proxy + 10 řádků Python)

### Watch List

29k. **Luma AI Uni-1** (2026-03-05, API waitlist) — unified understanding+generation image model
    - Decoder-only autoregressive transformer (ne diffusion) — reasoning before rendering
    - #1 human preference Elo (Overall, Style & Editing, Reference-Based), #1 RISEBench (reasoning)
    - ~$0.09/image @ 2K (vs Nano Banana 2 $0.10, NB Pro $0.13)
    - Multi-reference (až 9 obrázků), manga/webtoon, novel view synthesis, multilingual text
    - API: waitlist na lumalabs.ai/uni-1, token pricing: input $0.50/M text, output $45.45/M images
    - Enterprise: Publicis, Adidas, Mazda; integrováno do Luma Agents (creative AI assistant)
    - Relevance: kandidát pro `/nano` skill až bude API veřejné; autoregressive přístup zásadně odlišný od Flux/SDXL/Gemini

29b. **Foveated Diffusion** (arXiv 2603.23491, 2026-03-24) — spatially adaptive video/image gen
    - Neuniformní token alokace (fovea = high-res, periferie = low-res), perceptually indistinguishable od full-res
    - Řeší quadratic complexity growth — praktická efektivita pro video gen
    - Kód nepotvrzený; sledovat pro test1 pipeline upgrade

29c. **FSVideo** (arXiv 2602.02092) — 14B DIT base + 14B upsampler, image-to-video
    - "Order of magnitude faster" než existující modely
    - Sledovat jako potenciální alternativa Pyramid Flow pro test1

29d. **"Beyond the Prompt"** (arXiv 2603.10000, Mar 2026) — ICL a CoT mechanismy
    - ICL zlepšuje výkon snížením prompt ambiguity (ne jen přidáváním příkladů)
    - CoT aktivuje task decomposition capabilities
    - Validuje STOPA `skill-files.md` design: jasné trigger conditions = lepší ICL

29h. **Workflow Optimization for LLM Agents** (arXiv 2603.22386, Mar 23) — taxonomie static vs. dynamic workflow structures
    - IBM Research + Rensselaer; unified taxonomy: predetermined vs. runtime-adaptive workflows
    - Evaluation criteria beyond simple task metrics
    - Relevance: přímo validuje STOPA static tier přiřazení, navrhuje dynamic runtime adaptation
    - Kód: ne

29i. ~~**Hyperagents**~~ → INFO (metacognitive agents, no code, covered by /autoloop)

29j. **Clinejection Attack** (Willison, Mar 6) — prompt injection přes GitHub issue titles → `claude-code-action`
    - Attack vector: issue titles → cache poisoning → code execution
    - Anti-pattern pro STOPA hooks dotýkající se GitHub Actions

29e. **Mem0** (trending Mar 19, 2026) — graph-based memory architektura pro LLM
    - Enhances long-term conversational coherence; z UCL
    - Potenciální inspirace pro STOPA memory: graph relationships mezi learnings files

29f. **claude-agent-sdk-python + claude-agent-sdk-typescript** — oddělené SDK repos s CHANGELOGy
    - github.com/anthropics/claude-agent-sdk-python (+ typescript verze)
    - Building blocks pro custom multi-agent orchestraci mimo CC

29g. **Gemini 3.1 Flash-Lite** — $0.25/M input, 1/8 ceny Gemini 3.1 Pro
    - Competitor ultra-cheap inference tier
    - Referenční bod pro STOPA cost tiers (Haiku $1/M vs Flash-Lite $0.25/M)

18. **Gemini 3.1 Pro** (2026-03-16) — 77.1% ARC-AGI-2, $2/$12 pricing (stejné jako Gemini 3 Pro)
    - Competitor benchmark benchmark leader — sledovat pro multi-provider srovnání
    - GATE: 1 ✅ 3 ✅, 2 ❌ → [WATCH]

19. **Papers with Code sunsetted** → HF Trending Papers — nová adresa: huggingface.co/papers/trending
    - Aktualizovat bookmarky a /watch skill references

20. **MCP lazy loading** (CC) — reduces context usage by up to 95% for MCP-heavy setups
    - Relevance: STOPA sessions s mnoha MCP servery — potenciálně velká úspora

21. **Wan2.1 + LTX Video 0.9.5** (Diffusers 0.37.0) — nové video modely v Diffusers
    - LTX Video 0.9.5 = upgrade LTX-2.3 (Watch #7) — sledovat pro test1 upgrade

1. **Claude Code Channels** (v2.1.81) — Telegram/Discord integration přes `/telegram:configure`
   - Async push trigger model — potenciální mobile/async trigger pro STOPA orchestraci
   - Sloučeno: `--channels` MCP preview (v2.1.80) — proaktivní push zprávy do session
   - **Update 2026-03-26**: Virální Mac Mini 24/7 pattern — SyncThing sync, LaunchAgent crash recovery
   - **CRITICAL**: Channels nemá message queue — zprávy ztraceny pokud session neběží
   - Detailed architecture zaznamenána v `learnings/2026-03-26-channels-24x7-architecture.md`

2. **`/context` actionable suggestions** (v2.1.74) — identifikuje memory bloat a context-heavy tools
   - Relevance: STOPA memory maintenance — CC nám řekne co zabírá kontext
   - Vyzkoušet: `/context` v session se zatíženou pamětí

3. **Memory file timestamps** (v2.1.75) — CC nyní uvažuje o "freshness" memory souborů
   - STOPA learnings mají `date:` v YAML frontmatter — to by mělo stačit
   - Sledovat: co přesně CC kontroluje (filename timestamp vs. frontmatter date)

4. **`autoMemoryDirectory` setting** (v2.1.74) — custom cesta pro memory storage
   - Relevance: plugin distribuce — memory mimo `.claude/` adresář
   - Zvážit pro stopa-orchestration plugin (spolu s `CLAUDE_PLUGIN_DATA`)

5. **`/remote-control`** (v2.1.79) — bridge CC session do claude.ai/code + VS Code tabs
   - Auto-generované AI tituly pro VS Code session tabs
   - Relevance: STOPA orchestrace napříč prostředími (desktop ↔ web IDE)

6. **GitHub Spec Kit** (github/spec-kit, 81k★) — Spec-Driven Development toolkit
   - Direct competitor to STOPA, spec-centric vs. STOPA execution-centric
   - Full analysis: `.claude/memory/competitive-spec-kit.md`

7. **LTX-2.3** (Lightricks, Mar 5) — open-weights 4K video model, Diffusers compatible
   - Relevance: potenciální upgrade Pyramid Flow pro test1, video output pro NG-ROBOT

8. **Czech ABSA benchmarks** (arxiv 2602.22730, Feb 2026) — `ufal/robeczech-base`
   - Relevance: potenciální upgrade ZACHVEV sentiment pipeline

22. **BOULDER** (arxiv 2603.20133, Mar 20) — LLM reasoning degrades in multi-turn dialogue vs. single-shot
    - CoT benchmarks overestimate real agent performance; gap driven by role conditioning + tool-use context
    - Relevance: STOPA sub-agents run multi-turn → consider single-shot calls for reasoning-heavy evals

23. **MCPAgentBench** (arxiv 2512.24565, Jan 2026) — first MCP tool-use benchmark with distractor tools
    - Measures tool discrimination ability in sandbox environment
    - Relevance: external validation for STOPA MCP setup; test `/scout` + `/orchestrate` tool selection
    - Code: GitHub ✅

24. **CARE** (arxiv 2603.00039, Mar 2026) — confounder-aware LLM-as-judge, 26.8% error reduction
    - Separates verbosity/style bias from actual quality signal across 12 benchmarks
    - Relevance: upgrade `/critic` scoring to remove judge bias
    - Code: GitHub ✅ (SprocketLab/CARE)

25. **ToolTree** (arxiv 2603.12740) — MCTS for tool planning, ~10% gain on benchmarks
    - Dual-feedback evaluator + bidirectional pruning of tool sequences
    - Relevance: STOPA orchestrate uses sequential planning → tree search could help complex tasks

26. **3× flow matching papers** (Mar 2026) — FastLightGen (2603.01685), Warm-Start FM (2603.19360), Transition FM (2603.15689)
    - FastLightGen: 30% param reduction + 4-step sampling
    - Warm-Start: draft samples instead of noise → guaranteed speedup
    - Transition FM: global transition flow → single-step generation
    - Relevance: collectively advancing faster video gen for test1 Pyramid Flow upgrade

27. **SWE-CI** (arxiv 2603.03823) — CI-loop benchmark for long-term codebase maintenance
    - 100 tasks, 233-day histories, 71 consecutive commits — tests maintainability not just one-shot fixes
    - Relevance: better eval framework for `/fix-issue` and `/tdd` skills

28. **ClarEval** (arxiv 2603.00187) — benchmark for agent ambiguity detection / clarification questions
    - Tests whether code agents ask vs. guess on ambiguous instructions
    - Relevance: `/brainstorm` skill should detect vague input and ask rather than assume

9. **OpenClaw / NemoClaw** — messaging-first AI agent runtime, 250k+ stars
   - NemoClaw = NVIDIA wrapper (OpenShell runtime + guardrails), GTC 2026-03-16, early preview
   - Sledovat: NemoClaw GA release, MCP server integrace

## Scan History

### 2026-03-27 — targeted scan (Claude Desktop update, CC v2.1.85)
### 2026-03-26 — targeted + full scans (AutoDream eval, CC 2.1.83-84, papers)
### 2026-03-25 — papers scan + full scan (Auto Mode, Opus 128k output, 7 papers)
### 2026-03-24 — hands-on research + full scan (Diffusers SKIP, PyTorch WAIT, HTTP hooks GA)
### 2026-03-23 — 2× full scan (CHANGELOG deep-dive, batch cleanup of 7 items)

Older scan history: see `news-archive.md`

## Skipped Sources

<!-- Sources that consistently return nothing useful -->
