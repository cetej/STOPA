---
date: 2026-03-30
type: architecture
severity: high
component: memory
tags: [write-time-gating, salience, retrieval, dedup, noise-resistance, source-reputation]
summary: "Write-time gating (filtruj PŘED uložením) je strukturálně nadřazené read-time filtrování. Při 8:1 distractor ratio RAG kolabuje na 0%, gated store drží 100%. Implementováno: salience gate (source×novelty×reliability), source: pole, mandatory dedup."
source: external_research
uses: 1
harmful_uses: 0
related: [2026-03-29-paged-context-protocol.md, 2026-03-29-memcollab-agent-agnostic-memory.md]
verify_check: "Grep('Salience Gate', path='.claude/commands/scribe.md') → 1+ matches"
confidence: 0.9
successful_uses: 0
---

## Pattern

Inspirováno paperem arXiv:2603.15994 (Zahn & Chana, Cambridge, March 2026): "Selective Memory for AI — Write-Time Gating with Hierarchical Archiving".

Klíčový insight: nekontrolovaný write-path degraduje retrieval kvalitu **exponenciálně**, ne lineárně. Při 8:1 poměru šumu k signálu standardní RAG (Self-RAG) kolabuje na 0% přesnost, zatímco write-time gated store drží 100%.

## Implementace v STOPA

3 nové mechanismy přidané do /scribe write-path:

1. **Salience Gate** — 3-faktorový test PŘED zápisem:
   - `source_reputation` (1.0 user correction → 0.4 agent-generated)
   - `novelty` (1.0 nový → 0.1 duplikát)
   - `reliability` (1.0 verify_check passes → 0.3 unverifiable)
   - Práh: ≥0.4 write, 0.2-0.4 write as low, <0.2 gate

2. **`source:` pole** — nové YAML frontmatter field sledující provenienci learningu
   - Ovlivňuje jak write-time gating, tak retrieval scoring
   - Retrieval vzorec rozšířen: `severity × source_weight × time_decay`

3. **Mandatory Dedup** — existující SHOULD dedup zpřísněn na MUST s 60% overlap prahem

## Co paper říká a co je hype

Paper je solidní (Wikipedia, pharmacology, arXiv validace). Sociální média ho přefukují na "AI is poisoning its brain" — ve skutečnosti jde o RAG stores, ne model weights. Ale princip write-time > read-time filtrování je robustní a přímo aplikovatelný.
