---
title: "Anthropic's 512K Line Code Leak Reveals AI Engineering's Future"
slug: harness-engineering-moat-poetiq
source_type: url
url: ""
date_ingested: 2026-04-13
date_published: "2026-04"
entities_extracted: 2
claims_extracted: 5
---

# Harness Engineering as Economic Moat + Poetiq ARC-AGI-2

> **TL;DR**: Analýza Claude Code leaku (512K lines) argumentuje, že ekonomický moat v AI se přesouvá od modelů k "harness engineering" — orchestraci, paměti, verifikaci. Poetiq (ex-DeepMind) to dokázal dosažením 54% ARC-AGI-2 za $30.57/problém bez vlastního modelu, jen orchestrací kolem Gemini 3 Pro.

## Key Claims

1. Capability gap mezi frontier modely se zmenšuje — moat je v orchestrační vrstvě, ne v modelu — `[argued]`
2. Poetiq dosáhl 54% ARC-AGI-2 za $30.57/problém vs Gemini 3 Deep Think 45% za $77.16 — vyšší score za méně než polovinu ceny — `[asserted]`
3. Poetiq netrénoval vlastní model — recursive meta-system nad Gemini 3 Pro (baseline 31% za $0.81) — `[asserted]`
4. Claude Code leak ukázal, že i Anthropic staví složitý harness (KAIROS, compaction, structured tools) — model sám o sobě nestačí — `[verified]`
5. "AI will not replace software engineers — it will provide opportunities to build powerful software with the right scaffolding" — `[argued]`

## Entities

| Entity | Type | Status |
|--------|------|--------|
| [Poetiq](../entities/poetiq.md) | company | new |
| Harness engineering | concept | existing (covered in garry-tan source) |

## Relations

- Poetiq `uses` Gemini 3 Pro — base model wrapped in orchestration
- Poetiq `validates` harness engineering thesis — SOTA without own model

## Cross-References

- Related wiki sources: [garry-tan-thin-harness-fat-skills](garry-tan-thin-harness-fat-skills.md) (thin harness pattern), [karpathy-nopriors-autoagent-loopy-era](karpathy-nopriors-autoagent-loopy-era.md) (auto-research)
- Related memory: `reference_claude_code_leak.md` (detailed CC leak analysis)
- Contradictions: none
