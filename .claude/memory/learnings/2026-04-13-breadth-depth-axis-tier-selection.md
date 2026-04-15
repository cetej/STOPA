---
date: 2026-04-13
type: architecture
severity: high
component: orchestration
tags: [tier-selection, human-AI, depth, breadth, orchestration]
summary: "Tao's Copernican View maps directly to STOPA tier selection: AI agents cover breadth (scout, research, parallel generation), human judgment needed for depth (architecture, quality gate, tier escalation). Without human depth gate, pipelines produce 'odorless outputs' — technically correct but without insight."
source: external_research
uses: 3
successful_uses: 0
harmful_uses: 0
confidence: 1.0
verify_check: "Grep('ODORLESS', path='.claude/skills/critic/SKILL.md') → 1+ matches"
---

## Learning

Terence Tao & Tanya Klowden (arXiv:2603.26524) propose "Copernican View of Intelligence": AI and humans aren't on a smart→superhuman axis — they're qualitatively different cognitive types.

**Breadth vs Depth:**
- **AI excels at breadth**: mass exploration, parallel generation, automated verification, coverage
- **Humans excel at depth**: causal understanding, "smell test" intuition, narrative insight, quality judgment

**STOPA mapping:**
| AI Breadth (delegate) | Human Depth (eskalovat) |
|----------------------|------------------------|
| scout, deepresearch | tier selection decision |
| parallel sub-agents | architecture choices |
| autoloop variations | quality gate ("is this insight or just correct?") |
| critic syntax checks | "does this actually compound?" judgment |

**"Odorless outputs" anti-pattern**: pipelines without human depth gate produce formálně správné ale insight-free výstupy. Equivalent to AlphaProof IMO solutions — verifiable but "numerous redundant or inexplicable steps".

**Practical rule**: Když pipeline produkuje output který je "technically correct and new" but doesn't advance understanding → chybí human depth gate. Eskaluj na deep tier nebo přidej human review krok.
