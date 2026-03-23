# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Only ACTION and WATCH items are recorded here.
Archived items: `.claude/memory/news-archive.md`

## Last Scan

**2026-03-23** — full scan + spec-kit competitive analysis

## Active Items

### Action Items

1. **Adopt spec-kit patterns** (2026-03-23) — 3 patterns z github/spec-kit adoptováno
   - Constitution check (orchestrate, brainstorm, critic), handoff metadata (4 skills), checklist reframe (critic --spec)
   - Status: DONE — plugin v1.9.0

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

4. **OpenClaw** — messaging-first AI agent runtime, 250k+ stars
   - Sledovat: stabilizaci governance + opravy CVE před evaluací

5. **Seedance 2.0** (ByteDance) — video generation model

6. **MagCache + TaylorSeer** (Diffusers 0.37.0) — inference caching pro video gen

## Scan History

### 2026-03-23 — full scan (all tiers)
- CC: stále v2.1.81 — žádná nová verze, žádné nové API release notes
- NEW WATCH: Claude Code Channels, MagCache + TaylorSeer
- **Batch cleanup**: 7 action items zpracováno a archivováno, watch list přečíslován (10→6 items)

## Skipped Sources

<!-- Sources that consistently return nothing useful -->
