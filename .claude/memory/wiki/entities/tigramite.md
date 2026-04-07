---
name: Tigramite
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [prediction-research, orakulum-spec]
tags: [causal-discovery, time-series, correlation, python]
---

# Tigramite

> De-facto standard library for multivariate time series causal structure learning, supporting mixed data types via conditional independence tests.

## Key Facts

- GitHub: https://github.com/jakobrunge/tigramite (1.6k stars) (ref: sources/prediction-research.md)
- Key differentiator: native mixed-type support — ParCorr (linear), CMIknn (nonlinear), Gsquared (discrete), CMIknnMixed (ref: sources/prediction-research.md)
- Five algorithms: PCMCI, PCMCIplus, LPCMCI, RPCMCI, J-PCMCI+ (ref: sources/prediction-research.md)
- By Jakob Runge; operates on pandas DataFrames (ref: sources/prediction-research.md)
- Scalability limit: handles tens to low hundreds of variables; thousands is open problem (ref: sources/prediction-research.md)

## Relevance to STOPA

Recommended causal discovery layer in ORAKULUM prediction pipeline. Step 2 of recommended 3-layer pipeline: encode → Tigramite PCMCI+ → Chronos-2. Directly applicable to MONITOR (OSINT correlation), news analysis, financial monitoring.

## Mentioned In

- [Prediction Systems Research](../sources/prediction-research.md)
- [ORAKULUM Project Specification](../sources/orakulum-spec.md)
