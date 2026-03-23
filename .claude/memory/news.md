# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Only ACTION and WATCH items are recorded here.
Archived items: `.claude/memory/news-archive.md`

## Last Scan

**2026-03-23** — full scan (all tiers — žádné nové action items, 2 watch)

## Active Items

### Action Items

7. **Diffusers 0.37.0** (Mar 5) — Modular Diffusers, FIBO Edit, Cosmos Predict2.5
   - Impact: medium for NG-ROBOT — modular pipelines, JSON-based image editing
   - Status: open

8. **Claude Code v2.1.79** — `/remote-control` VSCode bridge, PreToolUse `deny` bug fix, streaming po řádcích
   - Impact: medium — remote monitoring orchestrovaných runs, bezpečnostní fix pro deny pravidla
   - Status: open

10. **API code execution zdarma** při použití s web search nebo web fetch
    - Impact: low-medium — upravit budget kalkulace
    - Status: open (low priority, defer)

16. **Claude Code v2.1.81** (Mar 20)
    - `--bare` flag pro scripted `-p` volání (přeskočí hooks, LSP, plugin sync)
    - `--channels` permission relay — MCP channel servery mohou forwradovat tool approval prompty
    - **Windows: line-by-line streaming ZAKÁZÁN** (rendering issues)
    - Plugin ref-tracking: re-clonují při každém loadu
    - Impact: medium — Windows streaming change + `--bare` pro scripting
    - Status: open

17. **`source: 'settings'` skutečně existuje** (v2.1.80) — přidáno jako inline plugin deklarace
    - Impact: low — informativní, stávající implementace ok
    - Status: open (low priority — update learnings.md)

18. **CC v2.1.77** (Mar 17) — breaking + bug fixes
    - **BREAKING**: Agent tool `resume` parameter odstraněn — použij `SendMessage({to: agentId})`
    - Status: open — doporučení: použít `SendMessage` pro agent resumption

19. **API: Automatic caching** (Feb 19) — přidat `cache_control` do request body
    - Impact: medium — potenciální úspora nákladů v NG-ROBOT pipeline
    - Status: open — evaluate pro NG-ROBOT

### Watch List

9. **LTX-2.3** (Lightricks, Mar 5, 2026) — open-weights 4K video model, Diffusers compatible
   - Relevance: potenciální upgrade Pyramid Flow pro test1, video output pro NG-ROBOT
   - GitHub: https://github.com/Lightricks/LTX-Video

10. **Google Flow** (redesign Feb/Mar 2026) — unified AI video workspace: Whisk + ImageFX + Veo 3.1 + Nano Banana
    - Multi-clip sequencing, character consistency, natural language edits. Žádné veřejné API.

11. **Czech ABSA benchmarks** (arxiv 2602.22730, Feb 2026) — `ufal/robeczech-base` pro ZACHVEV sentiment
    - Relevance: potenciální upgrade sentiment pipeline v Session 8

5. **OpenClaw** — 250k+ stars, messaging-first paradigma, bridge pluginy s CC
   - Relevance: potenciálně zajímavé jako distribution channel, ale security + governance blokují
   - Sledovat: stabilizaci governance + opravy CVE

6. **`--channels` MCP preview** (v2.1.80) — MCP servery mohou pushovat zprávy do session proaktivně

7. **Seedance 2.0** (ByteDance) — nový video generation model

12. **Claude Code Channels** (v2.1.81) — Telegram/Discord integration přes `/telegram:configure`
    - Async push trigger model — potenciální mobile/async trigger pro STOPA orchestraci

13. **MagCache + TaylorSeer** (Diffusers 0.37.0) — inference caching metody pro video gen pipelines

15. **Models API capability fields** (March 18) — `GET /v1/models` vrací `max_input_tokens`, `capabilities`

13. **1M kontext GA pro Sonnet 4.6** (March 13) — již GA, media limit zvýšen z 100 na 600 obrázků
    - Status: open (informativní, bez nutné akce)

## Scan History

### 2026-03-23 — full scan (all tiers)
- CC: stále v2.1.81 — žádná nová verze, žádné nové API release notes
- **NEW WATCH**: Claude Code Channels (Telegram/Discord async triggers) — #12
- **NEW WATCH**: MagCache + TaylorSeer caching v diffusers 0.37.0 — #13

### 2026-03-22 — quick scan (Tier 1)
- CC: stále v2.1.81 — žádná nová verze
- API: žádné nové release notes od March 18

### 2026-03-21 (2) — full scan
- CC v2.1.77: Agent tool `resume` param odstraněn (STOPA safe), SendMessage auto-resume, plugin validate vylepšen
- API: Automatic caching GA (Feb 19), Sonnet 3.7 + Haiku 3.5 retired (safe — aliases)
- LTX-2.3, Google Flow redesign, Czech ABSA benchmarks

## Skipped Sources

<!-- Sources that consistently return nothing useful -->
