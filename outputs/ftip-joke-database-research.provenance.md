# Provenance: FTIP Joke Database & Humor Vectors

**Date:** 2026-04-21
**Question:** Databáze vtipů ke stažení + humor feature extraction pro FTIP referenční korpus a kalibraci škály tvrdosti
**Scale:** complex (4 branches)
**Rounds:** 2 (discovery Haiku → reading Sonnet)
**Sources:** 77 objeveno / 17 přímo čteno / 10 blokováno (paywall/CAPTCHA/404)
**Verification:** partial (skipped dedicated verifier agent — reading agents reported self-confidence)

## Research Files

| File | Agent | Purpose |
|------|-------|---------|
| outputs/.research/ftip-discovery-A.md | Haiku | 15 dataset URLs (HF/Kaggle/GitHub/Czech/Reddit) |
| outputs/.research/ftip-discovery-B.md | Haiku | 15 academic taxonomy URLs (GTVH/BVT/HaHackathon/ColBERT) |
| outputs/.research/ftip-discovery-C.md | Haiku | 10 severity scale operationalization URLs |
| outputs/.research/ftip-discovery-D.md | Haiku | 41 feature extraction / taboo lexicon URLs |
| outputs/.research/ftip-reading-1.md | Sonnet | Dataset deep-dive: 8 sources read |
| outputs/.research/ftip-reading-2.md | Sonnet | Theory/scale deep-dive: 8 sources read (3 blocked) |
| outputs/.research/ftip-reading-3.md | Sonnet | Feature extraction deep-dive: 7 sources read (1 CAPTCHA) |
| outputs/ftip-joke-database-research.md | Lead | Final synthesis brief (Czech) |

## Uncertainty Summary

| Marker | Count |
|--------|-------|
| [VERIFIED] | 14 |
| [INFERRED] | 18 |
| [UNVERIFIED] | 9 |
| [SINGLE-SOURCE] | 6 |

**Unverified ratio:** 19% (under 30% gate — brief is usable)

## Blocked Sources (follow-up priority)

1. McGraw & Warren 2010 BVT — paywall 403 on Sage Journals
2. PMC11133054 multilingual taboo DB — CAPTCHA
3. Naughtyformer dataset download URL — not linked on arxiv page
4. HaHackathon direct dataset URL — need CodaLab registration
5. Getting Serious about Humor (arXiv:2403.00794) — HTML 404

## Budget Used

- Discovery: 4 agents × ~5 searches × Haiku = ~$0.10
- Reading: 3 agents × ~8 WebFetch × Sonnet = ~$0.80
- Synthesis + write: Lead (this session) = ~$0.30
- **Total:** ~$1.20
