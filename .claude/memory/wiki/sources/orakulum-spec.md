---
title: "ORAKULUM — Project Specification v0.2"
slug: orakulum-spec
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 9
claims_extracted: 5
---
# ORAKULUM — Project Specification v0.2

> **TL;DR**: ORAKULUM je sdílená Python analytická knihovna pro predikci a korelační analýzu z heterogenních datových zdrojů (GDELT, Polymarket, news). Tři projekty ji konzumují přes HTTP nebo přímý import: MONITOR (Node.js/FastAPI), POLYBOT, Záchvěv. Architektura používá sklearn-compatible rozhraní s bohatým PipelineResult výstupem a progresivní deps (core <100MB bez PyTorch).

## Key Claims

1. Tigramite PCMCI+ funguje na Windows s ParCorr (linear CI test) bez numba; CMIknn/CMIknnMixed vyžaduje numba jako opt-in extra — `[verified]`
2. TemporalAligner je kritická P0 komponenta: bez správného zarovnání heterogenních zdrojů (events, sentiment, prices) jsou korelace zkreslené — `[argued]`
3. Dual correlation backend: Tigramite primary + causal-learn (PC/FCI/GES) jako fallback — zabraňuje single point of failure v analytickém core — `[argued]`
4. Progresivní deps model (core <100MB, PyTorch jako optional extra) umožňuje deployment v prostředích bez GPU — `[asserted]`
5. Data adapter boundary: ORAKULUM dodává read-only data a analytiku, execution logika (paper trading, MCP tools) patří konzumentům — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| Tigramite | tool | existing |
| STUMPY | tool | new |
| Feast | tool | existing |
| Darts | tool | new |
| Chronos-2 | tool | existing |
| GDELT | tool | new |
| causal-learn | tool | new |
| PCMCI+ | concept | new |
| PipelineResult | concept | new |

## Relations

- Tigramite `implements` PCMCI+
- ORAKULUM `uses` Tigramite `as primary correlation backend`
- causal-learn `fallback-for` Tigramite
- STUMPY `implements` matrix profile anomaly detection
- Darts `wraps` time-series forecasting models including Chronos-2
