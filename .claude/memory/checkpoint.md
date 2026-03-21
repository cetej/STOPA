# Session Checkpoint

**Saved**: 2026-03-21
**Task**: Záchvěv — Session 7: Srozumitelný výstup + UI
**Branch**: main
**Repo**: https://github.com/cetej/ZACHVEV
**Status**: Bloky 1-8 implementovány, topic labeling + UI layout potřebují přepracovat

## Co je hotové (Sessions 1-7)

### Fáze 0 — PoC (kompletní ✓)
- [x] Reddit ingest via Arctic Shift API
- [x] Sentiment: `tabularisai/multilingual-sentiment-analysis` (DistilBERT, 5 tříd)
- [x] Embeddings: `Seznam/simcse-small-e-czech` (256-dim)
- [x] EWS detekce: ewstools (variance, lag-1 AC, Kendall tau)

### Topic Discovery (kompletní ✓)
- [x] UMAP (256d → 15d) + HDBSCAN clustering
- [x] TF-IDF-like labeling, Czech+English stopwords (rozšířené)
- [x] Emerging topic detection (growth ratio)

### Interpretace + Intervence (kompletní ✓)
- [x] CRI (Cascade Risk Index) — 3 pilíře: temporal 0.4, structural 0.3, narrative 0.3
- [x] 5 intervenčních strategií (inokulace, bridge_amplification, counter_framing, friction_injection, energy_redirection)
- [x] Targeting: SHA256 anonymizace, 3 role (influencer/bridge/catalyst)
- [x] Campaign planner: auto-populated kontext z dat
- [x] Content templates s českou diakritikou

### Webové rozhraní (Session 6-7)
- [x] FastAPI backend (port 8000) — `zachvev/api/app.py`
- [x] Streamlit frontend (port 8501) — `ui/app.py`
- [x] 4 tabs: Analýza, Targeting, Kampaň, Vizuály
- [x] Session history (save/load)
- [x] Interpretační vrstva (`zachvev/analyze/interpreter.py`) — situation_report, topic_description, strategy_explanation, targeting_explanation

### Session 7 — Bloky 1-8 implementovány
- [x] Blok 1: situation_report v češtině (interpret_situation)
- [x] Blok 2: topic_description (interpret_topic_description)
- [x] Blok 3: strategy_explanation (interpret_strategy_choice)
- [x] Blok 4: targeting_explanation (interpret_targeting)
- [x] Blok 5: example_posts v API response
- [x] Blok 6: top_authors v API response
- [x] Blok 7: UI tabs přestrukturovány — interpretace nahoře, metriky v expanderu
- [x] Blok 8: České diacritiky ve všech content templates

## NEVYŘEŠENÉ PROBLÉMY (pro Session 8)

### 1. Topic labeling — KRITICKÉ
**Problém**: TF-IDF keyword extraction z krátkých Reddit titulků produkuje nesmyslné labely ("proč / někdo / vás", "the / czech / for"). Stopwords byly rozšířeny, ale fundamentální přístup je špatný.

**Zjištění z analýzy**: CLI pipeline i web UI používají STEJNÝ kód (`topics.py:label_clusters()`). "Dobré" labely z CLI pocházely z velkého datasetu (5000-6615 postů) kde TF-IDF funguje lépe. Na menších live-fetched datech TF-IDF selhává.

**Možná řešení**:
- LLM-based labeling — poslat example_titles z clusteru do Claude a nechat pojmenovat téma
- Použít `top_title` (nejčtenější post v clusteru) jako label místo klíčových slov
- Hybrid: keywords + representative title
- BERTopic-style c-TF-IDF s lepší normalizací

### 2. UI layout — DŮLEŽITÉ
**Problém**: Uživatel řekl "Připomíná ti náhodně nasypaný hnůj" — layout je chaotický, informace nejsou vizuálně organizované. Potřebuje redesign.

### 3. growth_ratio edge case
**Problém**: `interpret_situation()` přistupuje k `row["growth_ratio"]` bez guardu — může failnout na `inf` hodnoty. `_build_topic_summaries` má fix (`np.isfinite()`), ale interpret_situation ne.

## Aktuální architektura

```
ZACHVEV/
├── zachvev/
│   ├── ingest/reddit.py          # Arctic Shift API
│   ├── process/
│   │   ├── sentiment.py          # DistilBERT sentiment
│   │   └── embeddings.py         # Seznam/simcse-small-e-czech
│   ├── detect/
│   │   ├── ews.py                # ewstools wrapper
│   │   └── topics.py             # UMAP + HDBSCAN + TF-IDF labeling
│   ├── analyze/
│   │   ├── interpreter.py        # CRI, narativní signály, interpretace v CZ
│   │   └── interventions.py      # 5 strategií, intervenční okna
│   ├── intervene/
│   │   ├── content.py            # Generátor obsahu (šablony + Claude API)
│   │   ├── targeting.py          # Analýza účtů, leverage scoring
│   │   ├── campaign.py           # Kampaňový plánovač
│   │   └── visuals.py            # Vizuální prompty
│   └── api/
│       ├── app.py                # FastAPI backend (v0.7.0)
│       └── models.py             # Pydantic modely
├── ui/
│   └── app.py                    # Streamlit frontend
├── scripts/
│   ├── poc_phase0.py
│   ├── discover_topics.py
│   ├── full_report.py
│   └── generate_campaign.py
└── data/
    ├── letna_sentiment.parquet   # 6615 postů test data
    ├── embeddings.npy            # 6615×256d
    └── sessions/                 # Uložené UI sessions
```

## Servery

- **NG-ROBOT**: `python ngrobot_web.py` z `NG-ROBOT/` → http://localhost:5001
- **Záchvěv API**: `uvicorn zachvev.api.app:app --host 0.0.0.0 --port 8000` z `ZACHVEV/` → http://localhost:8000
- **Záchvěv UI**: `streamlit run ui/app.py --server.port 8501 --server.headless true` z `ZACHVEV/` → http://localhost:8501

## Technické poznatky

| Problém | Řešení |
|---------|--------|
| Reddit API vyžaduje approval | Arctic Shift API (`arctic-shift.photon-reddit.com`) |
| FERNET-C5 je MaskedLM | `tabularisai/multilingual-sentiment-analysis` |
| HDBSCAN 95% noise na 256d | UMAP redukce (256→15d) před clusteringem |
| Port 8000 obsazený | `taskkill //F //IM python.exe` před restartem |
| TF-IDF labely nesmyslné | Rozšířit stopwords + zvážit LLM labeling (Session 8) |

## Resume Prompt

> Záchvěv — Session 8: Oprava topic labeling + UI redesign.
> Repo: ZACHVEV (branch main)
>
> Systém kompletní end-to-end: sběr → sentiment → embeddings → clustering → CRI → interpretace → intervence → kampaň → UI. Validováno na Letná datech (6615 postů, CRI 0.52).
>
> **Hlavní problémy k řešení:**
> 1. Topic labeling produkuje nesmyslné názvy — TF-IDF na krátkých titulcích selhává. Zvážit LLM-based labeling (poslat example titles do Claude → pojmenovat cluster).
> 2. UI layout je chaotický — potřebuje vizuální redesign (hierarchie informací, čisté karty, méně textu najednou).
> 3. growth_ratio edge case v interpret_situation() — chybí guard na inf hodnoty.
>
> Checkpoint: `STOPA/.claude/memory/checkpoint.md`
> Uncommitted changes: rozšířené stopwords v `topics.py`
