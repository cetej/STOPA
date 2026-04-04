# MiroShark — Open-Source Swarm Intelligence Engine

*Research report, 2026-04-04*

## TL;DR

MiroShark je anglický fork čínského projektu **MiroFish** (666ghj/Shanda Group). Nahraješ dokument/zprávu, systém extrahuje entity do Neo4j knowledge grafu, automaticky vygeneruje stovky AI agentů s unikátními osobnostmi a spustí simulaci sociální sítě (Twitter + Reddit + Polymarket paralelně). Výstupem je analytická zpráva o tom, jak se narativy šíří, mění a konvergují.

**Repo:** [github.com/aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
**Licence:** AGPL-3.0
**Stav:** 427 stars, 68 forks, aktivní vývoj (15 dní od vzniku, poslední push 2026-04-04)

---

## Architektura — 5 fází

### Fáze 1: Graph Build
- Nahraje se dokument (PDF, text, novinka)
- NER extrakce entit a vztahů do **Neo4j knowledge grafu**
- Few-shot příklady + rejection rules proti garbage entitám
- Paralelizovaný chunk processing s batched Neo4j writes (UNWIND)

### Fáze 2: Agent Setup
- Z každé entity v grafu se generuje persona
- 5 vrstev kontextu per agent:
  1. Atributy z grafu
  2. Vztahy (relationships)
  3. Sémantické vyhledávání
  4. Související uzly
  5. LLM-powered web research (auto-trigger pro veřejné osoby nebo při tenkém kontextu <150 znaků)
- Auto-detekce individual vs. institutional persona (keyword matching)

### Fáze 3: Simulace (CAMEL-AI/OASIS engine)
- 3 platformy běží paralelně přes `asyncio.gather`:
  - **Twitter** — posty, lajky, reposty
  - **Reddit** — komentáře, upvoty, vlákna
  - **Polymarket** — trading na constant-product AMM (ne 50/50 initial prices)
- **Market-Media Bridge**: sentiment ze sociálních sítí -> trader prompty, market ceny -> social media prompty
- Typicky ~40 kol x 100+ agentů
- Sliding-window round memory (staré kola kompaktuje background LLM)
- Belief state per agent: stance (-1 to +1), confidence (0-1), trust per agent (0-1)

### Fáze 4: Report (ReACT agent)
- Analytický agent s přístupem k:
  - `simulation_feed` (skutečné posty/komentáře/obchody)
  - `market_state` (ceny, P&L)
  - Graph search
  - Belief trajectory tools
- Cituje co agenti skutečně řekli a jak se trhy pohnuly

### Fáze 5: Interakce
- Chat s jednotlivými agenty (persona chat)
- Skupinové dotazy
- Profily agentů + historie simulace

---

## Technický stack

| Komponenta | Technologie |
|-----------|-------------|
| Backend | Python 3.11+, Flask, Pydantic |
| Frontend | Node.js 18+ |
| Databáze | Neo4j 5.15+ (knowledge graph + vector embeddings) |
| Simulační engine | OASIS (CAMEL-AI), bundled jako "wonderwall" |
| PDF parsing | PyMuPDF |
| LLM komunikace | OpenAI SDK (unified) |

### Podpora LLM — 4 deployment režimy

| Režim | Popis |
|-------|-------|
| **Cloud API** | OpenRouter, OpenAI, Anthropic — cokoliv OpenAI-kompatibilní |
| **Local Ollama** | Lokální modely (qwen3.5:27b, qwen3:14b, qwen3:8b) |
| **Claude Code CLI** | Přes CC subscription (bez API klíče, ale ~2-5s overhead per call) |
| **Hybrid (Smart Model)** | Ollama pro bulk simulační kola, cloud/Claude pro reporty a ontologii |

### Doporučené modely

**Cloud (OpenRouter):**
| Model | Cena za simulaci |
|-------|-----------------|
| Qwen3 235B A22B | ~$0.30 |
| GPT-5 Nano | ~$0.41 |
| Gemini 2.5 Flash Lite | ~$0.58 |
| DeepSeek V3.2 | ~$1.11 |

**Lokální (Ollama):**
| Model | VRAM | Rychlost |
|-------|------|----------|
| qwen3.5:27b | 20GB+ | ~40 t/s |
| qwen3.5:35b-a3b (MoE) | 16GB | ~112 t/s |
| qwen3:14b | 12GB | ~60 t/s |
| qwen3:8b | 8GB | ~42 t/s |

**Embeddings:** `nomic-embed-text` (Ollama, 768 dims) nebo `text-embedding-3-small` (OpenAI via OpenRouter)

**Omezení:** CAMEL-AI engine vyžaduje OpenAI-kompatibilní API i v Claude Code režimu — sám si řídí LLM spojení interně.

---

## Deployment

```bash
docker compose up -d
```

Spustí 3 služby:
- `neo4j:5.15-community` (porty 7474/7687)
- `ollama/ollama:latest` (port 11434)
- `ghcr.io/aaronjmars/miroshark:latest` (porty 3000/5001)

### HW požadavky

| | Lokální minimum | Doporučeno | Cloud režim |
|---|---|---|---|
| RAM | 16 GB | 32 GB | 4 GB |
| VRAM | 10 GB | 24 GB | Nepotřeba |
| Disk | 20 GB | 50 GB | Minimální |

**Gotcha:** Ollama defaultně používá 4096 token context, ale MiroShark prompty potřebují 10-30K. Nutný custom Modelfile s `PARAMETER num_ctx 32768`.

---

## Lineage (původ)

```
MiroFish (666ghj, Shanda Group, čínsky)
  └── MiroFish-Offline (nikmcfly) — přidal Neo4j + Ollama offline vrstvu
       └── MiroShark (aaronjmars) — anglický překlad, vylepšený flow,
                                     Claude Code integrace, model configs
```

Simulační engine pochází z **OASIS** (CAMEL-AI) — Open Agent Social Interaction Simulations.

---

## Ekosystém a komunita

| Metrika | Hodnota |
|---------|---------|
| Stars | 427 |
| Forks | 68 |
| Stáří | 15 dní (2026-03-20) |
| Autor | Aaron Elijah Mars (používá Claude Opus 4.6 jako co-author) |
| Open issues | 3 |

**Související projekty:**
- [miroshark-aeon](https://github.com/aaronjmars/miroshark-aeon) — public agent automation layer
- [supercompact-for-miroshark](https://github.com/JohnTammi/supercompact-for-miroshark) — TypeScript token mincer (40-60% cost reduction)
- [prelaunchagents](https://github.com/HusseinJX/prelaunchagents) — product launch simulator postavený na MiroShark

---

## Limity a kritika

### Technické
- Claude Code režim: ~2-5s overhead per LLM call (subprocess spawn) — jen pro malé simulace nebo hybrid
- CAMEL-AI simulační kola nemůžou používat Claude Code přímo — vždy potřeba Ollama nebo cloud API
- Ollama default context (4096) je příliš malý — vyžaduje ruční override
- Upstream MiroFish napsal 20letý student za 10 dní — codebase je stále early-stage

### Konceptuální
- **Žádné published benchmarky** porovnávající predikce s historickými výsledky
- Jeden analytik to popsal jako "SimCity for prediction" — fascinující pro exploraci, ale neprokázaná prediktivní přesnost
- OASIS framework je z výzkumného kontextu, ne production-validovaný pro reálné prediction markets
- Generuje přesvědčivé narativy, ale to != přesné predikce

---

## Relevance pro STOPA/naše projekty

### Co je zajímavé
1. **Knowledge graph -> persona generation pipeline** — automatická tvorba agentů z dokumentu
2. **Cross-platform bridge** (sentiment <-> ceny) — elegantní pattern pro propojení různých simulačních domén
3. **Belief state tracking** (stance, confidence, trust) — jednoduchý ale funkční model pro agent dynamics
4. **Smart Model routing** — levný model pro bulk, drahý pro analýzu — přesně náš budget tier pattern
5. **Sliding-window round memory** — kompakce starších kol backgroundem — relevantní pro naše autoloop

### Co je problematické
1. AGPL-3.0 licence — virální, omezuje komerční použití
2. Závislost na CAMEL-AI/OASIS (specifický framework, ne general-purpose)
3. Žádná validace prediktivní kvality
4. Early-stage codebase (15 dní, 1 hlavní přispěvatel)

### Potenciální využití
- **Záchvěv**: MiroShark pattern (knowledge graph -> agent personas -> simulace) by mohl doplnit naše EWS/CRI modely o "narrative simulation" vrstvu — jak se názorová kaskáda vyvine
- **MONITOR**: Simulace reakcí na zpravodajské události před jejich publikací
- **Obecně**: Belief state pattern (stance/confidence/trust per agent) je jednoduchý a dá se adoptovat nezávisle na MiroSharku

---

## Zdroje

- [GitHub: aaronjmars/MiroShark](https://github.com/aaronjmars/MiroShark)
- [GitHub: 666ghj/MiroFish](https://github.com/666ghj/MiroFish) (upstream)
- [GitHub: camel-ai/oasis](https://github.com/camel-ai/oasis) (simulační engine)
- [GitHub: nikmcfly/MiroFish-Offline](https://github.com/nikmcfly/MiroFish-Offline) (offline fork)
- [Microlaunch: MiroShark](https://microlaunch.net/p/miroshark)
- [Medium: MiroFish Swarm Intelligence](https://agentnativedev.medium.com/mirofish-swarm-intelligence-with-1m-agents-that-can-predict-everything-114296323663)
- [LinkedIn: Swarm Intelligence Forecasting](https://www.linkedin.com/pulse/swarm-intelligence-comes-forecasting-how-mirofish-simulates-borish-lahve)
