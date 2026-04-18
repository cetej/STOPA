---
date: 2026-04-12
type: best_practice
severity: medium
component: skill
tags: [skill-design, knowledge-extraction, ingest, compile, research]
summary: "Diarization = reading all documents about a subject and writing a structured profile that holds contradictions, notes temporal changes, and surfaces judgment no query can produce. This is the latent operation at the heart of /ingest and /compile."
source: external_research
maturity: draft
uses: 0
successful_uses: 0
harmful_uses: 0
confidence: 0.7
impact_score: 0.0
verify_check: "manual"
skill_scope: [ingest, compile, deepresearch]
---

## Detail

Garry Tan defines diarization as the step that makes AI useful for real knowledge work: "The model reads everything about a subject and writes a structured profile — a single page of judgment distilled from dozens or hundreds of documents."

Output includes contradictions surfaced and held, temporal changes noted, analyst judgment — not database retrieval.

Example: "SAYS: Datadog for AI agents / ACTUALLY BUILDING: 80% of commits are in billing module. She's building a FinOps tool disguised as observability." No SQL query produces this. No RAG pipeline produces this.

**STOPA application:**
- `/ingest` Phase 2 (Extract) is diarization — entity+claim extraction from raw sources
- `/compile` Phase 2 (Synthesis) is diarization at the article level
- `/deepresearch` synthesis phase is diarization at the research level
- When designing these phases, explicitly ask: "What judgment would a smart analyst make here that no query can make?"
