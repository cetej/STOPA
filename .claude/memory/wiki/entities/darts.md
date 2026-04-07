---
name: Darts
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [orakulum-spec]
tags: [time-series, prediction, python]
---

# Darts

> Unified Python library pro time-series forecasting — wrappuje desítky modelů (ARIMA, NHITS, TiDE, Chronos-2) za jednotné sklearn-like API, s podporou covariates a probabilistických predikcí.

## Key Facts

- PyPI: `darts>=0.29`, Python + PyTorch Lightning (ref: sources/orakulum-spec.md)
- ORAKULUM opt-in extra: `pip install orakulum[prediction]` — není v core deps kvůli PyTorch závislosti (ref: sources/orakulum-spec.md)
- TSPredictor wrapper: `model="nhits"`, `horizon=14`, `covariates=X`, vrací forecast s confidence intervals (ref: sources/orakulum-spec.md)
- Modely v ORAKULUM ModelRouter: ARIMA, ETS (local tier), NHITS, TiDE (global tier), Chronos-2 (foundation tier) (ref: sources/orakulum-spec.md)
- Target v1.0: TS forecast MAPE <15% na GIFT-Eval subsets (ref: sources/orakulum-spec.md)

## Relevance to STOPA

Primární forecasting backend pro ORAKULUM prediction modul (v0.2). Relevantní pro POLYBOT (market prediction) a Záchvěv (cascade onset timing prediction).

## Mentioned In

- [ORAKULUM Project Specification](../sources/orakulum-spec.md)
