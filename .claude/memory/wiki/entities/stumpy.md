---
name: STUMPY
type: tool
first_seen: 2026-04-07
last_updated: 2026-04-07
sources: [orakulum-spec]
tags: [time-series, anomaly-detection, python]
---

# STUMPY

> Python knihovna pro výpočet matrix profile — efektivní detekce anomálií (discords), opakujících se vzorů (motifs) a changepoints v časových řadách bez supervize.

## Key Facts

- PyPI: `stumpy>=1.12`, GitHub: TDAmeritrade/stumpy (ref: sources/orakulum-spec.md)
- Klíčové operace: matrix profile výpočet, discord detection (anomálie), motif discovery (opakující se vzory) (ref: sources/orakulum-spec.md)
- StumpyDetector v ORAKULUM: `window_size` parametr, vrací DataFrame(timestamp, score, is_anomaly, type[discord|motif]) (ref: sources/orakulum-spec.md)
- Součást ORAKULUM core deps (<100MB, bez PyTorch) (ref: sources/orakulum-spec.md)
- Cíl v0.1: GDELT anomaly detection AUC >0.80 (ref: sources/orakulum-spec.md)

## Relevance to STOPA

Klíčová komponenta ORAKULUM anomaly detection modulu (StumpyDetector). V kontextu MONITOR projektu: detekce anomálních geopolitických události z GDELT dat. V kontextu Záchvěv: detekce changepoints v cascade signálech.

## Mentioned In

- [ORAKULUM Project Specification](../sources/orakulum-spec.md)
