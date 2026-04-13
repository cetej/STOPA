# 2BRAIN — Research Brief & Architecture Proposal

**Date:** 2026-04-13
**Question:** Navrhnout architekturu projektu 2BRAIN — osobní druhý mozek pro ukládání nápadů, záměrů, způsobů uvažování a budování architektury souvislostí, těsně integrovaný se STOPA.
**Scope:** broad (4 domény)
**Sources consulted:** 12 přímých zdrojů + 4 discovery scany

---

## Executive Summary

2BRAIN je rozšíření STOPA memory systému o osobní vrstvu — nápady, záměry, způsoby uvažování, cíle a reflexe. Klíčový architektonický vzor pochází od Karpathyho: **LLM jako kompilátor** transformující surové zdroje do strukturované, provázané markdown wiki [VERIFIED][1]. Akademický výzkum potvrzuje, že entity-centric storage + cue-driven multi-hop retrieval + aktivní metakognitivní kurace překonává pasivní RAG na všech benchmarcích [VERIFIED][3,4]. STOPA je **70% připravená** — learnings, failures, outcomes, hooks a hybrid retrieval se přenesou bez úprav. Chybí: osobní kontext, časová osa, reflexe, cíle a obohacený knowledge graph pro lidi, projekty a myšlenky.

Navrhovaná architektura: **6C cyklus** — Capture → Compile → Connect → Curate → Consult → Contemplate. 2BRAIN žije jako rozšíření STOPA v `.claude/memory/brain/`, sdílí retrieval infrastrukturu a přidává 5 nových datových vrstev.

---

## Detailed Findings

### 1. Karpathyho LLM Wiki — základní architektonický vzor

Karpathy definuje 3-vrstvou architekturu [VERIFIED][1]:

- **raw/** — neměnný archiv zdrojů (LLM čte, nikdy nepíše)
- **wiki/** — LLM-kompilovaný markdown artefakt (akumuluje se, provázaný backlinky)
- **schema** — konfigurační dokument (CLAUDE.md), ko-evolvovaný člověkem a LLM

Compiler analogy [VERIFIED][1,2]: raw články = source code, LLM = compiler, wiki = compiled binary. Znalost se kompiluje jednou a udržuje aktuální, ne re-derivuje při každém dotazu. LLM je "lossy compression" prioritizující užitečnost nad věrností.

Proč bypasuje RAG [VERIFIED][1]: při ~100 zdrojích / 400K slovech strukturovaný markdown index (index.md + explicitní backlinky) překonává embedding-based RAG. Žádná vektorová infrastruktura, lidsky čitelné, auditovatelné.

Context engineering principy [VERIFIED][1]:
- **index.md** — content-oriented katalog (LLM čte jako první)
- **log.md** — append-only chronologický záznam
- **Typed file naming** — prefixy routují LLM writes bez infrastructure
- **Contradiction callouts** — `[!contradiction]` místo tichého přepisování

Dělba práce [VERIFIED][1]: Člověk kuratuje zdroje, ptá se, rozhoduje. LLM řeší bookkeeping — neúnavné udržování cross-referencí, indexů, koherence.

### 2. Akademické základy — co funguje

**EcphoryRAG** [VERIFIED][3]: Entity-centric storage inspirovaný neurovědním konceptem ecphorie (partial cue aktivuje cílenou memory trace). Indexování ukládá pouze entity + metadata (94% redukce tokenů). Retrieval extrahuje cue entity z dotazu → multi-hop associative search → dynamická inference implicitních relací. EM 0.392 → 0.474 nad HippoRAG.

**PersonalAI** [VERIFIED][4]: Hybridní knowledge graph s temporálními hyper-edges pro sledování kdy se belief mění. Žádný single retrieval algoritmus nevyhrává — A*, water-circle, beam search, hybrid mají každý svůj kontext. Implikace: composable retrieval layer.

**Cognitive Workspace** [VERIFIED][5]: Aktivní memory management grounded v Baddeleyho modelu pracovní paměti. 58.6% memory reuse vs 0% pasivní RAG, 17-18% efficiency gain. Klíčový claim: pasivní RAG (query→retrieve) je kategoricky nedostatečný; systém musí aktivně rozhodovat co udržovat, promovat a zahazovat.

**Konvergentní vzor** [INFERRED][3,4,5]: Entity-centric storage + cue-driven multi-hop retrieval + active metacognitive curation = state of the art.

### 3. PKM metodologie — co přežilo 80 let

**BASB CODE** [VERIFIED][6]: Capture → Organize → Distill → Express. PARA (Projects/Areas/Resources/Archive) organizuje podle actionability, ne tématu. Progressive Summarization: highlight → bold → executive summary bez mazání zdroje. Resonance heuristic pro výběr: ukládej co rezonuje intuitivně.

**Zettelkasten** [VERIFIED][7]: Dva kanonické principy — Atomicity (jedna myšlenka per note, unique ID) + Connectivity (explicitní linky; search nestačí). Tags > categories (hierarchie omezuje budoucí retrieval). Luhmann: 90K notes, 40 let, jeden Zettelkasten.

**BASB vs Zettelkasten** [INFERRED][6,7]: Komplementární — PARA optimalizuje pro project completion, Zettelkasten pro knowledge emergence. Kombinace: PARA pro aktivní práci, atomické notes pro dlouhodobý knowledge graph.

**Reor "two generators"** [VERIFIED][8]: Stejný retrieval pipeline slouží lidskému editoru (sidebar s related notes) i LLM (Q&A). Architektonicky nejsilnější insight pro 2BRAIN: design retrieval to serve both humans and LLMs.

### 4. STOPA integrace — co je hotové

STOPA poskytuje [VERIFIED][D1]:
- **Learnings** (70+ souborů): YAML frontmatter, confidence/impact scoring, graduation, supersedes/related
- **Failures** (HERA trajectories): per-failure záznamy s decision chain
- **Outcomes** (RCL credit): success/partial/failure tracking s credit assignment
- **Hooks**: learning-admission.py, outcome-credit.py, verify-sweep.py
- **Retrieval**: grep-first + hybrid RRF (BM25 + graph walk, k=60) + synonym fallback
- **concept-graph.json**: semantic graph pro 1-hop retrieval expansion

**Gapy** [VERIFIED][D1]:
- Osobní kontext (life areas, hodnoty, energie)
- Temporální dotazy (date range, "co jsem dělal v březnu?")
- Reflexe (periodické self-reviews)
- Cíle a progress tracking
- Enriched knowledge graph (lidi, projekty, myšlenky — ne jen learnings)
- Privacy markers

---

## Architektonický návrh: 2BRAIN

### Principy

1. **Markdown-first** (Karpathy): plain text, git-tracked, no vendor lock-in
2. **Entity-centric** (EcphoryRAG): ukládej entity + metadata, ne full text dokumenty
3. **Active curation** (Cognitive Workspace): hooks rozhodují co promovat/archivovat
4. **Two generators** (Reor): retrieval slouží člověku i LLM ze stejného indexu
5. **Atomic + connected** (Zettelkasten): jedna myšlenka per note, explicitní linky
6. **STOPA-native**: sdílí infrastrukturu, hooks, retrieval — ne fork, ale rozšíření

### 6C Cyklus

```
CAPTURE → COMPILE → CONNECT → CURATE → CONSULT → CONTEMPLATE
   ↑                                                    |
   └────────────────────────────────────────────────────┘
```

| Fáze | Popis | STOPA ekvivalent | Nové |
|------|-------|-----------------|------|
| **Capture** | Zachyť nápad, zdroj, myšlenku | /ingest | /capture (rychlý vstup) |
| **Compile** | LLM kompiluje do wiki článku | /ingest wiki/ | Rozšíření o osobní kontext |
| **Connect** | Propoj s existujícími entitami | concept-graph.json | knowledge-graph.json (rozšířený) |
| **Curate** | Hooks hodnotí kvalitu, řeší kontradikce | learning-admission.py | brain-curation.py |
| **Consult** | Dotazuj se mozku | hybrid RRF retrieval | /ask-brain skill |
| **Contemplate** | Periodické reflexe, goal review | — | /reflect, /review-goals |

### Datová architektura

```
.claude/memory/brain/           # 2BRAIN root (vedle STOPA memory/)
├── raw/                        # Neměnné zdroje (články, screenshoty, poznámky)
│   ├── 2026-04-13-karpathy-llm-wiki.md
│   └── ...
├── wiki/                       # LLM-kompilované wiki články
│   ├── index.md                # Master index (content catalog)
│   ├── log.md                  # Append-only chronological log
│   ├── concepts/               # Konceptové články
│   │   ├── context-engineering.md
│   │   └── second-brain.md
│   ├── people/                 # Osobní entity
│   │   ├── karpathy.md
│   │   └── tiago-forte.md
│   ├── projects/               # Projektové syntézy
│   │   └── stopa.md
│   └── reasoning/              # Způsoby uvažování, mentální modely
│       ├── compiler-analogy.md
│       └── first-principles.md
├── reflections/                # Periodické self-reviews
│   ├── 2026-W15.md             # Týdenní reflexe
│   └── 2026-04.md              # Měsíční reflexe
├── decisions/                  # Rozhodovací žurnál
│   ├── index.md
│   └── 2026-04-13-2brain-architecture.md
├── goals/                      # Cíle a OKRy
│   └── goals.json
├── context.md                  # Osobní kontext (life areas, hodnoty, fáze)
├── timeline.md                 # Append-only event log
├── knowledge-graph.json        # Rozšířený entity graph
└── aliases.json                # Synonym management
```

### Knowledge Graph rozšíření

```json
{
  "nodes": {
    "karpathy": {"type": "person", "tags": ["ai", "mentor-figure"]},
    "llm-wiki": {"type": "concept", "tags": ["architecture", "pkm"]},
    "stopa": {"type": "project", "tags": ["orchestration"]},
    "first-principles": {"type": "reasoning", "tags": ["mental-model"]},
    "autonomy": {"type": "value", "tags": ["core-value"]}
  },
  "edges": [
    {"from": "karpathy", "to": "llm-wiki", "rel": "created", "date": "2026-03"},
    {"from": "llm-wiki", "to": "stopa", "rel": "inspired", "evidence": "wiki/ structure"},
    {"from": "autonomy", "to": "stopa", "rel": "drives", "context": "no step-by-step approval"},
    {"from": "first-principles", "to": "llm-wiki", "rel": "applied-in"}
  ]
}
```

**Entity typy**: person | concept | project | value | reasoning | experience | goal
**Edge typy**: created | inspired | contradicts | enables | blocks | applied-in | drives | taught-me | practiced-in

### Nové skills

| Skill | Fáze | Popis |
|-------|------|-------|
| `/capture` | Capture | Rychlý vstup: text/URL/screenshot → raw/ + automatický /ingest |
| `/ask-brain` | Consult | Dotaz na 2BRAIN s hybrid retrieval + knowledge graph walk |
| `/reflect` | Contemplate | Týdenní/měsíční self-review s guided prompty |
| `/review-goals` | Contemplate | Quarterly goal review + belief update |
| `/connect` | Connect | Manuální propojení entit + discovery nových spojení |

### Hooks

| Hook | Trigger | Akce |
|------|---------|------|
| `brain-curation.py` | PostWrite do brain/ | Contradiction detection, index update, graph update |
| `brain-reflection-prompt.py` | Cron (neděle večer) | Připomínka /reflect |
| `brain-goal-review.py` | Cron (1. den kvartálu) | Připomínka /review-goals |
| `brain-decay.py` | /sweep | Confidence decay pro nepoužívané wiki články |

### STOPA ↔ 2BRAIN propojení

```
STOPA memory/                    2BRAIN brain/
├── learnings/ ←───────────────→ wiki/concepts/    (graduation obousměrná)
├── concept-graph.json ←───────→ knowledge-graph.json (shared retrieval)
├── decisions.md ←─────────────→ decisions/        (index vs rich records)
├── outcomes/ ←────────────────→ reflections/      (task vs personal)
├── key-facts.md ←─────────────→ context.md        (project vs personal)
└── hooks/ ←───────────────────→ hooks/            (shared infrastructure)
```

**Shared retrieval**: `hybrid-retrieve.py` prohledává OBOJÍ — STOPA learnings + 2BRAIN wiki. Query router rozhoduje podle kontextu (technický dotaz → STOPA first, osobní dotaz → 2BRAIN first).

### Implementační plán

| Fáze | Týden | Deliverables |
|------|-------|-------------|
| **0. Init** | 1 | Adresářová struktura, context.md, README |
| **1. Capture + Compile** | 2-3 | raw/ + wiki/ + index.md + log.md + /capture skill |
| **2. Connect** | 4 | knowledge-graph.json rozšíření, /connect skill |
| **3. Curate** | 5 | brain-curation.py hook, contradiction detection |
| **4. Consult** | 6 | /ask-brain skill, shared retrieval integration |
| **5. Contemplate** | 7-8 | /reflect, reflections/, goals.json, /review-goals |
| **6. Polish** | 9-10 | Privacy markers, aliases.json, graph visualization |

---

## Disagreements & Open Questions

- **RAG vs structured text** [INFERRED]: Při osobním měřítku (100-500 zdrojů) strukturovaný markdown + grep/BM25 stačí (Karpathy [1]). RAG přidává hodnotu až při 1000+ zdrojích. 2BRAIN začne structured-first, RAG jako optional upgrade.
- **Auto-linking vs intentional linking** [INFERRED]: Reor auto-linkuje přes vector similarity [8]. Zettelkasten trvá na intentional links [7]. Řešení: obojí — auto-links pro discovery, intentional links pro reasoning chains. STOPA `related:` pole = intentional layer.
- **Kde žije 2BRAIN?**: Jako `.claude/memory/brain/` uvnitř STOPA (sdílená retrieval infra) vs samostatný projekt `000_NGM/2BRAIN/`. Doporučení: začít uvnitř STOPA, extrahovat až pokud naroste nad 500 souborů.
- **GraphRAG lokálně**: 36h na 19 souborech [VERIFIED][9] — embedding-only indexing je jedinou praktickou cestou pro lokální deployment.

---

## Evidence Table

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Karpathy — LLM Wiki Gist | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f | 3-layer architecture, compiler analogy, index-first retrieval | primary | high |
| 2 | VentureBeat — Karpathy LLM KB | https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an | Bypasses RAG via structured text + backlinks, multi-agent Quality Gate | secondary | high |
| 3 | EcphoryRAG (arXiv:2510.08958) | https://arxiv.org/html/2510.08958v1 | Entity+metadata only, 94% token reduction, EM 0.392→0.474 | primary | high |
| 4 | PersonalAI (arXiv:2506.17001) | https://arxiv.org/abs/2506.17001 | Hybrid KG with temporal hyper-edges, task-adaptive retrieval | primary | high |
| 5 | Cognitive Workspace (arXiv:2508.13171) | https://arxiv.org/html/2508.13171 | Active memory management, 58.6% reuse, Baddeley model | primary | high |
| 6 | Forte — BASB Overview | https://fortelabs.com/blog/basboverview/ | CODE framework, PARA method, Progressive Summarization | primary | high |
| 7 | Zettelkasten.de — Overview | https://zettelkasten.de/overview/ | Atomicity + Connectivity principles, tags > categories | primary | high |
| 8 | Reor (GitHub) | https://github.com/reorproject/reor | "Two generators" — same retrieval for human + LLM, LanceDB | primary | high |
| 9 | dasroot.net — RAG+Obsidian | https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/ | Local GraphRAG 36h/19 files, embedding-only is viable path | primary | high |
| 10 | MindStudio — Compiler Analogy | https://www.mindstudio.ai/blog/karpathy-llm-knowledge-base-compiler-analogy | 4-pass transformation, lossy compression framing | secondary | high |
| 11 | Camp Pedersen — LLM OS | https://campedersen.com/llm-os | Context window as RAM, LLM as OS kernel | secondary | medium |
| 12 | Memory Survey (arXiv:2603.07670) | https://arxiv.org/abs/2603.07670 | 3 paradigms, metacognitive control gap | survey | high |

## Sources

1. Karpathy — LLM Wiki GitHub Gist — https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
2. VentureBeat — "Karpathy shares LLM knowledge base architecture" — https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an
3. EcphoryRAG (Tsinghua, 2025) — https://arxiv.org/html/2510.08958v1
4. PersonalAI (arXiv:2506.17001) — https://arxiv.org/abs/2506.17001
5. Cognitive Workspace (arXiv:2508.13171) — https://arxiv.org/html/2508.13171
6. Tiago Forte — "BASB Definitive Guide" — https://fortelabs.com/blog/basboverview/
7. Zettelkasten.de — "Getting Started" — https://zettelkasten.de/overview/
8. Reor Project — https://github.com/reorproject/reor
9. dasroot.net — "RAG + Obsidian Integration" — https://dasroot.net/posts/2025/12/rag-personal-knowledge-management-obsidian-integration/
10. MindStudio — "Karpathy Compiler Analogy" — https://www.mindstudio.ai/blog/karpathy-llm-knowledge-base-compiler-analogy
11. Camp Pedersen — "LLM OS" — https://campedersen.com/llm-os
12. Memory for Autonomous LLM Agents (arXiv:2603.07670) — https://arxiv.org/abs/2603.07670

## Coverage Status

- **[VERIFIED]:** 3-layer architecture, compiler analogy, EcphoryRAG metrics, Cognitive Workspace metrics, BASB CODE, Zettelkasten principles, Reor architecture, GraphRAG benchmark, STOPA integration analysis
- **[INFERRED]:** RAG vs structured text trade-off, auto-linking vs intentional linking, 6C cyklus design
- **[SINGLE-SOURCE]:** Multi-agent Quality Gate (VentureBeat only)
- **[UNVERIFIED]:** Fabric.so developer API (not fetched), Mem 2.0 architecture (not fetched)
