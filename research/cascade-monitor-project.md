# CascadeWatch — Detekce a predikce názorových lavin

Projektový dokument pro systém monitoringu, predikce a intervence na sociálních sítích.

**Verze:** 0.1 (2026-03-20)
**Stav:** Koncepční návrh

---

## 1. Cíl projektu

Vybudovat systém, který:

1. **Monitoruje** tok názorů na vybraných platformách v reálném čase
2. **Detekuje** prekritický stav — signály blížícího se tipping pointu
3. **Predikuje** pravděpodobnost, směr a sílu nadcházející kaskády
4. **Modeluje intervence** — jaký zásah v jakém čase má šanci kaskádu spustit/zastavit

Není to predikce budoucnosti (à la MiroFish). Je to **seismograf pro sociální dynamiku** — neříká, co se stane, ale kde se hromadí napětí.

---

## 2. Teoretický základ

### 2.1 Critical Slowing Down (CSD)

Systém blízko bifurkačního bodu se pomaleji zotavuje z perturbací. Měřitelné signály:

| Signál | Matematická definice | Chování před tipping pointem |
|--------|---------------------|------------------------------|
| **Autokorelace (lag-1 AC)** | `AC(1) = corr(x_t, x_{t-1})` | Roste → 1.0 |
| **Variance** | `σ² = E[(x - μ)²]` | Roste |
| **Skewness** | `γ = E[(x - μ)³] / σ³` | Mění znaménko (systém se naklání) |
| **Flickering** | Bimodální distribuce v okně | Přeskakování mezi dvěma stavy |
| **Spektrální reddening** | Posun power spectrum k nižším frekvencím | Dominují pomalé oscilace |

**Klíčový paper:** Scheffer et al. "Critical Transitions in Nature and Society" — univerzalita CSD signálů.

**Hotové nástroje:**
- `ewstools` (Python) — Bury, 2023, JOSS — variance, AC, spektrální EWS + deep learning (EWSNet)
- `EWSmethods` (R) — O'Brien, 2023, Ecography — univariate + multivariate EWS
- `pycascades` (Python, PIK Potsdam) — kaskádová dynamika na sítích

**Kritická mezera:** Tyto nástroje byly vyvinuty pro ekologická/klimatická data. Aplikace na sociální média je popsaná teoreticky, ale **žádný produkční systém neexistuje**. To je příležitost.

### 2.2 Prahové modely (Watts, Granovetter, Centola)

Každý uzel v síti má **práh** — podíl sousedů, kteří musí adoptovat názor, aby ho adoptoval i on.

```
Granovetter (1978): Individuální prahy → kolektivní dynamika
Watts (2002):       Síťová topologie určuje, zda lokální seed → globální kaskáda
Centola (2018):     Empiricky ověřeno — ~25% committed minority → norma se překlopí
```

**Pareto efekt (ESD, 2025):** Malá menšina vlivných uzlů může řídit majority transition — potvrzuje asymetrickou sílu intervencí.

**Implementace:**
- `benmaier/thresholdmodel` — Watts model na NetworkX grafech
- `CyNetDiff` — Cython, výkonný, Independent Cascade + Linear Threshold
- `pycascades` — tipping kaskády na komplexních sítích

### 2.3 Informační kaskády — detekce a predikce

State-of-the-art používá grafové neuronové sítě:

| Model | Přístup | Kód |
|-------|---------|-----|
| **CasCN** | Recurrent convolution na kaskádových grafech | github.com/ChenNed/CasCN |
| **CasCIFF** | Cross-domain information fusion | github.com/XiaoYuan011/CasCIFF |
| **CasFlow** | Hierarchické struktury + nejistota šíření | TKDE 2021 |
| **TIDE-MARK** | Temporal GNN + Markov, detekce fake news komunit | Nature Sci. Reports 2026 |

Kurátorský seznam: `github.com/ChenNed/Awesome-DL-Information-Cascades-Modeling`

### 2.4 Intervence a inokulace

**Centolův 25% práh:** Committed minority nad ~25% sítě spolehlivě překlopí normu — i proti ekonomickým incentivům udržet status quo.

**Van der Linden inokulace (Cambridge SDML):**
- Prebunking > debunking — předem exposovat oslabené manipulativní techniky
- Hry: Bad News, Go Viral!, Bad Vaxx — miliony hráčů, validováno v 5 jazycích
- 6 inokulačních videí validováno (Political Psychology, 2025)

**Timing intervence:**
- Rané fáze: cílení neutrálních jedinců propojených s adoptery (Applied Network Science, 2025)
- Rozjetá kaskáda: přesměrování energie, ne blokace (Streisand efekt)

---

## 3. Architektura systému

```
┌─────────────────────────────────────────────────────────────────┐
│                        CascadeWatch                              │
├─────────┬──────────┬──────────────┬──────────────┬──────────────┤
│  INGEST │ PROCESS  │   DETECT     │   PREDICT    │  INTERVENE   │
│         │          │              │              │              │
│ Sběr dat│ NLP +    │ EWS signály  │ Kaskádový    │ Agent-based  │
│ z platf.│ síťová   │ na časových  │ model +      │ simulace     │
│         │ analýza  │ řadách       │ threshold    │ intervencí   │
│         │          │              │ analýza      │              │
├─────────┴──────────┴──────────────┴──────────────┴──────────────┤
│                      STORAGE + STATE                             │
│  TimescaleDB/SQLite │ NetworkX grafy │ EWS history │ Alert log   │
├─────────────────────────────────────────────────────────────────┤
│                      DASHBOARD                                   │
│  Streamlit / Grafana — teploměry, alerty, síťové vizualizace    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.1 INGEST — Sběr dat

#### Datové zdroje (prioritizované pro český kontext)

| Zdroj | Typ dat | Sběr | Volume | Obtížnost |
|-------|---------|------|--------|-----------|
| **Twitter/X** | Tweety, retweety, reply grafy | API v2 (Basic $100/m) nebo Apify scraper | střední | nízká |
| **Reddit** | Posty + komentáře, upvotes | API (zdarma, rate-limited) nebo r/czech, r/europe | střední | nízká |
| **Facebook skupiny** | Příspěvky + komentáře | CrowdTangle (akademický) nebo Apify | vysoký | střední |
| **iDNES.cz komentáře** | Komentáře pod články | Web scraping (BeautifulSoup/Playwright) | střední | střední |
| **Novinky.cz komentáře** | Komentáře pod články | Web scraping | střední | střední |
| **Aktuálně.cz** | Komentáře pod články | Web scraping | nízký | střední |
| **Nyx.cz** | Diskuzní fórum, specifická komunita | API nebo scraping | nízký | nízká |
| **Telegram skupiny** | Zprávy v kanálech | Telethon (Python) | nízký–vysoký | střední |
| **YouTube komentáře** | Komentáře pod CZ videy | YouTube Data API v3 (zdarma) | střední | nízká |

#### Datový model (jeden záznam)

```python
@dataclass
class SocialPost:
    id: str                     # Unikátní ID záznamu
    platform: str               # twitter|reddit|idnes|novinky|...
    author_id: str              # Anonymizovaný hash autora
    timestamp: datetime         # Čas publikace (UTC)
    text: str                   # Plný text
    parent_id: str | None       # Reply/comment parent (pro graf)
    engagement: dict            # {"likes": N, "shares": N, "replies": N}
    url: str                    # Původní URL
    topic_tags: list[str]       # Přiřazená témata (po zpracování)

    # Přidáno v PROCESS fázi:
    sentiment: float            # -1.0 až +1.0
    embedding: list[float]      # 384-dim sentence embedding
    language: str               # cs/en/...
    entities: list[str]         # Extrahované entity (NER)
    narrative_cluster: int      # Přiřazený narativní klastr
```

#### Ingest pipeline

```
Cron (5-15 min interval)
│
├─ twitter_collector.py    → Twitter/X API / Apify
├─ reddit_collector.py     → Reddit API (PRAW)
├─ news_comments_collector.py → Playwright scraper pro iDNES/Novinky/Aktuálně
├─ telegram_collector.py   → Telethon
│
├─ Deduplikace (hash textu)
├─ Language detection (langdetect → filtr na "cs" + "en")
│
└─ → raw_posts tabulka v DB
```

**Rate limiting & etika:**
- Respektovat robots.txt a API rate limits
- Nescrapovat PII — autor_id je vždy hash, ne jméno
- Data jen pro analýzu agregátů, ne profilování jednotlivců
- GDPR compliance: žádné ukládání osobních údajů, jen agregované metriky

### 3.2 PROCESS — Zpracování textu a sítě

#### 3.2.1 Sentiment analýza

**Primární model pro češtinu:**

| Model | Zdroj | Přesnost | Velikost | Latence |
|-------|-------|----------|----------|---------|
| `fav-kky/FERNET-C5` | HuggingFace / Masaryk Uni | ~80% F1 na Czech sentiment | ~500 MB | ~50 ms/text |
| `ufal/robeczech-base` | ÚFAL, Karlova Univerzita | základ pro fine-tuning | ~500 MB | ~40 ms/text |
| `seznam/small-e-czech` | Seznam.cz | dobrý embeddings | ~130 MB | ~15 ms/text |

**Fallback pro angličtinu:** `cardiffnlp/twitter-roberta-base-sentiment-latest`

**Pipeline:**
```python
def process_sentiment(post: SocialPost) -> float:
    if post.language == "cs":
        # FERNET-C5 nebo fine-tuned RobeCzech
        return czech_sentiment_model.predict(post.text)
    else:
        # Cardiff Twitter RoBERTa
        return en_sentiment_model.predict(post.text)
```

#### 3.2.2 Sentence Embeddings (pro narativní clustering)

| Model | Jazyk | Dimenze | Poznámka |
|-------|-------|---------|----------|
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 50+ jazyků vč. CZ | 384 | Nejlepší poměr kvalita/rychlost |
| `seznam/small-e-czech` | CZ | 768 | Czech-specific, ale větší |

Embeddings slouží k:
1. Narativnímu clusteringu (HDBSCAN na embeddingech)
2. Detekci narativní konvergence (cosine similarity mezi klastry v čase)
3. Detekci nových narativů (outlier detection)

#### 3.2.3 Narativní clustering

```python
from hdbscan import HDBSCAN
from sklearn.metrics.pairwise import cosine_similarity

def cluster_narratives(embeddings: np.ndarray, min_cluster_size: int = 10):
    """
    HDBSCAN na sentence embeddingech.
    Výhody oproti K-means:
    - Nemusíme znát počet klastrů
    - Detekuje outliery (nové narativy)
    - Zvládá klastry různých velikostí
    """
    clusterer = HDBSCAN(
        min_cluster_size=min_cluster_size,
        metric='euclidean',
        cluster_selection_method='eom'  # Excess of Mass — robustní
    )
    labels = clusterer.fit_predict(embeddings)
    return labels, clusterer.probabilities_
```

**Sledované metriky per klastr:**
- Velikost klastru v čase (roste/klesá)
- Vnitřní koherence (průměrná cosine similarity)
- Sentiment distribuce uvnitř klastru
- Jazykový profil — dominantní fráze (TF-IDF)

#### 3.2.4 Síťová analýza

```python
import networkx as nx

def build_interaction_graph(posts: list[SocialPost]) -> nx.DiGraph:
    """
    Orientovaný graf: A → B pokud A odpověděl na B, retweetoval B, apod.
    Váha hrany = počet interakcí.
    """
    G = nx.DiGraph()
    for post in posts:
        if post.parent_id:
            parent = get_post(post.parent_id)
            G.add_edge(post.author_id, parent.author_id,
                       weight=G.get_edge_data(post.author_id, parent.author_id,
                                              default={"weight": 0})["weight"] + 1)
    return G
```

**Metriky sítě:**

| Metrika | Co měří | Signál |
|---------|---------|--------|
| **Modularita** (Louvain) | Míra oddělení komunit | Roste → polarizace |
| **Bridging nodes** | Uzly propojující oddělené klastry | Kaskáda často začíná zde |
| **Average path length** | Průměrná vzdálenost uzlů | Klesá → síť se zhuštuje |
| **Clustering coefficient** | Míra lokálního propojení | Roste uvnitř echo chamber |
| **Degree centrality entropy** | Rovnoměrnost vlivu | Klesá → dominance hub uzlů |

### 3.3 DETECT — Early Warning Signals

Jádro systému. Aplikace CSD teorie na časové řady ze sociálních dat.

#### 3.3.1 Konstruování časových řad

Z raw dat generujeme **denní/hodinové** časové řady per téma:

```python
def build_topic_timeseries(posts: list[SocialPost],
                           topic: str,
                           window: str = "1H") -> pd.DataFrame:
    """
    Pro dané téma vytvoří časové řady:
    - volume: počet postů za okno
    - sentiment_mean: průměrný sentiment
    - sentiment_std: rozptyl sentimentu
    - engagement_total: suma engagement
    - unique_authors: počet unikátních autorů
    - narrative_entropy: Shannon entropy narativních klastrů
    """
    topic_posts = [p for p in posts if topic in p.topic_tags]
    df = pd.DataFrame([vars(p) for p in topic_posts])
    df.set_index('timestamp', inplace=True)

    return df.resample(window).agg({
        'id': 'count',                          # volume
        'sentiment': ['mean', 'std'],            # sentiment stats
        'engagement': lambda x: sum(e['likes'] + e['shares'] for e in x),
        'author_id': 'nunique',                  # unique voices
        'narrative_cluster': lambda x: entropy(x.value_counts(normalize=True))
    })
```

#### 3.3.2 EWS výpočet

Používáme `ewstools` s vlastní konfigurací:

```python
import ewstools

def compute_ews(timeseries: pd.Series,
                rolling_window: float = 0.5) -> dict:
    """
    Compute Early Warning Signals na sentiment/volume časové řadě.

    rolling_window: podíl dat v rolling window (0.5 = polovina řady)

    Vrací dict s trendy EWS indikátorů.
    """
    ts = ewstools.TimeSeries(timeseries, transition=None)

    # Detrending — Gaussovský filtr (odstraní pomalé trendy)
    ts.detrend(method='Gaussian', bandwidth=0.2)

    # Klasické EWS
    ts.compute_var(rolling_window=rolling_window)     # Variance
    ts.compute_auto(rolling_window=rolling_window,    # Lag-1 AC
                    lag=1)
    ts.compute_auto(rolling_window=rolling_window,    # Lag-2 AC
                    lag=2)

    # Spektrální EWS
    ts.compute_spec(rolling_window=rolling_window,
                    pspec_roll_offset=20)

    # Deep learning EWS (EWSNet — trained on simulated bifurcations)
    ts.apply_classifier_ensemble(
        classifier='EWSNet',
        ensemble_size=25  # 25 modelů v ansambl → robustnější
    )

    return {
        'variance_trend': kendall_tau(ts.state['variance']),
        'ac1_trend': kendall_tau(ts.state['ac1']),
        'ac2_trend': kendall_tau(ts.state['ac2']),
        'spectral_ratio': ts.spec['smax_ratio'].iloc[-1],
        'ewsnet_probability': ts.dl_preds['EWSNet'].mean(),
        'raw': ts
    }
```

#### 3.3.3 Kompozitní Cascade Risk Index (CRI)

Klíčová inovace — **kombinace všech signálů do jednoho indexu**:

```python
def cascade_risk_index(ews: dict,
                       network: dict,
                       narrative: dict) -> float:
    """
    Kompozitní index rizika kaskády (0.0 - 1.0).

    Tři pilíře:
    1. Temporální (EWS na časových řadách)         — váha 0.4
    2. Strukturální (síťová topologie)              — váha 0.3
    3. Narativní (jazyková konvergence/divergence)  — váha 0.3
    """

    # --- TEMPORÁLNÍ PILÍŘ (0.4) ---
    temporal = weighted_mean([
        (normalize(ews['variance_trend']),     0.25),  # Rostoucí variance
        (normalize(ews['ac1_trend']),           0.25),  # Rostoucí autokorelace
        (ews['ewsnet_probability'],             0.30),  # DL predikce bifurkace
        (normalize(ews['spectral_ratio']),      0.20),  # Spektrální reddening
    ])

    # --- STRUKTURÁLNÍ PILÍŘ (0.3) ---
    structural = weighted_mean([
        (normalize(network['modularity_delta']),     0.30),  # Změna modularity
        (normalize(network['echo_chamber_density']), 0.25),  # Zhuštění echo chambers
        (normalize(network['bridge_stress']),         0.25),  # Zátěž mostových uzlů
        (1 - normalize(network['cross_cluster_comm']),0.20),  # Pokles meziklastrové komunikace
    ])

    # --- NARATIVNÍ PILÍŘ (0.3) ---
    narrative_score = weighted_mean([
        (normalize(narrative['convergence_rate']),    0.30),  # Jak rychle konvergují fráze
        (normalize(narrative['absolutism_index']),    0.25),  # Nárůst absolutních výrazů
        (normalize(narrative['urgency_shift']),       0.25),  # Posun k urgentnímu jazyku
        (normalize(narrative['new_frame_velocity']),  0.20),  # Rychlost šíření nového framu
    ])

    cri = 0.4 * temporal + 0.3 * structural + 0.3 * narrative_score

    return clip(cri, 0.0, 1.0)
```

#### 3.3.4 Alertní pásma

| CRI rozsah | Stav | Akce |
|------------|------|------|
| 0.0 – 0.3 | **Klid** (zelená) | Standardní monitoring |
| 0.3 – 0.5 | **Zvýšená pozornost** (žlutá) | Zvýšit frekvenci sběru, detailnější analýza |
| 0.5 – 0.7 | **Prekritický stav** (oranžová) | Alert, spustit predikční modely |
| 0.7 – 1.0 | **Kritický stav** (červená) | Plný alert, spustit intervenční simulace |

#### 3.3.5 Narativní signály — detailní detekce

```python
def detect_narrative_signals(posts: list[SocialPost],
                              window_days: int = 7) -> dict:
    """
    Jazykové markery blížící se kaskády.
    """
    texts = [p.text for p in posts]

    # 1. Absolutismus index
    # Slovník absolutních výrazů (CZ)
    absolutes_cs = {
        "vždy", "nikdy", "všichni", "nikdo", "musíme", "nesmíme",
        "jednoznačně", "rozhodně", "absolutně", "totálně", "každý",
        "žádný", "kompletně", "naprosto", "bezpodmínečně", "dost"
    }
    absolutism_ratio = count_matches(texts, absolutes_cs) / len(texts)

    # 2. Urgence index
    urgency_cs = {
        "teď", "ihned", "okamžitě", "hned", "právě teď", "musí se",
        "je nejvyšší čas", "nemůžeme čekat", "už je pozdě", "konečně",
        "probuďte se", "vzpamatujte se", "dokdy budeme"
    }
    urgency_ratio = count_matches(texts, urgency_cs) / len(texts)

    # 3. Dehumanizace index
    dehumanization_markers = {
        "ti lidé", "tihle", "oni", "takoví", "banda", "pakáž",
        "havěť", "sebrance", "lůza", "stádo", "ovce"
    }
    dehumanization_ratio = count_matches(texts, dehumanization_markers) / len(texts)

    # 4. Narativní konvergence — jak rychle roste dominantní frame
    embeddings = embed(texts)
    clusters = HDBSCAN(min_cluster_size=5).fit_predict(embeddings)
    largest_cluster_ratio = max(Counter(clusters).values()) / len(texts)
    convergence_rate = (largest_cluster_ratio - baseline_largest) / window_days

    # 5. Frame velocity — jak rychle se šíří nová fráze
    # TF-IDF tento týden vs minulý → top nové fráze → měření adoption rate
    new_frames = tfidf_diff(this_week_texts, last_week_texts, top_n=10)
    frame_velocity = mean([adoption_rate(frame, posts) for frame in new_frames])

    return {
        'absolutism_index': absolutism_ratio,
        'urgency_shift': urgency_ratio,
        'dehumanization_index': dehumanization_ratio,
        'convergence_rate': convergence_rate,
        'new_frame_velocity': frame_velocity,
        'dominant_frames': new_frames
    }
```

### 3.4 PREDICT — Predikční modely

#### 3.4.1 Threshold-based predikce (Watts model)

```python
from thresholdmodel import ThresholdModel

def predict_cascade_reach(network: nx.DiGraph,
                          seed_nodes: list[str],
                          threshold_distribution: str = 'uniform',
                          n_simulations: int = 1000) -> dict:
    """
    Monte Carlo simulace Watts threshold modelu.

    Pro každou simulaci:
    1. Přiřaď každému uzlu náhodný práh z distribuce
    2. Aktivuj seed uzly
    3. Iteruj dokud se kaskáda nezastaví
    4. Zaznamenej dosah (% aktivovaných uzlů)

    Výstup: distribuce dosahů → P(globální kaskáda)
    """
    results = []
    for _ in range(n_simulations):
        model = ThresholdModel(
            G=network,
            seed=seed_nodes,
            threshold=np.random.uniform(0.1, 0.5, size=len(network))
        )
        cascade = model.run()
        results.append(len(cascade[-1]) / len(network))

    return {
        'p_global_cascade': sum(1 for r in results if r > 0.5) / n_simulations,
        'median_reach': np.median(results),
        'p95_reach': np.percentile(results, 95),
        'distribution': results
    }
```

#### 3.4.2 EWSNet deep learning predikce

`ewstools` integruje EWSNet — neuronovou síť trénovanou na simulovaných bifurkacích:

```python
def predict_transition_probability(timeseries: pd.Series) -> dict:
    """
    EWSNet klasifikátor — predikuje typ přechodu:
    - No transition
    - Smooth transition
    - Critical transition (tipping point)

    Ansámbl 25 modelů pro robustnost.
    """
    ts = ewstools.TimeSeries(timeseries)
    ts.detrend(method='Gaussian', bandwidth=0.2)

    ts.apply_classifier_ensemble(
        classifier='EWSNet',
        ensemble_size=25
    )

    preds = ts.dl_preds['EWSNet']
    return {
        'p_no_transition': preds['No transition'].mean(),
        'p_smooth': preds['Smooth'].mean(),
        'p_critical': preds['Critical'].mean(),
        'confidence': 1 - preds.std().mean()  # Nízká variance = vysoká jistota
    }
```

#### 3.4.3 Hybridní skóre

```
Final prediction =
    0.35 × CRI (Cascade Risk Index)
  + 0.25 × EWSNet P(critical)
  + 0.20 × Watts P(global_cascade)
  + 0.20 × historical_baseline_adjustment

→ Výstup: pravděpodobnost kaskády v horizontu 24h / 72h / 7d
```

### 3.5 INTERVENE — Simulace intervencí

Aktivuje se jen při CRI > 0.5 (oranžová/červená zóna).

#### 3.5.1 Intervenční strategie (z výzkumu)

| Strategie | Fáze | Mechanismus | Evidence |
|-----------|------|-------------|----------|
| **Inokulace** | Preventivní | Prebunking manipulativních technik | van der Linden, 5+ RCTs |
| **Bridge amplification** | Prekritická | Zesílit hlas mostových uzlů | Applied Network Science 2025 |
| **Counter-framing** | Prekritická | Alternativní rámec, ne popření | Centola |
| **Friction injection** | Na tipping pointu | Zpomalit šíření (extra klik, delay) | Platformové experimenty |
| **Energy redirection** | Rozjetá kaskáda | Přesměrovat na konstruktivní akci | Crisis communication |

#### 3.5.2 Agent-based simulace intervence (Mini-MiroFish)

```python
def simulate_intervention(network: nx.DiGraph,
                          current_state: dict,
                          intervention: str,
                          n_agents: int = 30,
                          n_rounds: int = 5) -> dict:
    """
    Malá agent-based simulace pro testování intervencí.

    30 agentů = 30 archetypů z reálné sítě (ne náhodní).
    Agenti generováni z dat: sentiment, aktivita, síťová pozice.

    intervention: typ zásahu (viz strategie výše)

    Výstup: porovnání kaskádové dynamiky s/bez intervence.
    """
    # 1. Vygeneruj agenty z reálných dat
    agents = create_agent_archetypes(network, current_state, n=n_agents)

    # 2. Baseline simulace (bez intervence)
    baseline = run_simulation(agents, rounds=n_rounds, intervention=None)

    # 3. Simulace s intervencí
    treated = run_simulation(agents, rounds=n_rounds, intervention=intervention)

    return {
        'baseline_cascade_prob': baseline['cascade_probability'],
        'treated_cascade_prob': treated['cascade_probability'],
        'delta': baseline['cascade_probability'] - treated['cascade_probability'],
        'most_effective_timing': treated['optimal_round'],
        'key_agents': treated['most_influenced_archetypes']
    }
```

**LLM agenti vs rule-based:**

| Přístup | Výhody | Nevýhody | Náklady |
|---------|--------|----------|---------|
| **LLM agenti** (Ollama lokální) | Realistické jazykové reakce | Pomalé, stádní bias | $0 (lokální) |
| **Rule-based agenti** | Rychlé, deterministické, opakovatelné | Zjednodušené chování | $0 |
| **Hybrid** | LLM pro klíčové uzly, rules pro zbytek | Komplexnější kód | $0 |

**Doporučení:** Začít s rule-based (Watts threshold model), přidat LLM jen pro "kvalitativní naraci" — tzn. jazykem popsat, co se děje, ne simulovat každého agenta přes LLM.

---

## 4. Technický stack

### 4.1 Minimální stack (Tier 1 — Monitoring)

| Komponenta | Nástroj | Licence | Náklady |
|------------|---------|---------|---------|
| Jazyk | Python 3.11+ | — | $0 |
| DB | SQLite + TimescaleDB (nebo jen SQLite) | Open source | $0 |
| Sentiment CZ | FERNET-C5 / RobeCzech (HuggingFace) | MIT/Apache | $0 |
| Embeddings | paraphrase-multilingual-MiniLM-L12-v2 | Apache 2.0 | $0 |
| EWS | ewstools | MIT | $0 |
| Clustering | HDBSCAN (scikit-learn-contrib) | BSD | $0 |
| Sítě | NetworkX | BSD | $0 |
| Scraping | Playwright + BeautifulSoup | Apache/MIT | $0 |
| Dashboard | Streamlit | Apache 2.0 | $0 |
| Scheduling | cron / APScheduler | — | $0 |

**Celkové náklady Tier 1: $0** (vše lokální na existujícím stroji)

### 4.2 Rozšířený stack (Tier 2 — Predikce)

Přidává k Tier 1:

| Komponenta | Nástroj | Náklady |
|------------|---------|---------|
| Twitter/X data | API Basic | $100/měsíc |
| Cascade ML | CasCN / CasCIFF | $0 (open source) |
| Threshold sim | benmaier/thresholdmodel | $0 |
| Vizualizace sítí | Gephi Lite / pyvis | $0 |

**Celkové náklady Tier 2: ~$100/měsíc** (jen Twitter API)

### 4.3 Plný stack (Tier 3 — Intervence)

Přidává k Tier 2:

| Komponenta | Nástroj | Náklady |
|------------|---------|---------|
| LLM agenti | Ollama + Qwen2.5-7B / Llama 3.1-8B | $0 (lokální) |
| Nebo cloud LLM | DeepSeek API / Qwen-plus | $10-50/měsíc |
| Graf DB | Neo4j Community | $0 |
| Simulační framework | Vlastní nebo OASIS | $0 |

**Celkové náklady Tier 3: $0-150/měsíc**

### 4.4 Hardwarové požadavky

| Tier | RAM | GPU | Disk | CPU |
|------|-----|-----|------|-----|
| 1 (Monitoring) | 8 GB | Nepotřeba (CPU inference stačí) | 10 GB | 4 cores |
| 2 (Predikce) | 16 GB | Doporučeno (sentence-transformers) | 50 GB | 8 cores |
| 3 (Intervence + LLM) | 32 GB | 8 GB VRAM min (Ollama) | 100 GB | 8 cores |

---

## 5. Implementační plán

### Fáze 0: Proof of Concept (1 týden)

**Cíl:** Ověřit, že EWS signály jsou měřitelné na českých sociálních datech.

```
Úkoly:
□ Stáhnout historická data z jednoho zdroje (Reddit r/czech, 3 měsíce)
□ Spočítat sentiment (FERNET-C5)
□ Vytvořit denní časové řady
□ Aplikovat ewstools
□ Vizuálně ověřit — existovaly EWS signály před známou "bouří"?
   (např. reakce na politické rozhodnutí, virální kauza)
□ Go/no-go rozhodnutí
```

**Výstup:** Jupyter notebook s vizualizací — buď EWS fungují na CZ datech, nebo ne.

### Fáze 1: Monitoring MVP (2-3 týdny)

```
□ Ingest pipeline — 2-3 zdroje (Reddit + iDNES komentáře + Twitter)
□ NLP pipeline — sentiment + embeddings + clustering
□ EWS engine — rolling window na denních řadách
□ Cascade Risk Index — první verze (jednodušší, méně vah)
□ Dashboard — Streamlit s teploměry per téma
□ Alerting — email/Slack notifikace při CRI > 0.5
```

### Fáze 2: Predikce (2-3 týdny)

```
□ Síťová analýza — budování interakčních grafů
□ Threshold model — Monte Carlo simulace na reálných grafech
□ EWSNet integrace — deep learning predikce
□ Hybridní skóre — kombinace všech signálů
□ Historický backtest — validace na 5+ známých kaskádách
□ Kalibrace — ladění vah a prahů
```

### Fáze 3: Intervence (2-3 týdny)

```
□ Agent archetypes — generování z reálných dat
□ Rule-based simulace — Watts model s intervencemi
□ LLM narativní vrstva — kvalitativní popis dynamiky
□ A/B testování intervencí — porovnání strategií
□ Reporting engine — strukturované predikční zprávy
```

### Fáze 4: Produkce (průběžně)

```
□ Robustní scraping s retry + monitoring
□ Data retention policy (GDPR)
□ Performance optimalizace (batch processing, caching)
□ Rozšiřování zdrojů dat
□ Feedback loop — porovnání predikcí s realitou
```

---

## 6. Validace — Jak poznat, že to funguje

### 6.1 Retrospektivní validace

Vybrat 5-10 **známých českých názorových kaskád** z posledních 2 let:

| Příklad | Typ | Data k dispozici |
|---------|-----|-------------------|
| Reakce na politické rozhodnutí (energetická politika) | Politická | Twitter, iDNES komentáře |
| Virální kauza (mediální skandál) | Mediální | Reddit, Facebook |
| COVID opatření (historické) | Zdravotní politika | Twitter, Facebook skupiny |
| Sportovní událost s nacionalistickým podtextem | Kulturní | Twitter, komentáře |
| Environmentální protest / reakce na katastrofu | Environmentální | Reddit, zpravodajské komentáře |

**Metoda:**
1. Stáhnout historická data (pokud dostupná) pro období 2 týdny před + 1 týden po kaskádě
2. Spočítat EWS signály a CRI retrospektivně
3. Ověřit: **dal CRI alert alespoň 24-48 hodin před vrcholem kaskády?**

**Success criteria:** CRI > 0.5 alespoň 24h před kaskádou v ≥ 60 % případů, s false positive rate < 30 %.

### 6.2 Prospektivní validace

Po nasazení Tier 1:
- Logovat všechny alerty
- Po 3 měsících porovnat: kolik alertů vedlo k reálné kaskádě vs false positive
- Iterativně ladit prahy a váhy

### 6.3 Intervenční validace

Nejtěžší — nelze eticky dělat A/B test na reálné populaci. Možnosti:
- **Simulační validace** — porovnat predikovaný efekt intervence s tím, co se stalo bez intervence
- **Natural experiments** — najít případy, kde intervence (platformní nebo institucionální) přirozeně nastala, a porovnat s predikcí
- **Inokulační experimenty** — van der Lindenova metodika je eticky ověřená a má RCT design

---

## 7. Rizika a omezení

| Riziko | Dopad | Mitigace |
|--------|-------|----------|
| **EWS nefungují na sociálních datech** | Celý přístup selže | PoC fáze (Fáze 0) ověří před investicí |
| **Data access** — platformy omezí API | Nelze sbírat data | Multi-source strategie, scraping jako fallback |
| **False positives** — příliš mnoho alertů | Uživatelé ignorují | Konzervativní prahy, postupné ladění |
| **Etické riziko** — systém použit k manipulaci | Reputační + právní | Transparentnost, jen monitoring + obranné intervence |
| **GDPR** — ukládání sociálních dat | Právní | Anonymizace, agregace, no PII |
| **Stádní bias LLM** — agenti nejsou jako lidé | Intervenční simulace zavádí | Rule-based primárně, LLM jen pro naraci |
| **Concept drift** — jazykové vzory se mění | Modely degradují | Continuous retraining, feedback loop |

---

## 8. Etické mantinely

Tento systém je **seismograf, ne zbraň**. Jasné mantinely:

1. **Jen monitoring a obranné intervence.** Žádné ofenzivní operace (astroturfing, manipulace).
2. **Žádné profilování jednotlivců.** Vše na úrovni agregátů a archetypů.
3. **Transparentnost.** Metodologie veřejná, výstupy interpretovatelné.
4. **Data minimalizace.** Sbírat jen co je nutné, anonymizovat, mazat po retention period.
5. **Dual-use awareness.** Stejné nástroje lze použít k manipulaci — proto omezení přístupu k intervenčnímu modulu.

---

## 9. Porovnání s MiroFish

| Aspekt | MiroFish | CascadeWatch |
|--------|----------|--------------|
| **Vstup** | Jeden dokument | Kontinuální stream reálných dat |
| **Agenti** | Tisíce syntetických, LLM-generated | Desítky archetypů z reálných dat |
| **Predikce** | Sociální simulace → report | Statistické EWS + síťová analýza → index |
| **Validace** | Žádné benchmarky | Retrospektivní + prospektivní |
| **Náklady** | Tisíce $ za běh | $0-150/měsíc |
| **Silná stránka** | Kvalitativní narativní bohatost | Kvantitativní signály, měřitelnost |
| **Slabá stránka** | Nelze validovat, drahé | Méně "sexy", víc statistiky |
| **Přístup** | "Co by řekli syntetičtí lidé" | "Co říkají reální lidé a co to signalizuje" |

**Synergické použití:** CascadeWatch detekuje prekritický stav → MiroFish-like simulace (30 agentů) testuje intervenční scénáře.

---

## 10. České NLP zdroje — konkrétní modely a data

### 10.1 Sentiment modely pro češtinu

| Model | HuggingFace ID | Architektura | Trénink | Přesnost |
|-------|----------------|-------------|---------|----------|
| **LINDAT Sentiment** | `lindat.cz/1-4601` | RobeCzech fine-tuned | CSFD + Mall + Facebook | SOTA pro CZ |
| **FERNET-C5** | `fav-kky/FERNET-C5` | BERT-base | 93 GB Czech C5 corpus | 88.2% na CSFD |
| **FERNET-C5-RoBERTa** | `fav-kky/FERNET-C5-RoBERTa` | RoBERTa-base | 93 GB Czech C5 | ~89% |
| **RobeCzech** | `ufal/robeczech-base` | RoBERTa-base | Velký CZ korpus (ÚFAL) | ~85.4% na CSFD |
| **Czert-B** | `UWB-AIR/Czert-B-base-cased` | BERT-base | UWB AIR | základ pro fine-tuning |

**Doporučení pro CascadeWatch:** FERNET-C5-RoBERTa jako primární, LINDAT modely jako reference. Pro ABSA (aspect-based): mT5 fine-tuned na novém Czech ABSA datasetu (3100 vět, 2025).

### 10.2 Embedding modely (sentence-transformers kompatibilní)

Všechny od Seznam.cz, 15-20M parametrů:

| Model | HuggingFace ID | Dimenze | Licence | STS skóre |
|-------|----------------|---------|---------|-----------|
| **SimCSE-Small-E-Czech** | `Seznam/simcse-small-e-czech` | 256 | CC-BY 4.0 | dobré |
| **SimCSE-Dist-MPNet-ParaCrawl** | `Seznam/simcse-dist-mpnet-paracrawl-cs-en` | 256 | CC-BY 4.0 | 87.x |
| **SimCSE-Dist-MPNet-CzEng** | `Seznam/simcse-dist-mpnet-czeng-cs-en` | 256 | CC-BY-NC 4.0 | 87.83 |
| **RetroMAE-Small** | `Seznam/retromae-small-cs` | 256 | CC-BY 4.0 | — |

**Doporučení:** `simcse-small-e-czech` pro komerční použití (CC-BY 4.0), `simcse-dist-mpnet-czeng` pro výzkum (nejvyšší STS).

GitHub: `github.com/seznam/czech-semantic-embedding-models`

### 10.3 Morfologická analýza

| Nástroj | Rychlost | Přesnost | Poznámka |
|---------|----------|----------|----------|
| **MorphoDiTa** | 10-200K slov/s | Dobrá (slovníková) | Produkční, API na LINDAT |
| **UDPipe 2** | Pomalejší (neural) | Nejlepší | `czech-pdtc1.0` model, UD 2.12 |
| **Hybrid (2024)** | Střední | SOTA | 50% redukce chyb lemmatizace |
| **NameTag 3** | — | — | NER pro češtinu (ÚFAL) |

### 10.4 Trénovací datasety

| Dataset | Velikost | Typ | Zdroj |
|---------|----------|-----|-------|
| **CSFD** | 91 381 recenzí | Sentiment (3 třídy) | Česko-Slovenská filmová DB |
| **Mall.cz** | 145 307 recenzí | Sentiment (3 třídy) | E-shop |
| **Facebook CZ** | 10 000 postů | Sentiment (4 třídy) | České FB stránky |
| **Czech ABSA** | 3 100 vět | Aspect-based sentiment | Restaurace (LREC 2024) |
| **Czech ABSA Quadruplets** | 3 000 vět, 7K anotací | ABSA s opinion terms | github.com/biba10 (2025) |
| **V4 Twitter** | CZ tweety | Sentiment | X Academic API, 2023 |
| **SumeCzech** | 1M+ dokumentů | Články (ne sentiment) | iDNES, Novinky, Deník |
| **Verifee** | 10 000+ článků | Důvěryhodnost zdroje | 60 CZ zpravodajských webů |
| **BenCzechMark** | 50 úloh | Multiúlohový benchmark | HuggingFace CZLC |

Stahování ZCU datasety: `liks.fav.zcu.cz/sentiment/`

### 10.5 Scraping — praktický stav platforem

| Platforma | Metoda | Stav 2026 | Poznámka |
|-----------|--------|-----------|----------|
| **X/Twitter** | API Basic ($100/m) nebo `twscrape` | Funkční | twscrape porušuje ToS, API je legální |
| **Reddit** | PRAW (zdarma, rate-limited) | Funkční | r/czech, r/europe |
| **Facebook** | Prakticky uzavřeno | Nefunkční | Graph API gutted, CrowdTangle zrušen 2024 |
| **iDNES komentáře** | Playwright (JS-rendered) | Funkční | Vlastní komentářový systém |
| **Novinky.cz** | Playwright | Funkční | Seznam.cz provozuje |
| **Aktuálně.cz** | Playwright | Funkční | Ověřit commenting systém |
| **nyx.cz** | BeautifulSoup / Playwright | Funkční | Ověřit robots.txt + ToS |
| **Disqus (kde ho weby používají)** | Disqus Public API | Funkční | 1000 calls/h zdarma, nejčistší cesta |
| **YouTube CZ** | YouTube Data API v3 | Funkční | Zdarma, rate-limited |
| **Telegram** | Telethon (Python) | Funkční | Kanály přístupné |

**Praktická doporučení:**
- Start s Reddit (PRAW) + Disqus API — nejsnazší, legální, zdarma
- Fáze 2: přidat Twitter (API Basic $100/m) + Playwright pro iDNES/Novinky
- Facebook vynechat (GDPR + uzavřené API)

---

## 11. Další kroky

1. **Okamžitě:** Fáze 0 — PoC na historických Reddit datech
2. **Po validaci:** Fáze 1 — monitoring MVP
3. **Rozhodnutí:** Zda tohle má být standalone projekt nebo modul v STOPA ekosystému
4. **Dlouhodobě:** Integrace s NG-ROBOT — predikce čtenářské reakce na články

---

## 12. Zdroje a reference

### Akademické
- Scheffer et al. — "Critical Transitions in Nature and Society"
- Dakos et al. — "Early warning of climate tipping points from critical slowing down"
- Bury et al. (2021) — "Deep learning for early warning signals of tipping points" (PNAS)
- Watts (2002) — "A simple model of global cascades on random networks"
- Centola (2018) — "Experimental evidence for tipping points in social convention" (Science)
- Van der Linden — "Inoculating the Public against Misinformation" (Cambridge)
- "The Pareto effect in tipping social networks" (ESD, 2025)
- "Cascade-driven opinion dynamics on social networks" (arXiv, 2025)

### Nástroje
- ewstools: `github.com/ThomasMBury/ewstools` (Python EWS)
- EWSmethods: `github.com/duncanobrien/EWSmethods` (R EWS)
- pycascades: `github.com/pik-copan/pycascades` (tipping cascades)
- thresholdmodel: `github.com/benmaier/thresholdmodel` (Watts model)
- CyNetDiff: `github.com/eliotwrobson/CyNetDiff` (Cython cascade sim)
- CasCN: `github.com/ChenNed/CasCN` (deep learning cascades)
- CasCIFF: `github.com/XiaoYuan011/CasCIFF` (cascade prediction)
- Awesome-DL-Information-Cascades: `github.com/ChenNed/Awesome-DL-Information-Cascades-Modeling`
- early-warning-signals.org — Dakos/Scheffer originální toolbox

### České NLP
- LINDAT/CLARIAH-CZ: `lindat.cz`
- FERNET: `huggingface.co/fav-kky/FERNET-C5`
- RobeCzech: `huggingface.co/ufal/robeczech-base`
- Seznam embeddings: `github.com/seznam/czech-semantic-embedding-models`
- ZCU sentiment datasety: `liks.fav.zcu.cz/sentiment/`
- Czech ABSA: `github.com/biba10/Czech-ABSA-Opinion-Dataset-Benchmark`
- BenCzechMark: `huggingface.co/CZLC`

### Programy a platformy
- DARPA SocialSim: `darpa.mil/research/programs/computational-simulation-of-online-social-behavior`
- Bad News game: `getbadnews.com` (inokulace)
- TIDE-MARK: Nature Scientific Reports 2026 (temporal GNN fake news detection)
