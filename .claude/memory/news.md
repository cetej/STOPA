# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Only ACTION and WATCH items are recorded here.
Archived items: `.claude/memory/news-archive.md`

## Last Scan

**2026-03-23** — full scan #2 (CHANGELOG deep-dive)

## Active Items

### Action Items

1. **`effort` frontmatter pro skills** (2026-03-23, v2.1.80) — nový YAML klíč v SKILL.md
   - Status: DONE — verify→high, scout→low (critic/orchestrate/scribe already set)

2. **PreToolUse security fix — ověřit Dippy** (2026-03-23, v2.1.77)
   - Status: DONE — Dippy funguje. Fix se týká `deny` rules, které STOPA nepoužívá.

3. **`${CLAUDE_PLUGIN_DATA}` proměnná** (2026-03-23, v2.1.78) — plugin persistent state
   - stopa-orchestration plugin může ukládat state (budget, session data) bez souborů
   - Akce: zvážit při Plugin sync v2.0.0

### Watch List

7. **GitHub Spec Kit** (github/spec-kit, 81k★) — Spec-Driven Development toolkit
   - Official GitHub repo, 27 AI agents supported, extension/preset marketplace
   - Pipeline: specify → clarify → plan → tasks → analyze → implement
   - Relevance: direct competitor to STOPA orchestration, faster growth (81k★ in 7 months)
   - Key differentiator: spec-centric (documents drive code) vs STOPA execution-centric
   - Adopted patterns: constitution, handoff metadata, checklist reframe
   - Full analysis: `.claude/memory/competitive-spec-kit.md`

1. **Claude Code Channels** (v2.1.81) — Telegram/Discord integration přes `/telegram:configure`
   - Async push trigger model — potenciální mobile/async trigger pro STOPA orchestraci
   - Sloučeno: `--channels` MCP preview (v2.1.80) — proaktivní push zprávy do session

2. **LTX-2.3** (Lightricks, Mar 5) — open-weights 4K video model, Diffusers compatible
   - Relevance: potenciální upgrade Pyramid Flow pro test1, video output pro NG-ROBOT
   - GitHub: https://github.com/Lightricks/LTX-Video

3. **Czech ABSA benchmarks** (arxiv 2602.22730, Feb 2026) — `ufal/robeczech-base`
   - Relevance: potenciální upgrade ZACHVEV sentiment pipeline

4. **OpenClaw / NemoClaw** — messaging-first AI agent runtime, 250k+ stars
   - NemoClaw = NVIDIA wrapper (OpenShell runtime + guardrails), announced GTC 2026-03-16, early preview
   - Sledovat: NemoClaw GA release, MCP server integrace, opravy CVE
   - Zájem: autonomous 24/7 agenti mimo Claude Code sessions

5. **Seedance 2.0** (ByteDance) — video generation model

6. **MagCache + TaylorSeer** (Diffusers 0.37.0) — inference caching pro video gen

8. **`PostCompact` hook** (v2.1.76) — fires after context compaction
   - Potenciální použití: cleanup memory nebo refresh state po automatické kompakci
   - Zatím bez akce, sledovat

9. **`Elicitation` + `ElicitationResult` hooks** (v2.1.76) — MCP interactive dialogs
   - MCP servery mohou zobrazovat strukturované formuláře uživateli mid-task
   - Sledovat: může nahradit některé skill prompting vzory

10. **PyTorch 2.11** (released 2026-03-23) — dnes vydáno, features zatím neznámé
    - Relevance: NG-ROBOT závisí na PyTorch — sledovat release notes

## Scan History

### 2026-03-23 — full scan #2 (CHANGELOG deep-dive)
- CC CHANGELOG fetched — nalezeny 3 nové ACTION items (effort, PreToolUse fix, PLUGIN_DATA)
- NEW WATCH: PostCompact hook, Elicitation hooks, PyTorch 2.11
- DONE item (spec-kit) zůstává pro kontext, přesunout do archivu při dalším cleanup

### 2026-03-23 — full scan (all tiers)
- CC: stále v2.1.81 — žádná nová verze, žádné nové API release notes
- NEW WATCH: Claude Code Channels, MagCache + TaylorSeer
- **Batch cleanup**: 7 action items zpracováno a archivováno, watch list přečíslován (10→6 items)

## Skipped Sources

<!-- Sources that consistently return nothing useful -->
