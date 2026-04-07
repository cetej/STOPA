---
name: GDELT
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [orakulum-spec]
tags: [osint, research, web]
---

# GDELT

> Global Database of Events, Language and Tone — volně dostupná databáze geopolitických událostí z mediálních zdrojů, kódovaná ve formátu CAMEO (actor, event type, region, Goldstein scale, tone).

## Key Facts

- Přístup: Gamma API, volně dostupné (ref: sources/orakulum-spec.md)
- CAMEO kategorie relevantní pro MONITOR: "14" (protest), "18" (assault), "19" (conflict) (ref: sources/orakulum-spec.md)
- GDELTLoader v ORAKULUM: vrací DataFrame(date, actor1, actor2, event_type, goldstein, tone, url) (ref: sources/orakulum-spec.md)
- Riziko: high data quality gaps; mitigace: WORLDREP jako alt. zdroj, TemporalAligner handluje gaps (ref: sources/orakulum-spec.md)
- Target v0.1: GDELT anomaly detection AUC >0.80, target v1.0: >0.86 (Macis 2024 benchmark) (ref: sources/orakulum-spec.md)

## Relevance to STOPA

Primární datový zdroj pro ORAKULUM a MONITOR. Klíčový pro geopolitickou anomaly detection a causal correlation. GDELTLoader je P0 komponenta v ORAKULUM v0.1 roadmap.

## Mentioned In

- [ORAKULUM Project Specification](../sources/orakulum-spec.md)
