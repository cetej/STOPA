---
date: 2026-04-18
type: architecture
severity: medium
component: memory
tags: [retrieval, memory, complexity, hybrid-retrieve, tuning]
summary: "STOPA retrieval má implicitní complexity knob: grep=O(1) → BM25=O(log L) → graph walk=O(L). MC paper formalizuje tento vzor jako O(NL) interpolaci kde N=počet cached segmentů. Praktické pravidlo: pro shallow tasks (tier=light) stačí grep; pro deep tasks vždy hybrid (BM25+graph). Nepoužívej graph walk pokud grep vrátí 3+ matches — zbytečná kvadratická expanze."
source: external_research
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.0
maturity: draft
valid_until:
skill_scope: [orchestrate, scout, scribe]
related: [2026-04-18-mc-checkpoint-caching-retrieval-pattern.md, 2026-04-08-recency-beats-complex-memory.md, 2026-04-08-living-memory-over-static-retrieval.md]
verify_check: "Grep('task.tier.*light.*grep|tier=light', path='.claude/memory') → manual check"
model_gate:
impact_score: 0.0
task_context:
  task_class: research
  complexity: low
  tier: light
---

## Detail

MC complexity tabulka (Behrouz et al., arXiv:2602.24281):

| Segment config | Komplexita | STOPA retrieval ekvivalent |
|----------------|-----------|--------------------------|
| N=1 (fixní) | O(L) | Grep only |
| Konstantní segmenty | O(L²/C) | BM25 |
| Log segmenty | O(L log L) | BM25 + 1-hop graph |
| N=L (full) | O(L²) | Full graph walk |

**Praktické pravidlo pro hybrid-retrieve.py:**
- `tier=light` → grep only (N=1 ekvivalent)
- `tier=standard`, grep < 3 hits → BM25 (O(log L))
- `tier=deep` vždy → BM25 + graph walk
- Graf walk (O(L) expansions) pouze pokud BM25 < 3 relevantních

Log segmentování (SSC varianta) selhává na recall-intensive tasks — vzdálená minulost se překomprimuje. Analogicky: concept-graph walk po 1 hopu je dostatečný, 2-hop přidává šum (viz hybr retrieval pravidlo v memory-files.md: max 1-hop).
