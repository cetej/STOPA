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
