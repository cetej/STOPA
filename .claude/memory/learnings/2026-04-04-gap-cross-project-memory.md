---
date: 2026-04-04
type: architecture
severity: medium
component: memory
tags: [memory-sharing, cross-project, gap]
summary: "GAP: No documented mechanics for how memory should transfer between STOPA and target projects (NG-ROBOT, test1, ADOBE-AUTOMAT). Current sync script copies skills but not learnings. Need to define what gets shared vs stays project-local."
source: auto_pattern
uses: 0
harmful_uses: 0
confidence: 0.5
verify_check: manual
successful_uses: 0
---

## Knowledge Gap: Cross-Project Memory Sharing

Identified during /compile 2026-04-04. The wiki compilation found no learnings covering:
- Which memory files should transfer to target projects
- How to handle project-specific vs universal learnings
- Whether learnings from target projects should flow back to STOPA
- Cross-project dedup strategy

Current state: sync-orchestration.sh copies skills and hooks but NOT learnings or decisions.
The behavioral-genome.md says "Cross-project handoff: memory do auto-memory CÍLOVÉHO projektu" but no mechanics are documented.

**Action needed**: Define a cross-project memory protocol and document as a learning or ADR.
