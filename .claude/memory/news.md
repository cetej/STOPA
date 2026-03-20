# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Only ACTION and WATCH items are recorded here.

## Last Scan

**2026-03-20** — full scan

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

8. **Claude Code v2.1.79** — `/remote-control` VSCode bridge do claude.ai/code (browser/phone continuation), PreToolUse `deny` bug fix, streaming po řádcích
   - Impact: medium — remote monitoring orchestrovaných runs, bezpečnostní fix pro deny pravidla
   - Status: open

9. ~~**Extended thinking `display: "omitted"`**~~ (API) — vynechání thinking bloků z odpovědi pro rychlejší streaming, signatura zachována pro multi-turn
   - Impact: medium — ušetří tokeny v /orchestrate deep tier
   - Status: **DONE** — added to /orchestrate deep tier optimization section

10. **API code execution zdarma** při použití s web search nebo web fetch
    - Impact: low-medium — upravit budget kalkulace
    - Status: open (low priority, defer)

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

8. **PyTorch 2.10.0** (Jan 21, 2026) + MXFP8/MoE blog (Mar 15) — NG-ROBOT může benefitovat ze zrychlení
   - Relevance: dependency check pro NG-ROBOT (aktuálně na jaké verzi PyTorch?)

5. **OpenClaw** — 250k+ stars, 5 700+ AgentSkills, messaging integrations (WhatsApp/Telegram/Discord atd.)
   - Relevance: přímé propojení Claude Code ↔ OpenClaw přes bridge pluginy existuje. Distribution channel pro STOPA skills potenciálně zajímavý, ale security + governance blokují now.
   - Sledovat: stabilizaci governance po přechodu na foundation + opravy CVE

### Resolved Items

1. ~~Plugin System GA~~ — **DONE** (implemented in STOPA, v2.1.69+)
2. ~~`/loop` command~~ — **GA** (v2.1.71) — available now
3. ~~HTTP hooks~~ — **GA** (v2.1.63) — available now
4. ~~Token limit increase~~ — **CONFIRMED** (Opus 4.6: 64k default, 128k max output)

## Scan History

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
