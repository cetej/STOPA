---
date: 2026-04-08
type: best_practice
severity: high
component: orchestration
tags: [multi-agent, self-improvement, evolution, experience-sharing, farm-tier]
summary: "Sdílení evolučních trajektorií (patches, logs, failures) mezi agenty zdvojuje diversity toolsetů a zkracuje bug-repair z 5 na 1.4 iterací. Izolovaná evoluce ztrácí beneficiální objevy při prořezávání větví."
source: external_research
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.00
failure_class: coordination
verify_check: "manual"
---

## Detail

GEA (arXiv:2602.04837): skupinová evoluce agentů přes sdílení agregovaných trasí (code patches, execution logs, failure outcomes) dosahuje 71.0% vs 56.7% na SWE-bench Verified.

Klíčový mechanismus: každý agent čte VŠECHNY evoluční traces od groupmates, nejen vlastní historii. Výsledek: 17 vs 9 integrovaných ancestor tools (~2× diversity), 1.4 vs 5 iterací pro bug repair.

**Aplikace v STOPA:**
- `/orchestrate` farm tier: sdílený findings ledger jako Group Experience Sharing ekvivalent — agenti by měli zapisovat mezivýsledky do sdíleného JSON, ne jen do svých outputs
- `/self-evolve`: aktuální single-agent design — zvážit group variant kde N evolučních větví sdílí průběžné patche přes shared state
- Learnings/ + outcomes/ = statická implementace vzoru; GEA ukazuje dynamické sdílení během evoluce

**Performance-Novelty selektor** (score = αᵢ · √nov(i)): vhodný upgrade pro UCB1 v ASI-Evolve — přidává diversity kontrolu k výkonu.
