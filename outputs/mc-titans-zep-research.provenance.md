# Provenance: MC vs Titans vs Zep vs ACT-R for STOPA Memory

**Date:** 2026-04-18
**Question:** Jak MC, Titans, Zep, ACT-R řeší scaling/gating/decay a co přenést do STOPA?
**Scale:** comparison
**Rounds:** 3 phases (discovery → reading → synthesis + verification)
**Sources:** 16 consulted / 7 primary (3 live, 1 dead-but-exists, 1 fixed-truncation, 2 mixed)
**Verification:** PASS_WITH_CONCERNS (4 corrections applied)

## Research Files

| File | Agent | Model | Purpose |
|------|-------|-------|---------|
| outputs/.research/mc-titans-zep-discovery-1.md | discovery-1 | haiku | Titans URL discovery (5/5 calls) |
| outputs/.research/mc-titans-zep-discovery-2.md | discovery-2 | haiku | Zep + ACT-R URL discovery (3/5 calls) |
| outputs/.research/mc-titans-zep-research-1.md | reading-1 | sonnet | Titans mechanism + scaling (8/8 calls) |
| outputs/.research/mc-titans-zep-research-2.md | reading-2 | sonnet | Zep + ACT-R extraction (8/8 calls) |
| outputs/.research/mc-titans-zep-synthesis.md | lead | opus | Cross-paper comparison matrix |
| outputs/.research/mc-titans-zep-verification.md | verifier | sonnet | URL liveness + claim audit |

## Uncertainty Summary

| Marker | Count |
|--------|-------|
| [VERIFIED] | 14 |
| [INFERRED] | 3 (upgrades A, B, G — proposals derived from sources) |
| [SINGLE-SOURCE] | 0 |
| [UNVERIFIED] | 0 |

## Concerns addressed from verification

1. ✅ Shaped.ai URL truncation fixed
2. ✅ ACT-R PDF mirror URL added (Springer 303 workaround)
3. ✅ LongMemEval model specificity (gpt-4o) noted
4. ✅ Anderson & Lebiere (1998) as original formula source noted

## Budget

- Haiku discovery: 2 agents × ~5 calls = 10 calls ≈ $0.05
- Sonnet reading: 2 agents × 8 calls = 16 calls ≈ $0.25
- Sonnet verifier: 1 agent × ~29 tool uses ≈ $0.08
- Opus synthesis (lead): direct writing, no external calls ≈ $0.10
- **Total: ~$0.48** (comparison tier budget: ~$1.00)
