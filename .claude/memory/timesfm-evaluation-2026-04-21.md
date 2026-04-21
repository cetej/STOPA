# TimesFM 2.5 Evaluation — POLYBOT & BONANZA

**Date:** 2026-04-21
**Trigger:** HuggingFace transformers v5.5.0 (April 2026) added TimesFM 2.5 (Google Research, Apache-2.0, 200M params, 1024-step context, 256-step horizon, XReg covariates).
**Scope:** Evaluate fit as forecasting engine for POLYBOT (Polymarket paper trading) and BONANZA (Claude AI trading bot).
**Budget used:** 2 Explore agents, 1 WebSearch, 2 WebFetch, 0 compute (live test skipped — rationale below).

---

## Executive summary

TimesFM 2.5 is a strong general-purpose time-series foundation model, but neither POLYBOT nor BONANZA currently has a forecasting surface that would benefit meaningfully from it. POLYBOT solves a **binary prediction-market probability estimation** problem (multi-signal heuristic: Bayesian tracker + FinBERT sentiment + longshot-bias correction + CEX/Polymarket divergence), where a univariate price forecaster is mostly tangential — only one peripheral function (`crypto_feed.detect_divergence`) plausibly gains from a better short-horizon price forecast. BONANZA is in Sprint 1 with rule-based trailing stops and congressional-copy signals only; its Sprint 2 strategy files don't yet exist, so there is nothing to replace. Recommendation: **POLYBOT → low-priority hybrid (backtest before commit)**, **BONANZA → ignore until Sprint 2 introduces a forecasting surface worth replacing**.

---

## Current state — POLYBOT

| Aspect | Value |
|---|---|
| Has forecasting? | Yes, but **not time-series**: multi-signal probability estimation |
| Primary approach | Bayesian tracker + deviation heuristic + FinBERT sentiment + longshot bias (Becker 2021-25) + CEX/Polymarket divergence |
| Time-series ML used? | None (no ARIMA/LSTM/Prophet/transformer) |
| Inputs | Polymarket Gamma API (YES/NO price, liquidity), Binance OHLCV (5/15/60 min), CLOB orderbook, news + FinBERT sentiment, manual thesis priors |
| Output | `predicted_prob ∈ [0,1]`, confidence (low/med/high), edge, Kelly sizing → paper trade |
| Horizon | Crypto divergence 5-60 min; general markets = resolution date (event-terminal) |
| Scale | ~50 markets per scan, SQLite-logged history |
| Relevant files | `scanner.py`, `bayesian.py`, `crypto_feed.py` (168 lines), `longshot_bias.py`, `sentiment.py`, `tools/analysis.py` |

**Where TimesFM could plug in:** only `crypto_feed.py` — `get_price_change()` currently reads 2 klines and `detect_divergence()` converts `abs(change_pct)` into a capped ±35% offset from 50/50. A TimesFM forecast on the last 256-1024 5-min closes would replace that naive momentum proxy with `prob_up` derived from the quantile distribution. **Not a replacement for the rest of the stack.**

## Current state — BONANZA

| Aspect | Value |
|---|---|
| Has forecasting? | **No** |
| Primary approach | Rule-based trailing stop (5% default) + congressional copy-trading (STOCK Act via Lambda Finance) + Claude Desktop + Alpaca MCP v2 |
| Time-series ML used? | None |
| Inputs | Alpaca positions, congressional transaction metadata (politician, symbol, action, amount range) |
| Output | Buy/sell orders, trailing stops, option chains — no probability/quantile output |
| Horizon | N/A |
| Scale | Per-trade, no screening |
| Relevant files | `src/bonanza/config.py`, `broker/alpaca.py`, `api.py`, `db.py`. Strategy files `trailing_stop.py`, `copy_trade.py`, `wheel.py` are **Sprint 2 placeholders — don't exist yet** |

**Where TimesFM could plug in:** nowhere today. Sprint 2 roadmap is not delivered; there is no predictive model to compare against.

---

## TimesFM 2.5 — technical specs

Source: [google/timesfm-2.5-200m-pytorch](https://huggingface.co/google/timesfm-2.5-200m-pytorch), [google-research/timesfm](https://github.com/google-research/timesfm), [Let's Data Science release note](https://letsdatascience.com/news/timesfm-releases-25-time-series-model-update-416fba8f).

| Spec | Value |
|---|---|
| Params | **200M** (down from 500M in 2.0) |
| Architecture | Decoder-only foundation model, QKV-fused since Oct 2025 |
| Context length | up to **1024** timesteps |
| Horizon length | up to **256** timesteps (optional 30M continuous quantile head extends to ~1000) |
| Output shape | point `(B, H)` + quantiles `(B, H, 10)` = 10th-90th percentile |
| Frequency handling | No frequency indicator required (any-freq since 2.5) |
| Covariates | **XReg** supported (restored Oct 2025) |
| Backends | PyTorch or JAX/Flax |
| Install | `pip install timesfm` or `uv pip install -e .[torch]` |
| Checkpoint download | ~800 MB from HF on first `from_pretrained()` |
| Hardware | Runs on CPU; `torch_compile=True` adds 20-60s warmup but speeds subsequent inference |
| License | **Apache-2.0** (open, but "not an officially supported Google product") |
| Paper | [arXiv:2310.10688](https://arxiv.org/abs/2310.10688) (ICML 2024) |

Minimal call:

```python
import numpy as np, timesfm
m = timesfm.TimesFM_2p5_200M_torch.from_pretrained("google/timesfm-2.5-200m-pytorch", torch_compile=True)
m.compile(timesfm.ForecastConfig(max_context=1024, max_horizon=256,
         normalize_inputs=True, use_continuous_quantile_head=True,
         fix_quantile_crossing=True, infer_is_positive=True))
point, q = m.forecast(horizon=12, inputs=[np.asarray(last_256_closes, dtype=np.float32)])
# point.shape == (1, 12), q.shape == (1, 12, 10)
prob_up = float((q[0, -1, :] > last_256_closes[-1]).mean())
```

---

## Quick test — SKIPPED (with rationale)

A stub script demonstrating the integration surface is at [`.claude/memory/intermediate/timesfm-quick-test.py`](.claude/memory/intermediate/timesfm-quick-test.py). It is **not executed**.

Reasons for skipping the live run:

1. **BONANZA has no forecasting surface** → live inference on BONANZA data is meaningless because there is no baseline to compare against.
2. **POLYBOT's primary prediction layer is binary event resolution**, not time-series forecasting. The one plausible integration point (`crypto_feed.py`) is a peripheral signal in a multi-signal system.
3. **A single inference proves nothing.** Real evaluation requires paired historical data: N past divergence events with known Polymarket resolutions, then measuring MAE/RMSE and directional accuracy of TimesFM vs the current `momentum_signal` baseline. That is a dedicated `/autoresearch` task with several hours of data engineering, not a 15-minute smoke test.
4. **Setup cost vs payoff.** ~800 MB checkpoint download + torch_compile warmup + potential Windows encoding/DLL quirks would consume 30-60 min to produce a shape-confirming printout that doesn't inform the adopt/ignore decision.

The decision between `adopt/hybrid/ignore` is answered by fit analysis, not by a toy inference.

---

## Recommendation — POLYBOT

### Verdict: **Hybrid, low priority**

TimesFM 2.5 should **not replace** POLYBOT's prediction layer. The core edge of POLYBOT is multi-signal fusion on binary prediction-market contracts, where the forecasting task is "what is P(event resolves YES)" — a classification-style problem with sparse ground truth, not a regression on a continuous series. TimesFM is trained on continuous time-series forecasting and has no native notion of event resolution, longshot bias, or order-book imbalance.

However, **one narrow integration is defensible**: replace the 2-kline `momentum_signal` in `crypto_feed.detect_divergence()` with a TimesFM-derived `prob_up_at_horizon` computed from the last 256 5-min closes. That gives a properly calibrated probability distribution instead of a linear-capped offset, which is strictly more information.

**Expected impact:**
- Upside: better short-horizon probability estimation on crypto contracts (~subset of ~50 markets). Cleaner Kelly sizing on divergence trades.
- Downside: latency (model load + per-scan inference), memory footprint (~800 MB), an additional dependency (torch). Polymarket crypto contracts often resolve on discrete event conditions (e.g., "BTC closes above $X by Friday") — a point forecast doesn't cleanly map onto that without additional modeling.
- **Gate before commit:** requires paired backtest on historical divergence events.

### Migration plan (if backtest passes)

1. **Collect backtest dataset** — export the last 90 days of POLYBOT `predictions` rows where contract is crypto-based (BTC/ETH), with Polymarket resolution known. Join with Binance 5-min klines at trade timestamp (pull t-256 candles). ~2-4 hours.
2. **Build evaluation harness** — for each historical row: (a) current momentum_signal output, (b) TimesFM-derived prob_up at horizon matching contract expiry. Score both against realized resolution (Brier score, directional accuracy, calibration curve).
3. **Decide on gating** — if TimesFM Brier < current Brier by ≥ 5% on holdout, proceed. Otherwise write learning and abandon.
4. **Wrap as optional signal** — add `crypto_forecast.py` module, gated by config flag `USE_TIMESFM_FORECAST=1`. Default off. Emit `prob_up` alongside existing `momentum_signal` for 1-2 weeks of paper trading.
5. **Promote or revert** — after ~30 paper trades with both signals logged, compare realized P&L with/without the override. Promote only if edge improvement is robust across BTC and ETH.

---

## Recommendation — BONANZA

### Verdict: **Ignore**

BONANZA has no forecasting code to replace. Strategy files (`trailing_stop.py`, `copy_trade.py`, `wheel.py`) are Sprint 2 placeholders that don't exist yet. Adopting TimesFM now would be premature optimization: it would commit to a transformer-based forecasting stack before the Sprint 2 strategy design has decided whether forecasting is even in scope.

**Re-evaluate TimesFM when:** Sprint 2 ships and introduces either (a) a numerical price-prediction signal beyond trailing stops, or (b) a multi-symbol screening phase where short-horizon forecasts could filter candidates. At that point the evaluation should compare TimesFM against simpler alternatives (EMA/MACD direction, XGBoost on TA features) before defaulting to a 200M-param foundation model.

---

## Rules followed

- No global install of TimesFM (no install performed at all).
- No modification of POLYBOT or BONANZA production code.
- Output written to STOPA memory only.
- Stayed under 6-8 WebSearch budget (1 WebSearch + 2 WebFetch used).
- Absolute date in filename (2026-04-21 = today).

## Sources

- [google/timesfm-2.5-200m-pytorch — HuggingFace model card](https://huggingface.co/google/timesfm-2.5-200m-pytorch)
- [google-research/timesfm — GitHub](https://github.com/google-research/timesfm)
- [TimesFM 2.5 release note — Let's Data Science](https://letsdatascience.com/news/timesfm-releases-25-time-series-model-update-416fba8f)
- [A decoder-only foundation model for time-series forecasting — Google Research blog](https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/)
- [TimesFM paper — arXiv:2310.10688 (ICML 2024)](https://arxiv.org/abs/2310.10688)
