# Idea File: Nový primitiv pro sdílení znalostí s AI agenty — Research Brief

**Date:** 2026-04-05
**Question:** Co je Karpathyho "idea file" koncept, jak funguje v praxi (OpenClaw/Monica), co je compilation layer pattern a jaké jsou broader implikace?
**Scope:** standard
**Sources consulted:** 41

---

## Executive Summary

Andrej Karpathy 4. dubna 2026 pojmenoval koncept, který se formoval celý předchozí rok: **idea file** — Markdown dokument popisující *co* postavit, ne *jak*. Agent si přečte záměr a postaví implementaci sám [VERIFIED][2][3]. Není to vynález ex nihilo — autoresearch `program.md` (březen 2026) [VERIFIED][6], AGENTS.md (srpen 2025) [VERIFIED][25][26] a SKILL.md (prosinec 2025) [VERIFIED][24] jsou starší instantiace téhož principu. Karpathyho přínos je meta-pojmenování a první referenční implementace (`llm-wiki.md` gist).

Praktická demonstrace: Shubham Saboo (Google Cloud AI PM) provozuje 6 OpenClaw agentů na Mac Mini koordinovaných přes sdílené markdown soubory [VERIFIED][7][9]. Jeho agent Monica autonomně instaluje software, píše performance reviews a reaguje na externí specifikace [VERIFIED][10][11][12]. Tvrzení, že Monica přečetla konkrétně Karpathyho idea file a identifikovala compilation gap, je plausibilní ale přímo neověřené [UNVERIFIED].

Nejdůležitější technická mezera: **compilation layer** — přeměna surových denních signálů na strukturované znalosti. Akademický mainstream (EverMemOS [VERIFIED][15], MAGMA [VERIFIED][16], Letta sleep-time [VERIFIED][17]) konverguje na 3-fázový lifecycle (ingest → consolidate → reflect), ale žádná open-source implementace nedemonstruje end-to-end reflection loop pro cross-temporal pattern detection [INFERRED][13][15][17][21].

---

## Detailed Findings

### 1. Karpathyho tři koncepty: od autoresearch k idea file

Karpathy vytvořil tři propojené artefakty v rychlém sledu:

**autoresearch** (6.–7. března 2026 [VERIFIED][6]): `program.md` jako Markdown instrukce pro agenta, agent iteruje na kódu. Karpathy explicitně: "you don't 'use it' directly, it's just a recipe/idea — give it to your agent" [SINGLE-SOURCE][5]. Za 2 dny agent provedl 700 experimentů a zlepšil training speed o 11% [INFERRED][6].

**LLM Wiki / Knowledge Bases** (2.–3. dubna 2026 [VERIFIED][1]): Posun od kódových experimentů ke knowledge compilation. Tři vrstvy: immutable `raw/` sources → LLM-compiled wiki (interlinked `.md`) → schema/config. Klíčová vlastnost: každý dotaz je zároveň příspěvek — wiki kompounduje [VERIFIED][3][13].

**Idea File** (4. dubna 2026 [VERIFIED][2][3]): Meta-pojmenování principu. Definice: sdílíme záměr v Markdownu, ne kód. `llm-wiki.md` gist je první publikovaný idea file — explicitně navržen pro copy-paste do libovolného LLM agenta [VERIFIED][3].

### 2. OpenClaw & Monica: idea files v praxi

**OpenClaw** je open-source self-hosted agent framework (~349K GitHub stars [VERIFIED][7]). Tvůrce: Peter Steinberger, zakladatel PSPDFKit [VERIFIED][7]. Architektura: Node.js gateway na lokálním hw, 7 markdown workspace souborů (SOUL.md, AGENTS.md, HEARTBEAT.md, MEMORY.md...), koordinace přes sdílené .md soubory, ne API [VERIFIED][8][36].

**Monica** je Chief of Staff agent Shubhama Saboo — vedoucí 6-členného týmu (Monica, Dwight, Kelly, Ross, Pam, Rachel) na Mac Mini [VERIFIED][9]. Dokumentované schopnosti:

- Autonomní instalace mem0 pluginu včetně Ollama modelů a SQLite vector storage [SINGLE-SOURCE][10]
- Týdenní performance reviews ostatních agentů s grading a action items [SINGLE-SOURCE][11]
- Síťový discovery a ovládání Sonos reproduktoru [SINGLE-SOURCE][12]

Vzor koordinace: agenti sdílí markdown soubory (THESIS.md, SIGNALS.md, FEEDBACK-LOG.md) místo API volání [VERIFIED][36]. Jeden agent píše, ostatní čtou — emergent consensus přes text, ne přes protokol.

### 3. Compilation layer: pojmenovaná mezera

Problém: 60 dní denních signálů v souborech, ale žádný agent je nekompiluje do strukturovaných znalostí. Agent vidí jen dnešek, nemůže říct "tohle je třetí OCR tool tento kvartál."

DEV.to to explicitně pojmenovává: "RAG performs information retrieval. What Karpathy's workflow performs is knowledge compilation" [VERIFIED][13].

**Akademická konvergence na 3-fázový lifecycle:**

| Fáze | Co dělá | Implementace |
|------|---------|-------------|
| **Ingest** | Rychlé zachycení atomických jednotek | EverMemOS MemCells [VERIFIED][15], Karpathy raw/ [VERIFIED][3] |
| **Consolidate** | Asynchronní syntéza do struktur | Letta sleep-time [VERIFIED][17], Cognee ECL [VERIFIED][18] |
| **Reflect** | Pattern detection přes čas | AWS AgentCore [UNVERIFIED][21], Supermemory [UNVERIFIED][40] |

**Klíčové systémy:**

- **Zep/Graphiti** [VERIFIED][14]: temporal knowledge graph, automaticky evaluuje nové info proti existujícímu grafu
- **EverMemOS** [VERIFIED][15]: SOTA na LoCoMo benchmarku, 3-fázový memory lifecycle
- **ByteRover** [VERIFIED][20]: hierarchický Context Tree čistě na Markdown, zero infrastruktura — přímá kompatibilita se STOPA architekturou
- **A-MEM** [VERIFIED][39]: Zettelkasten-inspired, nové memories triggerují update existujících
- **Mem0** [VERIFIED][19]: graph-based varianta, produkční deployment

**Kritická mezera:** Fáze 3 (reflection) je nejméně implementovaná. Letta, AWS AgentCore a Supermemory ji claimují, ale žádná open-source implementace s verifikovatelným cross-temporal pattern detection nebyla nalezena [INFERRED][15][17][21].

### 4. Ekosystém: Markdown jako lingua franca agentů

**Standardy a adopce:**

- **AGENTS.md**: OpenAI (08/2025), Linux Foundation AAIF (12/2025) s AWS, Anthropic, Google, Microsoft jako platinum members [VERIFIED][25][26]
- **SKILL.md**: Anthropic → agentskills.io, cross-platform (20+ nástrojů), progressive disclosure (~100 tokenů metadata, <5K body) [VERIFIED][24]
- **Cloudflare**: CDN-level HTML→markdown konverze, 80% token redukce [VERIFIED][29]

**Nástroje pro distribuci idea files:**

| Nástroj | Co dělá | Zdroj |
|---------|---------|-------|
| **GitHub spec-kit** | 4 spec soubory jako executable artifacts | [VERIFIED][30] |
| **AWS Kiro** | 3-file spec format s event-driven hooks | [VERIFIED][31] |
| **ai-rules-sync** | Sync agent rules přes 10+ nástrojů | [VERIFIED][38] |
| **BMAD-METHOD** | 12+ agent personas definovaných .md soubory | [VERIFIED][37] |
| **aider CONVENTIONS** | Community-shared agent behavior specs | [VERIFIED][34] |

**Teoretický rámec** (arXiv:2603.09619v2 [VERIFIED][32]): Context Engineering → Intent Engineering → Specification Engineering. "Whoever controls the context controls behavior; whoever controls intent controls strategy; whoever controls specifications controls scale."

### 5. Kritika

Birgitta Böckeler na martinfowler.com [VERIFIED][28] — nejpřísnější analýza SDD:

- Agenti specifikace ignorují nebo over-interpretují
- Overhead disproportionální pro malé tasky
- Historická paralela: Model-Driven Development také sliboval abstrakci nad kódem a selhal

Nuance: SDD komprimuje feedback loop na minuty (≠ waterfall), ale vyžaduje expertizu rozpoznat špatné specifikace [INFERRED][28].

---

## Disagreements & Open Questions

- **Graph DB vs Markdown:** Akademický mainstream (Zep, MAGMA, Kumiho) preferuje graph. Karpathy a ByteRover demonstrují plain Markdown. Trade-off: graph = lepší relational queries, Markdown = zero infrastruktura.
- **Konvergence standardů:** Zda SKILL.md a AGENTS.md splynout nebo zůstanou paralelní — AAIF governance nejasná.
- **Fowler/Böckeler kritika:** Je to MDD 2.0 nebo legitimní paradigma shift? Klíčový test: zvládnou agenti respektovat specifikace konzistentně s rostoucí capability?
- **Monica+idea file claim:** Saboo cituje Karpathyho jako inspiraci, Monica má demonstrovanou schopnost, ale přesný tweet "čte llm-wiki gist a identifikuje compilation gap" nebyl přímo ověřen.

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Karpathy — LLM Knowledge Bases tweet | https://x.com/karpathy/status/2039805659525644595 | Virální post o LLM wiki pattern | primary | high |
| 2 | Karpathy — idea file tweet | https://x.com/karpathy/status/2040470801506541998 | Definice "idea file" konceptu | primary | high |
| 3 | Karpathy — llm-wiki.md gist | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f | První idea file — popis LLM Wiki pattern | primary | high |
| 4 | Karpathy — autoresearch tweet | https://x.com/karpathy/status/2030371219518931079 | program.md jako agent instrukce | primary | high |
| 5 | Karpathy — "recipe/idea" tweet | https://x.com/karpathy/status/2031137476438548874 | autoresearch = idea, ne tool | primary | high |
| 6 | karpathy/autoresearch GitHub | https://github.com/karpathy/autoresearch | program.md předchůdce idea file | primary | high |
| 7 | openclaw/openclaw GitHub | https://github.com/openclaw/openclaw | Self-hosted agent framework, ~349K stars | primary | high |
| 8 | OpenClaw docs — Multi-Agent | https://docs.openclaw.ai/concepts/multi-agent | Isolated workspaces, markdown coordination | primary | high |
| 9 | Saboo — 6 agents tweet | https://x.com/Saboo_Shubham_/status/2021651758490284108 | Monica = Chief of Staff, Mac Mini | primary | high |
| 10 | Saboo — Monica mem0 install | https://x.com/Saboo_Shubham_/status/2025266379906236435 | Autonomní instalace softwaru | primary | high |
| 11 | Saboo — Monica reviews | https://x.com/Saboo_Shubham_/status/2028678449561501991 | Týdenní agent performance reviews | primary | high |
| 12 | Saboo — Monica Sonos | https://x.com/Saboo_Shubham_/status/2035919432967753884 | Síťový discovery, cituje Karpathyho | primary | high |
| 13 | DEV.to — Compile, Don't Search | https://dev.to/rotiferdev/compile-your-knowledge-dont-search-it-what-llm-knowledge-bases-reveal-about-agent-memory-32pg | RAG = retrieval, wiki = compilation | secondary | high |
| 14 | Zep/Graphiti — arXiv:2501.13956 | https://arxiv.org/abs/2501.13956 | Temporal knowledge graph, 94.8% DMR | primary | high |
| 15 | EverMemOS — arXiv:2601.02163 | https://arxiv.org/abs/2601.02163 | 3-phase memory lifecycle, SOTA LoCoMo | primary | high |
| 16 | MAGMA — arXiv:2601.03236 | https://arxiv.org/abs/2601.03236 | Dual-stream ingest/consolidation | primary | high |
| 17 | Letta — Sleep-Time Compute | https://www.letta.com/blog/sleep-time-compute | Background consolidation during idle | primary | high |
| 18 | Cognee GitHub | https://github.com/topoteretes/cognee | ECL pipeline, 12K+ stars, production | primary | high |
| 19 | Mem0 — arXiv:2504.19413 | https://arxiv.org/abs/2504.19413 | Graph-based agent memory, 26% improvement | primary | high |
| 20 | ByteRover — arXiv:2604.01599 | https://arxiv.org/abs/2604.01599 | Hierarchical Context Tree, pure Markdown | primary | high |
| 21 | AWS AgentCore Memory | https://aws.amazon.com/blogs/machine-learning/building-smarter-ai-agents-agentcore-long-term-memory-deep-dive/ | Episodic extraction→consolidation→reflection | primary | high |
| 22 | Kumiho — arXiv:2603.17244 | https://arxiv.org/abs/2603.17244 | Formal belief revision for memory graphs | primary | high |
| 23 | Karpathy — vibe coding tweet | https://x.com/karpathy/status/1886192184808149383 | Coined "vibe coding" Feb 2025 | primary | high |
| 24 | agentskills.io — SKILL.md spec | https://agentskills.io/specification | Cross-platform agent skills standard | primary | high |
| 25 | Linux Foundation — AAIF | https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation | AGENTS.md + MCP + goose, platinum members | primary | high |
| 26 | OpenAI — AAIF announcement | https://openai.com/index/agentic-ai-foundation/ | OpenAI created AGENTS.md Aug 2025 | primary | high |
| 27 | GitHub Blog — agents.md analysis | https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/ | Best practices from 2500+ repos | primary | high |
| 28 | Böckeler (martinfowler.com) — SDD critique | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html | Agents ignore specs, MDD parallel | primary | high |
| 29 | Cloudflare — Markdown for Agents | https://blog.cloudflare.com/markdown-for-agents/ | HTML→MD 80% token reduction | primary | high |
| 30 | GitHub spec-kit | https://github.com/github/spec-kit | Spec files as executable artifacts | primary | high |
| 31 | AWS Kiro | https://kiro.dev/blog/introducing-kiro/ | 3-file spec format with hooks | primary | high |
| 32 | arXiv:2603.09619v2 — Context Engineering | https://arxiv.org/abs/2603.09619v2 | CE → IE → SE hierarchy | primary | high |
| 33 | Red Hat — Four Pillars | https://developers.redhat.com/articles/2026/03/30/vibes-specs-skills-agents-ai-coding | vibes → specs → skills → agents | primary | high |
| 34 | Addy Osmani — Spec for agents | https://addyosmani.com/blog/good-spec/ | What/why > how for agent specs | primary | high |
| 35 | The New Stack — Skills vs MCP | https://thenewstack.io/skills-vs-mcp-agent-architecture/ | SKILL.md token economy | secondary | low (dead link) |
| 36 | openclaw-multi-agent-kit | https://github.com/raulvidis/openclaw-multi-agent-kit | Shared .md coordination pattern | primary | high |
| 37 | BMAD-METHOD | https://github.com/bmad-code-org/BMAD-METHOD | 12+ agent personas as .md files | primary | high |
| 38 | ai-rules-sync | https://github.com/lbb00/ai-rules-sync | Cross-tool agent rules sync | primary | high |
| 39 | A-MEM — arXiv:2502.12110 | https://arxiv.org/abs/2502.12110 | Zettelkasten-inspired memory evolution | primary | high |
| 40 | Supermemory | https://supermemory.ai/research/ | Relational versioning, dual timestamps | primary | medium |
| 41 | MemOS — arXiv:2505.22101 | https://arxiv.org/abs/2505.22101 | Memory as OS resource, MemCubes | primary | high |

---

## Sources

1. Karpathy — X post "LLM Knowledge Bases" — https://x.com/karpathy/status/2039805659525644595
2. Karpathy — X post "idea file" — https://x.com/karpathy/status/2040470801506541998
3. Karpathy — llm-wiki.md gist — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
4. Karpathy — autoresearch tweet — https://x.com/karpathy/status/2030371219518931079
5. Karpathy — "recipe/idea" tweet — https://x.com/karpathy/status/2031137476438548874
6. karpathy/autoresearch — https://github.com/karpathy/autoresearch
7. openclaw/openclaw — https://github.com/openclaw/openclaw
8. OpenClaw docs Multi-Agent — https://docs.openclaw.ai/concepts/multi-agent
9. Saboo — 6 agents — https://x.com/Saboo_Shubham_/status/2021651758490284108
10. Saboo — Monica mem0 — https://x.com/Saboo_Shubham_/status/2025266379906236435
11. Saboo — Monica reviews — https://x.com/Saboo_Shubham_/status/2028678449561501991
12. Saboo — Monica Sonos — https://x.com/Saboo_Shubham_/status/2035919432967753884
13. DEV.to — Compile, Don't Search — https://dev.to/rotiferdev/compile-your-knowledge-dont-search-it-what-llm-knowledge-bases-reveal-about-agent-memory-32pg
14. Zep/Graphiti arXiv:2501.13956 — https://arxiv.org/abs/2501.13956
15. EverMemOS arXiv:2601.02163 — https://arxiv.org/abs/2601.02163
16. MAGMA arXiv:2601.03236 — https://arxiv.org/abs/2601.03236
17. Letta Sleep-Time — https://www.letta.com/blog/sleep-time-compute
18. Cognee — https://github.com/topoteretes/cognee
19. Mem0 arXiv:2504.19413 — https://arxiv.org/abs/2504.19413
20. ByteRover arXiv:2604.01599 — https://arxiv.org/abs/2604.01599
21. AWS AgentCore — https://aws.amazon.com/blogs/machine-learning/building-smarter-ai-agents-agentcore-long-term-memory-deep-dive/
22. Kumiho arXiv:2603.17244 — https://arxiv.org/abs/2603.17244
23. Karpathy — vibe coding — https://x.com/karpathy/status/1886192184808149383
24. agentskills.io — https://agentskills.io/specification
25. Linux Foundation AAIF — https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
26. OpenAI AAIF — https://openai.com/index/agentic-ai-foundation/
27. GitHub Blog agents.md — https://github.blog/ai-and-ml/github-copilot/how-to-write-a-great-agents-md-lessons-from-over-2500-repositories/
28. Böckeler (martinfowler.com) — https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
29. Cloudflare Markdown — https://blog.cloudflare.com/markdown-for-agents/
30. GitHub spec-kit — https://github.com/github/spec-kit
31. AWS Kiro — https://kiro.dev/blog/introducing-kiro/
32. arXiv:2603.09619v2 — https://arxiv.org/abs/2603.09619v2
33. Red Hat Four Pillars — https://developers.redhat.com/articles/2026/03/30/vibes-specs-skills-agents-ai-coding
34. Osmani — https://addyosmani.com/blog/good-spec/
35. The New Stack Skills vs MCP — https://thenewstack.io/skills-vs-mcp-agent-architecture/
36. openclaw-multi-agent-kit — https://github.com/raulvidis/openclaw-multi-agent-kit
37. BMAD-METHOD — https://github.com/bmad-code-org/BMAD-METHOD
38. ai-rules-sync — https://github.com/lbb00/ai-rules-sync
39. A-MEM arXiv:2502.12110 — https://arxiv.org/abs/2502.12110
40. Supermemory — https://supermemory.ai/research/
41. MemOS arXiv:2505.22101 — https://arxiv.org/abs/2505.22101

---

## Coverage Status

- **[VERIFIED]:** Karpathy idea file definition a gist [2][3]; autoresearch repo [6]; OpenClaw GitHub + docs [7][8]; Saboo agenti [9-12]; DEV.to compilation framing [13]; Zep [14]; EverMemOS [15]; Letta [17]; Cognee [18]; Cloudflare [29]; AAIF [25][26]; SKILL.md spec [24]; Böckeler critique [28]; spec-kit [30]; Kiro [31]; Context Engineering [32]
- **[INFERRED]:** Absence of open-source reflection loop (derived from surveying 12+ systems); connection between autoresearch program.md and idea file concept; compilation > retrieval distinction
- **[SINGLE-SOURCE]:** Saboo's specific capability claims [10][11][12] (jeho tweety, no independent confirmation); Karpathy "recipe/idea" tweet [5]
- **[UNVERIFIED]:** Exact "Monica reads Karpathy's idea file" event; AWS AgentCore reflection specifics [21]; The New Stack token comparison [35] (dead link); Supermemory claims [40]
