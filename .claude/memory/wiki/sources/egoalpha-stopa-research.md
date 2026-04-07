---
title: "EgoAlpha Prompt Techniques vs. STOPA — Research Brief"
slug: egoalpha-stopa-research
source_type: research_output
date_ingested: 2026-04-07
entities_extracted: 7
claims_extracted: 4
---

# EgoAlpha Prompt Techniques vs. STOPA — Research Brief

> **TL;DR**: Z 38 analyzovaných technik z EgoAlpha prompt-in-context-learning repozitáře STOPA již implementuje 25 vzorů. Klíčové validace: progressive skill withdrawal (SKILL.compact.md) odpovídá SKILL0 (+9.7% ALFWorld), permission-tier governance validována Agent Skills Survey (26.1% zranitelností), Amdahl gate unikátní v orchestračních systémech. Identifikovány 5 high-impact mezer: self-consistency voting pro critic, FActScore atomic verification, few-shot examples, inter-phase completeness verifier (VMAO), hypothesis annotation.

## Key Claims

1. SKILL0 progressive skill withdrawal +9.7% ALFWorld při 0.5K vs. 5-7K tokenů — validuje STOPA SKILL.compact.md — `[verified]`
2. Agent Skills Survey: 26.1% komunitních skills obsahuje zranitelnosti — validuje permission-tier governance — `[verified]`
3. VMAO inter-phase completeness verifier: quality 3.1→4.2 při přidání verifikátoru MEZI fáze — `[argued]`
4. Self-consistency voting (Wang et al.) +20% na math benchmarks přes 3x běh + majority vote — `[verified]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| SKILL0 (progressive skill withdrawal) | paper | new |
| VMAO (inter-phase completeness verifier) | paper | new |
| FActScore | paper | new |
| Self-consistency voting | concept | existing (reflexion.md adjacent) |
| EgoAlpha prompt-in-context-learning | tool | new |
| Voyager (skill library) | paper | new |
| Agent Skills Survey | paper | new |

## Relations

- `SKILL0` `validates` `STOPA SKILL.compact.md`
- `VMAO` `proposes` `Inter-phase completeness verifier`
- `FActScore` `enables` `Atomic claim decomposition in /verify`
- `EgoAlpha prompt-in-context-learning` `catalogs` `Self-consistency voting`
- `Voyager (skill library)` `validates` `STOPA skills graduation pipeline`
- `Agent Skills Survey` `validates` `STOPA permission-tier governance`
