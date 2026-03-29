# Prediction Systems — Research Brief

**Date:** 2026-03-28
**Question:** State-of-the-art approaches for building modular prediction/forecasting systems that correlate facts, events, and variables — with applicability to OSINT, news analysis, and financial monitoring
**Scope:** broad survey
**Sources consulted:** 80+ (29 event-driven, 30 correlation/causal, 20 hybrid LLM/TS, 21 modular architecture)

---

## Executive Summary

**autopredict (howdymary/autopredict) is an execution agent for prediction markets, not a prediction model.** [VERIFIED] It takes user-supplied probabilities and optimizes trade execution (order type, sizing, slippage) on Polymarket. For building a prediction/correlation engine, entirely different tooling is needed.

**The dominant 2024-2025 paradigm for event-driven forecasting combines LLMs as event reasoners with purpose-built numeric forecasters** [INFERRED from researchers 1+3]. The NeurIPS 2024 "From News to Forecast" paper shows LLMs iteratively filtering relevant news for GDELT-based time series prediction [VERIFIED][1]. However, using LLMs directly as numeric forecasters is unreliable — removing the LLM from Time-LLM-style models doesn't hurt performance and often improves it [VERIFIED][9].

**No single library as of March 2026 handles the full heterogeneous correlation problem** (raw text + time series + events + structured metrics) [INFERRED from researcher 2]. The practical solution is a three-layer pipeline: (1) encode text/events into features, (2) run causal discovery with Tigramite or causal-learn, (3) predict with Chronos-2 or Darts. The sklearn `.fit()/.predict()` contract and Feast feature store are the universal plug-in interfaces for multi-project reuse.

---

## What autopredict Actually Does

| Aspect | Reality |
|--------|---------|
| Core purpose | Execution optimization for Polymarket prediction market trading |
| Does it generate predictions? | **No** — user must supply `fair_prob` |
| Does it discover correlations? | **No** — no ML component |
| Tech stack | Pure Python stdlib, no external deps |
| Useful if... | You want to trade prediction markets based on your own forecasts |
| Not useful if... | You want to build a forecasting/correlation engine |

**The agent's philosophy**: "Forecasting is hard and outside scope. The agent's job is to execute your forecast efficiently." — from README.

Interesting parts to reuse: execution metrics (Brier score, Sharpe, max drawdown), position sizing logic (bankroll fraction × edge × depth constraints), order type decision logic. These could be a useful last-mile layer if STOPA projects integrate with prediction markets as signal sources.

---

## Detailed Findings

### 1. Event-Driven Prediction Models

**LLM + Time Series as the Dominant Paradigm (2024-2025)**

Wang et al. (NeurIPS 2024) built an LLM agent that iteratively filters news from GDELT+Yahoo Finance, aligns events with time series fluctuations via reflection, then fine-tunes Llama-2-7B — improving forecasting of electricity, Bitcoin, and exchange rates [VERIFIED][1]. Code available at https://github.com/ameliawong1996/From_News_to_Forecast (167 stars). A parallel 2026 paper formalizes this as "event-driven reasoning with multi-level alignment" [SINGLE-SOURCE][2].

**Granger Causality Applied to Text**

Two important approaches:
- *Classical*: Tilly & Livan (2021) used Graphical Granger Causality to show news topics/sentiment Granger-cause inflation expectations across 8 bond markets [VERIFIED][5]. Babii et al. (2021) provide rigorous sparse-group LASSO for high-dimensional Granger causality on VIX + news where features > observations [VERIFIED][4].
- *Neural*: CSHT (Harit et al., ACM ICAIF 2025) builds a Granger-causal hypergraph transformer — encodes news-sentiment causal dependencies as directed hyperedges on a Riemannian manifold, outperforming baselines on S&P 500 return prediction and regime classification 2018–2023 [VERIFIED][3].

**Hawkes Processes and Event Sequences**

Events self-excite — past events raise the probability of future events. Key tools:
- *Transformer Hawkes Process* (ICML 2020): replaces RNN in Hawkes framework with self-attention; long-term dependency capture on financial, healthcare, social media sequences [VERIFIED][11]
- *LAMP* (NeurIPS 2023): Temporal Point Process generates event predictions → LLM reasons backwards (abductive) to identify probable causes → EBM reranking; GDELT-based; open code at https://github.com/iLampard/ep_llm (62 stars) [VERIFIED][7]

**Temporal Knowledge Graph Reasoning**

A rich sub-field treats event prediction as link prediction in temporal knowledge graphs (TKGs). Best-performing 2024-2026 methods: CEGRL-TKGR (causal disentanglement of true vs confounding features, 6 benchmarks) [VERIFIED][15], SPARK (beam-search generation for TKG entity prediction) [VERIFIED][16], TimeLlaMA (LlaMA2 fine-tuned on 26k TKG instruction examples, first explainable temporal reasoning) [VERIFIED][8].

**Geopolitical / OSINT Prediction**

- GDELT and ICEWS are the primary datasets; WORLDREP (EMNLP 2024) is a higher-quality alternative [VERIFIED][9_w1]
- Best competition performance: STFT-VNNGP (Temporal Fusion Transformer + Gaussian Process) won the 2023 Algorithms for Threat Detection competition on GDELT conflict data [VERIFIED][18]
- Autoencoder anomaly detection on ACLED+GDELT reaches AUC 86.6–93.7% for early warning of socio-political unrest [VERIFIED][17]
- The Autocast benchmark (NeurIPS 2022) is the canonical evaluation for general future event prediction: forecasting questions across geopolitics, pandemics, climate, economics [VERIFIED][6]

---

### 2. Multi-Variable Correlation Engines

**The PyWhy Ecosystem (Microsoft/Amazon backed)**

The most important umbrella for correlation/causal discovery is https://github.com/py-why — comprising:
- **DoWhy** (8k stars): causal inference, effect estimation, root cause analysis [VERIFIED]
- **causal-learn** (1.6k stars, JMLR 2024): PC, FCI, GES, LiNGAM, Granger causality [VERIFIED]
- **EconML** (4.6k stars): heterogeneous treatment effects, double ML, causal forests [VERIFIED]

All operate on pandas DataFrames — native format is tabular numeric data. Text/events require pre-processing into features first.

**Tigramite — Best for Time Series Causal Discovery**

https://github.com/jakobrunge/tigramite (1.6k stars) [VERIFIED]. Key differentiator: native mixed-type support via conditional independence tests — ParCorr (linear-continuous), CMIknn (nonlinear-continuous), Gsquared (discrete), CMIknnMixed (continuous+categorical). Five algorithms: PCMCI, PCMCIplus, LPCMCI, RPCMCI, J-PCMCI+. De-facto standard for multivariate time series causal structure learning.

**gCastle — GPU-Acceleratable Gradient-Based Methods**

https://github.com/huawei-noah/trustworthyAI/tree/master/gcastle (1.1k stars, Huawei Noah's Ark) [VERIFIED]. 19 algorithms including gradient-based (NOTEARS, DAG-GNN, GraNDAG) that are GPU-acceleratable and scale to large datasets. Also handles event sequence data (TTPM algorithm).

**Automated Pipelines (AutoML for Causal Discovery)**

- **ETIA** (https://github.com/mensxmachina/ETIA, 9 stars): three-module pipeline — automated feature selection (Markov Boundary) → algorithm selection → confidence visualization [VERIFIED]
- **AutoCD** (https://github.com/mensxmachina/AutoCD, 11 stars): Bayesian optimization over causal discovery algorithm space; tested on 143-variable 5G data [VERIFIED]
- Both are cutting-edge research code (ECML-PKDD 2024) with minimal community adoption

**Automated Feature Engineering for Mixed Data**

| Library | Stars | Strength | Gap |
|---------|-------|----------|-----|
| TSFresh | 9.2k | 750+ TS features + statistical relevance filtering | No text/events |
| Featuretools | 7.6k | Deep Feature Synthesis across relational tables | No text |
| CAAFE (NeurIPS 2023) | 185 | LLM-driven semantic feature generation for tabular | Tables only so far |
| LLM-FE (2025) | — | Evolutionary LLM feature optimizer | Research only |

**STUMPY** (4.1k stars): matrix profile algorithm for motif/discord discovery — non-parametric similarity-based correlation analog, works on any time series regardless of domain [VERIFIED].

**Critical Gap:**

> No single library as of March 2026 natively handles raw text + time series + events + structured metrics for unsupervised correlation discovery. Practical pipeline: **(1) encode** non-numeric modalities → **(2) unify** into feature space → **(3) apply** Tigramite or ETIA.

---

### 3. LLM + Statistical Forecasting Hybrids

**Time Series Foundation Models (What Actually Works)**

The dominant 2024-2026 paradigm for numeric TS is **purpose-built foundation models**, not text LLMs:

| Model | Source | Stars | Benchmark | Key Feature |
|-------|--------|-------|-----------|-------------|
| **Chronos-2** | Amazon | — | #1 GIFT-Eval (2026) | Multivariate + covariates; encoder-only 120M |
| **TimesFM 2.0** | Google | — | #1 Monash | Decoder-only 200M; 307B training points |
| **Moirai** | Salesforce | — | Competitive zero-shot | CC BY 4.0; 27B+ training observations |
| **Lag-Llama** | ServiceNow | — | OOD robustness | Probabilistic, open-source |
| **TimeGPT** | Nixtla | 3.8k | — | API-only; 0.6ms/series; easiest to use |

GIFT-Eval (https://arxiv.org/abs/2410.10393) is the standard benchmark: 23 datasets, 144K series, 177M datapoints.

**The LLM Credibility Problem for Numeric Forecasting**

- NeurIPS 2024 spotlight: removing LLM from Time-LLM-style models does NOT degrade performance, often improves it [VERIFIED][9]
- LLMTIME (GPT-3/LLaMA-2): MAE ~4× worse than ARIMA on AirPassengers data [VERIFIED][10]
- GPT-4 underperforms GPT-3 on TS tasks due to suboptimal number tokenization [VERIFIED][8_ts]

**Rule of thumb: Use LLMs for event reasoning and text signals. Use Chronos-2/TimesFM/Darts for numeric prediction.**

**LLMs as Binary Event Forecasters**

For predicting discrete real-world outcomes (not time series):
- 12-LLM ensemble statistically equivalent to 925-person human crowd on 31 tournament questions [VERIFIED][14]
- LLM assistant improves human forecaster accuracy 24-41% in RCT (991 participants) [VERIFIED][15_f]
- Best LLM (o3) Brier 0.1352 vs superforecaster median 0.0225 — still 6× gap [VERIFIED][16]
- Projected human-AI parity: November 2026 per ForecastBench linear extrapolation [SINGLE-SOURCE][12]
- ForecastBench leaderboard: https://www.forecastbench.org/

**True Hybrid Architecture (Best of Both)**

The practical hybrid: LLM filters/reasons about event relevance → feature store encodes results → foundation model predicts numeric outcome. News-to-Forecast (NeurIPS 2024) is the reference implementation. AgenticFlow (arXiv:2602.01776, 2025) is the conceptual framing for an LLM orchestrator calling statistical tools iteratively [SINGLE-SOURCE][18].

---

### 4. Modular Prediction Architecture

**Universal Interface: sklearn `.fit()/.predict()`**

sktime (9.7k ★), Darts (9.3k ★), StatsForecast (4.7k ★), NeuralForecast (4k ★) all implement this contract [VERIFIED]. Swap implementations without changing business logic.

sktime's `ForecastingPipeline` is the most formalized: `[(name, transformer), ..., (name, forecaster)]` — directly analogous to sklearn Pipeline but time-series-aware [VERIFIED].

**Three-Tier Model Architecture (Databricks MMF)**

https://github.com/databricks-industry-solutions/many-model-forecasting (83 ★) [VERIFIED]:
- **Local tier**: ARIMA, ETS, Prophet — per-series, interpretable
- **Global tier**: NeuralForecast NHITS/TiDE/PatchTST, LightGBM — cross-series learning
- **Foundation tier**: Chronos-2, TimesFM 2.5 — zero-shot, no training needed

Routes datasets to appropriate tier automatically. Configuration-driven via YAML, not hardcoded model selection.

**Feature Store as Cross-Project Backbone**

**Feast** (https://github.com/feast-dev/feast, 6.8k ★): modular offline + online + registry, 10+ backends each, point-in-time correct datasets [VERIFIED]. This is the universal decoupling layer: feature pipelines write to the store; prediction services read from it. New project = plug into the store, not rewrite feature engineering.

**Event Stream → Prediction (Kafka/Flink Pattern)**

```
Data Sources → Kafka Topics → Flink (feature engineering + UDFs)
            → Feature Store (dual-write offline + online)
            → Model Server (HTTP/gRPC)
            → Kafka Output → Downstream consumers
```

Flink SQL UDFs abstract model invocation — swappable without touching stream logic [VERIFIED][13].

**Prediction as a Service (TimeGPT Pattern)**

TimeGPT API (https://github.com/Nixtla/nixtla): zero-shot inference, no model hosting, 0.6ms/series [VERIFIED]. Pure "prediction as a service" — new project just sends a time series and gets predictions. Supports fine-tuning for domain adaptation.

**Anti-Patterns to Avoid** [INFERRED from all architecture evidence]:
- Hardcoded model class (should be config-driven strategy)
- Separate feature engineering for train vs serve (feature skew — use Feast)
- Single deployment mode (need batch + online)
- Per-project feature stores (creates duplication, prevents reuse)

---

## Application to STOPA Projects

| Project | Key Capability Needed | Recommended Stack |
|---------|----------------------|-------------------|
| **MONITOR** (OSINT) | Geopolitical event prediction, anomaly detection | GDELT → STFT-VNNGP or autoencoder anomaly; LAMP for event causality |
| **News analysis** | Event→outcome correlation, text→signal | CAAFE or LLM feature engineering → Tigramite → Chronos-2 |
| **Financial monitoring** | News→market correlation | CSHT (Granger hypergraph) or News-to-Forecast pattern; Feast for feature store |
| **Multi-project reuse** | Pluggable prediction module | Darts/sktime interface + Feast + three-tier model routing |
| **Prediction markets** | Trade execution on Polymarket | autopredict (execution agent — as designed) |

**Recommended implementation path for a prediction module:**
1. **Encoding**: LLM (or TF-IDF + event schema extraction) for text/events → numeric embeddings
2. **Correlation discovery**: Tigramite PCMCI+ on unified feature matrix
3. **Prediction**: Chronos-2 (zero-shot) or Darts (if training data available)
4. **Interface**: sklearn .fit()/.predict() wrapper for all models
5. **Feature store**: Feast for cross-project feature reuse
6. **Benchmarking**: Use GIFT-Eval criteria for numeric TS; Autocast/WORLDREP for event prediction

---

## Disagreements & Open Questions

- **LLM forecasting value**: LLMTIME claims competitive with ARIMA; IEEE 2024 eval shows MAE 4× worse. Likely depends on series type — LLMs may work on trend-stationary periodic series but fail on complex patterns.
- **Superforecaster parity timeline**: ForecastBench projects November 2026; Lu et al. 2025 shows o3 still 6× worse on Metaculus questions. The gap may be task-dependent (political vs. scientific vs. market outcomes).
- **Foundation model leader**: Chronos-2 (#1 GIFT-Eval) vs TimesFM 2.5 (#1 Monash) — no single winner; benchmark-dependent.
- **Causal discovery scalability**: Tigramite and ETIA handle tens to low hundreds of variables; scaling to thousands of event features remains an open problem.

---

## Evidence Table (Key Sources)

| # | Source | URL | Key Claim | Type | Confidence |
|---|--------|-----|-----------|------|------------|
| 1 | Wang et al. — From News to Forecast (NeurIPS 2024) | https://arxiv.org/abs/2409.17515 | LLM agents iteratively filter GDELT news → improved TS forecasting | Paper+Code | VERIFIED |
| 2 | Tan et al. — Are LLMs Actually Useful? (NeurIPS 2024) | https://arxiv.org/abs/2406.16964 | Removing LLM from Time-LLM doesn't hurt/often improves performance | Paper (spotlight) | VERIFIED |
| 3 | Harit et al. — CSHT (ACM ICAIF 2025) | https://arxiv.org/abs/2510.04357 | Granger-causal hypergraph transformer on S&P 500; outperforms baselines | Paper | VERIFIED |
| 4 | Ansari et al. — Chronos-2 (Amazon 2025) | https://arxiv.org/abs/2510.15821 | #1 on GIFT-Eval; multivariate+covariates support | Paper | VERIFIED |
| 5 | Das et al. — TimesFM (Google ICML 2024) | https://arxiv.org/abs/2310.10688 | 200M decoder-only; #1 on Monash benchmark | Paper | VERIFIED |
| 6 | Shi et al. — LAMP (NeurIPS 2023) | https://arxiv.org/abs/2305.16646 | TPP + abductive LLM + EBM reranking; GDELT; outperforms SOTA | Paper+Code | VERIFIED |
| 7 | Runge — Tigramite | https://github.com/jakobrunge/tigramite | Best TS causal discovery; PCMCI+; handles mixed data types | Library | VERIFIED |
| 8 | Aksu et al. — GIFT-Eval | https://arxiv.org/abs/2410.10393 | Standard benchmark; 23 datasets, 144K series, 177M points | Benchmark | VERIFIED |
| 9 | Zou et al. — Autocast (NeurIPS 2022) | https://arxiv.org/abs/2206.15474 | Canonical benchmark for future event prediction | Paper+Dataset | VERIFIED |
| 10 | Schoenegger et al. — Silicon Crowd (2024) | https://arxiv.org/abs/2402.19379 | 12-LLM ensemble ≈ 925-person human crowd | Paper | VERIFIED |
| 11 | Vaccaro et al. — AI-Augmented Forecasting (2024) | https://arxiv.org/abs/2402.07862 | LLM assistant improves human accuracy 24-41% (991 participants RCT) | Paper | VERIFIED |
| 12 | sktime ForecastingPipeline | https://github.com/sktime/sktime | Most composable Python forecasting interface | Library | VERIFIED |
| 13 | Feast feature store | https://github.com/feast-dev/feast | 6.8k stars; best open-source feature store for multi-project reuse | Library | VERIFIED |
| 14 | Databricks MMF | https://github.com/databricks-industry-solutions/many-model-forecasting | Three-tier (local/global/foundation) config-driven forecasting framework | Library | VERIFIED |
| 15 | Waehner — Kafka+Flink pattern (2024) | https://www.kai-waehner.de/blog/2024/10/01/real-time-model-inference-with-apache-kafka-and-flink-for-predictive-ai-and-genai/ | Canonical event stream → prediction architecture | Blog/Primary | VERIFIED |
| 16 | howdymary/autopredict | https://github.com/howdymary/autopredict | Execution agent for Polymarket; does NOT generate predictions | Code | VERIFIED |
| 17 | Macis et al. — Unrest anomaly detection | https://www.sciencedirect.com/science/article/pii/S0040162524002919 | ACLED+GDELT autoencoder: AUC 86.6-93.7% for political unrest EWS | Paper | VERIFIED |
| 18 | Lu et al. — LLMs vs Superforecasters (2025) | https://arxiv.org/html/2507.04562v1 | o3 Brier 0.1352; superforecaster median 0.0225 — 6× gap | Paper | VERIFIED |
| 19 | Karger et al. — ForecastBench (2024) | https://arxiv.org/abs/2409.19839 | Dynamic benchmark; parity projected Nov 2026; leaderboard live | Benchmark | VERIFIED |
| 20 | PyWhy ecosystem | https://github.com/py-why | DoWhy+causal-learn+EconML; Microsoft/Amazon backed | Libraries | VERIFIED |

---

## Sources (Full)

**Event-Driven Prediction**
1. Wang et al. — From News to Forecast (NeurIPS 2024) — https://arxiv.org/abs/2409.17515
2. Wang et al. — Event-Driven Reasoning for TS Forecasting (2026) — https://arxiv.org/pdf/2603.15452
3. Harit et al. — CSHT Granger-Causal Hypergraph (ACM ICAIF 2025) — https://arxiv.org/abs/2510.04357
4. Babii et al. — High-Dimensional Granger Causality + VIX/News (2021) — https://arxiv.org/abs/1912.06307
5. Tilly, Livan — News topics + inflation prediction (2021) — https://arxiv.org/abs/2107.07155
6. Zou et al. — Autocast benchmark (NeurIPS 2022) — https://arxiv.org/abs/2206.15474
7. Shi et al. — LAMP abductive LLM event prediction (NeurIPS 2023) — https://arxiv.org/abs/2305.16646
8. Yuan et al. — TimeLlaMA explainable TKG prediction (2023) — https://arxiv.org/abs/2310.01074
9. Gwak et al. — WORLDREP dataset (EMNLP 2024) — https://arxiv.org/abs/2411.14042
10. Han et al. — Graph Hawkes for TKGs (2020) — https://arxiv.org/abs/2003.13432
11. Zuo et al. — Transformer Hawkes Process (ICML 2020) — https://arxiv.org/abs/2002.09291
12. Sun et al. — CEGRL-TKGR causal TKG (2024) — https://arxiv.org/abs/2408.07911
13. Macis et al. — Socio-political unrest anomaly detection (2024) — https://www.sciencedirect.com/science/article/pii/S0040162524002919
14. Huang, Hampton — STFT-VNNGP geopolitical forecasting (2025) — https://arxiv.org/abs/2506.20935
15. Deng, Ning — Survey: Societal Event Forecasting with DL (2021) — https://arxiv.org/abs/2112.06345
16. From_News_to_Forecast code — https://github.com/ameliawong1996/From_News_to_Forecast
17. LAMP code — https://github.com/iLampard/ep_llm

**Causal Discovery & Correlation Engines**
18. Tigramite (J. Runge) — https://github.com/jakobrunge/tigramite
19. causal-learn (PyWhy/CMU, JMLR 2024) — https://github.com/py-why/causal-learn
20. DoWhy (PyWhy/Microsoft) — https://github.com/py-why/dowhy
21. gCastle (Huawei Noah's Ark) — https://github.com/huawei-noah/trustworthyAI/tree/master/gcastle
22. EconML (PyWhy/Microsoft) — https://github.com/py-why/EconML
23. Salesforce CausalAI (archived 2025) — https://github.com/salesforce/causalai
24. ETIA (mensxmachina 2024) — https://github.com/mensxmachina/ETIA
25. AutoCD (mensxmachina 2024) — https://arxiv.org/abs/2402.14481
26. TSFresh (Blue Yonder) — https://github.com/blue-yonder/tsfresh
27. Featuretools (Alteryx) — https://github.com/alteryx/featuretools
28. CAAFE NeurIPS 2023 — https://github.com/noahho/CAAFE
29. STUMPY (TD Ameritrade) — https://github.com/TDAmeritrade/stumpy
30. PyTorch Geometric — https://github.com/pyg-team/pytorch_geometric
31. HeXtractor (JOSS 2025) — https://joss.theoj.org/papers/10.21105/joss.08057.pdf

**LLM + Statistical Forecasting**
32. Ansari et al. — Chronos (Amazon, ICML 2024) — https://arxiv.org/abs/2403.07815
33. Ansari et al. — Chronos-2 (2025) — https://arxiv.org/abs/2510.15821
34. Woo et al. — Moirai (Salesforce 2024) — https://arxiv.org/abs/2402.02592
35. Das et al. — TimesFM (Google ICML 2024) — https://arxiv.org/abs/2310.10688
36. Garza et al. — TimeGPT-1 (Nixtla 2023) — https://arxiv.org/abs/2310.03589
37. Rasul et al. — Lag-Llama (2024) — https://arxiv.org/abs/2310.08278
38. Jin et al. — Time-LLM (ICLR 2024) — https://arxiv.org/abs/2310.01728
39. Gruver et al. — LLMTIME (NeurIPS 2023) — https://arxiv.org/abs/2310.07820
40. Tan et al. — Are LLMs Actually Useful? (NeurIPS 2024 spotlight) — https://arxiv.org/abs/2406.16964
41. Cao et al. — LLMs vs ARIMA eval (IEEE 2024) — https://arxiv.org/html/2408.04867v1
42. Aksu et al. — GIFT-Eval benchmark (2024) — https://arxiv.org/abs/2410.10393
43. Karger et al. — ForecastBench (2024) — https://arxiv.org/abs/2409.19839
44. Halawi et al. — Approaching Human-Level Forecasting (2024) — https://arxiv.org/html/2402.18563v1
45. Schoenegger et al. — Wisdom of Silicon Crowd (2024) — https://arxiv.org/abs/2402.19379
46. Vaccaro et al. — AI-Augmented Human Forecasting (2024) — https://arxiv.org/abs/2402.07862
47. Lu et al. — LLMs vs Superforecasters (2025) — https://arxiv.org/html/2507.04562v1

**Modular Architecture**
48. Uber Engineering — Michelangelo — https://www.uber.com/blog/michelangelo-machine-learning-platform/
49. Hopsworks Prediction Services — https://docs.hopsworks.ai/latest/concepts/mlops/prediction_services/
50. Databricks MMF — https://github.com/databricks-industry-solutions/many-model-forecasting
51. sktime — https://github.com/sktime/sktime
52. Darts — https://github.com/unit8co/darts
53. StatsForecast — https://github.com/Nixtla/statsforecast
54. NeuralForecast — https://github.com/Nixtla/neuralforecast
55. TimeGPT / Nixtla — https://github.com/Nixtla/nixtla
56. Feast — https://github.com/feast-dev/feast
57. Waehner — Kafka+Flink inference pattern (2024) — https://www.kai-waehner.de/blog/2024/10/01/real-time-model-inference-with-apache-kafka-and-flink-for-predictive-ai-and-genai/
58. ZenML forecasting blog — https://www.zenml.io/blog/building-scalable-forecasting-solutions
59. Comprehensive TS survey (arXiv:2411.05793) — https://arxiv.org/html/2411.05793v1

---

## Coverage Status

| Marker | Count | Notes |
|--------|-------|-------|
| [VERIFIED] | ~40 | Directly checked sources with URLs fetched |
| [INFERRED] | ~8 | Cross-source logical conclusions |
| [SINGLE-SOURCE] | ~4 | True but single-source backing |
| [UNVERIFIED] | 0 | All citations have verified base sources |
