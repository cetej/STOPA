---
name: causal-learn
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [orakulum-spec]
tags: [causal-discovery, python, time-series]
---

# causal-learn

> Python knihovna pro causal structure learning (PC, FCI, GES algoritmy) — fallback backend v ORAKULUM correlation modulu pro případ selhání Tigramite.

## Key Facts

- PyPI: `causal-learn>=0.1.3.8` (ref: sources/orakulum-spec.md)
- Algoritmy: PC (Peter-Clark), FCI (Fast Causal Inference), GES (Greedy Equivalence Search) (ref: sources/orakulum-spec.md)
- Role v ORAKULUM: fallback pokud Tigramite PCMCI+ selže (zejm. na Windows při numba problémech) (ref: sources/orakulum-spec.md)
- Sdílí CausalGraph output interface s Tigramite pro transparentní záměnnost (ref: sources/orakulum-spec.md)
- ORAKULUM extra: `pip install orakulum[causal-fallback]` (ref: sources/orakulum-spec.md)

## Relevance to STOPA

Sekundární komponenta ORAKULUM correlation pipeline. Vzor "primary + fallback backend" je architektonicky zajímavý pro STOPA: dual-backend s sdíleným interface snižuje single-point-of-failure riziko.

## Mentioned In

- [ORAKULUM Project Specification](../sources/orakulum-spec.md)
