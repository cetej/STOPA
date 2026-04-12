---
name: ByteRover Memory Architecture
description: arXiv:2604.01599 — hierarchical Context Tree, 5-tier retrieval, maturity tiers with hysteresis, SOTA LoCoMo/LongMemEval without embeddings
type: reference
---

ByteRover (arXiv:2604.01599, 2026-04-02): Agent-native memory where same LLM curates and reasons (no external service split).

Key patterns applicable to STOPA:
- **Tiered retrieval** is critical (−29.4 pp in ablation). STOPA needs keyword index cache.
- **Exponential decay** with hysteresis (τ=30d, maturity tiers: Draft→Validated→Core). STOPA should migrate from linear to exponential.
- **Topic hierarchy** (Domain→Topic→Subtopic→Entry) with auto-generated `context.md` summaries. STOPA needs 2-level topics.
- **Relations graph** had minimal ablation impact (−0.4 pp) — STOPA `related:` field is sufficient.
- **Markdown-on-disk without embeddings** achieves SOTA — validates STOPA design.

Full analysis: `outputs/byterover-memory-analysis.md`
Proposals: A (topic clustering), B (tiered cache), C (exponential decay), D (formal curate ops), E (auto-summaries)
