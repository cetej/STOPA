---
date: 2026-04-23
scope: Analýza 34 URL (7 GitHub, 4 research, 20 X/Twitter) z otevřených karet uživatele
method: 4 paralelní agenti, Jina Reader fallback pro X.com, WebFetch pro GitHub/arXiv
---

# Browser Tabs Research — 2026-04-23

## TL;DR — Top 5 action items (prioritized)

| # | Cíl | Zdroj | Akce | Úsilí |
|---|------|-------|------|-------|
| 1 | **TACO** — self-evolving context compression pro coding agents | [arXiv:2604.19572](https://arxiv.org/abs/2604.19572) (via @omarsar0) | Deep-dive + adopt patterns do `/compact`, `farm-ledger`, `intermediate/` | M |
| 2 | **MONITOR reference implementation** | [koala73/worldmonitor](https://github.com/koala73/worldmonitor) 52k⭐ | Studovat Country Intelligence Index + dual mapping, aplikovat na MONITOR | L |
| 3 | **Context Mode MCP** — tool output compression před kontextem | [mksglu/context-mode](https://github.com/mksglu/context-mode) 8.5k⭐ | /radar eval + porovnat s /compact, zvážit adopci | S |
| 4 | **llm-wiki-compiler v0.2.0** — up from 6/10 v radaru | [atomicmemory/llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) | Side-by-side eval proti `/compile`, update radar entry | M |
| 5 | **TAR trajectories format** pro `failures/` + `outcomes/` | [arXiv:2604.01437](https://arxiv.org/abs/2604.01437) | Přejmenovat trajectory sekce na Thought/Action/Result, ~20 řádek edits | XS |

**Bonus:** 4 kandidáti pro `/scribe` learnings (DeepMind attack vectors, Jena/IIT Delhi evidence-ignoring paper, Sakana AC/DC, UCSD field study).

---

## Cross-cutting témata (opakující se napříč zdroji)

1. **Context compression je hot topic** — TACO (arXiv), Context Mode (mksglu), Claude Context (Zilliz), Claude Opus 4.7 features. 3 tweety + 2 repos nezávisle řeší stejný problém = signál, že `/compact` + `intermediate/` architektura STOPA je na správné stopě, ale je prostor na upgrade.

2. **Agent reliability & evaluation** — TAR trajectories, UCSD field study, Jena/IIT Delhi "68% ignoruje evidence", GBrain Minions queue. STOPA má failures/+outcomes/+eval infrastrukturu, tyto zdroje validují směr a přidávají konkrétní metrics.

3. **Video editing via AI agents** — browser-use/video-use, heygen-com/hyperframes, @liu8in. Tři nezávislé projekty cílí AI-driven video. Pro NG-ROBOT media expansion relevantní.

4. **Agent security** — DeepMind 6 attack vectors, "can't sanitize a pixel". Přímo pro MONITOR (OSINT scraping) a browse/fetch skills.

---

## GitHub repos (7)

### 1. [koala73/worldmonitor](https://github.com/koala73/worldmonitor) — **Fit 9/10 — Adopt (study)**
Real-time global intelligence dashboard, 52k⭐, 8.3k forks, active (v2.5.23 z 2026-03-01). TypeScript + Vite, Tauri 2 (Rust desktop), Ollama/Groq, Protocol Buffers, MapLibre + globe.gl, Country Intelligence Index. AGPL-3.0.

**Pro:** MONITOR (Czech intelligence terminal), ZACHVEV (cross-stream correlation), KARTOGRAF (MapLibre).
**Akce:** (a) extrahnout Country Intelligence Index scoring formuli, (b) vzor dual mapping engines (2D+3D), (c) analýza 500+ feed orchestrace, (d) Protocol Buffers schema pro intelligence events. AGPL-3.0 compatibility check před adopcí.

### 2. [atomicmemory/llm-wiki-compiler](https://github.com/atomicmemory/llm-wiki-compiler) — **Fit 8/10 (up from 6) — Adopt (eval first)**
Compiler raw sources → interlinked markdown wiki. 692⭐, v0.2.0 (2026-04-16, 7 dní stará). Node 18+, MCP server included, Obsidian-compatible. MIT.

**Pro:** STOPA `/compile` skill + 2BRAIN. Přímý překryv funkcionality.
**Akce:** (a) spustit llm-wiki-compiler na `.claude/memory/learnings/` a porovnat s output `/compile`, (b) pokud wins, `/compile` se stane wrapperem kolem MCP, (c) update radar entry z 6/10 Watch → 8/10 Adopt Eval.

### 3. [Hawksight-AI/semantica](https://github.com/Hawksight-AI/semantica) — **Fit 7/10 — Watch**
Python framework pro context graphs + decision intelligence, 1.1k⭐. Neo4j/FalkorDB, W3C PROV-O provenance, React Knowledge Explorer.

**Pro:** STOPA `concept-graph.json`, `decisions.md`, `outcomes/` — profesionální verze STOPA markdown patternů.
**Akce:** Watch — heavyweight deps (Neo4j/vector store), ale extrahnout vzory (a) provenance frontmatter pro learnings, (b) Allen interval algebra pro `valid_until` pole, (c) PageRank pro retrieval ranking.

### 4. [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) — **Fit 7/10 — Watch (high priority)**
HTML markup → MP4 přes Puppeteer + FFmpeg + GSAP, deterministický rendering, 9.5k⭐, v0.4.15 **2026-04-23 (dnes!)**. HeyGen backing, Apache 2.0. "AI-first" se skills pro Claude/Cursor.

**Pro:** NG-ROBOT media extension, `/klip` alternativa pro deterministic video.
**Akce:** (a) ověřit zda mají hotový CC skill v repo, (b) potenciální /klip complement pro infographic/data viz videa (Kling zůstává na generative).

### 5. [browser-use/video-use](https://github.com/browser-use/video-use) — **Fit 6/10 — Watch**
Open-source video editor poháněný Claude Code, 3.4k⭐. FFmpeg, ElevenLabs, Manim/Remotion, **self-evaluation s 3 correction loops**, `project.md` session persistence.

**Pro:** NG-ROBOT video pipeline. Analogický pattern k STOPA autoloop + checkpoint.
**Akce:** (a) studovat self-eval loop design pro analogii v `/klip`, (b) převzít vzor "text artifact → on-demand visual render" pro token efficiency.

### 6. [Alishahryar1/free-claude-code](https://github.com/Alishahryar1/free-claude-code) — **Fit 3/10 — Discard**
FastAPI proxy routing CC API → NVIDIA NIM / OpenRouter / DeepSeek, 3.6k⭐. Cost savings ale kvalita off-brand modelů pod CC standardem.

**Akce:** Discard pro produkci (konflikt s "verify before done"). RTK už řeší token savings bez quality sacrifice.

### 7. [VoltAgent/awesome-claude-design](https://github.com/VoltAgent/awesome-claude-design) — **Fit 2/10 — Discard**
68 pre-built DESIGN.md templatů pro claude.ai/design. 1.3k⭐.

**Akce:** Off-topic pro STOPA (backend/CLI projekty). `behavioral-genome.md` § Visual Anti-Slop už pokrývá design rules.

---

## Research articles (4)

### 1. [arXiv:2604.01437](https://arxiv.org/abs/2604.01437) — **Fit 7/10 — Adopt pattern**
**Reproducible, Explainable, and Effective Evaluations of Agentic AI for SE**
Li & Storhaug. Review 18 papers (ICSE/FSE/ASE/ISSTA) → navrhuje **Thought-Action-Result (TAR) trajectories** jako first-class evaluation artifact.

**Pro STOPA:** Přesně formalizuje to, co dělá `failures/` + `outcomes/`. Nízko-rizikové sjednocení.
**Akce:** Přejmenovat trajectory sekce v `failures/*.md` + `outcomes/*.md` na explicit `## Thought → ## Action → ## Result`. Přidat notu do `rules/memory-files.md`. Commit-ready: ~20 řádek edits napříč 2 soubory.

### 2. [arXiv:2502.17424](https://arxiv.org/pdf/2502.17424) — **Fit 5/10 — Cite v commit-invariants.md**
**Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs**
Betley, Tan et al. Úzký tréning má nelokální behavioral efekty napříč doménami.

**Pro STOPA:** Validuje design `commit-invariants.md` — safety invariants musí krýt širší spektrum než primary metric. `/self-evolve` iterativní optimalizace = analogický narrow loop.
**Akce:** Přidat citaci do hlavičky `rules/commit-invariants.md`. `/scribe` learning s `source: external_research`, `confidence: 0.6`.

### 3. [arXiv:2604.15039](https://www.alphaxiv.org/abs/2604.15039v1) — **Fit 0/10 — Discard**
**Prefill-as-a-Service: KVCache cross-datacenter**
Infra paper o distribuci KV cache. STOPA je vrstva NAD API, inference infrastructure není v scope.

### 4. [turingpost.com/p/token](https://www.turingpost.com/p/token) — **Fit 1/10 — Discard**
"AI 101" tutorial, populárně-naučný. STOPA už má hlubší pochopení tokenů (budget.md, RTK, graduated compaction).

---

## X/Twitter posts (20 analyzed, 19 accessible)

### High priority (Fit 8-10)

#### @omarsar0 (2047046550770368549) — **Fit 10/10 — Deep-dive #1**
**TACO — self-evolving context compression framework pro long-horizon terminal agents.** Automaticky objevuje compression rules. Benchmarks: TerminalBench, SWE-Bench Lite, CompileBench s MiniMax-2.5.
→ **[arXiv:2604.19572](https://arxiv.org/abs/2604.19572)**, academy.dair.ai
**Akce:** Fetch paper, `/scribe` critical pattern, integrovat patterns do `/compact` + `farm-ledger` + `intermediate/`.

#### @ihtesham2005 (2046680428640354790) — **Fit 9/10 — Deep-dive #2**
**Context Mode MCP server** — komprimuje tool output před vstupem do kontextu. 6× delší kontext. Příklady: Playwright 56KB→299B, GitHub issues 59KB→1.1KB.
→ [github.com/mksglu/context-mode](https://github.com/mksglu/context-mode) 8.5k⭐, ELv2
**Akce:** Fetch repo, porovnat s `/compact` skill, zvážit jako MCP dependency pro scout/deepresearch.

#### @socialwithaayan (2046573707112620156) — **Fit 9/10 — Deep-dive #3**
**Claude Context (Zilliz)** — MCP server s hybrid semantic+BM25 search pro codebases. AST-based chunking. ~40% token savings. 6.2k⭐, TypeScript, MIT. Multi-provider embeddings.
**Akce:** Compare s existujícím `scripts/hybrid-retrieve.py` (grep+BM25+graph walk RRF). AST chunking = potenciální upgrade.

#### @ZabihullahAtal (2046859194343768136) — **Fit 9/10 — Deep-dive #4**
Reference na arXiv:2604.01437 (TAR trajectories — viz research articles #1).

#### @MillieMarconnni (2046892074541474195) — **Fit 9/10 — Deep-dive #5**
**Kritika AI research agentů** (Jena + IIT Delhi paper). Numbers: 68% ignoruje evidence, 71% neaktualizuje beliefs, 26% reviduje hypotézy, 7% používá nezávislé evidence lines.
**Akce:** Najít paper (arXiv search: "Jena IIT Delhi AI research agents evidence 2026"), `/scribe` critical pattern, **zvážit belief-update-rate invariant pro `/autoresearch` a `/deepresearch`**.

#### @askalphaxiv (2047013292850151788) — **Fit 8/10**
**Sakana AC/DC** framework — co-evoluce modelů (merging/mutation) a tasks (LLM scientist generates synthetic challenges).
**Akce:** Hledat paper "Discovering Novel LLM Experts via Task-Capability Coevolution", potenciální inspirace pro `/self-evolve` curriculum agent.

#### @heygurisingh (2046908145667359167) — **Fit 8/10**
**UCSD field study** (Huang et al., Dec 2025) — 13 observed + 99 surveyed experienced devs. Plánují před promptingem, verifikují každý diff, odmítají "vibe coding".
**Akce:** Najít paper, `/scribe` jako external validation pro `behavioral-genome.md § Verification` + Code Editing Discipline.

#### @Suryanshti777 (2046983238619656252) — **Fit 8/10**
**Claude Opus 4.7 features** — /ultrareview, Auto mode, Task budgets, nový tokenizer (1.0-1.35× více tokenů), 2576px vision, xHigh effort mode.
**Akce:** `/scribe` key-facts update, zvážit aktualizaci budget tiers (tokenizer change = cost impact).

#### @HowToAI_ (2045749883773333717) — **Fit 8/10**
**Google DeepMind paper — 6 attack vectors na AI agenty:** hidden HTML/CSS, steganografie v pixelech, jailbreaky v dokumentech, data exfil, cross-agent infekce. *"Can't sanitize a pixel."*
**Akce:** Deep-dive (hledat paper), `/scribe` critical pattern pro MONITOR + browse + fetch + ingest. Rozšířit `feedback_input_sanitization.md`.

### Medium priority (Fit 6-7)

#### @RidgerZhu (2046736781035618602) — **Fit 7/10**
Looped LLMs scaling (Parcae, Ouro, Kimi, Delta-rule attention). Reakce na "Claude Mythos".
**Akce:** Rozšířit `reference_parcae_looped_scaling.md` o Mythos context a CPT techniky.

#### @TawohAwa (2046566836012306544) — **Fit 7/10**
**Video Use** — duplicita s GitHub repo browser-use/video-use (viz #5 GitHub).

#### @garrytan (2045427057656729985) — **Fit 7/10**
**GBrain v0.11 "Minions"** — Postgres/PGLite + BullMQ job queue fixující nespolehlivost OpenClaw subagentů. "10× rychlejší, více reliable."
**Akce:** Najít GBrain/Minions repo (Garry Tan YC), aplikovat na farm tier reliability.

#### @DAIEvolutionHub (2045086522651861469) — **Fit 6/10**
**DeepTutor** — open-source AI tutoring s real-time personalized curriculum. 6.4k⭐ za týden.
→ [github.com/HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor)
**Akce:** Pokud má curriculum algoritmus, inspirace pro `skill-generator` + `curriculum-hints` v SKILL.md.

#### @hasantoxr (2046898117241635240) — **Fit 6/10**
free-claude-code proxy — duplicita s GitHub repo #6 (viz výše).

### Low priority / Skip (Fit 1-5)

| Účet | Téma | Fit | Důvod |
|------|------|-----|-------|
| @elora_khatun | Anthropic 13 free kurzů | 5/10 | Watch — "Agent Skills" + "MCP Advanced" courses |
| @liu8in | HyperFrames demo | 5/10 | Duplicita s GitHub #4 |
| @chrisfirst | Seedance 2.0 viral efekt | 3/10 | Off-topic video gen |
| @TheTuringPost | Token 101 | 2/10 | 101 material |
| @isaakfreeman | MIT PhD drop pro digital humans | 1/10 | Vision post, žádná technika |
| @IATheYoker | 9 CC repos "90% nezná" | N/A | Content v obrázku, neaccessible |

---

## Doporučený next step

**Okamžité (dnes, <30 min):**
1. Fetch [arXiv:2604.19572 TACO](https://arxiv.org/abs/2604.19572) + `/scribe` learning → nejvyšší ROI
2. Update `radar.md` entry pro llm-wiki-compiler: 6/10 Watch → 8/10 Adopt Eval
3. TAR rename: `failures/` + `outcomes/` trajectory sekce → Thought/Action/Result format

**Tento týden:**
4. Fetch [koala73/worldmonitor](https://github.com/koala73/worldmonitor) README detailně, `/improve` routing do MONITOR
5. Deep-dive Context Mode ([mksglu/context-mode](https://github.com/mksglu/context-mode)) — side-by-side s `/compact`
6. Hledat 3 papery (DeepMind attacks, Jena evidence-ignoring, UCSD field study) a zapsat jako learnings

**Backlog:**
7. Sakana AC/DC study pro `/self-evolve` curriculum patterns
8. GBrain/Minions queue pattern pro farm tier
9. HyperFrames eval pro NG-ROBOT video extension

---

## Provenance

- Zpracováno: 4 paralelní general-purpose agenty
- Metoda: WebFetch pro GitHub/arXiv, Jina Reader (`r.jina.ai/...`) fallback pro X.com (všech 19 accessible tweety úspěšně)
- 1 post skipped (@IATheYoker — obsah v obrázku bez OCR)
- Duplicity rozpoznány: Alishahryar1/free-claude-code = @hasantoxr, heygen-com/hyperframes = @liu8in, browser-use/video-use = @TawohAwa
- Total tool uses: 36 (agent calls), token usage: ~340k
