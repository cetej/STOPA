---
title: "Czech Vocabulary Size and Open Lexical Resources"
slug: czech-lexical-resources-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 7
claims_extracted: 4
---
# Czech Vocabulary Size and Open Lexical Resources

> **TL;DR**: Survey of Czech lexical resources for NLP/data use. MorfFlex CZ 2.1 is the most comprehensive morphological resource (126.9M triples, 238 MB), but all LINDAT/Charles University resources are CC BY-NC-SA (non-commercial only). The only commercially-usable open options are Czech Wiktionary dump (CC BY-SA) and kaikki.org extract (68,766 words). Czech NLP resources have a significant commercial-use gap.

## Key Claims

1. MorfFlex CZ 2.1 contains 126,906,921 lemma-tag-wordform triples, reflecting Czech's rich morphology — `[verified]`
2. All major Czech NLP academic resources (LINDAT) are CC BY-NC-SA 4.0 — non-commercial only, creating a gap for commercial applications — `[verified]`
3. kaikki.org provides the most download-friendly open resource: 68,766 distinct Czech words in JSONL format (CC BY-SA, 36 MB gzip) — `[verified]`
4. Czech active vocabulary estimate is ~150,000 words; English 1M+; Czech morphology means one lexeme generates 10-20+ word forms making cross-language comparisons methodologically problematic — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| MorfFlex CZ | tool | new |
| DeriNet | tool | new |
| LINDAT/CLARIAH-CZ | company | new |
| kaikki.org | tool | new |
| Czech WordNet | tool | new |
| ÚFAL Charles University | company | new |
| Czech National Corpus (ČNK) | tool | new |

## Relations

- MorfFlex CZ `published_by` ÚFAL Charles University
- DeriNet `published_by` ÚFAL Charles University
- LINDAT/CLARIAH-CZ `hosts` MorfFlex CZ
- LINDAT/CLARIAH-CZ `hosts` DeriNet
- kaikki.org `extracts_from` Czech Wiktionary
