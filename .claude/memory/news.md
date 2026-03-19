# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Only ACTION and WATCH items are recorded here.

## Last Scan

**2026-03-19** — full (×2, odpolední scan)

## Active Items

### Action Items

1. ~~**Plugin `git-subdir` source type** (v2.1.69)~~ — **DONE** (plugin.json + README updated, v1.3.0)

2. **`${CLAUDE_PLUGIN_DATA}` persistent state** (v2.1.78) — plugin-specific storage surviving updates
   - Impact: medium — use for plugin memory instead of `.claude/memory/`
   - Status: open

3. **New hook events** (v2.1.69-76) — PostCompact, StopFailure, TaskCompleted implemented. InstructionsLoaded, TeammateIdle, Elicitation still open.
   - Impact: high — PostCompact, StopFailure, TaskCompleted now active
   - Status: **partially done** — 3/6 events implemented

4. **Skills frontmatter fields** (v2.1.69) — `model:` and `effort` now on all 11 skills. `maxTurns`, `disallowedTools`, `${CLAUDE_SKILL_DIR}` still unused.
   - Impact: high — per-skill model selection active (haiku/sonnet/opus assigned)
   - Status: **partially done** — model: + effort: done, maxTurns/disallowedTools open

5. ~~**`--plugin-dir` breaking change** (v2.1.76)~~ — **DONE** (README updated with repeated flags note)

6. **Agent Teams** — native parallel agent coordination (still research preview)
   - Impact: high for /orchestrate deep tier
   - Status: open — needs `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

7. **Diffusers 0.37.0** (Mar 5) — Modular Diffusers, FIBO Edit, Cosmos Predict2.5
   - Impact: medium for NG-ROBOT — modular pipelines, JSON-based image editing
   - Status: open

8. **Claude Code v2.1.79** — `/remote-control` VSCode bridge do claude.ai/code (browser/phone continuation), PreToolUse `deny` bug fix, streaming po řádcích
   - Impact: medium — remote monitoring orchestrovaných runs, bezpečnostní fix pro deny pravidla
   - Status: open

9. **Extended thinking `display: "omitted"`** (API) — vynechání thinking bloků z odpovědi pro rychlejší streaming, signatura zachována pro multi-turn
   - Impact: medium — ušetří tokeny v /orchestrate deep tier
   - Status: open

10. **API code execution zdarma** při použití s web search nebo web fetch
    - Impact: low-medium — upravit budget kalkulace
    - Status: open

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

### Resolved Items

1. ~~Plugin System GA~~ — **DONE** (implemented in STOPA, v2.1.69+)
2. ~~`/loop` command~~ — **GA** (v2.1.71) — available now
3. ~~HTTP hooks~~ — **GA** (v2.1.63) — available now
4. ~~Token limit increase~~ — **CONFIRMED** (Opus 4.6: 64k default, 128k max output)

## Scan History

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
