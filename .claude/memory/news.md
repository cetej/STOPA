# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Only ACTION and WATCH items are recorded here.
Archived items: `.claude/memory/news-archive.md`

## Last Scan

**2026-03-26** — full scan (all tiers)

## Active Items

### Action Items

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

10. **`PostCompact` hook** (v2.1.76) — fires after context compaction
    - Potenciální použití: cleanup memory nebo refresh state po automatické kompakci

11. **`Elicitation` + `ElicitationResult` hooks** (v2.1.76) — MCP interactive dialogs
    - MCP servery mohou zobrazovat strukturované formuláře uživateli mid-task

12. **PyTorch 2.11** (released 2026-03-23) — **EVALUATED 2026-03-24**
    - FlexAttention = compiler-driven API pro arbitrary attention patterns, FA4 backend jen H100/B200
    - FA4 backend explicitně "expect breaking changes" — není production-safe
    - Migrace z SDPA = 1-2 dny (dynamic=False, block_mask caching, no dropout)
    - **Verdict: WAIT do PyTorch 2.12 (~květen 2026). Prototypovat attention patterns na Triton path teď.**

13. **MagCache + TaylorSeer** (Diffusers 0.37.0) — inference caching pro video gen

14. **Seedance 2.0** (ByteDance) — video generation model

15. **Mistral Small 4** (Apache 2.0, 119B, 2026-03-17) — unifikovaný model: reasoning (Magistral) + multimodal (Pixtral) + agentic coding (Devstral)
    - Potenciální open-weights alternativa pro STOPA standard/deep tier subagenty

16. **Flowception + Direction-Magnitude Decoupling** (ICLR 2026) — dvě paper na rychlejší/lepší flow matching video gen
    - Flowception: non-autoregressive, variable-length, 3× méně FLOPs vs AR
    - DMD: lightweight magnitude capture + directional caching
    - Relevance: potenciální upgrade Pyramid Flow na test1

17. **Veo 3.1** (Google) — video generation model, dostupný přes ComfyUI custom nodes + fal.ai/muapi
    - Relevance: sledovat pro video gen pipeline upgrade

## Scan History

### 2026-03-26 — full scan (all tiers)
- Tier 1: žádné nové CC/API updates od včerejšího scanu; Agent SDK repos (python/typescript) identifikovány
- Tier 2: PyTorch/Diffusers — žádné nové verze od 2.11/0.37.0; Gemini 3.1 Flash-Lite ($0.25/M) jako nový WATCH
- Tier 2b: 3 nové WATCH papers — Codified Context (ACTION, open-source), Foveated Diffusion, FSVideo
- Tier 2b: Beyond the Prompt (2603.10000) — validuje STOPA skill description design
- Tier 3: žádné nové trending repos nad rámec OpenClaw (known); Reddit bez výsledků
- Tier 4: Mem0 trending (graph-based memory); Gemini Flash-Lite; prompt injection awareness (Karpathy+Willison)
- Key insight: Codified Context paper potvrzuje STOPA architekturu, ale identifikuje mezeru — chybějící retrieval hooks

### 2026-03-25 — papers scan (Tier 1 + Tier 2b)
- Tier 1: žádné nové CC/API updates od včerejšího full scanu
- Tier 2b: 7 nových papers — 3 ACTION (BOULDER, MCPAgentBench, CARE), 4 WATCH
- Key insight: BOULDER shows multi-turn dialogue degrades reasoning → review STOPA sub-agent architecture
- Code gen: SWE-CI (CI-loop benchmark), ClarEval (ambiguity detection), ToolTree (MCTS planning)
- Video gen: 3× flow matching papers (FastLightGen, Warm-Start, Transition FM)

### 2026-03-25 — full scan (all tiers)
- **🔥 AUTO MODE** — nový CC permission mode (research preview, 2026-03-24), safeguard classifier
- **Computer Use on Mac** — Claude ovládá desktop (klik, psaní, apps), research preview, macOS only
- **Dispatch** (~Mar 17) — remote tasks z iPhonu na Mac, QR párování, Pro/Max
- CC: v2.1.81 stále nejnovější verze; auto mode je feature, ne nová verze CC
- SECURITY: malicious litellm 1.82.7/1.82.8 (credential stealer) → naše projekty litellm nepoužívají → SAFE
- NEW ACTION: Opus 4.6 64k default output / 128k upper bound
- NEW WATCH: Gemini 3.1 Pro (ARC-AGI-2 77.1%), Wan2.1 v diffusers, LTX Video 0.9.5
- NEW WATCH: Papers with Code sunsetted → HF Trending Papers, MCP lazy loading (95% context reduction)
- INFO: Karpathy autoresearch scaled to 910 experiments/8h on Kubernetes

### 2026-03-24 — hands-on research (3 items evaluated)
- Modular Diffusers 0.37.0 → SKIP (Pyramid Flow incompatible, 2 hard env konflikty)
- HTTP hooks v CC → IMPLEMENT NOW (GA od v2.1.63, TLS bug workaround via localhost proxy)
- PyTorch 2.11 FlexAttention → WAIT (FA4 backend nestabilní, H100/B200 only)

### 2026-03-24 — full scan (all tiers)
- Tier 1: API — 3 nové ACTION (1M GA, thinking.display, Models capabilities) + urgent Haiku 3 retirement (Apr 19)
- Tier 2: PyTorch 2.11 features potvrzeny (FlexAttention + FA4), Modular Diffusers 0.37.0 → ACTION
- Tier 3/4: Mistral Small 4, Flowception, Veo 3.1, HTTP hooks → WATCH
- INFO: Cursor Composer 2, MALUS satire (Willison), AI dev productivity stats (19% slowdown)

### 2026-03-24 — quick scan (desktop claude updates)
- Verze: stále v2.1.81 (Mar 21) — žádná nová verze
- DONE items archivovány (effort frontmatter, PreToolUse fix, Spec Kit)
- NEW WATCH: /context suggestions, memory timestamps, autoMemoryDirectory, /remote-control
- INFO: effort "max" odstraněn v v2.1.72 — STOPA nepoužívá "max" → bez dopadu

### 2026-03-23 — full scan #2 (CHANGELOG deep-dive)
- CC CHANGELOG fetched — nalezeny 3 nové ACTION items (effort, PreToolUse fix, PLUGIN_DATA)
- NEW WATCH: PostCompact hook, Elicitation hooks, PyTorch 2.11

### 2026-03-23 — full scan (all tiers)
- CC: stále v2.1.81 — žádná nová verze, žádné nové API release notes
- NEW WATCH: Claude Code Channels, MagCache + TaylorSeer
- **Batch cleanup**: 7 action items zpracováno a archivováno

## Skipped Sources

<!-- Sources that consistently return nothing useful -->
