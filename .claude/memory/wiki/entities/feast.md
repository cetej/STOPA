---
name: Feast
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [prediction-research, orakulum-spec]
tags: [feature-store, mlops, multi-project]
---

# Feast

> Open-source feature store for ML with modular offline + online + registry, 10+ backends, point-in-time correct datasets — the recommended cross-project feature reuse backbone.

## Key Facts

- GitHub: https://github.com/feast-dev/feast (6.8k stars) (ref: sources/prediction-research.md)
- Modular: 10+ backends for offline, online, and registry (ref: sources/prediction-research.md)
- Point-in-time correct datasets prevent feature skew between train and serve (ref: sources/prediction-research.md)
- Decoupling pattern: feature pipelines write to store; prediction services read from it (ref: sources/prediction-research.md)
- New project = plug into the store, not rewrite feature engineering (ref: sources/prediction-research.md)

## Relevance to STOPA

Recommended as the shared backbone for prediction features across MONITOR, POLYBOT, ZÁCHVĚV, and ORAKULUM projects. Prevents per-project feature duplication.

## Mentioned In

- [Prediction Systems Research](../sources/prediction-research.md)
- [ORAKULUM Project Specification](../sources/orakulum-spec.md)
