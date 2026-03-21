# Session Checkpoint

**Saved**: 2026-03-21
**Task**: Záchvěv — Session 5: Intervenční obsahová vrstva
**Branch**: master
**Repo**: https://github.com/cetej/ZACHVEV
**Status**: Fáze 0 + analýza/intervence hotové, další krok = obsahová produkce

## Kontext projektu

**Záchvěv** je systém pro detekci, predikci a modelování intervencí u názorových kaskád na sociálních sítích. Funguje jako seismograf — detekuje kde se hromadí napětí a blíží tipping point. Na rozdíl od MiroFish (syntetičtí agenti) analyzuje reálná data z reálných sítí.

**Projektový dokument**: `STOPA/research/cascade-monitor-project.md` (700+ řádků, 12 kapitol)

## Co je hotové

### Fáze 0 — PoC (kompletní ✓)
- [x] Repozitář + pyproject.toml
- [x] Reddit ingest via Arctic Shift API (ne PRAW — Reddit zavřel self-service API)
- [x] Sentiment: `tabularisai/multilingual-sentiment-analysis` (ne FERNET-C5 — ten je MaskedLM, ne klasifikátor)
- [x] Embeddings: `Seznam/simcse-small-e-czech` (256-dim)
- [x] EWS detekce: ewstools (variance, lag-1 AC, Kendall tau trendy)
- [x] Validace na syntetických + reálných datech (r/czech Jan-Feb 2025)

### Topic Discovery (kompletní ✓)
- [x] UMAP (256d → 15d) + HDBSCAN clustering
- [x] TF-IDF-like labeling, Czech stopwords
- [x] Emerging topic detection (growth ratio 7d vs prev 7d)
- [x] Topic dashboard vizualizace

### Letná Case Study (kompletní ✓)
- [x] 6615 postů (Feb-Mar 2026), demonstrace Milion chvilek
- [x] Topic 14 (vláda/politika) — oba EWS signály rostou (variance τ=+0.545, AC τ=+0.283)
- [x] Potvrzeno: systém detekuje pre-kaskádové napětí u reálné české politické události

### Interpretace + Intervence (kompletní ✓)
- [x] `zachvev/analyze/interpreter.py` — Cascade Risk Index (3 pilíře: temporal 0.4, structural 0.3, narrative 0.3)
- [x] České narativní slovníky (absolutismus, urgence, dehumanizace, polarizace, mobilizace)
- [x] Situační analýza v češtině (textový report)
- [x] `zachvev/analyze/interventions.py` — 5 strategií (inokulace, bridge amplification, counter-framing, friction injection, energy redirection)
- [x] Detekce intervenčních oken, doporučení strategií podle CRI + fáze
- [x] `scripts/full_report.py` — kompletní pipeline data→interpretace→intervence
- [x] Validace na Letná datech: CRI 0.52 (PREKRITICKÝ STAV)

## Aktuální struktura repozitáře

```
ZACHVEV/
├── pyproject.toml
├── CLAUDE.md
├── zachvev/
│   ├── ingest/
│   │   └── reddit.py          # Arctic Shift API collector
│   ├── process/
│   │   ├── sentiment.py       # tabularisai/multilingual-sentiment-analysis
│   │   └── embeddings.py      # Seznam/simcse-small-e-czech (256d)
│   ├── detect/
│   │   ├── ews.py             # ewstools wrapper (variance, AC1, Kendall tau)
│   │   └── topics.py          # UMAP + HDBSCAN topic discovery
│   ├── analyze/
│   │   ├── interpreter.py     # CRI index, narativní signály, situační analýza
│   │   └── interventions.py   # 5 strategií, intervenční okna, doporučení
│   └── viz/                   # (prázdné — Streamlit dashboard později)
├── scripts/
│   ├── poc_phase0.py          # ingest → sentiment → EWS pipeline
│   ├── discover_topics.py     # topic discovery + per-topic EWS
│   └── full_report.py         # kompletní analýza + intervence
└── data/                      # (gitignored) parquety, embeddings, reporty
```

## Technické poznatky (důležité pro další session)

| Problém | Řešení |
|---------|--------|
| Reddit API vyžaduje Responsible Builder Policy approval | Přepojeno na Arctic Shift API (`arctic-shift.photon-reddit.com`) |
| FERNET-C5-RoBERTa je MaskedLM, ne klasifikátor | Nahrazeno `tabularisai/multilingual-sentiment-analysis` (DistilBERT, 5 tříd) |
| HDBSCAN 95% noise na 256d embeddings | UMAP redukce (256d → 15d) před clusteringem |
| ewstools `apply_classifier_ewsnet` API changed | Nepoužíváme EWSNet, stačí statistické EWS (variance + AC) |
| `created_utc` z Arctic Shift je epoch int, ne string | `_epoch_to_datetime()` helper + epoch cursor pro paginaci |

## Další krok — Session 5: Intervenční obsahová vrstva

### Cíl
Přeměnit abstraktní strategická doporučení na **konkrétní akční výstupy**: texty zpráv, vizuály, cílení na klíčové účty. Systém nemá jen říct "použij counter-framing" — má navrhnout **konkrétní obsah** a **kam ho distribuovat**.

### Nové moduly k implementaci

#### 1. `zachvev/intervene/content.py` — Generátor intervenčního obsahu
Vstup: strategie + topic info + narativní kontext
Výstup: konkrétní texty/obsahy pro šíření

- **Pro každou z 5 strategií** navrhnout šablony a generátor obsahu:
  - Inokulace → prebunkingové posty ("Pozor na tuto techniku manipulace: ...")
  - Counter-framing → přerámování ("Místo X se podívejme na Y...")
  - Bridge amplification → podpůrné zprávy pro mostové hlasy
  - Friction injection → kontextové štítky, fact-check labely
  - Energy redirection → konstruktivní alternativy ("Chcete změnu? Tady je jak...")

- **Formáty výstupů:**
  - Krátký post (Reddit/Twitter/X styl, max 280 znaků)
  - Střední post (Facebook/Reddit styl, 1-3 odstavce)
  - Celý článek/zpráva pro web (strukturovaný, s titulkem, lead, tělo)
  - Prompt pro generování obrázku/memu (pro AI image generátor)
  - Infografika brief (data + vizuální layout popis)

- **LLM generování:** Použít Claude API pro finální copywriting. Modul připraví strukturovaný prompt s kontextem (topic keywords, sentiment, narativní markery, cílová strategie) → Claude vygeneruje text v požadovaném formátu a tónu.

#### 2. `zachvev/intervene/targeting.py` — Identifikace klíčových účtů a pákového efektu
Vstup: topic data + user aktivita z postů
Výstup: seznam klíčových účtů pro distribuci

- **Metriky pro identifikaci klíčových účtů:**
  - Volume: kdo nejvíc publikuje v daném topicu
  - Engagement: čí posty mají nejvyšší score/komentáře
  - Cross-topic reach: kdo publikuje napříč tématy (mostové uzly)
  - Sentiment influence: korelace mezi posty účtu a sentiment shift

- **Pákový efekt:**
  - Identifikovat účty s disproporčním dosahem (vysoké engagement/post ratio)
  - Rozlišit: influenceři (velký dosah), mosty (cross-community), katalyzátoři (startují diskuze)
  - Pro každou strategii doporučit jiný typ účtu (bridge amplification → mosty, counter-framing → influenceři, atd.)

- **Data z Arctic Shift:** Rozšířit reddit.py o stahování comment-level dat a user profilů. Author field v postech → frequency analysis, engagement scoring.

#### 3. `zachvev/intervene/campaign.py` — Kampaňový plánovač
Vstup: CRI result + obsah + targeting
Výstup: kompletní akční plán

- Spojí obsah (co říct) + targeting (komu/kde) + timing (kdy) do uceleného plánu
- Vygeneruje timeline: "Den 1: prebunking posty přes X, Den 2: counter-frame článek přes Y..."
- Odhad dosahu a efektivity
- Export do formátu připraveného pro exekuci

#### 4. Vizuální obsah
- Integrace s existujícím `visual-data-architect` skillem pro generování JSON promptů pro Nano Banana Pro
- Návrh memů/infografik: textový brief → vizuální prompt → generování
- Šablony pro typické formáty (srovnávací infografika, fact-check karta, narativní mapa)

### Úkoly Session 5

```
1. Vytvořit zachvev/intervene/__init__.py
2. Vytvořit zachvev/intervene/content.py — generátor obsahu (šablony + LLM prompt builder)
3. Vytvořit zachvev/intervene/targeting.py — analýza účtů, pákový efekt, doporučení distribuce
4. Rozšířit ingest/reddit.py — stahování komentářů a author dat pro targeting
5. Vytvořit zachvev/intervene/campaign.py — kampaňový plánovač (obsah + targeting + timing)
6. Vytvořit zachvev/intervene/visuals.py — generování vizuálních promptů (memy, infografiky)
7. Vytvořit scripts/generate_campaign.py — end-to-end: analýza → obsah → targeting → plán
8. Otestovat na Letná datech — vygenerovat ukázkovou kampaň
9. Aktualizovat CLAUDE.md s novou architekturou
10. Commit + push
```

### Architektonické rozhodnutí k prodiskutování

- **LLM pro obsah:** Použít Claude API přes `anthropic` SDK? Nebo lokální model? Claude je kvalitnější pro češtinu, ale stojí peníze. Hybrid: šablony pro jednoduché formáty, Claude pro články a komplexní obsah.
- **Etika:** Systém generuje obsah určený k ovlivňování diskurzu. Potřebuje jasné mantinely — kdo může používat, na co, s jakým oversight. Implementovat jako config/policy layer.
- **Targeting privacy:** Identifikace klíčových účtů z veřejných dat je legální, ale citlivé. Anonymizace v reportech? Agregované profily místo jmen?

## Resume Prompt

> Záchvěv — Session 5: Intervenční obsahová vrstva.
> Repo: https://github.com/cetej/ZACHVEV (branch master)
>
> Systém umí: sběr dat (Arctic Shift) → sentiment → embeddings → topic discovery → EWS detekce → CRI index → situační analýza → intervenční doporučení. Validováno na Letná datech (CRI 0.52, prekritický stav).
>
> **Další krok:** Přeměnit abstraktní strategická doporučení na konkrétní akční výstupy. Nové moduly v `zachvev/intervene/`:
> 1. `content.py` — generátor textů (posty, články, memy) pro 5 intervenčních strategií
> 2. `targeting.py` — identifikace klíčových účtů s největším dosahem (pákový efekt)
> 3. `campaign.py` — kampaňový plánovač (obsah + targeting + timing)
> 4. `visuals.py` — vizuální prompty pro AI generátory (memy, infografiky)
>
> Podrobný plán: viz checkpoint (`STOPA/.claude/memory/checkpoint.md`)
> Technické poznatky (Arctic Shift místo PRAW, tabularisai místo FERNET, UMAP před HDBSCAN): tamtéž.
