---
name: project_orakulum
description: ORAKULUM — shared Python prediction/correlation library for MONITOR, Polybot, and Záchvěv
type: project
---

ORAKULUM je sdílená Python knihovna pro predikci a korelační analýzu z heterogenních datových zdrojů (text, události, čísla, časové řady).

**Why:** MONITOR, Polybot a Záchvěv sdílejí ~60% potřebné funkcionality (encoding událostí, causal discovery, anomaly detection). Bez sdílené knihovny by se kód duplikoval a divergoval. Analogie: ngm-terminology řeší sdílenou terminologii, ORAKULUM řeší sdílenou predikci.

**How to apply:**
- Spec: `STOPA/outputs/orakulum-spec.md`
- Research: `STOPA/outputs/prediction-research.md` (80+ zdrojů)
- Plánované repo: `github.com/cetej/ORAKULUM`, adresář `000_NGM/ORAKULUM`
- Stack: Python 3.10+, Tigramite (PCMCI+), STUMPY, Darts/sktime, Chronos-2
- Konzumenti: MONITOR (Node.js → microservice), Polybot (přímý import), Záchvěv (přímý import)
- 6 modulů: encoding, correlation, prediction, anomaly, markets, store
- API kontrakt: sklearn `.fit()/.predict()` pro všechny prediktory
- Markets modul portuje execution logiku z howdymary/autopredict
- Roadmap: v0.1 (encoding+correlation+anomaly) → v0.2 (prediction+pipeline) → v0.3 (markets+binary) → v1.0 (production)
- STOPA skill `/predict` bude wrappovat ORAKULUM pro Claude Code sessions
