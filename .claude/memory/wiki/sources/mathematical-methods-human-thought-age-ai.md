---
title: "Mathematical Methods and Human Thought in the Age of AI"
slug: mathematical-methods-human-thought-age-ai
source_type: url
url: "https://arxiv.org/abs/2603.26524"
date_ingested: 2026-04-13
date_published: "2026-03-27"
entities_extracted: 4
claims_extracted: 7
---

# Mathematical Methods and Human Thought in the Age of AI

> **TL;DR**: Tao & Klowden navrhují "Copernican View of Intelligence" — AI a lidé jsou kvalitativně odlišné typy kognitivních schopností (breadth vs depth), ne body na škále hloupý→chytrý. Klíčový insight: AI dělá práci "richer and broader but not necessarily deeper". Paper varuje před "odorless proofs" a navrhuje 3-stage model lidsko-AI spolupráce.

## Key Claims

1. AI představuje "přirozený vývoj nástrojů" — je to kognitivní analogie Koperníkovy revoluce (lidská inteligence ≠ privilegovaná) — `[argued]`
2. AI decouples formu intelektuálního produktu od procesu jeho tvorby — bezprecedentní výzva oproti předchozím technologiím — `[argued]`
3. AI excels at breadth (mass generation, exploration), humans at depth (causality, intuition, "smell test") — `[argued with examples]`
4. AlphaProof's IMO řešení: formálně správné ale "numerous redundant or inexplicable steps" — illustruje failure of depth — `[verified]`
5. Circular citation risk: AI deep research tools vytvářejí feedback loops kontaminující znalostní bázi — `[verified example: vlastní Erdős Problems site]`
6. Formalizace proofs trvá 5-10× déle než původní kompozice — `[asserted]`
7. Největší riziko: "flood of largely AI-generated papers containing results that are technically correct and new, but which do not contribute to broader mathematical narratives" — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Terence Tao](../entities/terence-tao.md) | person | new |
| [Copernican View of Intelligence](../entities/copernican-view-intelligence.md) | concept | new |
| [Human-AI Centauri](../entities/human-ai-centauri.md) | concept | updated |
| AlphaProof | tool | existing (not in wiki, well-known) |

## Relations

- Terence Tao `created_by` Copernican View of Intelligence — paper authors
- Copernican View of Intelligence `extends` Human-AI Centauri — both address human-AI complementarity
- Copernican View of Intelligence `contradicts` "AI na škále smart→superhuman" framing — ontological reframing

## Cross-References

- Related learnings: 2026-04-10-rlm-architectural-principles.md (breadth/depth implicitly in RLM P1-P4), 2026-04-11-compression-regime-maps-to-tiers.md (tier selection maps to depth needed)
- Related wiki articles: orchestration-multi-agent.md (breadth coverage), skill-evaluation.md (depth quality)
- Related entities: human-ai-centauri.md (complementarity pattern), tool-genesis.md (tool evolution framing)
- Contradictions: none detected
