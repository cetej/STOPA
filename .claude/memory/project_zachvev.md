---
name: project_zachvev
description: Záchvěv — systém pro detekci názorových kaskád na sociálních sítích, inspirován MiroFish ale založený na reálných datech (EWS, síťová analýza, narativní signály)
type: project
---

Záchvěv je nový projekt pro detekci, predikci a modelování intervencí u názorových lavin na sociálních sítích.

**Why:** Inspirace projektem MiroFish (AI swarm engine, 33K stars na GitHubu), ale jiný přístup — místo simulace tisíců syntetických LLM agentů ($$$) analyzuje reálná data z reálných sítí ($0). Validovatelný retrospektivně na známých kauzách.

**How to apply:**
- Projektový dokument: `STOPA/research/cascade-monitor-project.md`
- Checkpoint s implementačním plánem: `STOPA/.claude/memory/checkpoint.md`
- Fáze 0 = PoC na Reddit r/czech datech s ewstools
- Klíčové nástroje: ewstools (EWS), FERNET-C5 (CZ sentiment), Seznam embeddings, NetworkX, HDBSCAN
- Cascade Risk Index = 3 pilíře: temporální (0.4) + strukturální (0.3) + narativní (0.3)
