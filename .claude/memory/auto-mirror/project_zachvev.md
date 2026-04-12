---
name: project_zachvev
description: Záchvěv — systém pro detekci názorových kaskád + generování intervenčních kampaní (EWS, CRI, targeting, content generation)
type: project
---

Záchvěv je kompletní pipeline pro detekci, predikci a intervenci u názorových kaskád na sociálních sítích.

**Why:** Inspirace projektem MiroFish, ale jiný přístup — místo simulace syntetických agentů analyzuje reálná data z reálných sítí. Validovatelný retrospektivně na známých kauzách.

**How to apply:**
- Repo: `github.com/cetej/ZACHVEV` (branch master)
- Projektový dokument: `STOPA/research/cascade-monitor-project.md`
- Kompletní pipeline: INGEST → PROCESS → DETECT → ANALYZE → INTERVENE
- Stack: Arctic Shift API, tabularisai sentiment, Seznam embeddings, ewstools, UMAP+HDBSCAN
- CRI = 3 pilíře: temporální (0.4) + strukturální (0.3) + narativní (0.3)
- Session 5 (2026-03-21): přidána intervenční vrstva — content.py, targeting.py, campaign.py, visuals.py
- Policy layer: hedging jazyk, zákaz pomluvy, ověřitelná fakta, anonymizace účtů
- Validováno na Letná datech: CRI 0.52, 417 účtů, 6-fázová kampaň
