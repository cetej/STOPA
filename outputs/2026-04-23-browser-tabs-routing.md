---
date: 2026-04-23
parent: 2026-04-23-browser-tabs-research.md
scope: Routing decisions + deep-dive findings + /watch postmortem
method: 4 parallel deep-dive agents (papers, tier-1 repos, tier-2 repos, watch-postmortem)
---

# Browser Tabs Routing Report — 2026-04-23

Deeper analysis s konkrétními routing decisions. Parent report: [outputs/2026-04-23-browser-tabs-research.md](2026-04-23-browser-tabs-research.md).

## Routing distribuce (13 findings)

| Decision | Count | Items |
|----------|-------|-------|
| `implement-now` | 2 | Jena falsification gate, DeepMind attack learning |
| `implement-gradual` | 2 | TACO compact, gbrain pattern extraction |
| `pilot-eval` | 3 | llm-wiki-compiler, context-mode, semantica (updated) |
| `cross-project` | 4 | worldmonitor→MONITOR+ZACHVEV, hyperframes→NG-ROBOT, DeepMind→MONITOR, claude-context→NG-ROBOT |
| `knowledge-only` | 2 | UCSD 2.1 steps, Sakana AC/DC |
| `watch` | 2 | DeepTutor, heygen skill structure |
| `discard` | — | (from parent report: free-claude-code, awesome-claude-design, KVCache, Token 101) |

---

## Papery — deep-dive results (5)

### 1. 🔴 **LLM Agents Ignore Evidence** — 68%/26% confirmation bias (25K runs)
**Score: 9.5/10 — `implement-now` (S effort)**

- **Empirie:** 25 000 agent runs, 8 domén, 11 LLMs. 68% tras ignoruje evidence, 26% provádí refutation-driven belief revision, 7% nezávislých evidence lines. Counter-example prompting zvedá rule discovery 42→56%. Base model variance 41.4% vs scaffold 1.5% (model > framework).
- **Action:** Edit `.claude/skills/autoresearch/SKILL.md` — přidat mandatory "Falsification Step" PŘED každou iterací: explicit zápis *"What evidence would refute current hypothesis? Did I seek it?"*. Counter-example prompting pattern jako Phase 2.5. Kritický learning s `maturity: core` kandidát.
- **Effort:** S (30min-2h)

### 2. 🔴 **DeepMind 6 Attack Vectors** — "Can't sanitize a pixel"
**Score: 8.5/10 — `cross-project` + `implement-now` (XS + M effort)**

- **Core:** Franklin et al. (SSRN March 2026) — 6 kategorií: Content Injection (86% success), Semantic Manipulation, Cognitive State (80%+ RAG poisoning), Behavioural Control (58-93%), Systemic, HITL. Steganography (LSB) v obrázcích = extracting injected instructions invisibly.
- **Action A (STOPA XS):** `/scribe` high-severity learning `2026-04-23-agent-attack-vectors.md` — type=architecture, severity=critical, tags=[security, fetch, browse, ingest]. verify_check povinně.
- **Action B (Cross-project M):** `/improve` route do **MONITOR** (highest OSINT exposure) + **NG-ROBOT** (external content): GitHub issue "Input sanitization layer per DeepMind 6-vector framework (HTML comments, CSS-hidden text as priority)."
- **Effort:** XS+M (2-8h pro PoC)

### 3. 🟡 **TACO** — Self-Evolving Context Compression ([arXiv:2604.19572](https://arxiv.org/abs/2604.19572))
**Score: 7/10 — `implement-gradual` (M effort)**

- **Core:** Plug-and-play framework který automaticky objevuje compression rules z trajectories místo fixních heuristik. 10% token reduction (MiniMax-2.5), 1-4% perf improvement, 2-3% accuracy gain při stejném budget. TerminalBench, SWE-Bench Lite, CompileBench, DevEval, CRUST-Bench.
- **Action:** Rozšířit `/compact` o experimentální mode — čte `outcomes/` + `farm-ledger.md`, extrahuje opakující se nízkohodnotové patterns (npm install logs, test outputs), navrhne compression rules jako learnings. Start: jeden konkrétní PoC pattern.
- **Effort:** M (2-8h)

### 4. 🟢 **Professional Devs Don't Vibe** — 2.1 steps ([arXiv:2512.14012](https://arxiv.org/abs/2512.14012))
**Score: 6/10 — `knowledge-only` (XS effort)**

- **Core:** UCSD + Cornell (Huang et al.), N=13 observed + N=99 surveyed. Experienced devs delegují max **2.1 kroků** před validací. Externí empirická validace STOPA orchestrate (budget tiers + critic gate per 2 rounds).
- **Action:** `/scribe` learning `2026-04-23-ucsd-field-study-validation.md` — tag `orchestration-validation`, citation hotová pro budoucí `behavioral-genome.md § Verification` update.
- **Effort:** XS (<30min)

### 5. 🟢 **Sakana AC/DC** — Task-Capability Coevolution (ICLR 2026, [OpenReview](https://openreview.net/forum?id=efNINVs2So))
**Score: 5/10 — `knowledge-only` (S scribe effort)**

- **Core:** Coevolution LLM modelů (merging/mutation) + úkolů (synthetic data). Archive stepping stones, ne single-run improvement. Broader expertise coverage BEZ explicit benchmark optimization.
- **Action:** `/scribe` learning: "AC/DC archive pattern = keep multiple versions skillu v `.claude/skills/<name>/versions/` se success metrics. Prerequisite: 3+ skills se self-evolve historií. Čekat." Předčasné implementovat.
- **Effort:** S scribe, L implement (deferred)

---

## Repos — deep-dive results (8)

### 1. 🔴 **garrytan/gbrain** — Minions + self-wiring graph (10.6k⭐)
**Score: 8/10 — `implement-gradual` (S+M)**

- **Klíčová evidence:** Production-proven (Garry Tan's personal infra, 17,888 pages, 21 cron jobs, 12 days built). Published benchmark: **753ms vs 10s timeout, $0 vs $0.03/run, 100% vs 0% success under gateway load**. n=1 ale konkrétní.
- **2 extractable patterns:**
  - (a) Self-wiring graph via regex cascade (typed relations: FOUNDED → INVESTED → ADVISES) — zero LLM calls pro edge extraction
  - (b) Postgres durable queue (FOR UPDATE SKIP LOCKED, 3 retries exp backoff, cascade cancel)
- **Mapping na STOPA:**
  - Minions rule "deterministic → queue, judgment → subagents" = empirická validace STOPA `farm` tier
  - Self-wiring = upgrade `/ingest` auto-populate concept-graph.json (currently LLM-based)
  - Durable queue = optional farm tier enhancement (feature-flagged)
- **Action:**
  1. `/scribe` learning `2026-04-23-gbrain-validates-farm-tier.md` s 753ms vs 10s benchmark jako rationale
  2. `/improve` cross-project: propose self-wiring-graph do NG-ROBOT, MONITOR, 2BRAIN
  3. Radar: add entry 8/10
  4. Port regex cascade do Python (S effort) pro `/ingest`
- **NEPŘIJÍMAT gbrain jako celek** — 30 MCP tools, Bun runtime, Postgres dep = too heavy

### 2. 🔴 **koala73/worldmonitor** — Intel dashboard (52k⭐)
**Score: 8/10 — `cross-project` (M+S)**

- **CII formula:** `baseline × 0.4 + event × 0.6`, event = unrest 25% + conflict 30% + security 20% + info 25%. Log-damping, conflict floors. Composite risk: `convergence × 0.3 + CII × 0.5 + infra × 0.2 + theater/breaking boosts`.
- **Trending spike detection:** 5+ mentions AND 3× over 7d baseline AND 2+ sources AND 30min cooldown.
- **Cable health:** exponential decay λ = ln(2)/168h.
- **Stack:** TS + Vite + Tauri (Rust) + MapLibre/globe.gl/deck.gl + 65+ data sources + 60+ Vercel Edge Functions + Convex/Redis. **AGPL-3.0 non-commercial** = blocker pro commercial track projekty, **ale algoritmy jsou idea-level fair use**.
- **Action:**
  1. `/improve` → **MONITOR**: CII formulace + 4-component event score
  2. `/improve` → **ZACHVEV**: spike detection threshold (5+ AND 3× AND 2+ AND 30min)
  3. Radar add 8/10 (výrazně vyšší než existing items)
- **NE** kopírovat kód — re-implementovat algoritmy v Python/Rust dle MONITOR/ZACHVEV stacku.

### 3. 🔴 **mksglu/context-mode** — FTS5 intent-driven filtering MCP (9k⭐)
**Score: 9/10 — `pilot-eval` (S)**

- **Zásadní rozlišení proti `/compact`:** NE LLM summarization. **Intent-driven FTS5 filtering**: output >5KB + intent → SQLite BM25+Porter indexace v sandboxu, vrátí se jen matching sections. Raw výstup nikdy nevstoupí do context window. 24h TTL cache per-project. Sandboxed subprocess 11 languages. Truncation 60% začátek + 40% konec.
- **Benchmark:** 315KB→5.5KB (98% reduction v 21 scénářích).
- **Stack:** TS, 12 platforms supported (CC, Gemini CLI, Copilot, Cursor, ...). ELv2 OK pro interní use.
- **Filosofický contrast:** STOPA `/compact` = lossy summarization (Haiku), context-mode = lossless indexed retrieval. Odlišný use-case.
- **Action:**
  1. Install: `/plugin marketplace add mksglu/context-mode` → `/plugin install context-mode@context-mode` v isolated sandbox
  2. Side-by-side: run 1× `/scout` + 1× `/deepresearch` s/bez. Měř token consumption + retrieval quality + latency
  3. Pokud >50% úspora bez quality loss → nahradit část STOPA `/compact`. Jinak dokumentovat divergent design
  4. Learning: "lossy vs lossless compaction tradeoff"
- **Effort:** S (1h)
- **Risk:** SessionStart hook konflikt možný

### 4. 🔴 **heygen-com/hyperframes** — HTML→MP4 deterministic (9.5k⭐, release DNES)
**Score: 8/10 — `implement-now` + `cross-project` (S)**

- **Core:** `@hyperframes/engine` = Puppeteer + FFmpeg streaming. HTML/CSS/GSAP → deterministic frame capture → MP4. Zero build. **30 releases za 6 týdnů**, extrémní cadence.
- **Skill structure v repo:** `.claude/settings.json`, 5 skills (`hyperframes` 4500-line SKILL.md, `hyperframes-cli`, `hyperframes-registry`, `gsap`, `website-to-hyperframes`). AGENTS.md + CLAUDE.md top-level.
- **vs `/klip`:** Kling = generative (scéna, postava). Hyperframes = deterministic (text overlays, data viz, bar chart races). Komplement, ne náhrada.
- **Action:**
  1. **NG-ROBOT** `/improve`: high priority, spec = "Install `npx hyperframes init`, první PoC = bar chart race nebo animated caption+TTS z existing článku dat"
  2. **STOPA**: Edit `/klip` skill description — cross-reference pattern "pro HTML-driven deterministic video použij hyperframes, pro generative Kling"
  3. Zkoumat jejich 4500-line SKILL.md jako reference pro STOPA `/klip` + `/nano` enrichment
- **Effort:** S (2-3h PoC)
- **Risks:** Node 22 (většina 20 LTS), 30 releases = pin verze

### 5. 🟡 **Hawksight-AI/semantica** — REVISED up from 7/10
**Score: 8/10 — `pilot-eval` (M)**

- **OPRAVA předchozí evaluace:** In-memory je *default* backend! Neo4j je OPTIONAL. FalkorDB, Apache AGE, Neptune taky. `pip install semantica` bez infra.
- **3 přímé alignmenty s STOPA:**
  - W3C PROV-O provenance = standard pro `source:` field (interop s ByteRover, HippoRAG)
  - Bi-temporal facts = implementuje Zep paper který STOPA cituje v `memory-files.md`
  - Allen's 13-relation interval algebra = queries "learnings valid during execution window X"
- **Action:**
  1. Radar: 7→8 s korekcí "Neo4j optional, in-memory default"
  2. Pilot: dump 30d `decisions.md` + `outcomes/*.md` do semantica in-memory; porovnat query capabilities s grep-first
  3. `/improve` → **MONITOR**: PROV-O má pro OSINT audit trail regulatory value
- **Effort:** M

### 6. 🟡 **atomicmemory/llm-wiki-compiler v0.2.0** — UP from 6/10 to 8/10
**Score: 8/10 — `pilot-eval` (S)**

- **v0.2.0 (2026-04-16) nové features:** semantic search (top 15 embedding pre-filter), lint pass (6 rule-based checks, no LLM), multi-provider, MCP server 7 tools, Obsidian tags/aliases/MOC.md, 211 tests (up from 91).
- **STOPA gap:** paragraph-level attribution (`^[filename.md]`) currently ABSENT v `/compile`. MCP server (homegrown Python currently).
- **Action:**
  1. Radar: 6→8 s notem "v0.2.0 release 2026-04-16"
  2. Sandbox pilot: `npm i -g llm-wiki-compiler@0.2.0`, symlink `learnings/` → `sources/`, run `llmwiki compile` on 20 representative learnings
  3. Diff against existing `wiki/*.md`, check `^[filename]` quality
  4. If wins: `/compile v2` delegates to llm-wiki-compiler, STOPA keeps frontmatter pass-through
- **Effort:** S (2-3h pilot)
- **Risks:** directory ingest of MD+YAML frontmatter nedokumentováno. TS dep do Python-centric stacku.

### 7. 🟡 **zilliztech/claude-context** — momentum update (7.95k⭐, 2d)
**Score: 6→7/10 — `cross-project` (radar update)**

- **Za 2 dny:** +1.5k⭐, 4 commits (Trendshift badge, MILVUS_ADDRESS docs, status docs, MerkleDAG fix). **No breaking change**, incremental polish.
- **STOPA fit:** STOPA hybrid = grep+BM25+graph over memory (MB). claude-context = BM25+dense over codebase (MB-GB) + AST chunking + Merkle incremental. **Orthogonální**, ne redundant. Gap: STOPA nemá AST chunking.
- **Action:**
  1. Radar: 6→7 s note "momentum +1.5k⭐ za 2 dny, incremental polish"
  2. `/improve` → **NG-ROBOT** (větší codebase, highest priority target): pilot Milvus self-host Docker, measure precision vs grep-only
  3. **NEPŘIDÁVAT do STOPA** (meta-projekt, malý codebase, Milvus + OpenAI API vendor lock)

### 8. 🟢 **HKUDS/DeepTutor** — expectation downgrade (21.1k⭐ ale...)
**Score: 6→5/10 — `watch` (XS scribe)**

- **Zklamání:** žádný state machine, IRT, Bayesian knowledge tracing, ani micro-lessons. "Personalized curriculum" = LLM mode-switching (6 modes: Chat/Deep Solve/Quiz/Research/Math Animator/Visualize) + persistent Summary + Profile context. 21.1k⭐ = product success, ne reusable library.
- **Jeden extrakt:** Summary + Profile split pattern → potenciální learning pro STOPA memory architecture (running digest vs stable identity)
- **Action:**
  1. Radar: add 5/10 Watch, down-weight z expected
  2. `/scribe` learning `2026-04-23-deeptutor-summary-profile-pattern.md`
  3. NE pursue integration
- **NE-validuje** Karpathy microGPT `curriculum-hints:` hypothesis — carry on as-is s existing STOPA pattern.

---

## /watch + /radar Post-Mortem

### Proč 32 z 34 URL missed

**Root cause: E — uživatelovy otevřené taby nejsou machine-readable vstup pro žádný skill.**

| Gap | Evidence |
|-----|----------|
| **G1: No batch URL mode** | `/radar` má URL/scan/digest, žádný batch. `/watch` nepřijímá URL inputs vůbec (`watch:30-36`). |
| **G2: Voice Registry krytí 4/10 handles** | Z user tabs: @omarsar0, @liu8in, @garrytan, @deedydas, Sakana **chybí** v Voice Registry (`watch:106-117`). Jen 4 handles proběhly OR-query (`watch:124`). |
| **G3: X/Twitter direct fetch blocked** | `radar:45` + `watch:120` explicit statement. Jina Reader fallback funguje JEN po manual paste. |
| **G4: arXiv scan non-deterministic** | `site:arxiv.org` generic SERP queries nezachycují specific paper IDs. TACO by musel být indexován Googlem pod keyword match. |
| **G5: Scheduled tasks neviditelné runtime** | `news.md:8-14` shows `arxiv-daily-digest` tag, ale `settings.json` žádný cron binding. Externí scheduling. |
| **G6: Last /radar scan 2026-04-17** | 6 dní bez scan = ztráta repo release window. |
| **G7: Brain ↔ STOPA memory bridge missing** | `brain/inbox.md` processes to `wiki/entities/`, ale nikdy protékajou do `radar.md`. Dual-memory parallel. |
| **G8: Watchlist accounts missing key handles** | `brain/watchlist.md:53-59` má 6 handles, z toho 4 překryv s Voice Registry. @omarsar0, @liu8in, @garrytan, Sakana **nechybí v obou**. |

### Zachyceno (2/34)

- **llm-wiki-compiler** (radar.md:30, 6/10, 2026-04-22, source: `manual`)
- **Claude Context Zilliz** (radar.md:32, 6/10, 2026-04-21, source: `manual`)

Obě manual paste. Všechny ostatní mimo percepci.

### Navrhovaná vylepšení (P0-P2)

| Priorita | Vylepšení | Effort | Mechanism |
|----------|-----------|--------|-----------|
| **P0** | `/radar batch` mode — textový seznam URL → paralelní fetch (Jina) + score + append do radar.md | S | Parser v `radar:30-36`, new Phase "Batch Evaluation" |
| **P0** | `/radar tabs` — Chrome MCP `tabs_context_mcp` → filtr na GitHub/arXiv/X → pipe do `/radar batch` | S | Existing MCP + wrapper |
| **P1** | Voice Registry + watchlist.md expansion: +@omarsar0, +@garrytan, +@liu8in, +Sakana AI, +DeepMind research | XS | Edit 2 soubory |
| **P1** | Brain ↔ STOPA bridge: hook po `brain-ingest` check entity tag `tool` → propose radar entry | M | Post-processing step |
| **P1** | Browser bookmarks scan — Chrome MCP JS eval `chrome.bookmarks.getRecent()` daily | M | scheduled task |
| **P2** | GitHub user-watchlist `/radar scan` → `gh api user/subscriptions` | M | GH CLI v radar Batch 2 |
| **P2** | Scheduled `/radar scan` (ut+so 10:00) | XS | `create_scheduled_task` |
| **P3** | `hf papers` CLI pokud dostupné místo SERP | S | detect + branch |

---

## Executive action plan

### Immediate (teď, XS effort, ~30 min)
1. ✅ Update radar.md: 8 entries (5 new + 3 updates) — kompiluje data z této session
2. ✅ Create 3 scribe learnings: Jena confirmation bias (CRITICAL), DeepMind attacks (CRITICAL), UCSD field study (MEDIUM)
3. ✅ Expand `brain/watchlist.md` + `watch/SKILL.md` Voice Registry s 4 handles

### This week (S+M effort)
4. Implement Jena falsification gate in `/autoresearch` Phase 2.5 (S, critical)
5. Hyperframes PoC → NG-ROBOT via `/improve` (S)
6. Context-mode pilot → side-by-side s `/compact` (S)
7. `/radar batch` mode implementation (S)

### Next 2 weeks (M+L effort)
8. TACO compact enhancement — PoC pattern (M)
9. llm-wiki-compiler pilot na `learnings/` (S-M)
10. semantica pilot — PROV-O provenance (M)
11. gbrain self-wiring regex port do Python (S)
12. DeepMind security sanitizer PoC pro MONITOR (M, cross-project)

### Deferred (research, no action)
- Sakana AC/DC — čekat 3+ skills s self-evolve historií
- DeepTutor — product not library, no curriculum algo
- claude-context (Zilliz) — NG-ROBOT only, ne STOPA

### Cross-project /improve queue
1. **MONITOR:** CII formula (worldmonitor) + PROV-O (semantica) + DeepMind sanitizer
2. **ZACHVEV:** spike detection threshold (worldmonitor)
3. **NG-ROBOT:** hyperframes video pipeline + claude-context code search pilot
4. **2BRAIN:** semantica bi-temporal provenance eval

---

## Provenance

- 4 parallel deep-dive agents: papers (total 161s, 97k tokens), tier-1 repos (252s, 109k), tier-2 repos (179s, 110k), postmortem (223s, 155k).
- Fetched: 5 papers (all found), 8 GitHub repos (all found), 8 skill/memory files (postmortem evidence).
- Corrections from initial research:
  - semantica 7→8 (Neo4j is optional, in-memory default)
  - llm-wiki-compiler 6→8 (v0.2.0 has MCP server + paragraph attribution)
  - claude-context 6→7 (momentum update)
  - DeepTutor 6→5 (no curriculum algorithm, product not library)
