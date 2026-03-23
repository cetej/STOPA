# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Only ACTION and WATCH items are recorded here.

## Last Scan

**2026-03-23** — full scan (all tiers — žádné nové action items, 2 watch)

**2026-03-22** — quick scan (Tier 1 only — 1 den od posledního full scanu)

**2026-03-21 (2)** — full scan (AI/ML ecosystem: PyTorch, Diffusers, video gen, Czech NLP)

## Active Items

### Action Items

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
   - Status: **DONE** — env var enabled in settings.json, /orchestrate deep tier updated with Teams workflow. Live testing pending on real task.

7. ~~**Diffusers 0.37.0** (Mar 5) — Modular Diffusers, FIBO Edit, Cosmos Predict2.5~~
   - Impact: medium for NG-ROBOT — modular pipelines, JSON-based image editing
   - Status: open

18. **CC v2.1.77** (Mar 17) — breaking + bug fixes
    - **BREAKING**: Agent tool `resume` parameter odstraněn — použij `SendMessage({to: agentId})` místo toho. STOPA skills SAFE (použití jen v textu, ne jako param).
    - `SendMessage` auto-resumes stopped agents (dříve chyba)
    - `--resume` opravuje race condition při truncation recent history
    - `claude plugin validate` kontroluje skill/agent/command frontmatter + `hooks/hooks.json`
    - `/fork` přejmenován na `/branch` (alias zachován)
    - Status: open — doporučení: použít `SendMessage` pro agent resumption

19. **API: Automatic caching** (Feb 19) — přidat `cache_control` do request body, systém posouvá cache point automaticky. Eliminuje manuální správu breakpointů. Dostupné na Claude API i Azure AI Foundry (preview).
    - Impact: medium — potenciální úspora nákladů v NG-ROBOT pipeline
    - Status: open — evaluate pro NG-ROBOT

20. **API: Sonnet 3.7 + Haiku 3.5 retired** (Feb 19) — `claude-3-7-sonnet-20250219` a `claude-3-5-haiku-20241022` vrací chyby. STOPA safe (aliases).
    - Status: SAFE — zkontrolováno, žádný hardcoded ID v STOPA

8. **Claude Code v2.1.79** — `/remote-control` VSCode bridge do claude.ai/code (browser/phone continuation), PreToolUse `deny` bug fix, streaming po řádcích
   - Impact: medium — remote monitoring orchestrovaných runs, bezpečnostní fix pro deny pravidla
   - Status: open

9. ~~**Extended thinking `display: "omitted"`**~~ (API) — vynechání thinking bloků z odpovědi pro rychlejší streaming, signatura zachována pro multi-turn
   - Impact: medium — ušetří tokeny v /orchestrate deep tier
   - Status: **DONE** — added to /orchestrate deep tier optimization section

10. **API code execution zdarma** při použití s web search nebo web fetch
    - Impact: low-medium — upravit budget kalkulace
    - Status: open (low priority, defer)

16. **Claude Code v2.1.81** (Mar 20) — nová verze po v2.1.80
    - `--bare` flag pro scripted `-p` volání (přeskočí hooks, LSP, plugin sync) — užitečné v CI/hooks
    - `--channels` permission relay — MCP channel servery mohou forwradovat tool approval prompty (např. na telefon)
    - **Windows: line-by-line streaming ZAKÁZÁN** (rendering issues) — uživatel na Win 11, může ovlivnit UX
    - Plugin ref-tracking: ref-tracked plugins re-clonují při každém loadu — může zpomalit STOPA plugin startup
    - MCP OAuth CIMD (SEP-991) podpora — pro MCP servery s OAuth
    - Plan mode skrývá "clear context" option by default
    - Fix: multiple concurrent CC sessions vyžadovaly opakovanou re-autentizaci
    - Impact: medium — Windows streaming change + `--bare` pro scripting
    - Status: open

17. **`source: 'settings'` skutečně existuje** (v2.1.80 CC changelog) — přidáno jako inline plugin deklarace
    - Naše learnings.md říká "agent hallucinated" — ale feature BYLA přidána v 2.1.80
    - Pravděpodobně: agent testoval před vydáním 2.1.80, nebo testoval špatně
    - github source funguje — žádná akce potřeba, ale learnings.md anti-pattern je nepřesný
    - Impact: low — informativní, stávající implementace ok
    - Status: open (low priority — update learnings.md)

12. **Claude Code v2.1.80** — nová verze po v2.1.79
    - ~~`source: 'settings'` pro plugin marketplace~~ — NEEXISTUJE (agent hallucinal, schema neobsahuje tento source typ)
    - `effort` frontmatter pro skills GA — `effort: high/medium/low/auto` v SKILL.md frontmatter
    - `rate_limits` v statusline skriptech — ukazuje využití rate limitů (5h/7d okna: session, weekly, weekly_sonnet)
    - `--channels` (research preview) — MCP servery mohou pushovat zprávy do session
    - Bug fix: `--resume` opravuje ztracené parallel tool results
    - ~80 MB méně paměti při startu na velkých repozitářích
    - Impact: medium — `effort` frontmatter + `rate_limits` relevantní, marketplace přes `github` source funguje
    - Status: **DONE** — marketplace implementován přes `github` source v settings.json (NG-ROBOT, ADOBE-AUTOMAT)

13. **1M kontext GA pro Sonnet 4.6** (March 13) — již GA, není potřeba beta header
    - Media limit zvýšen z 100 na 600 obrázků/PDF stran na 1M kontextu
    - Impact: low — pro nás bez změny, používáme 4.6 modely, limits se aplikují automaticky
    - Status: open (informativní, bez nutné akce)

14. **Claude Haiku 3 odchod** (April 19, 2026) — `claude-3-haiku-20240307` bude stažen
    - Naše skills používají alias `haiku` (ne hardcoded ID) → jsme safe
    - Impact: low — žádná akce potřeba v STOPA, aliases zůstávají funkční
    - Status: SAFE (zkontrolováno 2026-03-20 — žádný hardcoded claude-3-haiku v projektu)

15. **Models API capability fields** (March 18) — `GET /v1/models` vrací `max_input_tokens`, `max_tokens`, `capabilities`
    - Impact: low — potenciálně využitelné v /budget skill pro dynamické limity
    - Status: open (low priority)

11. **OpenClaw** — osobní AI agent runtime (250k+ GitHub stars, 5 700+ AgentSkills, messaging integrations)
    - Architektura: messaging gateway → LLM backend (Claude/GPT-4o/Ollama) → 5 700+ community skills
    - Relevance pro STOPA: různé paradigma (messaging-first vs coding-first), ale skills ekosystém architektonicky podobný
    - Bezpečnostní rizika: CVE-2026-25253 (CVSS 8.8 RCE), 12 % komunitních skills obsahuje malware
    - Governance: creator odešel do OpenAI (feb 2026), přechod na open-source foundation
    - Existují bridge pluginy: `openclaw-plugin-claude-code` (CC uvnitř OpenClaw), `openclaw-claude-code-skill` (MCP bridge)
    - **Verdict**: WATCH — potenciálně zajímavé jako distribution channel nebo mobile access layer, ale nyní nestabilní governance + security

### Watch List

9. **LTX-2.3** (Lightricks, Mar 5, 2026) — open-weights video model, 4K, ~50 FPS. Dostupný přes Diffusers LTX-Video pipeline.
   - Relevance: potenciální upgrade Pyramid Flow pro test1, video output pro NG-ROBOT
   - Status: WATCH — vyžaduje novější Diffusers než 0.37.0

10. **Google Flow redesign** (Feb/Mar 2026) — Google sloučil Whisk + ImageFX + Flow do jednoho workspace (Veo 3.1 + "Nano Banana"). Multi-clip sequencing, character consistency, lasso inpainting. Žádné veřejné API.
    - Relevance: ukázka směru SOTA video-gen UX, konkurenční kontext pro NG-ROBOT
    - Status: WATCH — sledovat až bude API

11. **Czech ABSA benchmarks** (arxiv 2602.22730, Feb 2026) — 19 LLMs benchmarkovano na Czech aspect-based sentiment. `ufal/robeczech-base` (Czech RoBERTa) na HuggingFace fine-tuned pro sentiment.
    - Relevance: potenciální upgrade ZACHVEV sentiment pipeline (Session 8) od `tabularisai/multilingual-sentiment-analysis`
    - Status: WATCH — evaluate v Session 8

1. **MCP elicitation** (v2.1.76) — servers request structured input mid-task via interactive dialog
   - Relevance: could enable interactive orchestration flows
5. **FlashAttention-4 + KernelAgent** (PyTorch blog, Mar 2026) — FA4 rychlejší attention, KernelAgent = multi-agent GPU kernel optimization
   - Relevance: potenciální zrychlení inference v NG-ROBOT
6. **Direction-Magnitude Decoupling** (ICLR 2026) — rychlá video generace přes flow matching s nižší výpočetní náročností
   - Relevance: potenciální vylepšení Pyramid Flow
7. **ViFeEdit** (Mar 16, 2026) — video generation + editing trénovaný jen na 2D obrázcích
   - Relevance: alternativní přístup k video editaci pro test1
2. **Flowception** — non-autoregressive variable-length video gen, 3x less FLOPs than full-sequence flows
   - Relevance: potential improvement over Pyramid Flow for test1
3. **Hook-enforced orchestration** — `barkain/claude-code-workflow-orchestration`
   - Relevance: competing pattern, stronger enforcement than convention-based
4. **MCP Memory Servers** — persistent memory via MCP instead of file-based
   - Relevance: alternative to our .claude/memory/ architecture
6. **`--channels` MCP preview** (v2.1.80) — MCP servery mohou pushovat zprávy do session proaktivně
   - Relevance: pokud by MCP server monitoroval NG-ROBOT pipeline, mohl by notifikovat přímo do session

7. **Seedance 2.0** (ByteDance) — nový video generation model, neoficiální API přístup dostupný na GitHubu
   - Relevance: alternativa k Pyramid Flow pro test1, mít na paměti

12. **Claude Code Channels** (v2.1.81) — Telegram/Discord integration přes `/telegram:configure`
    - Async push trigger model — uživatel může poslat instrukce z telefonu do CC session
    - Relevance: potenciální mobile/async trigger pro STOPA orchestraci, notification layer pro deep tier runs
    - Status: WATCH — sledovat stabilizaci, pak evaluovat pro STOPA

13. **MagCache + TaylorSeer** (Diffusers 0.37.0) — inference caching metody pro video gen pipelines
    - Relevance: zrychlení inference pro test1/Pyramid Flow
    - Status: WATCH — evaluovat při příštím test1 update

8. **PyTorch 2.10.0** (Jan 21, 2026) + MXFP8/MoE blog (Mar 15) — NG-ROBOT může benefitovat ze zrychlení
   - Relevance: dependency check pro NG-ROBOT (aktuálně na jaké verzi PyTorch?)

9. **LTX-2.3** (Lightricks, Mar 5, 2026) — open-weights video model, 4K, credibly production-quality open source
   - Lightricks popisuje jako "první open-weights model, který odstraňuje asterisk ve více dimenzích najednou"
   - Dostupné přes Diffusers (LTX-Video pipeline), ale LTX-2.3 je novější než verze v 0.37.0
   - Relevance: potenciální upgrade pro test1 (Pyramid Flow alternativa) a NG-ROBOT video výstup
   - GitHub: https://github.com/Lightricks/LTX-Video

10. **Google Flow** (redesign Feb/Mar 2026) — unified AI video workspace: Whisk + ImageFX + Veo 3.1 + Nano Banana
    - Multi-clip sequencing, character consistency, audio sync, lasso-based inpainting, natural language edits
    - Powered by Veo 3.1 — nejnovější Google video model, dostupný v Flow (ne jako API zatím)
    - Relevance: konkurenční landscape pro NG-ROBOT/test1 — ukazuje kam se ubírá SOTA video gen UX
    - Info: https://bonega.ai/en/blog/google-flow-march-2026-unified-ai-video-workspace

11. **Czech Aspect-Based Sentiment Analysis** (arxiv 2602.22730, Feb 2026) — benchmarks 19 LLMs pro Czech ABSA
    - Fine-tuned LLMs dosahují SOTA, ale menší ABSA modely překonávají general-purpose LLMs v zero/few-shot
    - BenCzechMark + CzechBench jsou aktivní benchmarking suites pro Czech LLM evaluaci
    - Relevance: ZACHVEV — sentiment pipeline používá `tabularisai/multilingual-sentiment-analysis`, ale existují lepší Czech-specific alternativy (RobeCzech fine-tuned pro sentiment)
    - Zvážit: evaluace RobeCzech (`ufal/robeczech-base`) jako případný upgrade sentimentu pro ZACHVEV

5. **OpenClaw** — 250k+ stars, 5 700+ AgentSkills, messaging integrations (WhatsApp/Telegram/Discord atd.)
   - Relevance: přímé propojení Claude Code ↔ OpenClaw přes bridge pluginy existuje. Distribution channel pro STOPA skills potenciálně zajímavý, ale security + governance blokují now.
   - Sledovat: stabilizaci governance po přechodu na foundation + opravy CVE

### Resolved Items

1. ~~Plugin System GA~~ — **DONE** (implemented in STOPA, v2.1.69+)
2. ~~`/loop` command~~ — **GA** (v2.1.71) — available now
3. ~~HTTP hooks~~ — **GA** (v2.1.63) — available now
4. ~~Token limit increase~~ — **CONFIRMED** (Opus 4.6: 64k default, 128k max output)

## Scan History

### 2026-03-23 — full scan (all tiers)
- CC: stále v2.1.81 — žádná nová verze, žádné nové API release notes
- **NEW WATCH**: Claude Code Channels (Telegram/Discord async triggers) — #12
- **NEW WATCH**: MagCache + TaylorSeer caching v diffusers 0.37.0 — #13
- Video gen landscape: Wan 2.2 + HunyuanVideo-1.5 vedou open-source, MAGI-1 + SkyReels emerging
- PyTorch blog: TorchSpec (speculative decoding), GDPA kernels — low relevance
- timm/einops: beze změn
- Czech NLP: nic nového

### 2026-03-22 — quick scan (Tier 1)
- CC: stále v2.1.81 — žádná nová verze
- API: žádné nové release notes od March 18
- Žádné nové položky k přidání

### 2026-03-21 (2) — full scan
- CC v2.1.77: Agent tool `resume` param odstraněn (STOPA safe), SendMessage auto-resume, plugin validate vylepšen
- API: Automatic caching GA (Feb 19), Sonnet 3.7 + Haiku 3.5 retired (safe — aliases)
- LTX-2.3 (Lightricks) — open-weights 4K video, Diffusers compatible
- Google Flow redesign — Veo 3.1, no public API yet
- Czech ABSA benchmarks (arxiv 2602.22730) — `ufal/robeczech-base` pro ZACHVEV sentiment

### 2026-03-21 — full scan (AI/ML ecosystem)
- CC v2.1.81: `--bare` flag, Windows streaming disabled, plugin ref-tracking, `--channels` relay, plan mode hide clear-context
- `source: 'settings'` confirmed real in v2.1.80 CC changelog — learnings.md anti-pattern was inaccurate
- Diffusers: no new release since 0.37.0 (Mar 5) — WAN 2.1 + LTX-Video 0.9.8 distilled in 0.37.0
- **NEW**: LTX-2.3 (Lightricks, Mar 5) — open-weights 4K production-quality video model (WATCH #9)
- **NEW**: Google Flow redesign (Feb/Mar 2026) — Whisk+ImageFX+Veo 3.1 unified workspace (WATCH #10)
- **NEW**: Czech ABSA LLM benchmarks (arxiv 2602.22730, Feb 2026) — RobeCzech potenciální upgrade pro ZACHVEV sentiment (WATCH #11)
- PyTorch blog: ExecuTorch edge deployment (Mar 5), Voice Agents (Mar 18) — low relevance pro naše projekty
- Flow matching/video gen: žádné nové signifikantní papery od ViFeEdit (Mar 16, tracked) a DMD (ICLR, tracked)
- Czech NLP: BenCzechMark + CzechBench aktivní, žádný nový model release tento týden

### 2026-03-20 — full scan
- CC v2.1.80: `effort` frontmatter GA, `rate_limits` statusline, `--channels` MCP preview, --resume bug fix, -80MB paměti
- `source: "settings"` hallucinated by agent — neexistuje ve schema. Použit `github` marketplace source místo toho.
- 1M kontext GA pro Sonnet 4.6 + Opus 4.6 (March 13) — bez beta headeru
- Haiku 3 retirement April 19, 2026 — STOPA safe (žádný hardcoded model ID)
- Models API vrací capability fields (March 18)
- Seedance 2.0 (ByteDance), PyTorch 2.10.0, einops 0.8.2, timm (Feb 23)
- **Implementováno**: marketplace.json + github source v settings.json pro NG-ROBOT a ADOBE-AUTOMAT

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

## Skipped Sources

<!-- Sources that consistently return nothing useful -->
