# Provenance: Attention Mechanism Innovations

**Date:** 2026-03-29
**Question:** Současný stav adoptace XSA, AttnRes, Differential Attention a Value Residual Learning v produkčních LLM architekturách
**Scale:** survey
**Rounds:** 1 research round (3 parallel agents) + 1 verification round
**Sources:** 32 consulted / 27 accepted / 5 rejected (undated/SEO)
**Verification:** DONE_WITH_CONCERNS → addressed

## Research Files

| File | Agent | Purpose |
|------|-------|---------|
| outputs/.research/attention-research-1.md | researcher-1 (sonnet) | XSA + Value Residual Learning |
| outputs/.research/attention-research-2.md | researcher-2 (sonnet) | AttnRes + Differential Attention |
| outputs/.research/attention-research-3.md | researcher-3 (sonnet) | Production architectures Q4 2024–Q1 2026 |
| outputs/.research/attention-synthesis.md | lead | Merged evidence + status table |
| outputs/.research/attention-verification.md | verifier (sonnet) | Citation audit — 10 top claims |

## Verification Outcomes

| Concern | Resolution |
|---------|-----------|
| KV cache 7.6 GB / 28x — not directly in paper HTML | Marked [INFERRED] from published parameters |
| ADFormer, RaDiT — named without sources | Removed from final brief |
| Source numbering gap in research-3.md | Fixed via unified numbering in final brief |

## Uncertainty Summary

| Marker | Count |
|--------|-------|
| [VERIFIED] | ~20 |
| [INFERRED] | 3 |
| [SINGLE-SOURCE] | 3 |
| [UNVERIFIED] | 3 |

**[UNVERIFIED] rate: ~10%** (below 30% warning threshold)
