# ORAKULUM — Project Specification

**Verze:** 0.2
**Datum:** 2026-03-28
**Autor:** deepresearch syntéza + architektonická analýza + review (10 bodů)

---

## 1. Mise

ORAKULUM je sdílená Python knihovna + API server pro **predikci a korelační analýzu** z heterogenních datových zdrojů. Tři cílové projekty ji konzumují:

| Konzument | Stack | Integrace | Používá z ORAKULUM |
|-----------|-------|-----------|-------------------|
| **MONITOR** | Node.js (Express) | FastAPI HTTP | Anomaly detection, event correlation, geopolitická predikce |
| **POLYBOT** | Python (FastMCP) | Přímý import | Event→odds korelace, market data, encoding, prediction |
| **Záchvěv** | Python | Přímý import | Cascade prediction, narativní korelace, changepoint detection |

### Boundary pravidlo

ORAKULUM dodává **analytiku a data** — nikdy execution:
- **V ORAKULUM:** encoding, correlation, prediction, anomaly detection, read-only data adaptery, API server
- **V konzumentech:** execution logika (POLYBOT paper trading engine, MCP tools), projekt-specifické datové zdroje (ČNB, Arctic Shift, Reddit), UI/UX

---

## 2. Architektura

```
┌────────────────────────────────────────────────────────────────┐
│                         ORAKULUM                               │
│                                                                │
│  ┌──────────┐  ┌────────────┐  ┌──────────────┐  ┌─────────┐ │
│  │ SOURCES  │→ │  ENCODING  │→ │ CORRELATION  │→ │PREDICTION│ │
│  │          │  │            │  │              │  │          │ │
│  │ gdelt    │  │ text(tfidf)│  │ tigramite    │  │ ts(darts)│ │
│  │ news     │  │ events     │  │ causal-learn │  │ foundatn │ │
│  │ polymark │  │ numeric    │  │ granger      │  │ binary   │ │
│  │          │  │ temporal   │  │ causal graph │  │ router   │ │
│  │          │  │ mixed      │  │              │  │          │ │
│  └──────────┘  └────────────┘  └──────────────┘  └─────────┘ │
│                                                                │
│  ┌──────────┐  ┌────────────┐  ┌──────────────┐  ┌─────────┐ │
│  │ ANOMALY  │  │   STORE    │  │    SERVE     │  │  UTILS  │ │
│  │          │  │            │  │              │  │         │ │
│  │ stumpy   │  │ local(sql) │  │ fastapi      │  │ metrics │ │
│  │ changept │  │ feast      │  │ routes       │  │ viz     │ │
│  │          │  │            │  │              │  │ config  │ │
│  └──────────┘  └────────────┘  └──────────────┘  └─────────┘ │
│                                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ PIPELINE — sklearn-compatible kroky + PipelineResult    │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

### Designové principy

1. **sklearn kontrakt**: Všechny moduly implementují `.fit()` / `.transform()` / `.predict()` / `.detect()`
2. **Hybrid Pipeline**: Kroky jsou sklearn-compatible, ale Pipeline vrací bohatý `PipelineResult(forecast, causal_graph, anomalies, metadata)`
3. **Progresivní deps**: v0.1 core < 100MB (bez PyTorch). Heavy deps (Chronos-2, Darts, sentence-transformers) jsou opt-in extras v0.2+
4. **Data adapter ≠ execution**: `sources/` modul dodává read-only data. Execution logika patří konzumentům
5. **Dual correlation backend**: Tigramite (primary, ověřeno na Windows) + causal-learn (fallback)
6. **Žádné API klíče v kódu**: Env vars pro vše

---

## 3. Struktura projektu

```
ORAKULUM/
├── pyproject.toml
├── README.md
├── CLAUDE.md
├── .claude/
│   ├── settings.json
│   └── memory/
├── src/
│   └── orakulum/
│       ├── __init__.py              # Public API exports
│       ├── py.typed                 # PEP 561
│       ├── pipeline.py              # Pipeline + PipelineResult
│       │
│       ├── sources/                 # Modul 0: Data loaders (read-only)
│       │   ├── __init__.py
│       │   ├── base.py              # BaseSource(ABC)
│       │   ├── gdelt.py             # GDELTLoader (CAMEO events, Gamma API)
│       │   ├── news.py              # NewsFetcher (generic RSS/API news)
│       │   └── polymarket.py        # PolymarketLoader (read-only: markets, orderbook, prices)
│       │
│       ├── encoding/                # Modul 1: Feature encoding
│       │   ├── __init__.py
│       │   ├── base.py              # BaseEncoder(ABC)
│       │   ├── text.py              # TextEncoder (TF-IDF default; sentence-transformers opt-in)
│       │   ├── events.py            # EventEncoder (CAMEO → daily feature matrix)
│       │   ├── numeric.py           # NumericEncoder (scaling, lag features, rolling stats)
│       │   ├── temporal.py          # TemporalAligner (align heterogeneous sources to common freq)
│       │   └── mixed.py             # MixedEncoder (orchestrace encoderů)
│       │
│       ├── correlation/             # Modul 2: Causal/correlation discovery
│       │   ├── __init__.py
│       │   ├── base.py              # BaseCorrelation(ABC)
│       │   ├── tigramite.py         # TigramiteDiscovery (PCMCI+, ParCorr; CMIknn s numba opt-in)
│       │   ├── causal_learn.py      # CausalLearnDiscovery (PC, FCI, GES — fallback)
│       │   ├── granger.py           # GrangerCausality (klasický + sparse LASSO)
│       │   └── graph.py             # CausalGraph (output + NetworkX + viz)
│       │
│       ├── prediction/              # Modul 3: Forecasting (v0.2)
│       │   ├── __init__.py
│       │   ├── base.py              # BasePredictor(ABC) — sklearn interface
│       │   ├── timeseries.py        # TSPredictor (Darts/sktime wrapper)
│       │   ├── foundation.py        # FoundationPredictor (Chronos-2, TimesFM)
│       │   ├── binary.py            # BinaryPredictor (LLM ensemble pro events)
│       │   └── router.py            # ModelRouter (local/global/foundation tier)
│       │
│       ├── anomaly/                 # Modul 4: Anomaly & changepoint detection
│       │   ├── __init__.py
│       │   ├── base.py              # BaseDetector(ABC)
│       │   ├── matrix_profile.py    # StumpyDetector (motifs, discords)
│       │   ├── autoencoder.py       # AEDetector (pro OSINT unrest detection, v0.2)
│       │   └── changepoint.py       # ChangepointDetector (PELT, BOCPD)
│       │
│       ├── store/                   # Modul 5: Feature store
│       │   ├── __init__.py
│       │   ├── base.py              # BaseStore(ABC)
│       │   ├── local.py             # LocalStore (SQLite/parquet cache)
│       │   └── feast.py             # FeastStore (production, opt-in)
│       │
│       ├── serve/                   # Modul 6: FastAPI server
│       │   ├── __init__.py
│       │   ├── app.py               # FastAPI app factory
│       │   ├── routes/
│       │   │   ├── anomaly.py       # POST /api/v1/anomaly
│       │   │   ├── correlation.py   # POST /api/v1/correlation
│       │   │   ├── predict.py       # POST /api/v1/predict (v0.2)
│       │   │   ├── sources.py       # GET /api/v1/sources/{source}/data
│       │   │   └── health.py        # GET /health
│       │   └── schemas.py           # Pydantic request/response models
│       │
│       ├── cli.py                   # Typer CLI (v0.1: serve + detect)
│       │
│       └── utils/
│           ├── __init__.py
│           ├── metrics.py           # AUC, F1, MAPE, Sharpe, calibration
│           ├── viz.py               # Causal graph viz, prediction plots
│           └── config.py            # Settings (pydantic-settings, env vars)
│
├── tests/
│   ├── conftest.py                  # Fixtures, sample data generators
│   ├── test_sources/
│   ├── test_encoding/
│   ├── test_correlation/
│   ├── test_prediction/
│   ├── test_anomaly/
│   ├── test_serve/
│   └── test_integration/            # End-to-end pipeline tests
│
├── examples/
│   ├── quickstart.py                # Minimal E2E demo
│   ├── monitor_gdelt.py             # GDELT → anomaly + causal graph
│   ├── polybot_edge.py              # News → market correlation
│   └── zachvev_cascade.py           # Reddit signals → changepoint detection
│
└── docs/
    ├── LEARNINGS.md
    └── TROUBLESHOOTING.md
```

---

## 4. API Design

### 4.0 Sources (Data Loaders)

```python
from orakulum.sources import GDELTLoader, PolymarketLoader, NewsFetcher

# GDELT events
gdelt = GDELTLoader(
    cameo_categories=["14", "18", "19"],  # protest, assault, conflict
    region="Middle East",
    date_range=("2025-01-01", "2026-03-28")
)
events_df = gdelt.fetch()  # DataFrame: date, actor1, actor2, event_type, goldstein, tone, url

# Polymarket (read-only)
poly = PolymarketLoader()
markets = poly.get_active_markets(category="politics")
book = poly.get_order_book(condition_id="0x...")
prices = poly.get_price_history(condition_id="0x...", days=90)

# Generic news
news = NewsFetcher(sources=["reuters", "bbc"], keywords=["conflict", "sanctions"])
articles_df = news.fetch(days=30)  # DataFrame: date, title, body, source, url
```

**Konzument-specifické loadery (NE v ORAKULUM):**
- MONITOR: ČNB, ČHMÚ, NÚKIB, ČTK — zůstávají v `MONITOR/apis/sources-cz/`
- Záchvěv: Arctic Shift, Reddit API — zůstávají v Záchvěv pipeline
- POLYBOT: Binance WebSocket — zůstává v POLYBOT

### 4.1 Encoding

```python
from orakulum.encoding import TextEncoder, EventEncoder, NumericEncoder, MixedEncoder
from orakulum.encoding import TemporalAligner

# Temporal alignment — KRITICKÉ pro správnost korelace
aligner = TemporalAligner(
    freq="1D",                # target: daily
    aggregation={
        "events": "count",    # počet událostí za den
        "sentiment": "mean",  # průměrný sentiment
        "prices": "last",     # zavírací cena
    },
    fill_strategy="ffill",    # forward fill for gaps
)
aligned_df = aligner.align({
    "events": gdelt_events,      # nepravidelné, vícekrát denně
    "sentiment": news_sentiment,  # nepravidelné
    "prices": market_prices       # minutové
})

# Text → features (TF-IDF default, bez PyTorch)
text_enc = TextEncoder(method="tfidf", max_features=500)
text_features = text_enc.fit_transform(documents)

# Text → features (sentence-transformers, requires [text] extra)
text_enc_deep = TextEncoder(method="sentence-transformers", model="all-MiniLM-L6-v2")

# Events → features
event_enc = EventEncoder(cameo_categories=["14", "18", "19"], aggregation="daily")
event_features = event_enc.fit_transform(gdelt_events)

# Numeric
numeric_enc = NumericEncoder(lag_features=[1, 7, 30], rolling_windows=[7, 30])

# Combined
mixed = MixedEncoder(encoders={
    "text": text_enc,
    "events": event_enc,
    "numeric": numeric_enc
})
X = mixed.fit_transform(aligned_df)
```

### 4.2 Correlation Discovery

```python
from orakulum.correlation import TigramiteDiscovery, CausalLearnDiscovery, GrangerCausality

# Primary: Tigramite PCMCI+ (ParCorr — lineární, v0.1 default)
discovery = TigramiteDiscovery(
    method="pcmci+",
    ci_test="parcorr",         # v0.1 default (bez numba)
    # ci_test="cmiknn_mixed",  # v0.2 (vyžaduje [nonlinear] extra)
    max_lag=7,
    significance=0.05
)
causal_graph = discovery.fit(X)

# Fallback: causal-learn (pokud Tigramite selže)
discovery_alt = CausalLearnDiscovery(
    method="pc",               # PC algorithm
    significance=0.05
)
causal_graph = discovery_alt.fit(X)

# Inspect results (společný CausalGraph interface)
causal_graph.summary()                         # textový přehled
causal_graph.to_networkx()                     # NetworkX DiGraph
causal_graph.plot()                            # matplotlib
causal_graph.get_parents("target_var")         # přímé příčiny
causal_graph.get_strength("var_a", "var_b")    # síla vazby

# Granger causality (klasický, vždy funguje)
granger = GrangerCausality(max_lag=5, method="sparse_lasso")
results = granger.fit(X, target="market_return")
results.significant_causes()  # [(var, lag, p_value), ...]
```

### 4.3 Anomaly Detection

```python
from orakulum.anomaly import StumpyDetector, ChangepointDetector

# Matrix profile — motif/discord discovery
detector = StumpyDetector(window_size=24)
anomalies = detector.fit_detect(timeseries)
# Returns: DataFrame(timestamp, score, is_anomaly, type[discord|motif])

# Changepoint detection (cascade onset pro Záchvěv)
cp = ChangepointDetector(method="pelt", penalty="bic")
changepoints = cp.fit_detect(cascade_signal)
# Returns: list of ChangePoint(timestamp, direction, magnitude, confidence)
```

### 4.4 Prediction (v0.2)

```python
from orakulum.prediction import TSPredictor, FoundationPredictor, ModelRouter

# Darts/sktime wrapper (requires [prediction] extra)
predictor = TSPredictor(model="nhits", horizon=14)
predictor.fit(train_series, covariates=X)
forecast = predictor.predict(horizon=14)

# Zero-shot: Chronos-2 (requires [foundation] extra)
foundation = FoundationPredictor(model="chronos-2-base")
forecast = foundation.predict(series, horizon=30)  # no fit needed

# Auto-routing: local/global/foundation
router = ModelRouter(
    local=["arima", "ets"],
    global_=["nhits", "tide"],
    foundation=["chronos-2"],
    selection="auto"
)
router.fit(train_data)
forecast = router.predict(horizon=14)
forecast.confidence_intervals()
```

### 4.5 Pipeline

```python
from orakulum import Pipeline

pipeline = Pipeline([
    ("align", TemporalAligner(freq="1D")),
    ("encode_events", EventEncoder(aggregation="daily")),
    ("encode_news", TextEncoder(method="tfidf", max_features=500)),
    ("combine", MixedEncoder()),
    ("discover", TigramiteDiscovery(method="pcmci+", max_lag=7)),
    ("detect", StumpyDetector(window_size=24)),
])

pipeline.fit(historical_data)
result = pipeline.run(new_data)

# PipelineResult — bohatý výstup se side-outputy
result.anomalies        # DataFrame s detekovanými anomáliemi
result.causal_graph     # CausalGraph objekt
result.features         # transformovaná feature matice
result.metadata         # timing, params, versions
```

### 4.6 Serve (FastAPI)

```python
# Automatický start
# $ orakulum serve --port 8420

# MONITOR (Node.js) volá:
# POST /api/v1/anomaly
# { "source": "gdelt", "region": "Middle East", "window": 24 }
# → { "anomalies": [...], "metadata": {...} }

# POST /api/v1/correlation
# { "data": [...], "method": "pcmci+", "max_lag": 7 }
# → { "graph": {...}, "significant_links": [...] }

# GET /api/v1/sources/gdelt/data?region=Middle+East&days=30
# → { "events": [...], "count": 1234 }

# GET /health
# → { "status": "ok", "version": "0.1.0", "modules": [...] }
```

---

## 5. Dependencies

### Core (always installed, <100MB, žádný PyTorch)

```toml
[project]
name = "orakulum"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "numpy>=1.24",
    "pandas>=2.0",
    "scikit-learn>=1.3",
    "stumpy>=1.12",              # matrix profile — anomaly
    "ruptures>=1.1",             # changepoint detection
    "tigramite>=5.2",            # PCMCI+ (ParCorr — linear CI test)
    "joblib>=1.3",               # chybí v tigramite deps (ověřeno na Windows)
    "networkx>=3.0",             # causal graph
    "httpx>=0.27",               # async HTTP pro sources (sdílený s POLYBOT)
    "fastapi>=0.115",            # API server
    "uvicorn>=0.30",             # ASGI server
    "typer>=0.12",               # CLI
    "pydantic-settings>=2.0",    # config
]
```

### Extras (opt-in per project need)

```toml
[project.optional-dependencies]
nonlinear = [
    "numba>=0.59",               # pro Tigramite CMIknn/CMIknnMixed
]
causal-fallback = [
    "causal-learn>=0.1.3.8",    # PC/FCI/GES fallback pokud Tigramite selže
]
text = [
    "sentence-transformers>=2.0", # deep text embeddings (PyTorch!)
]
prediction = [
    "darts>=0.29",               # unified forecasting (PyTorch Lightning)
]
foundation = [
    "chronos-forecasting",       # Amazon Chronos-2 (PyTorch + transformers)
]
feast = [
    "feast[redis]>=0.38",       # production feature store
]
viz = [
    "matplotlib>=3.7",
    "plotly>=5.0",
]
all = ["orakulum[nonlinear,causal-fallback,text,prediction,foundation,feast,viz]"]
dev = ["pytest>=8.0", "pytest-cov", "mypy", "ruff"]
```

### Install příklady

```bash
# MONITOR — anomaly + correlation (lightest)
pip install orakulum[viz]

# POLYBOT — correlation + future prediction
pip install orakulum[prediction,viz]

# Záchvěv — correlation + changepoint + prediction
pip install orakulum[prediction,viz]

# Full (development/research)
pip install orakulum[all,dev]

# Pokud Tigramite CMIknn potřebný (nonlinear mixed data)
pip install orakulum[nonlinear]

# Pokud Tigramite nefunguje
pip install orakulum[causal-fallback]
```

---

## 6. Roadmap

### v0.1 — Core (4-6 session dní)

| Komponenta | Scope | Priorita |
|-----------|-------|----------|
| **sources.gdelt** | GDELT event loader (CAMEO, date range, region filter) | P0 |
| **sources.news** | Generic news fetcher (RSS/API) | P1 |
| **sources.polymarket** | Read-only: markets, orderbook, prices, events | P1 |
| **encoding.temporal** | TemporalAligner — align heterogeneous sources to common freq | P0 |
| **encoding.numeric** | Scaling, lag features, rolling stats | P0 |
| **encoding.text** | TF-IDF (default, bez PyTorch) | P0 |
| **encoding.events** | GDELT CAMEO → daily feature matrix | P0 |
| **encoding.mixed** | MixedEncoder orchestrace | P0 |
| **correlation.tigramite** | PCMCI+ wrapper (ParCorr — linear) | P0 |
| **correlation.causal_learn** | PC/FCI fallback | P1 |
| **correlation.granger** | Klasický Granger + sparse LASSO | P1 |
| **correlation.graph** | CausalGraph output + NetworkX + viz | P0 |
| **anomaly.matrix_profile** | STUMPY wrapper, discord detection | P0 |
| **anomaly.changepoint** | ruptures PELT wrapper | P0 |
| **serve.app** | FastAPI factory + health route | P0 |
| **serve.routes.anomaly** | POST /api/v1/anomaly | P0 |
| **serve.routes.correlation** | POST /api/v1/correlation | P0 |
| **serve.routes.sources** | GET /api/v1/sources/{source}/data | P1 |
| **cli** | `orakulum serve` + `orakulum detect` | P0 |
| **utils.metrics** | AUC, F1, MAPE, Sharpe | P0 |
| **utils.config** | Pydantic settings, env vars | P0 |
| Tests | Unit tests pro každý modul | P0 |
| **examples/quickstart.py** | Minimal E2E demo | P0 |

**Ověření v0.1:** GDELT data (Middle East) → TemporalAligner → PCMCI+ causal graph → STUMPY anomaly detection. Výstup: causal graph PNG + anomaly list JSON. FastAPI server odpovídá na /api/v1/anomaly z curl.

### v0.2 — Prediction + Pipeline (3-4 session dny)

| Komponenta | Scope | Priorita |
|-----------|-------|----------|
| **prediction.timeseries** | Darts/sktime wrapper (NHITS, TiDE) | P0 |
| **prediction.foundation** | Chronos-2 zero-shot adapter | P0 |
| **prediction.router** | Auto-selection local/global/foundation | P1 |
| **pipeline** | Pipeline class + PipelineResult | P0 |
| **encoding.text** upgrade | sentence-transformers opt-in | P1 |
| **correlation.tigramite** upgrade | CMIknn s numba (nonlinear) | P1 |
| **anomaly.autoencoder** | AEDetector pro OSINT unrest detection | P1 |
| **store.local** | SQLite/parquet feature cache | P1 |
| **serve.routes.predict** | POST /api/v1/predict | P0 |
| **cli** rozšíření | `orakulum correlate`, `orakulum predict` | P1 |
| **examples/monitor_gdelt.py** | Full MONITOR pipeline demo | P0 |
| **examples/zachvev_cascade.py** | Záchvěv cascade detection demo | P0 |

**Ověření v0.2:** MONITOR pipeline end-to-end na GDELT. Záchvěv cascade onset detection na Letná validation datasetu. Prediction benchmark na GIFT-Eval subset.

### v0.3 — Binary Prediction + Polish (2-3 session dny)

| Komponenta | Scope | Priorita |
|-----------|-------|----------|
| **prediction.binary** | LLM ensemble pro binary event prediction | P0 |
| **store.feast** | Feast integration (production) | P2 |
| **examples/polybot_edge.py** | POLYBOT market scanning + correlation demo | P0 |
| Docker setup | Dockerfile + docker-compose | P1 |

**Ověření v0.3:** Binary predictor backtested na Autocast benchmark subset. POLYBOT demo: news events → market correlation → edge identification.

### v1.0 — Production Ready

- CI/CD (GitHub Actions)
- PyPI publish
- STOPA skill wrapper (`/predict`)
- MONITOR, POLYBOT, Záchvěv integration PRs
- Benchmarking suite (GIFT-Eval subset + Autocast + Letná data)
- Documentation (Sphinx/MkDocs)

---

## 7. Integrace s cílovými projekty

### MONITOR (Node.js → FastAPI HTTP)

```javascript
// MONITOR server volá ORAKULUM FastAPI
const resp = await fetch('http://localhost:8420/api/v1/anomaly', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    source: 'gdelt',
    region: 'Middle East',
    window: 24,
    method: 'stumpy'
  })
});
const { anomalies, metadata } = await resp.json();

// Correlation discovery
const corrResp = await fetch('http://localhost:8420/api/v1/correlation', {
  method: 'POST',
  body: JSON.stringify({
    source: 'gdelt',
    region: 'Middle East',
    method: 'pcmci+',
    max_lag: 7,
    days: 90
  })
});
const { graph, significant_links } = await corrResp.json();
```

### POLYBOT (Python přímý import)

```python
# POLYBOT importuje ORAKULUM pro analytiku
from orakulum.sources import PolymarketLoader
from orakulum.encoding import TextEncoder, NumericEncoder, TemporalAligner
from orakulum.correlation import TigramiteDiscovery
from orakulum.prediction import BinaryPredictor  # v0.3

# Data z ORAKULUM adapteru (read-only)
loader = PolymarketLoader()
markets = loader.get_active_markets(category="politics")
prices = loader.get_price_history(condition_id="0x...", days=90)

# Correlation: news events → market price movements
aligner = TemporalAligner(freq="1D")
aligned = aligner.align({"news": news_features, "prices": prices})
discovery = TigramiteDiscovery(method="pcmci+", max_lag=7)
graph = discovery.fit(aligned)

# Execution zůstává v POLYBOT (paper trading engine, MCP tools, risk management)
```

### Záchvěv (Python přímý import)

```python
from orakulum.encoding import TextEncoder, TemporalAligner
from orakulum.correlation import TigramiteDiscovery
from orakulum.anomaly import ChangepointDetector, StumpyDetector

# Cascade onset detection
aligner = TemporalAligner(freq="6H")  # 6-hour windows
aligned = aligner.align({
    "reddit_volume": volume_series,
    "sentiment": sentiment_series,
    "entity_mentions": entity_counts
})

# Najdi kauzální strukturu: co šíří co
discovery = TigramiteDiscovery(method="pcmci+", max_lag=4)  # 4×6h = 1 den
graph = discovery.fit(aligned)

# Detekuj onset kaskády
cp = ChangepointDetector(method="pelt", penalty="bic")
onsets = cp.fit_detect(aligned["reddit_volume"])
```

---

## 8. Base Interfaces (ABC contracts)

```python
# sources/base.py
class BaseSource(ABC):
    @abstractmethod
    def fetch(self, **kwargs) -> pd.DataFrame: ...

# encoding/base.py
class BaseEncoder(ABC):
    @abstractmethod
    def fit(self, X: pd.DataFrame) -> "BaseEncoder": ...
    @abstractmethod
    def transform(self, X: pd.DataFrame) -> pd.DataFrame: ...
    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        return self.fit(X).transform(X)

# correlation/base.py
class BaseCorrelation(ABC):
    @abstractmethod
    def fit(self, X: pd.DataFrame) -> "BaseCorrelation": ...
    @abstractmethod
    def get_graph(self) -> "CausalGraph": ...

# prediction/base.py
class BasePredictor(ABC):
    @abstractmethod
    def fit(self, y, X=None) -> "BasePredictor": ...
    @abstractmethod
    def predict(self, horizon: int, X=None) -> pd.DataFrame: ...

# anomaly/base.py
class BaseDetector(ABC):
    @abstractmethod
    def fit(self, X: pd.DataFrame) -> "BaseDetector": ...
    @abstractmethod
    def detect(self, X: pd.DataFrame) -> pd.DataFrame: ...
    def fit_detect(self, X: pd.DataFrame) -> pd.DataFrame:
        return self.fit(X).detect(X)

# pipeline.py
@dataclass
class PipelineResult:
    features: pd.DataFrame | None = None
    causal_graph: CausalGraph | None = None
    anomalies: pd.DataFrame | None = None
    forecast: pd.DataFrame | None = None
    metadata: dict = field(default_factory=dict)
```

---

## 9. CLI Interface

### v0.1

```bash
# Start FastAPI server (MONITOR integrace)
orakulum serve --port 8420 --reload

# Quick anomaly scan
orakulum detect --source gdelt --region "Middle East" --window 24 --output json
```

### v0.2+

```bash
# Correlation discovery
orakulum correlate --input data.parquet --method pcmci+ --max-lag 7

# Forecast
orakulum predict --input series.csv --model chronos-2 --horizon 30

# Market data
orakulum sources polymarket --category politics --active
```

---

## 10. Metriky úspěchu

| Modul | Metrika | Target v0.1 | Target v1.0 |
|-------|---------|-------------|-------------|
| anomaly | GDELT anomaly detection AUC | >0.80 | >0.86 (Macis 2024 benchmark) |
| anomaly | Záchvěv cascade onset F1 | — | >0.75 |
| correlation | F1 na syntetických causal links | >0.70 | >0.85 |
| prediction | TS forecast MAPE (GIFT-Eval subset) | — | <15% |
| serve | API response latency (anomaly) | <5s | <1s |
| general | Unit test coverage | >80% | >90% |
| general | Core import time (bez extras) | <2s | <1s |

**Poznámka:** Brier score pro binary prediction je metrika POLYBOTu, ne ORAKULUM.

---

## 11. Rizika a mitigace

| Riziko | Pst. | Dopad | Mitigace |
|--------|------|-------|----------|
| Tigramite CMIknn selže na Windows (numba) | Nízká | Střední | ParCorr funguje (ověřeno). CMIknn jako opt-in [nonlinear] extra. causal-learn jako fallback |
| Chronos-2 příliš velký (PyTorch) | Nízká | Nízký | Base model 120M OK. Je v [foundation] extra, ne core. TimeGPT API fallback |
| GDELT data quality / gaps | Vysoká | Střední | WORLDREP jako alt. zdroj. Validation v encoding pipeline. TemporalAligner handle gaps |
| FastAPI přidává complexity | Nízká | Nízký | Standardní framework, minimální custom middleware |
| Záchvěv data format nekompatibilní | Nízká | Nízký | Shared BaseEncoder interface + TemporalAligner |
| Feast overkill pro dev | Střední | Nízký | LocalStore (SQLite) jako default. Feast je [feast] extra |

---

## 12. Rozhodnutí z review (2026-03-28)

| # | Bod | Rozhodnutí | Dopad na spec |
|---|-----|-----------|---------------|
| 1 | Polybot status | Existující Python MCP server (FastMCP, httpx, torch) | Přímý import, markets modul zachován |
| 2 | Tigramite Windows | Funguje (ParCorr OK, CMIknn potřebuje numba) | Dual backend: Tigramite primary + causal-learn fallback |
| 3 | MONITOR integrace | FastAPI od začátku | Nový `serve/` modul jako P0 v roadmapě |
| 4 | Pipeline class | Hybrid: sklearn kroky + vlastní PipelineResult | `pipeline.py` s bohatým výstupem (graf, anomálie, metadata) |
| 5 | Heavy deps | Lehký core (<100MB), PyTorch jako extras | TF-IDF default, Chronos/Darts/sentence-transformers opt-in |
| 6 | Temporal alignment | TemporalAligner jako P0 | Nový `encoding/temporal.py` — kritické pro korektnost |
| 7 | Metriky | Per-modul (AUC, F1, MAPE), Brier → POLYBOT | Tabulka metrik přepracována |
| 8 | CLI scope | v0.1: `serve` + `detect`, zbytek v0.2 | CLI minimální, rozšiřuje se postupně |
| 9 | Data loaders | Hybrid: sdílené (GDELT, news, Polymarket) v ORAKULUM | Nový `sources/` modul |
| 10 | Markets boundary | Data adapter v ORAKULUM, execution v POLYBOTu | `sources/polymarket.py` = read-only, bez execution |
